import socket

import time


class _test_ur:
    def __init__(self, port) -> None:
        self.port = port
        self.com_to_pc_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self._connect()
        while True:
            data = self.com_to_pc_socket.recv(1024)
            if not data:
                print("Connection closed by the server")
                break
                # print(f"Main_Received: {data.decode('utf-8')}")
            data = data.decode('utf-8')
            self.com_to_pc_socket.sendall(("cfd" + data).encode())

    def _connect(self):
        # ソケットが接続されるまで待つ
        while True:
            try:
                self.com_to_pc_socket.connect(('localhost', self.port))
                print("Connected to the server!")
                break
            except ConnectionRefusedError:
                print("Connection failed. Retrying...")
                time.sleep(1)
        print(f"Connected by {self.port}")
