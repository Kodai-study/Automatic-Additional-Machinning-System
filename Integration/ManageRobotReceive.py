from common_data_type import TransmissionTarget


class ManageRobotReceive:

    def __init__(self, integration_instance):
        self._integration_instance = integration_instance
        self._ur_command_handlers = {
            "SIG 0,ATT_IMP_READY": self._send_message_to_cfd,
            "SIG 0,ATT_DRL_READY": self._send_message_to_cfd,
        }
        self._cfd_command_handlers = {
            "DR_STK_TURNED": self._send_message_to_ur,
            "CYL 001,ON": self._undefine,
            "CYL 003,ON": self._undefine,
            "SNS 001,ON": self._undefine,
            "SNS 002,ON": self._undefine,
            "SIG 0,FST_POSITION": self._send_message_to_ur,
        }

    def _send_message_to_cfd(self, message: str):
        # self._integration_instance.send_request_queue.put(
        #     {"target": TransmissionTarget.CFD, "message": message})
        print("send to cfd: ", message)

    def _send_message_to_ur(self, message: str):
        self._integration_instance.send_request_queue.put(
            {"target": TransmissionTarget.UR, "message": message})
        # print("send to ur: ", message)

    def _undefine(self, message: str):
        print("getmessage ", message)

    def handle_receiv_message(self, receiv_data: tuple):
        if receiv_data["target"] == TransmissionTarget.UR:
            handler = self._ur_command_handlers.get(receiv_data["message"])
        elif receiv_data["target"] == TransmissionTarget.CFD:
            handler = self._cfd_command_handlers.get(receiv_data["message"])
        elif receiv_data["target"] == TransmissionTarget.TEST_TARGET_1:
            handler = self._send_message_to_ur
        elif receiv_data["target"] == TransmissionTarget.TEST_TARGET_2:
            handler = self._send_message_to_cfd
        handler(receiv_data["message"])
