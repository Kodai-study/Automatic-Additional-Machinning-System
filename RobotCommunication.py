# coding: utf-8
from queue import Queue
import socket
from threading import Thread
import socket
import time

TEST_HOST = 'localhost'
TEST_PORT1 = 5000
TEST_PORT2 = 5001

TEST_stop_flag = False


class RobotCommunicationHandler:
    """
    ロボットとの通信を管理するクラス
    常にロボットとのソケット接続を確立しておき、
    送信要求や受信に関する処理を行う
    """

    def __init__(self):
        self.send_queue = None
        self.receive_queue = None
        self.samp_stop_flag = False

    def test_receive_string(self, sock: socket.socket):
        """
        テスト用関数。
        ソケットからデータを受信し、標準出力に出力する。

        Args:
            sock (socket.socket): 受信するソケット。
            接続が完了しているものを渡す。
        """
        while not TEST_stop_flag:
            try:
                data = sock.recv(1024)
                if not data:
                    print("Connection closed by the server")
                    break
                print(f"Main_Received: {data.decode('utf-8')}")
            except Exception as e:
                print(f"Error: {e}")
                break

    def communication_loop(self, send_queue: Queue, receive_queue: Queue):
        """
        受信する、統合スレッドからの送信要求の待ち受けのループを開始する

        Args:
            send_queue (Queue): 統合スレッドに送るデータを入れるキュー\n
            receive_queue (Queue): 統合スレッドから受け取ったデータを入れるキュー
        """
        self.send_queue = send_queue
        self.receive_queue = receive_queue

        # UR、CFD用の2つのソケットの作成(現在はサンプル)
        try:
            self.samp_socket1 = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.samp_socket2 = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)

            self.samp_socket1.connect((TEST_HOST, TEST_PORT1))
            self.samp_socket2.connect((TEST_HOST, TEST_PORT2))
        except Exception as e:
            print('Socket Error: ', e)

        # 2つのソケットと同時に通信するためのスレッドを2つ作成
        receive_thread1 = Thread(
            target=self.test_receive_string, args=(self.samp_socket1,))
        receive_thread1.start()
        receive_thread2 = Thread(
            target=self.test_receive_string, args=(self.samp_socket2,))
        receive_thread2.start()

        while not TEST_stop_flag:
            # send_queueに値が入っているか監視
            if not self.send_queue.empty():
                # send_queueから値を取り出す
                send_data = self.send_queue.get()
                # 取り出した値を接続先に送信
                self.samp_socket1.sendall(send_data.encode('utf-8'))
                self.samp_socket2.sendall(send_data.encode('utf-8'))
                print('Sent:', send_data)


def test_send_data():
    """
    通信スレッドからの送信をテストする。
    2つのソケットに0.1秒間隔で交互に送信する。
    受信した側は、送信したデータを標準出力に出力する。
    """
    from test_receiv import test_receive
    # 別スレッドで、自身からの通信を待ち受けるサーバプログラムを起動する
    receive_thread1 = Thread(target=test_receive, args=(TEST_PORT1,))
    receive_thread2 = Thread(target=test_receive, args=(TEST_PORT2,))
    receive_thread1.start()
    receive_thread2.start()

    communication_thread.start()

    # キューで送信要求を送る
    for i in range(10):
        send_data = f"hello_{i}"
        send_queue.put(send_data)
        time.sleep(0.1)

    receive_thread1.join()
    receive_thread2.join()
    receive_queue.put("exit")


def test_receiv_data():
    """
    通信スレッドの受信をテストする。
    2つのソケットから、1秒ごとに交互にデータを受信する。
    受信したデータを標準出力に出力する。
    """
    from test_send import test_send

    # データを送信するスレッドを2つ作成し、それぞれ別のポートで同時に待ち受ける
    send_thread1 = Thread(target=test_send, args=(TEST_PORT1, 1))
    send_thread2 = Thread(target=test_send, args=(TEST_PORT2, 2))
    send_thread1.start()
    send_thread2.start()

    communication_thread.start()

    send_thread1.join()
    send_thread2.join()


# 通信スレッドと、受信もしくは送信スレッドを立ち上げることで、通信のテストを行う
if __name__ == '__main__':
    communication_handler = RobotCommunicationHandler()

    # 送信要求を入れるキューと、受信したデータを入れるキューを作成
    send_queue = Queue()
    receive_queue = Queue()
    communication_thread = Thread(
        target=communication_handler.communication_loop, args=(send_queue, receive_queue))

    test_receiv_data()
    # test_send_data()
    TEST_stop_flag = True
    print("receive_thread joined")
