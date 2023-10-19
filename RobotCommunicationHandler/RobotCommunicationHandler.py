# coding: utf-8

from common_data_type import *
from queue import Queue

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


