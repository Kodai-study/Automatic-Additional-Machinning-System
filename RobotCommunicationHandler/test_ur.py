import socket
from threading import Thread
import time
import tkinter as tk


class _test_ur:
    def __init__(self, port) -> None:
        self.is_echo_back = False
        self.port = port
        self.com_to_pc_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

    def _start_test_ur_screen(self):
        root2 = tk.Tk()
        root2.title("Send Message")
        tk.Label(root2, text="Enter message:").grid(row=0, column=0)
        message_entry = tk.Entry(root2)
        message_entry.grid(row=0, column=1)
        send_button = tk.Button(
            root2, text="Send", command=lambda: self.send_message(message_entry.get()))
        send_button.grid(row=1, column=0, columnspan=2)
        root2.mainloop()

    def start(self):
        self._connect()
        simulate_thread = Thread(target=self._start_test_ur_screen)
        simulate_thread.start()
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
        while True:
            try:
                self.com_to_pc_socket.connect(('localhost', self.port))
                print("Connected to the server!")
                break
            except ConnectionRefusedError:
                print("Connection failed. Retrying...")
                time.sleep(1)
        print(f"Connected by {self.port}")

    def send_message(self, message):
        self.com_to_pc_socket.sendall(message.encode())
