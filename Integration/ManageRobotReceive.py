from threading import Thread
from Integration.handlers_communication import _change_gui_status, _handle_connection_success, _send_message_to_cfd, _send_message_to_ur, _send_to_gui
from Integration.handlers_image_inspection import _start_accuracy_inspection_inspection, _start_pre_processing_inspection, _start_tool_inspeciton
from Integration.handlers_robot_action import change_robot_first_position, reservation_process, start_process
from RobotCommunicationHandler.RobotInteractionType import RobotInteractionType


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
            "DR_STK_TURNED": lambda: _start_tool_inspeciton(self._integration_instance.image_inspection_controller),
            "ISRESERVED": reservation_process,
            "FIN_FST_POSITION": change_robot_first_position,
            "TEST_PRE_INSPECTION": lambda: _start_pre_processing_inspection(self._integration_instance.image_inspection_controller)
        }

    def _select_handler(self, command: str):
        """メッセージの種類に応じて、ハンドラを選択する

        Args:
            command (str): メッセージの文字列

        Returns:
            function: ハンドラ
        """
        if command in self._special_command_handlers:
            return self._special_command_handlers[command]

        instruction, dev_num, detail = self._split_command(command)
        if instruction == "SIG":
            return self._select_handler_ur_sig(
                dev_num, detail, command=command)
        elif instruction == "CYL":
            return self._select_handler_cyl(dev_num, detail, command=command)
        elif instruction == "WRK":
            return self._select_handler_wrk(dev_num, detail, command=command)
        return None

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

    def _select_handler_ur_sig(self, dev_num: int, detail: str, command: str):
        """
        SIG命令のハンドラを選択する
        """
        if dev_num != 0:
            return self._undefine

        if detail == "ATT_IMP_READY" or detail == "ATT_DRL_READY" or detail == "FST_POSITION":
            return lambda: _send_message_to_cfd(command, self._integration_instance.send_request_queue)

        return self._undefine

    def _select_handler_cyl(self, dev_num: int, detail: str, command: str):
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

    def _select_handler_wrk(self, dev_num: int, detail: str, command: str):
        """
        WRK命令のハンドラを選択する
        """
        if dev_num == 0 and detail == "TAP_FIN":
            return lambda: _send_message_to_ur(command, self._integration_instance.send_request_queue)

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

    def _write_database(self, message: str):
        pass

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
            return

        if receiv_data["msg_type"] == RobotInteractionType.MESSAGE_RECEIVED:
            handler = self._select_handler(receiv_data["message"])

        if not handler:
            def handler(): self._undefine(receiv_data["message"])

        Thread(target=handler).start()
