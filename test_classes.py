from queue import Queue
from enum import Enum, auto
import time

stop_flag = False


class TransmissionTarget(Enum):
    """
    送信先を表す列挙型
    """

    TEST_TARGET_1 = auto()

    TEST_TARGET_2 = auto()

    UR = auto()
    """
    URに送信する
    """
    CFD = auto()
    """
    CFDに送信する
    """


class RobotCommunicationHandler:
    """
    ロボットとの通信を管理するクラス
    常にロボットとのソケット接続を確立しておき、
    送信要求や受信に関する処理を行う
    """

    def __init__(self):
        self.send_queue = None
        self.receive_queue = None

    def communication_loop(self, send_queue: Queue, receive_queue: Queue):
        """
        受信する、統合スレッドからの送信要求の待ち受けのループを開始する

        Args:
            send_queue (Queue): 統合スレッドに送るデータを入れるキュー\n
            receive_queue (Queue): 統合スレッドから受け取ったデータを入れるキュー
        """
        self.send_queue = send_queue
        self.receive_queue = receive_queue
        self.cnt = 0

        while not stop_flag:
            if self.cnt % 2 == 0:
                self.receive_queue.put(
                    {"target": TransmissionTarget.TEST_TARGET_1, "message": "test1"})
            else:
                self.receive_queue.put(
                    {"target": TransmissionTarget.TEST_TARGET_2, "message": "test2"})

            time.sleep(1)
