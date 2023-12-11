import datetime
from threading import Thread
from Integration.handlers_communication import _change_gui_status, _handle_connection_success, _notice_finish_process, notice_change_status, _send_message_to_cfd, _send_message_to_ur, _send_to_gui
from Integration.handlers_database import write_database
from Integration.handlers_image_inspection import _start_accuracy_inspection_inspection, _start_pre_processing_inspection, _start_tool_inspeciton
from Integration.handlers_robot_action import change_robot_first_position, reservation_process, start_process
from Integration.process_number import Processes, get_process_number
from RobotCommunicationHandler.RobotInteractionType import RobotInteractionType
from common_data_type import TransmissionTarget


class ManageRobotReceive:
    """
    ロボットから受け取ったメッセージを判別して、対応する処理を行うクラス

    通信ソフトから取得したデータを、そのままhandle_receiv_message 関数に渡して呼び出す。
    """

    def __init__(self, integration_instance):
        """
        Args:
            integration_instance (Integration): 統合スレッドのインスタンス。
            このインスタンスから、キューなどにアクセスする。
        """
        self._integration_instance = integration_instance
        self._special_command_handlers = {
            "ISRESERVED": reservation_process,
            "FIN_FST_POSITION": change_robot_first_position,
            "TEST_PRE_INSPECTION": lambda: _start_pre_processing_inspection(self._integration_instance.image_inspection_controller, self._integration_instance.work_list, self._integration_instance.write_list, self._integration_instance.database_accesser),
            "SIZE 0,ST": lambda: print("サイズを教えてください")
        }
        self._handl_selectors = {
            "SIG": self._select_handler_ur_sig,
            "CYL": self._select_handler_cyl,
            "WRK": self._select_handler_wrk,
            "SNS": self._select_handler_sensor,
            "RDSW": self._select_handler_sensor_reed_switch,
            "EJCT": self._select_handler_ejector,
            "WRKSNS": self._select_handler_workSensor,
        }

    def _select_handler(self, command: str, target: TransmissionTarget):
        """メッセージの種類に応じて、ハンドラを選択する

        Args:
            command (str): メッセージの文字列

        Returns:
            function: ハンドラ
        """
        if command in self._special_command_handlers:
            return self._special_command_handlers[command]

        instruction, dev_num, detail = self._split_command(command)
        process_number = get_process_number(instruction, dev_num, detail)
        is_get_serial_num = False
        if process_number is not None:
            is_get_serial_num, serial_number = self._manage_work_status_list(
                process_number)

        handle_selector = self._handl_selectors.get(instruction)
        if not handle_selector:
            return lambda: self._undefine(command)

        if is_get_serial_num:
            return handle_selector(
                dev_num, detail, command=command, serial_number=serial_number)
        elif process_number is not None:
            time = datetime.datetime.now()

            def _handle():
                handle_selector(dev_num, detail, command=command)
                self._integration_instance.write_list.append(
                    {"process_type": process_number, "process_time": time})
            return _handle

        return handle_selector(dev_num, detail, command=command, target=target)

    def _manage_work_status_list(self, process_num):

        filtered_progress = [
            item for item in self._integration_instance.work_list if item["process"].value < process_num.value]

        # filtered_progress の要素がない場合
        if not filtered_progress:
            self._integration_instance.work_list.append(
                {"process": process_num, "serial_number": None})
            return False, None

        max_progress_item = max(
            filtered_progress, key=lambda item: item["process"].value, default=None)

        if max_progress_item is None:
            print("ワーク管理の部分でエラーです")
            return False, None

        if process_num == Processes.end_process:
            self._integration_instance.work_list = [d for d in self._integration_instance.work_list if d.get(
                'process') != max_progress_item['process']]
        else:
            max_progress_item["process"] = process_num

        return max_progress_item["serial_number"] is not None, max_progress_item["serial_number"]

    def _test_select_handler_report(self, command: str):
        """メッセージの種類に応じて、ハンドラを選択する

        Args:
            command (str): メッセージの文字列

        Returns:
            function: ハンドラ
        """

        if command == "SIG DET":
            return lambda: _send_to_gui(self._integration_instance.gui_request_queue, command)

        instruction, dev_num, detail = self._split_command(command)
        if instruction == "SIG":
            if dev_num == 0:
                if detail == "ATT_IMP_READY" or detail == "ATT_DRL_READY":
                    return lambda: _send_to_gui(self._integration_instance.gui_request_queue, command)

    def _select_handler_ur_sig(self, dev_num: int, detail: str, command: str, serial_number: int = None, target: TransmissionTarget = None):
        """
        SIG命令のハンドラを選択する
        """
        if dev_num != 0:
            return self._undefine

        sensor_time = datetime.datetime.now()
        if detail == "ATT_IMP_READY" or detail == "ATT_DRL_READY" or detail == "FST_POSITION":
            def _handler():
                write_database(
                    self._integration_instance.database_accesser, "SIG", dev_num, detail, sensor_time, serial_number)
                _send_message_to_ur(
                    command, self._integration_instance.send_request_queue)
            return _handler()

        return self._undefine

    def _select_handler_workSensor(self, dev_num: int, detail: str, command: str, serial_number: int = None, target: TransmissionTarget = None):
        if dev_num != 0:
            return self._undefine(command)
        print("ワークの枚数は", detail, "枚です")

    def _select_handler_cyl(self, dev_num: int, detail: str, command: str, serial_number: int = None, target: TransmissionTarget = None):
        """
        CYL命令のハンドラを選択する
        """
        is_status_on = detail == "ON"

        def change_cylinder_status(): return _change_gui_status(
            self._integration_instance.gui_request_queue, self._integration_instance.robot_status,
            "cylinder", dev_num, is_status_on)

        if self._integration_instance.is_monitor_mode:
            return change_cylinder_status

        # CYL 001,ON
        if dev_num == 1 and is_status_on:
            def _handler():
                start_process()
                change_cylinder_status()
            return _handler

        # CYL 003,ON
        elif dev_num == 3 and is_status_on:
            def _handler():
                _start_accuracy_inspection_inspection(
                    self._integration_instance.image_inspection_controller)
                change_cylinder_status()
            return _handler

        return change_cylinder_status

    def _select_handler_wrk(self, dev_num: int, detail: str, command: str, serial_number: int = None, target: TransmissionTarget = None):
        """
        WRK命令のハンドラを選択する
        """
        if dev_num == 0 and detail == "TAP_FIN":
            return lambda: _send_message_to_ur(command, self._integration_instance.send_request_queue)

    def _select_handler_ejector(self, dev_num: int, detail: str, command: str, target: TransmissionTarget):
        if detail == "ST":
            return lambda: _send_message_to_cfd(command, self._integration_instance.send_request_queue)

        if dev_num != 0:
            return self._undefine(command)

        if target == TransmissionTarget.CFD or target == TransmissionTarget.TEST_TARGET_2:
            return lambda: _send_message_to_ur(command, self._integration_instance.send_request_queue)
        elif target == TransmissionTarget.UR or target == TransmissionTarget.TEST_TARGET_1:
            return lambda: _send_message_to_cfd(command, self._integration_instance.send_request_queue)

    def _select_handler_sensor(self, dev_num: int, detail: str, command: str, serial_number: int = None, target: TransmissionTarget = None):
        """
        SNS命令のハンドラを選択する
        """
        is_on = detail == "ON"
        sensor_time = datetime.datetime.now()

        if detail == "ST":
            return lambda: _send_message_to_cfd(command, self._integration_instance.send_request_queue)

        def _common_sensor_handler():
            _send_message_to_ur(
                command, self._integration_instance.send_request_queue)
            write_database(self._integration_instance.database_accesser,
                           "SNS", dev_num, detail, sensor_time, serial_number)
            self._change_robot_status("sensor", dev_num, is_on)

        if dev_num == 1 and is_on:
            def _handler():
                _common_sensor_handler()
                _notice_finish_process(
                    self._integration_instance.gui_request_queue, True)
                print("良品ワークが排出されました")
            return _handler

        elif dev_num == 2 and is_on:
            def _handler():
                _common_sensor_handler()
                _notice_finish_process(
                    self._integration_instance.gui_request_queue, False)
                print("不良品ワークが排出されました")
            return _handler

        return _common_sensor_handler

    def _select_handler_sensor_reed_switch(self, dev_num: int, detail: str, command: str, serial_number: int = None, target: TransmissionTarget = None):
        door_number = (dev_num / 2) + 1
        kind = "forward" if dev_num % 2 == 0 else "backward"
        self._integration_instance.robot_status["reed_switch"][door_number][kind] = (
            detail == "ON")
        notice_change_status(self._integration_instance.gui_request_queue)

    def _split_command(self, command: str):
        command_copy = command
        _split_list = command_copy.split(" ")
        instruction = _split_list[0]
        if len(_split_list) == 2:
            command_copy = _split_list[1]
            _split_list = command_copy.split(",")
            try:
                dev_num = int(_split_list[0])
            except ValueError:
                dev_num = _split_list[0]
            detail = _split_list[1] if len(_split_list) == 2 else None

        else:
            dev_num = None
            detail = None
        return instruction, dev_num, detail

    def _undefine(self, message: str):
        """
        ハンドラ。適切な処理がまだ割り当てられていないメッセージを受け取ったときに呼び出される
        Args:
            message (str): _description_
        """
        print("undefined message : ", message)

    def handle_receiv_message(self, receiv_data: dict):
        """
        通信ソフトから受け取ったメッセージを判別して、対応する処理を行う

        Args:
            receiv_data (dict): 受け取ったメッセージの情報を格納した辞書
        """

        # もし"msg_type"か"target"がなかったら、エラーを出力して終了
        if not receiv_data.get("msg_type") or not receiv_data.get("target"):
            print("Error: msg_type or target is not defined : message",
                  receiv_data.get("message"))
            return

        if receiv_data["msg_type"] == RobotInteractionType.SOCKET_CONNECTED:
            _handle_connection_success(self._integration_instance.gui_request_queue,
                                       receiv_data["target"])
            if receiv_data["target"] == TransmissionTarget.UR or receiv_data["target"] == TransmissionTarget.TEST_TARGET_1:
                self._integration_instance.is_ur_connected = True
            elif receiv_data["target"] == TransmissionTarget.CFD or receiv_data["target"] == TransmissionTarget.TEST_TARGET_2:
                self._integration_instance.is_cfd_connected = True
            return

        if receiv_data["msg_type"] == RobotInteractionType.MESSAGE_RECEIVED:
            handler = self._select_handler(
                receiv_data["message"], receiv_data["target"])

        if not handler:
            def handler(): self._undefine(receiv_data["message"])

        Thread(target=handler).start()

    def _change_robot_status(self, device_kind: str, device_number, status):
        self._integration_instance.robot_status[device_kind][device_number] = status
        notice_change_status(self._integration_instance.gui_request_queue)

    def _get_robot_status(self, device_kind: str, device_number):
        return self._integration_instance.robot_status[device_kind][device_number]
