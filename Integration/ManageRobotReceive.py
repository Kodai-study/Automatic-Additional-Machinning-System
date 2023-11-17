from GUIDesigner.GUISignalCategory import GUISignalCategory
from RobotCommunicationHandler.RobotInteractionType import RobotInteractionType
from common_data_type import TransmissionTarget
from test_flags import TEST_UR_CONNECTION_LOCAL


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
        self._ur_command_handlers = {
            "SIG 0,ATT_IMP_READY": self._send_message_to_cfd,
            "SIG 0,ATT_DRL_READY": self._send_message_to_cfd
        }
        self._cfd_command_handlers = {
            "DR_STK_TURNED": self._send_message_to_ur,
            "CYL 001,ON": self._undefine,
            "CYL 003,ON": self._undefine,
            "SNS 001,ON": self._undefine,
            "SNS 002,ON": self._undefine,
            "SIG 0,FST_POSITION": self._send_message_to_ur
        }
        self._report_test_handlers = {
            "SIG 0,ATT_DRL_READY": self._send_to_gui,
            "SIG 0,ATT_IMP_READY": self._send_to_gui,
            "SIG DET": self._send_to_gui,
            "FINISH": self._send_to_gui
        }

    def _send_message_to_cfd(self, message: str):
        """
        メッセージのハンドラ。CFDにメッセージを送信する

        Args:
            message (str): 送信するコマンド文字列
        """
        # self._integration_instance.send_request_queue.put(
        #     {"target": TransmissionTarget.CFD, "message": message})
        print("send to cfd: ", message)

    def _send_message_to_ur(self, message: str):
        """
        メッセージのハンドラ。URにメッセージを送信する

        Args:
            message (str): 送信するコマンド文字列
        """
        self._integration_instance.send_request_queue.put(
            {"target": TransmissionTarget.TEST_TARGET_1 if TEST_UR_CONNECTION_LOCAL else TransmissionTarget.UR,
             "message": message})
        # print("send to ur: ", message)

    def _undefine(self, message: str):
        """
        ハンドラ。適切な処理がまだ割り当てられていないメッセージを受け取ったときに呼び出される
        Args:
            message (str): _description_
        """
        print("undefined message : ", message)

    def _handle_connection_success(self, target: TransmissionTarget):
        """接続成功時に呼び出されるハンドラ

        Args:
            target (TransmissionTarget): 接続成功した相手
        """
        self._integration_instance.gui_request_queue.put(
            (GUISignalCategory.ROBOT_CONNECTION_SUCCESS, target))

    def _send_to_gui(self, message: str):
        """GUIに、ロボットから受け取ったメッセージをそのまま送信する

        Args:
            message (str): ロボットから受け取ったメッセージ
        """
        self._integration_instance.gui_request_queue.put(
            (RobotInteractionType.MESSAGE_RECEIVED, message))

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
            self._handle_connection_success(receiv_data["target"])
            return

        if receiv_data["target"] == TransmissionTarget.UR:
            # handler = self._ur_command_handlers.get(receiv_data["message"])
            handler = self._report_test_handlers.get(receiv_data["message"])
        elif receiv_data["target"] == TransmissionTarget.CFD:
            # handler = self._cfd_command_handlers.get(receiv_data["message"])
            handler = self._report_test_handlers.get(receiv_data["message"])
        elif receiv_data["target"] == TransmissionTarget.TEST_TARGET_1:
            handler = self._report_test_handlers.get(receiv_data["message"])
        elif receiv_data["target"] == TransmissionTarget.TEST_TARGET_2:
            handler = self._report_test_handlers.get(receiv_data["message"])

        if not handler:
            handler = self._undefine
        handler(receiv_data["message"])
