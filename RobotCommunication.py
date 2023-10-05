# coding: utf-8
from enum import Enum
from queue import Queue
import socket
from threading import Thread
from test_receiv import receive
import socket
import time

PORT = 5000


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

        HOST = 'localhost'

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print('Connected to', HOST, 'on port', PORT)
            while True:
                # send_queueに値が入っているか監視
                if not self.send_queue.empty():
                    # send_queueから値を取り出す
                    send_data = self.send_queue.get()
                    # 取り出した値を接続先に送信
                    s.sendall(send_data.encode('utf-8'))
                    print('Sent:', send_data)


                if not self.receive_queue.empty():
                    # receive_queueから値を取り出す
                    receive_data = self.receive_queue.get()
                    print('receiv :', receive_data)
                    if receive_data == "exit":
                        break
                time.sleep(0.1)


if __name__ == '__main__':
    # ポート番号をコマンドライン引数から取得する
    communication_handler = RobotCommunicationHandler()

    # 別スレッドで、自身からの通信を待ち受けるサーバプログラムを起動する
    receive_thread = Thread(target=receive, args=(PORT,))
    receive_thread.start()
    send_queue = Queue()
    receive_queue = Queue()
    communication_thread = Thread(
        target=communication_handler.communication_loop, args=(send_queue, receive_queue))

    communication_thread.start()
    for i in range(10):
        send_data = f"hello_{i}"
        send_queue.put(send_data)
        time.sleep(0.1)
    receive_thread.join()
    receive_queue.put("exit")
    print("receive_thread joined")