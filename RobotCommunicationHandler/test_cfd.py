import socket
from threading import Thread
import time
import tkinter as tk
import atexit
import select


class _test_cfd:
    def __init__(self, receiv_control_port: int, send_cmd_port: int) -> None:
        self.is_echo_back = False
        self.receiv_control_port = receiv_control_port
        self.send_cmd_port = send_cmd_port
        self.receiv_control_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.receiv_control_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.send_cmd_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.send_cmd_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        atexit.register(lambda: self.receiv_control_socket.close())
        self.receiv_control_socket.setblocking(0)  # ノンブロッキングモードに設定
        self.send_cmd_socket.setblocking(0)        # ノンブロッキングモードに設定

    def _start_test_cfd_screen(self):
        """URとの通信をテストするGUIを立ち上げる関数
        テキストボックスにコマンドを入れて送信すると、PCに対してコマンドを送信し、
        PCからの受信を受けると、テキストボックスにその履歴を表示する
        """
        root_cfd = tk.Tk()
        root_cfd.title("CFD 接続テスト")
        tk.Label(root_cfd, text="Enter message:").grid(row=0, column=0)
        message_entry = tk.Entry(root_cfd)
        message_entry.grid(row=0, column=1)
        send_button = tk.Button(
            root_cfd, text="Send", command=lambda: self.send_message(message_entry.get()))
        send_button.grid(row=1, column=0, columnspan=2)
        # TextウィジェットとScrollbarウィジェットの配置
        self.text_widget = tk.Text(
            root_cfd, wrap=tk.WORD, height=20, width=50, state=tk.DISABLED)

        tk.Label(root_cfd, text="Received message:").grid(row=2, column=0)
        self.text_widget.grid(row=3, column=0, columnspan=2, sticky="nsew")

        scrollbar = tk.Scrollbar(root_cfd)
        scrollbar.grid(row=3, column=2, sticky="ns")

        # TextとScrollbarを連動させる
        self.text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_widget.yview)

        # ウィンドウサイズが変更されたときにTextウィジェットもリサイズされるように設定
        root_cfd.grid_rowconfigure(2, weight=1)
        root_cfd.grid_columnconfigure(1, weight=1)
        root_cfd.mainloop()

    def start(self):
        simulate_thread = Thread(target=self._start_test_cfd_screen)
        simulate_thread.start()
        self._connect()
        self.receiv_control_socket.setblocking(1)  # ブロッキングモードに設定

        while True:
            data = self.receiv_control_socket.recv(1024)
            if not data:
                print("Connection closed by the server")
                break
            data = data.decode('utf-8')
            self._add_message_history(data)

            if self.is_echo_back:
                self.receiv_control_socket.sendall(("cfd : " + data).encode())

    def _add_message_history(self, message: str):
        """受信メッセージの履歴の表示を追加する関数

        Args:
            message (str): 受け取ったメッセージ文字列
        """
        self.text_widget.config(state=tk.NORMAL)  # 編集可能にする
        if not message.endswith("\n"):
            message += "\n"

        self.text_widget.insert(tk.END, message)  # 末尾にデータを追加
        self.text_widget.see(tk.END)             # スクロールして末尾を表示
        self.text_widget.config(state=tk.DISABLED)

    def _connect(self):
        """こちらからPCに接続しに行き、接続が完了するまでループを回す
        """
        """両方のソケットで接続を待ち受ける"""
        self.receiv_control_socket.bind(
            ("localhost", self.receiv_control_port))
        self.receiv_control_socket.listen()
        self.send_cmd_socket.bind(("localhost", self.send_cmd_port))
        self.send_cmd_socket.listen()

        inputs = [self.receiv_control_socket, self.send_cmd_socket]
        connections = []

        while len(connections) < 2:
            readable, _, _ = select.select(inputs, [], [])
            for s in readable:
                if s in inputs:
                    connection, _ = s.accept()
                    print(f"Connected by {s.getsockname()[1]}")
                    connections.append(connection)
                    inputs.remove(s)

        self.receiv_control_socket, self.send_cmd_socket = connections

    def send_message(self, message):
        self.send_cmd_socket.sendall(message.encode())
