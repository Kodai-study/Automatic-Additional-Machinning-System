import socket
import time
import tkinter as Tk


class _test_ur:
    def __init__(self, port) -> None:
        self.is_echo_back = False
        self.port = port
        self.com_to_pc_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

    def _start_test_ur_screen(self):
        root = Tk.Tk()
        root.title("UR")
        root.geometry("300x300")
        self.label = Tk.Label(root, text="UR")
        self.label.pack()
        self.button = Tk.Button(root, text="Echo Back")
        self.button.pack()
        root.mainloop()

    def start(self):
        self._connect()
        self._start_test_ur_screen()

        while True:
            data = self.com_to_pc_socket.recv(1024)
            if not data:
                print("Connection closed by the server")
                break
            data = data.decode('utf-8')
            print(f"TEST_CFD_Received: {data}")

            if self.is_echo_back:
                self.com_to_pc_socket.sendall(("cfd : " + data).encode())

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
