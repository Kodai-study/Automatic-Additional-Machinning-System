import datetime
from queue import Queue
import time
from DBAccessHandler.DBAccessHandler import DBAccessHandler
from GUIDesigner.GUIDesigner import GUIDesigner
from GUIDesigner.GUISignalCategory import GUISignalCategory
from ImageInspectionController.ImageInspectionController import ImageInspectionController
from ImageInspectionController.InspectDatas import ToolInspectionData
from ImageInspectionController.OperationType import OperationType
from Integration.ManageRobotReceive import ManageRobotReceive
from Integration.handlers_gui_responce import GuiResponceHandler
from Integration.process_number import Processes
from RobotCommunicationHandler.RobotCommunicationHandler \
    import TEST_PORT1, TEST_PORT2, RobotCommunicationHandler
from threading import Thread
from RobotCommunicationHandler.test_cfd import _test_cfd
from RobotCommunicationHandler.test_ur import _test_ur
from test_flags import TEST_CFD_CONNECTION_LOCAL, TEST_UR_CONNECTION_LOCAL
from common_data_type import TransmissionTarget


class Integration:
    """
    統合プロセスのメインクラス
    すべてのスレッドはここでインスタンス化され、管理される
    """

    def __init__(self):
        self.send_request_queue = Queue()  # 通信ソフトに対して送信要求を行うキュー
        self.comm_receiv_queue = Queue()  # 通信ソフトが受信したデータの受け取りを行うキュー
        self.gui_request_queue = Queue()  # GUIからの要求を受け取るキュー
        self.gui_responce_queue = Queue()  # GUIからの要求に対する応答を返すキュー
        self.wait_cmd_flag = None
        self.wait_message = None
        # 通信相手のURが立ち上がっていなかった場合、localhostで通信相手を立ち上げる
        if TEST_UR_CONNECTION_LOCAL:
            self.test_ur = _test_ur(TEST_PORT1)

        if TEST_CFD_CONNECTION_LOCAL:
            self.test_cfd = _test_cfd(TEST_PORT2)

        self.robot_message_handler = ManageRobotReceive(self)
        self.robot_status = {
            "is_connection": False,
            "limit_switch": False,
            "lighting": {
                "back_light": False, "bar_light": False, "ring_light": False
            },
            "sensor": {
                1: False, 2: False, 3: False, 4: False, 5: False, 6: False
            },
            "reed_switch": {
                1: {"forward": False, "backward": False}, 2: {"forward": False, "backward": False},
                3: {"forward": False, "backward": False}, 4: {"forward": False, "backward": False}, 5: {"forward": False, "backward": False}
            },
            "door_status": {
                1: False, 2: False, 3: False, 4: False
            },
            "door_lock": {
                1: False, 2: False, 3: False, 4: False
            },
            "ejector": {
                "attach": False, "detach": False
            }
        }
        self.process_data_list = []
        self.work_list = []
        self.write_list = []
        self._test_insert_process_datas()
        self.image_inspection_controller = ImageInspectionController()
        self.database_accesser = DBAccessHandler()
        self.communicationHandler = RobotCommunicationHandler()
        self.guiDesigner = GUIDesigner()

        # TODO 現在の画面がモニタ画面かどうかのフラグをGUIと共有する
        self.is_monitor_mode = False
        self.is_processing_mode = False
        self.tool_stock_position = 1
        self.work_stock_number = -1
        self.gui_responce_handler = GuiResponceHandler(
            self, self.send_request_queue, self.gui_request_queue)

    def _test_insert_work_datas(self):
        self.work_list = [
            {"process": Processes.start, "serial_number": None}]
        self.write_list = [{"process_type": Processes.start,
                            "process_time": datetime.datetime.now()},
                           {"process_type": Processes.move_to_process,
                            "process_time": datetime.datetime.now()}]

    def _test_insert_process_datas(self):
        self.process_data_list = [
            {"process_id": 1, "model_name": "加工データ(型番)1",
             "average_time": datetime.timedelta(minutes=1, seconds=23),
             "regist_process_count": 10,
             "process_time": datetime.timedelta(minutes=12, seconds=34),
             "good_count": 7,
             "remaining_count": 2},
            {"process_id": 2, "model_name": "加工データ(型番)2",
             "average_time": datetime.timedelta(minutes=2, seconds=34),
             "regist_process_count": 20,
             "process_time": datetime.timedelta(minutes=23, seconds=45),
             "good_count": 8,
             "remaining_count": 10}
        ]

    def _test_watching_guiResponce_queue(self):
        """
        テスト用関数。  GUIから、ロボットへの操作要求があると、そのコマンドを送信する
        """
        while True:
            if not self.gui_responce_queue.empty():
                # send_queueから値を取り出す
                send_data = self.gui_responce_queue.get()
                self.gui_responce_handler.handle(send_data)
            time.sleep(0.1)

    def _wait_command(self, target: TransmissionTarget, message: str):
        self.wait_cmd_flag = False
        self.wait_message = {"target": target, "message": message}
        while not self.wait_cmd_flag:
            time.sleep(0.1)
        self.wait_message = None
        return True

    def _robot_message_handle(self):
        while True:
            if not self.comm_receiv_queue.empty():
                # send_queueから値を取り出す
                receiv_data = self.comm_receiv_queue.get()
                if self.wait_message is not None:
                    if self.wait_message["target"] == receiv_data["target"] and self.wait_message["message"] == receiv_data["message"]:
                        self.wait_cmd_flag = True

                self.robot_message_handler.handle_receiv_message(receiv_data)
            time.sleep(0.1)

    def _initialization(self):
        self.is_ur_connected = False
        self.is_cfd_connected = False
        # 通信が確立するまで待機
        while not (self.is_ur_connected and self.is_cfd_connected):
            time.sleep(0.5)

    def _start_process(self):
        for stock_number in range(1, 9):
            self._wait_command(
                TransmissionTarget.TEST_TARGET_2, "DR_STK_TURNED")
            result = self.image_inspection_controller.perform_image_operation(
                OperationType.TOOL_INSPECTION, ToolInspectionData(is_initial_phase=True, tool_position_number=stock_number))
            print(f"工具{stock_number}個めの検査 : 結果 {result}")
            if not result.result:
                self.gui_request_queue.put(
                    GUISignalCategory.CANNOT_CONTINUE_PROCESSING, f"{stock_number}個の工具がエラーです")
                return

        # TODO ワークの個数を取得する
        self._wait_command(
            TransmissionTarget.TEST_TARGET_1, "SIG 0,ATT_IMP_READY")

    def main(self):

        # 通信スレッドを立ち上げる
        self.communication_thread = Thread(
            target=self.communicationHandler.communication_loop,
            args=(self.send_request_queue, self.comm_receiv_queue))
        self.communication_thread.start()

        # 通信相手のURがいない場合、localhostで通信相手をスレッドで立ち上げる
        if TEST_UR_CONNECTION_LOCAL:
            test_ur_thread = Thread(target=self.test_ur.start)
            test_ur_thread.start()

        if TEST_CFD_CONNECTION_LOCAL:
            test_cfd_thread = Thread(target=self.test_cfd.start)
            test_cfd_thread.start()

        Thread(target=self._initialization).start()
        test_send_thread = Thread(
            target=self._robot_message_handle)
        test_send_thread.start()
        test_watching_guiResponce_queue_thread = Thread(
            target=self._test_watching_guiResponce_queue)
        test_watching_guiResponce_queue_thread.start()
        self.guiDesigner.start_gui(
            self.gui_request_queue, self.gui_responce_queue)
