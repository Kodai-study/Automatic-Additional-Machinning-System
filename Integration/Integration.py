import datetime
from queue import Queue
import time
from DBAccessHandler.DBAccessHandler import DBAccessHandler
from GUIDesigner.GUIDesigner import GUIDesigner
from GUIDesigner.GUIRequestType import GUIRequestType
from ImageInspectionController.ImageInspectionController import ImageInspectionController
from ImageInspectionController.InspectDatas import ToolInspectionData
from ImageInspectionController.OperationType import OperationType
from Integration.ManageRobotReceive import ManageRobotReceive
from Integration.process_number import Processes
from RobotCommunicationHandler.RobotCommunicationHandler \
    import TEST_PORT1, TEST_PORT2, RobotCommunicationHandler
from threading import Thread
from RobotCommunicationHandler.RobotInteractionType import RobotInteractionType
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

        # 通信相手のURが立ち上がっていなかった場合、localhostで通信相手を立ち上げる
        if TEST_UR_CONNECTION_LOCAL:
            self.test_ur = _test_ur(TEST_PORT1)

        if TEST_CFD_CONNECTION_LOCAL:
            self.test_cfd = _test_cfd(TEST_PORT2)

        self.robot_message_handler = ManageRobotReceive(self)
        self.robot_status = {"sensor": {"sensor1": False, "sensor2": False},
                             "cylinder": {1: False, 2: False}}
        # self.work_list = [
        #     {"process": Processes.start, "serial_number": None}]
        # self.write_list = [{"process_type": Processes.start,
        #                     "process_time": datetime.datetime.now()},
        #                    {"process_type": Processes.move_to_process,
        #                     "process_time": datetime.datetime.now()}]
        self.work_list = []
        self.write_list = []

        self.image_inspection_controller = ImageInspectionController()
        self.database_accesser = DBAccessHandler()

        # TODO 現在の画面がモニタ画面かどうかのフラグをGUIと共有する
        self.is_monitor_mode = False

    def _test_watching_guiResponce_queue(self):
        """
        テスト用関数。  GUIから、ロボットへの操作要求があると、そのコマンドを送信する
        """
        while True:
            if not self.gui_responce_queue.empty():
                # send_queueから値を取り出す
                send_data = self.gui_responce_queue.get()
                if send_data[0] == GUIRequestType.ROBOT_OPERATION_REQUEST:
                    if TEST_UR_CONNECTION_LOCAL:
                        self.send_request_queue.put(
                            {"target": TransmissionTarget.TEST_TARGET_1, "message": str(send_data[1])})
                    else:
                        self.send_request_queue.put(
                            {"target": TransmissionTarget.UR, "message": str(send_data[1])})

                elif send_data[0] == GUIRequestType.UPLOAD_PROCESSING_DETAILS:
                    self.is_registor_process_data = True
            time.sleep(0.1)

    def _robot_message_handle(self):
        while True:
            if not self.comm_receiv_queue.empty():
                # send_queueから値を取り出す
                receiv_data = self.comm_receiv_queue.get()
                self.robot_message_handler.handle_receiv_message(receiv_data)
            time.sleep(0.1)

    def _initialization(self):
        self.is_ur_connected = False
        self.is_cfd_connected = False
        self.is_registor_process_data = False
        # 通信が確立するまで待機
        while not (self.is_ur_connected and self.is_cfd_connected):
            time.sleep(0.5)

        while not self.is_registor_process_data:
            time.sleep(1)

        for stock_number in range(8):
            print("検査", stock_number, self.image_inspection_controller.perform_image_operation(
                OperationType.TOOL_INSPECTION, ToolInspectionData(is_initial_phase=True, tool_position_number=stock_number)))

    def main(self):
        communicationHandler = RobotCommunicationHandler()
        guiDesigner = GUIDesigner()

        # 通信スレッドを立ち上げる
        self.communication_thread = Thread(
            target=communicationHandler.communication_loop,
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
        guiDesigner.start_gui(self.gui_request_queue, self.gui_responce_queue)
