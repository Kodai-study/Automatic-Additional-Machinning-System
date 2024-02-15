from queue import Queue
import threading
import time
from DBAccessHandler.DBAccessHandler import DBAccessHandler
from ImageInspectionController.ImageInspectionController import ImageInspectionController
from ImageInspectionController.InspectionResults import ToolInspectionResult
from Integration.ManageRobotReceive import ManageRobotReceive
from Integration.ProcessManager import ProcessManager
from Integration.GuiResponceHandler import GuiResponceHandler
from RobotCommunicationHandler.RobotCommunicationHandler \
    import TEST_PORT1, TEST_PORT2_RECEIV, TEST_PORT2_SEND, RobotCommunicationHandler
from threading import Thread
from RobotCommunicationHandler.test_cfd import _test_cfd
from RobotCommunicationHandler.test_ur import _test_ur
from test_flags import TEST_CFD_CONNECTION_LOCAL, TEST_FEATURE_CONNECTION, TEST_UR_CONNECTION_LOCAL, TEST_FEATURE_GUI
from common_data_type import LightingType, ToolType, TransmissionTarget
from Integration.ProcessDataManager import ProcessDataManager
if TEST_FEATURE_GUI:
    from GUIDesigner.GUIDesigner import GUIDesigner
    from GUIDesigner.GUIRequestType import GUIRequestType
    from GUIDesigner.GUISignalCategory import GUISignalCategory
