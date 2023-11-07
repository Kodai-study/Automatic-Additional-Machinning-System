# coding: utf-8
from queue import Queue
import socket
from threading import Thread
import socket
import time
from RobotCommunicationHandler.RobotInteractionType import RobotInteractionType
from common_data_type import TransmissionTarget
from test_flags import TEST_CFD_CONNECTION_LOCAL, TEST_PROCESSING_REPORT, TEST_UR_CONNECTION_LOCAL, TEST_Windows


TEST_HOST_ADDRESS = 'localhost'
HOST_LINUX_ADDRESS = '192.168.16.101'
UR_HOST_ADDRESS = '192.168.16.8'
CFD_HOST_ADDRESS = '192.168.16.9'
TEST_PORT1 = 5000
TEST_PORT2 = 5001
UR_PORT_NUMBER = 8765
CFD_PORT_NUMBER = 8766


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
        self.request_send_queue = None
        self.receive_data_queue = None
        self.samp_stop_flag = False

    def test_receive_string(self, target: TransmissionTarget, sock: socket.socket):
        """
        テスト用関数。
        ソケットからデータを受信し、標準出力と統合ソフトへのキューに出力する。

        Args:
            target (TransmissionTarget): 送受信する相手を指す。\n
            sock (socket.socket): 受信するソケット。接続が完了しているものを渡す。
        """

        while True:
            try:
                data = sock.recv(1024)
                if not data:
                    print("Connection closed by the server")
                    break
                print(f"""Main_Received  target = {
                      target}, message = {data.decode('utf-8')}""")

                self.receive_data_queue.put(
                    {"target": target, "message": data.decode('utf-8'),
                     "msg_type": RobotInteractionType.MESSAGE_RECEIVED})
            except Exception as e:
                print(f"Error: {e}")
                continue

    def connect_to_ur(self, socket: socket.socket, host: str, port: int) -> socket.socket:
        """
        URとの接続を行うために、接続を待ち受ける関数

        Args:
            socket (socket.socket): 接続するソケット
            host (str): 接続先のIPアドレス
            port (int): 接続先のポート番号

        Returns:
            socket.socket: 接続が完了したソケット
            """
        socket.bind((host, port))
        socket.listen()
        print(f"""UR との接続を待機中... IPアドレス:{
            host} ポート番号: {port}, """)
        socket, _ = socket.accept()
        return socket

    def connect_to_cfd(self, socket: socket.socket, host: str, port: int) -> socket.socket:
        """
        CFDとの接続を行うために、接続を待ち受ける関数

        Args:
            socket (socket.socket): 接続するソケット
            host (str): 接続先のIPアドレス
            port (int): 接続先のポート番号

        Returns:
            socket.socket: 接続が完了したソケット
            """
        while True:
            try:
                socket.connect((host, port))
                print("Connected to the server!")
                break
            except ConnectionRefusedError:
                print("CFD Connection failed. Retrying...")
                time.sleep(1)
        print(f"Connected by {port}")
        print(f"""CFD との接続を待機中... IPアドレス:{
            host} ポート番号: {port}, """)
        return socket

    def communication_loop(self, request_send_queue: Queue, receive_data_queue: Queue):
        """
        受信する、統合スレッドからの送信要求の待ち受けのループを開始する

        Args:
            send_queue (Queue): 統合スレッドからの送信要求を受け取るキュー\n
            receive_queue (Queue): 統合スレッドへ受け取ったデータを渡すキュー
        """
        self.request_send_queue = request_send_queue
        self.receive_data_queue = receive_data_queue

        # UR、CFD用の2つのソケットの作成(現在はサンプル)
        try:

            if not TEST_UR_CONNECTION_LOCAL:
                self.samp_socket_ur = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)

                if TEST_Windows:
                    self.samp_socket_ur = self.connect_to_ur(
                        self.samp_socket_ur, TEST_HOST_ADDRESS, UR_PORT_NUMBER)
                else:
                    self.samp_socket_ur = self.connect_to_ur(
                        self.samp_socket_ur, HOST_LINUX_ADDRESS, UR_PORT_NUMBER)

                receive_data_queue.put({"target": TransmissionTarget.UR,
                                        "msg_type": RobotInteractionType.SOCKET_CONNECTED})
            else:
                self.dummy_ur_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)

                if TEST_Windows:
                    self.dummy_ur_socket = self.connect_to_ur(
                        self.dummy_ur_socket, TEST_HOST_ADDRESS, TEST_PORT1)
                else:
                    self.dummy_ur_socket = self.connect_to_ur(
                        self.dummy_ur_socket, HOST_LINUX_ADDRESS, TEST_PORT1)
                receive_data_queue.put({"target": TransmissionTarget.TEST_TARGET_1,
                                        "msg_type": RobotInteractionType.SOCKET_CONNECTED})

            if not TEST_CFD_CONNECTION_LOCAL:
                self.samp_socket_cfd = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)

                if TEST_Windows:
                    self.samp_socket_cfd = self.connect_to_cfd(
                        self.samp_socket_cfd, TEST_HOST_ADDRESS, CFD_PORT_NUMBER)
                else:
                    self.samp_socket_cfd = self.connect_to_cfd(
                        self.samp_socket_cfd, HOST_LINUX_ADDRESS, CFD_PORT_NUMBER)

                receive_data_queue.put({"target": TransmissionTarget.CFD,
                                        "msg_type": RobotInteractionType.SOCKET_CONNECTED})

            else:
                self.dummy_cfd_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                if TEST_Windows:
                    self.dummy_cfd_socket = self.connect_to_cfd(
                        self.dummy_cfd_socket, TEST_HOST_ADDRESS, TEST_PORT2)
                else:
                    self.dummy_cfd_socket = self.connect_to_cfd(
                        self.dummy_cfd_socket, HOST_LINUX_ADDRESS, TEST_PORT2)
                receive_data_queue.put({"target": TransmissionTarget.TEST_TARGET_2,
                                        "msg_type": RobotInteractionType.SOCKET_CONNECTED})

        except Exception as e:
            print('Socket Error: ', e)

        if TEST_UR_CONNECTION_LOCAL:
            # 2つのソケットと同時に通信するためのスレッドを2つ作成
            receive_thread1 = Thread(
                target=self.test_receive_string, args=(TransmissionTarget.TEST_TARGET_1, self.dummy_ur_socket))
            receive_thread1.start()

        if TEST_CFD_CONNECTION_LOCAL:
            receive_thread2 = Thread(
                target=self.test_receive_string, args=(TransmissionTarget.TEST_TARGET_2, self.dummy_cfd_socket))
            receive_thread2.start()

        elif TEST_PROCESSING_REPORT:
            # 2つのソケットと同時に通信するためのスレッドを2つ作成
            receive_thread1 = Thread(
                target=self.test_receive_string, args=(TransmissionTarget.UR, self.samp_socket_ur))
            receive_thread1.start()
            # send_input_command(self.samp_socket_ur)

        while True:
            # send_queueに値が入っているか監視
            if not self.request_send_queue.empty():
                # send_queueから値を取り出す
                send_data = self.request_send_queue.get()

                if (send_data['target'] == TransmissionTarget.UR):
                    target_socket = self.samp_socket_ur
                elif (send_data['target'] == TransmissionTarget.CFD):
                    target_socket = self.samp_socket_cfd
                elif (send_data['target'] == TransmissionTarget.TEST_TARGET_1):
                    target_socket = self.dummy_ur_socket
                elif (send_data['target'] == TransmissionTarget.TEST_TARGET_2):
                    target_socket = self.dummy_cfd_socket

                target_socket.sendall(
                    send_data['message'].encode('utf-8'))
            time.sleep(0.1)
