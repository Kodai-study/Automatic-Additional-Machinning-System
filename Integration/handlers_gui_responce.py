from queue import Queue
from typing import List
from DBAccessHandler.DBAccessHandler import DBAccessHandler
from GUIDesigner.GUIRequestType import GUIRequestType
from GUIDesigner.GUISignalCategory import GUISignalCategory
from ImageInspectionController.ImageInspectionController import ImageInspectionController
from ImageInspectionController.InspectionResults import CameraControlResult
from ImageInspectionController.OperationType import OperationType
from common_data_type import CameraType, TransmissionTarget
from test_flags import TEST_CFD_CONNECTION_LOCAL, TEST_UR_CONNECTION_LOCAL


class GuiResponceHandler:
    def __init__(self, integration, send_request_queue: Queue, gui_request_queue: Queue):
        self.send_request_queue = send_request_queue
        self.integration = integration
        self.gui_request_queue = gui_request_queue

    def handle(self, send_data):
        if send_data[0] == GUIRequestType.ROBOT_OPERATION_REQUEST:
            if TEST_UR_CONNECTION_LOCAL:
                self.send_request_queue.put(
                    {"target": TransmissionTarget.TEST_TARGET_1, "message": str(send_data[1])})
            else:
                self.send_request_queue.put(
                    {"target": TransmissionTarget.UR, "message": str(send_data[1])})

        elif send_data[0] == GUIRequestType.UPLOAD_PROCESSING_DETAILS:
            self.is_processing_mode = True
            if TEST_CFD_CONNECTION_LOCAL:
                self.send_request_queue.put(
                    {"target": TransmissionTarget.TEST_TARGET_2, "message": "ISRESERVED"})
                self.integration._start_process()

            else:
                self.send_request_queue.put(
                    {"target": TransmissionTarget.CFD, "message": "ISRESERVED"})
                self.integration._start_process()

        elif send_data[0] == GUIRequestType.LOGIN_REQUEST:
            self._login(send_data[1]["id"], send_data[1]["password"])

        elif send_data[0] == GUIRequestType.CAMERA_FEED_REQUEST:
            self._camera_feed(
                self.integration.image_inspection_controller, send_data[1])

        elif send_data[0] == GUIRequestType.STATUS_REQUEST:
            pass

        elif send_data[0] == GUIRequestType.LIGHTING_CONTROL_REQUEST:
            pass

        elif send_data[0] == GUIRequestType.REQUEST_PROCESSING_DATA_LIST:
            pass

    def _login(self, id: str, password: str, database_accesser: DBAccessHandler):
        sql = f"""
        SELECT t_login.employee_no, t_login.password, t_login.authority,
            m_employee.employee_name, m_employee.affiliation
        FROM t_login
        JOIN m_employee ON t_login.employee_no = m_employee.employee_no
        WHERE t_login.employee_no = {id} AND t_login.password = {password}
        """
        result = database_accesser.fetch_data_from_database(sql)
        if len(result) != 1:
            self.gui_request_queue.put(
                GUIRequestType.LOGIN_REQUEST, {"is_success": False})
        else:
            self.gui_request_queue.put(GUISignalCategory.LOGIN_REQUEST,
                                       {"is_success": True, "authority": result[0]["authority"]})

    def _camera_feed(self, image_inspection_controller: ImageInspectionController,  camera_list: List[CameraType]):
        camera_control_result: List[CameraControlResult] = image_inspection_controller.perform_image_operation(
            OperationType.TAKE_INSPECTION_SNAPSHOT, camera_list)
        update_camera_list = []
        for camera_result in camera_control_result:
            if camera_result.is_success:
                update_camera_list.append(
                    (camera_result.camera_type, camera_result.image_path))

        self.gui_request_queue.put(
            GUIRequestType.CAMERA_FEED_REQUEST, update_camera_list)
