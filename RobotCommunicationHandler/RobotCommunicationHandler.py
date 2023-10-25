# coding: utf-8
from queue import Queue
from enum import Enum, auto
import socket
from threading import Thread
import socket
import time
from RobotCommunicationHandler.ProcessingReportOperation import send_input_command
from test_flags import TEST_PROCESSING_REPORT, TEST_UR_CONN, TEST_Windows


TEST_HOST_ADDRESS = 'localhost'
HOST_LINUX_ADDRESS = '192.168.16.101'
UR_HOST_ADDRESS = '192.168.16.8'
CFD_HOST_ADDRESS = '192.168.16.9'
TEST_PORT1 = 5000
TEST_PORT2 = 5001
UR_PORT_NUMBER = 8765
CFD_PORT_NUMBER = 8766


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

    送信を行うときは、send_queueに送信要求を入れる。形式はdictを使用し、
        {"target": TransmissionTarget, "message": str}
    のようにする。TransmissionTargetをインポートし、送信先を指定する。

    受信は、同じようにreceive_queueから受け取る。形式はdictを使用し、
        {"target": TransmissionTarget, "message": str}
    のようになる。
    """

    def __init__(self):
        self.send_queue = None
        self.receive_queue = None
        self.samp_stop_flag = False

    def test_receive_string(self, target: TransmissionTarget, sock: socket.socket):
        """
        テスト用関数。
        ソケットからデータを受信し、標準出力に出力する。

        Args:
            sock (socket.socket): 受信するソケット。
            接続が完了しているものを渡す。
        """

        while True:
            try:
                data = sock.recv(1024)
                if not data:
                    print("Connection closed by the server")
                    break
                print(f"Main_Received: {data.decode('utf-8')}")

                self.receive_queue.put(
                    {"target": target, "message": data.decode('utf-8')})
            except Exception as e:
                print(f"Error: {e}")
                continue

    def communication_loop(self, send_queue: Queue, receive_queue: Queue):
        """
        受信する、統合スレッドからの送信要求の待ち受けのループを開始する

        Args:
            send_queue (Queue): 統合スレッドからの送信要求を受け取るキュー\n
            receive_queue (Queue): 統合スレッドへ受け取ったデータを渡すキュー
        """
        self.send_queue = send_queue
        self.receive_queue = receive_queue

        # UR、CFD用の2つのソケットの作成(現在はサンプル)
        try:

            if not TEST_UR_CONN:
                self.samp_socket_ur = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)

                # self.samp_socket_cfd = socket.socket(
                #     socket.AF_INET, socket.SOCK_STREAM)
                # self.samp_socket_cfd.connect((TEST_HOST, TEST_PORT2))

                if TEST_Windows:
                    self.samp_socket_ur.bind(
                        (TEST_HOST_ADDRESS, UR_PORT_NUMBER))
                    self.samp_socket_ur.listen()
                    print(TEST_HOST_ADDRESS, UR_PORT_NUMBER)
                    print(f"""UR との接続を待機中... IPアドレス:{
                        TEST_HOST_ADDRESS} ポート番号: {UR_PORT_NUMBER}, """)

                else:
                    self.samp_socket_ur.bind(
                        (HOST_LINUX_ADDRESS, UR_PORT_NUMBER))
                    self.samp_socket_ur.listen()
                    print(HOST_LINUX_ADDRESS, UR_PORT_NUMBER)

                self.samp_socket_ur, _ = self.samp_socket_ur.accept()
                # TODO: 統合スレッドとの通信体系をわかりやすい形にする
                # time.sleep(2)
                receive_queue.put("UR_CONN_SUCCESS")

            else:
                self.dummy_ur_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)

                # self.dummy_cfd_socket = socket.socket(
                #     socket.AF_INET, socket.SOCK_STREAM)
                # self.dummy_cfd_socket.connect((TEST_HOST, TEST_PORT2))

                self.dummy_ur_socket.bind((TEST_HOST_ADDRESS, TEST_PORT1))
                self.dummy_ur_socket.listen()
                self.dummy_ur_socket, _ = self.dummy_ur_socket.accept()
                # TODO: 統合スレッドとの通信体系をわかりやすい形にする
                receive_queue.put("UR_CONN_SUCCESS")

        except Exception as e:
            print('Socket Error: ', e)

        if TEST_PROCESSING_REPORT:
            # 2つのソケットと同時に通信するためのスレッドを2つ作成
            receive_thread1 = Thread(
                target=self.test_receive_string, args=(TransmissionTarget.TEST_TARGET_1, self.samp_socket_ur))
            receive_thread1.start()
            # send_input_command(self.samp_socket_ur)
            

        if TEST_UR_CONN:
            # 2つのソケットと同時に通信するためのスレッドを2つ作成
            receive_thread1 = Thread(
                target=self.test_receive_string, args=(TransmissionTarget.TEST_TARGET_1, self.dummy_ur_socket))
            receive_thread1.start()
        # receive_thread2 = Thread(
        #     target=self.test_receive_string, args=(TransmissionTarget.TEST_TARGET_2, self.samp_socket_cfd))
        # receive_thread2.start()

            # send_queueに値が入っているか監視
        if not self.send_queue.empty():
            # send_queueから値を取り出す
            send_data = self.send_queue.get()

            if (send_data['target'] == TransmissionTarget.TEST_TARGET_1):
                target_socket = self.samp_socket_ur if not TEST_UR_CONN else self.dummy_ur_socket
            elif (send_data['target'] == TransmissionTarget.TEST_TARGET_2):
                target_socket = self.samp_socket_cfd if not TEST_UR_CONN else self.dummy_cfd_socket

            target_socket.sendall(
                send_data['message'].encode('utf-8'))
        time.sleep(0.1)
