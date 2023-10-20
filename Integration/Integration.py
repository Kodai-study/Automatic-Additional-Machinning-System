from queue import Queue
import time
from GUIDesigner.GUIDesigner import GUIDesigner
from RobotCommunicationHandler.RobotCommunicationHandler \
    import TEST_PORT1, RobotCommunicationHandler, TransmissionTarget
from threading import Thread
from RobotCommunicationHandler.test_ur import _test_ur
from test_flags import TEST_GUI_REQUEST, TEST_UR_CONN


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
        if TEST_UR_CONN:
            self.test_ur = _test_ur(TEST_PORT1)

    def test_send(self):
        """
        GUIからの要求をシミュレートし、送信キューに値を入れるテスト関数
        """
        while True:
            self.send_request_queue.put(
                {"target": TransmissionTarget.TEST_TARGET_1, "message": "test"})
            time.sleep(5)

    def test_watching_guiRequest_queue(self):
        """
        テスト用関数。  GUIからの送信要求があると、そのまま通信スレッドのキューに入れて送信する
        """
        while True:
            if not self.gui_request_queue.empty():
                # send_queueから値を取り出す
                send_data = self.gui_request_queue.get()
                self.send_request_queue.put(
                    {"target": TransmissionTarget.TEST_TARGET_1, "message": str(send_data)})
            time.sleep(0.1)

    def main(self):
        communicationHandler = RobotCommunicationHandler()
        guiDesigner = GUIDesigner()
        # 通信スレッドを立ち上げる
        self.communication_thread = Thread(
            target=communicationHandler.communication_loop,
            args=(self.send_request_queue, self.comm_receiv_queue))
        self.communication_thread.start()

        # 通信相手のURがいない場合、localhostで通信相手をスレッドで立ち上げる
        if (TEST_UR_CONN):
            test_ur_thread = Thread(target=self.test_ur.start)
            test_ur_thread.start()

        if TEST_GUI_REQUEST:
            # GUIからの送信要求をそのまま相手に送信するスレッドを立ち上げる
            test_send_thread = Thread(
                target=self.test_watching_guiRequest_queue)

        test_send_thread.start()
        guiDesigner.start_gui(self.gui_request_queue, self.gui_responce_queue)
