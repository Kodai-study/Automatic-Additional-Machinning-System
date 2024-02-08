from queue import Queue
from typing import List
from DBAccessHandler.DBAccessHandler import DBAccessHandler
from GUIDesigner.GUIRequestType import GUIRequestType
from GUIDesigner.GUISignalCategory import GUISignalCategory
from ImageInspectionController.ImageInspectionController import ImageInspectionController
from ImageInspectionController.InspectionResults import CameraControlResult, LightningControlResult
from ImageInspectionController.OperationType import OperationType
from common_data_type import CameraType, LightingType, TransmissionTarget
from test_flags import TEST_CFD_CONNECTION_LOCAL


class GuiResponceHandler:
    def __init__(self, integration, send_request_queue: Queue, gui_request_queue: Queue):
        self.send_request_queue = send_request_queue
        self.integration = integration
        self.gui_request_queue = gui_request_queue

    def handle(self, send_data):
        if send_data[0] == GUIRequestType.ROBOT_OPERATION_REQUEST:
            if TEST_CFD_CONNECTION_LOCAL:
                self.send_request_queue.put(
                    {"target": TransmissionTarget.TEST_TARGET_2, "message": str(send_data[1])})
            else:
                self.send_request_queue.put(
                    {"target": TransmissionTarget.CFD, "message": str(send_data[1])})

        elif send_data[0] == GUIRequestType.UPLOAD_PROCESSING_DETAILS:
            target = TransmissionTarget.TEST_TARGET_2 if TEST_CFD_CONNECTION_LOCAL else TransmissionTarget.CFD
            message = "MODE 0,RESERVE_SET\n" if send_data[1] else "MODE 0,RESERVE_RESET\n"
            self.send_request_queue.put({"target": target, "message": message})

        elif send_data[0] == GUIRequestType.LOGIN_REQUEST:
            self._login(send_data[1]["id"], send_data[1]["password"])

        elif send_data[0] == GUIRequestType.CAMERA_FEED_REQUEST:
            self._camera_feed(
                self.integration.image_inspection_controller, send_data[1])

        elif send_data[0] == GUIRequestType.STATUS_REQUEST:
            self._reload_status()

        elif send_data[0] == GUIRequestType.LIGHTING_CONTROL_REQUEST:
            self._lighting_feed(
                self.integration.image_inspection_controller, self.integration.robot_status, send_data[1][0], send_data[1][1])

        elif send_data[0] == GUIRequestType.REQUEST_PROCESSING_DATA_LIST:
            self._get_process_data_list()

        elif send_data[0] == GUIRequestType.UPLOAD_PROCESSING_DETAILS:
            self.send_request_queue.put(
                {"target": TransmissionTarget.CFD if TEST_CFD_CONNECTION_LOCAL else TransmissionTarget.TEST_TARGET_2, "message": "MODE 0,RESERVE_SET"})

    def _login(self, id: str, password: str, database_accesser: DBAccessHandler):
        sql = f"""
        SELECT t_login.employee_no, t_login.password, t_login.authority,
            m_employee.employee_name, m_employee.affiliation
        FROM t_login
        JOIN m_employee ON t_login.employee_no = m_employee.employee_no
        WHERE t_login.employee_no = %s AND t_login.password = %s
        """
        result = database_accesser.fetch_data_from_database(sql, id, password)
        if len(result) != 1:
            self.gui_request_queue.put(
                GUIRequestType.LOGIN_REQUEST, {"is_success": False})
        else:
            self.gui_request_queue.put(GUIRequestType.LOGIN_REQUEST,
                                       {"is_success": True, "authority": result[0]["authority"]})

    def _camera_feed(self, image_inspection_controller: ImageInspectionController,  camera_list: List[CameraType]):
        camera_control_result: List[CameraControlResult] = image_inspection_controller.perform_image_operation(
            OperationType.TAKE_INSPECTION_SNAPSHOT, camera_list)
        update_camera_list = []
        if not camera_control_result:
            return
        for camera_result in camera_control_result:
            if camera_result.is_success:
                update_camera_list.append(
                    (camera_result.camera_type, camera_result.image_path))

        self.gui_request_queue.put((
            GUIRequestType.CAMERA_FEED_REQUEST, update_camera_list))

    def _reload_status(self):
        fetch_status_commands = [
            ("DOOR", [0, 1, 2, 3]),
            ("DLC", [0, 1, 2, 3]),
            ("RDSW", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
            ("LMSW", [0]),
            ("EMSW", [0]),
            ("SNS", [0, 1, 2, 3, 4, 5]),
            ("WRKSNS", [0])
        ]

        # リスト内包表記を使用
        commands = [f"{cmd} {num},ST" for cmd,
                    nums in fetch_status_commands for num in nums]

        # 条件分岐をループの外に移動
        target = TransmissionTarget.TEST_TARGET_2 if TEST_CFD_CONNECTION_LOCAL else TransmissionTarget.CFD
        for cmd in commands:
            self.send_request_queue.put({"target": target, "message": cmd})

    def _lighting_feed(self,  image_inspection_controller: ImageInspectionController, robot_status: dict, lighting_type: LightingType, status: bool):
        light_type_dict = {
            LightingType.ACCURACY_LIGHTING: "back_light",
            LightingType.PRE_PROCESSING_LIGHTING: "ring_light",
            LightingType.TOOL_LIGHTING: "bar_light"
        }
        result: LightningControlResult = image_inspection_controller.perform_image_operation(
            OperationType.CONTROL_LIGHTING, (lighting_type, status))
        if not result or not result.is_success:
            return
        self.gui_request_queue.put((GUIRequestType.LIGHTING_CONTROL_REQUEST, {
            "target": lighting_type, "state":  result.lighting_state}))

        light_type_key = light_type_dict[lighting_type]
        for key in robot_status["lighting"]:
            if key == light_type_key:
                robot_status["lighting"][key] = result.lighting_state
            else:
                robot_status["lighting"][key] = False
        self.gui_request_queue.put(
            (GUISignalCategory.SENSOR_STATUS_UPDATE, None))

    def _get_process_data_list(self):
        self.integration.process_data_manager.refresh_process_data()
        self.gui_request_queue.put(
            (GUIRequestType.REQUEST_PROCESSING_DATA_LIST, self.integration.process_data_manager))