toggle_flag = True
QUEUE_WATCH_RATE = 0.03


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
        if TEST_FEATURE_CONNECTION:
            if TEST_UR_CONNECTION_LOCAL:
                self.test_ur = _test_ur(TEST_PORT1)

            if TEST_CFD_CONNECTION_LOCAL:
                self.test_cfd = _test_cfd(TEST_PORT2_SEND, TEST_PORT2_RECEIV)

        self.robot_status = {
            "is_connection": True,
            "ejector": False,
            "lighting": {
                "back_light": False, "bar_light": False, "ring_light": False
            },
            "sensor": {
                0: False, 1: False, 2: False, 3: False, 4: False, 5: False
            },
            "reed_switch": {
                0: {"forward": False, "backward": False}, 1: {"forward": False, "backward": False}, 2: {"forward": False, "backward": False},
                3: {"backward": False}, 4: {"forward": False, "backward": False}
            },
            "door_lock": False,
            "door": False,
            "limit_switch": False,
            "stepper_motor": False
        }
        self.tool_stock_informations = [None] * 9
        self.tool_stock_informations[0] = "Do not use!!"
        self.tool_stock_informations = [
            None,
            ToolInspectionResult(result=True, error_items=None,
                                 tool_type=ToolType.M3_DRILL, tool_length=44.5, drill_diameter=2.54),
            ToolInspectionResult(result=True, error_items=None,
                                 tool_type=ToolType.M4_DRILL, tool_length=49.27, drill_diameter=3.43),
            ToolInspectionResult(result=True, error_items=None,
                                 tool_type=ToolType.M5_DRILL, tool_length=54.01, drill_diameter=4.36),
            ToolInspectionResult(result=True, error_items=None,
                                 tool_type=ToolType.M6_DRILL, tool_length=54.60, drill_diameter=5.22),
            ToolInspectionResult(result=True, error_items=None,
                                 tool_type=ToolType.M3_TAP, tool_length=36.04, drill_diameter=2.83),
            ToolInspectionResult(result=True, error_items=None,
                                 tool_type=ToolType.M4_TAP, tool_length=36.75, drill_diameter=3.73),
            ToolInspectionResult(result=True, error_items=None,
                                 tool_type=ToolType.M5_TAP, tool_length=42.56, drill_diameter=4.92),
            ToolInspectionResult(result=True, error_items=None,
                                 tool_type=ToolType.M6_TAP, tool_length=44.87, drill_diameter=5.7),
        ]
        self.image_inspection_controller = ImageInspectionController(self._update_light_status,
            self.tool_stock_informations)
        self.database_accesser = DBAccessHandler()
        self.process_data_manager = ProcessDataManager(self.database_accesser)

        if TEST_FEATURE_CONNECTION:
            self.communicationHandler = RobotCommunicationHandler()
        if TEST_FEATURE_GUI:
            self.guiDesigner = GUIDesigner()
        self.robot_message_handler = ManageRobotReceive(self)

        self.is_processing_mode = False
        self.gui_responce_handler = GuiResponceHandler(
            self, self.send_request_queue, self.gui_request_queue)
        self.process_manager = ProcessManager(self.tool_stock_informations)
        self.message_wait_conditions = {}
        self.send_request_queue.put(
            ({"target": TransmissionTarget.CFD, "message": "MODE 0,RESERVE_RESET\n"}))
        
        request_state_command = [["SNS", 0,1,2,3,4,5],["EJCT",0],["RDSW",0,1,2,3,4,5,7,8,9],["DLC",0],["DOOR",0],["LMSW",0]]
        for commands in request_state_command:
            for command in commands[1:]:
                self.send_request_queue.put(
                    ({"target": TransmissionTarget.CFD, "message": f"{commands[0]} {command},ST\n"}))


    def _watching_guiResponce_queue(self):
        """
        GUIから、ロボットへの操作要求があると、そのコマンドを送信する
        """
        while True:
            if not self.gui_responce_queue.empty():
                # send_queueから値を取り出す
                send_data = self.gui_responce_queue.get()
                self.gui_responce_handler.handle(send_data)
            time.sleep(QUEUE_WATCH_RATE)

    def _regist_wait_command(self, target_or_message_type: TransmissionTarget, message: str):
        waiting_condition = threading.Condition()
        self.message_wait_conditions[(
            target_or_message_type, message)] = waiting_condition
        return waiting_condition

    def _robot_message_handle(self):
        while True:
            if self.comm_receiv_queue.empty():
                time.sleep(QUEUE_WATCH_RATE)
                continue
                # send_queueから値を取り出す
            receiv_data = self.comm_receiv_queue.get()
            if receiv_data.get("message"):
                waiting_condition = self.message_wait_conditions.get(
                    (receiv_data["target"], receiv_data["message"]))
            else:
                waiting_condition = self.message_wait_conditions.get(
                    (receiv_data["target"], receiv_data["msg_type"]))
            if waiting_condition:
                with waiting_condition:
                    waiting_condition.notify_all()

            self.robot_message_handler.handle_receiv_message(receiv_data)
            print("受信データ : ", receiv_data)

    def _initialization(self):
        self.is_ur_connected = False
        self.is_cfd_connected = False
        # 通信が確立するまで待機
        while not (self.is_ur_connected and self.is_cfd_connected):
            time.sleep(0.5)

    def _test_camera_request(self, request_list: list):
        global toggle_flag

        toggle_flag = not toggle_flag
        camera_image_list = []
        for camera_type in request_list:
            camera_image_list.append((
                camera_type, "resource/images/title.png" if toggle_flag else "resource/images/test.png"))
        self.gui_request_queue.put(
            (GUIRequestType.CAMERA_FEED_REQUEST, camera_image_list))

    def _update_light_status(self, lighting_type: LightingType, status: bool):
        light_type_dict = {
            LightingType.ACCURACY_LIGHTING: "back_light",
            LightingType.PRE_PROCESSING_LIGHTING: "ring_light",
            LightingType.TOOL_LIGHTING: "bar_light"
        }
        self.robot_status["lighting"][light_type_dict[lighting_type]] = status
        self.gui_responce_queue.put(
            (GUISignalCategory.SENSOR_STATUS_UPDATE, None))

    def main(self):
        # 通信スレッドを立ち上げる
        if TEST_FEATURE_CONNECTION:
            # 通信相手のURがいない場合、localhostで通信相手をスレッドで立ち上げる
            if TEST_UR_CONNECTION_LOCAL:
                test_ur_thread = Thread(target=self.test_ur.start)
                test_ur_thread.daemon = True
                test_ur_thread.start()

            if TEST_CFD_CONNECTION_LOCAL:
                test_cfd_thread = Thread(target=self.test_cfd.start)
                test_cfd_thread.daemon = True
                test_cfd_thread.start()

            self.communication_thread = Thread(
                target=self.communicationHandler.communication_loop,
                args=(self.send_request_queue, self.comm_receiv_queue))
            self.communication_thread.daemon = True
            self.communication_thread.start()

        time.sleep(3)

        test_send_thread = Thread(
            target=self._robot_message_handle)
        test_send_thread.daemon = True
        test_send_thread.start()

        if TEST_FEATURE_GUI:
            test_watching_guiResponce_queue_thread = Thread(
                target=self._watching_guiResponce_queue)
            test_watching_guiResponce_queue_thread.daemon = True
            test_watching_guiResponce_queue_thread.start()

            self.guiDesigner.start_gui(
                self.gui_request_queue, self.gui_responce_queue, self.robot_status)
        else:
            self._watching_guiResponce_queue()
            # start_process(self)
