from queue import Queue
from GUIDesigner.GUIRequestType import GUIRequestType
from common_data_type import TransmissionTarget
from test_flags import TEST_CFD_CONNECTION_LOCAL, TEST_UR_CONNECTION_LOCAL


class GuiResponceHandler:
    def __init__(self, integration, send_request_queue: Queue):
        self.send_request_queue = send_request_queue
        self.integration = integration

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
            pass

        elif send_data[0] == GUIRequestType.CAMERA_FEED_REQUEST:
            pass

        elif send_data[0] == GUIRequestType.STATUS_REQUEST:
            pass

        elif send_data[0] == GUIRequestType.LIGHTING_CONTROL_REQUEST:
            pass

        elif send_data[0] == GUIRequestType.REQUEST_PROCESSING_DATA_LIST:
            pass
