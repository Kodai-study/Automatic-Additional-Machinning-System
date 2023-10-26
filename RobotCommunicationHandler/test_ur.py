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
        """URとの通信をテストするGUIを立ち上げる関数
        テキストボックスにコマンドを入れて送信すると、PCに対してコマンドを送信し、
        PCからの受信を受けると、テキストボックスにその履歴を表示する
        """
        root2 = tk.Tk()
        root2.title("UR 接続テスト")
        tk.Label(root2, text="Enter message:").grid(row=0, column=0)
        message_entry = tk.Entry(root2)
        message_entry.grid(row=0, column=1)
        send_button = tk.Button(
            root2, text="Send", command=lambda: self.send_message(message_entry.get()))
        send_button.grid(row=1, column=0, columnspan=2)
        # TextウィジェットとScrollbarウィジェットの配置
        self.text_widget = tk.Text(
            root2, wrap=tk.WORD, height=20, width=50, state=tk.DISABLED)

        tk.Label(root2, text="Received message:").grid(row=2, column=0)
        self.text_widget.grid(row=3, column=0, columnspan=2, sticky="nsew")

        scrollbar = tk.Scrollbar(root2)
        scrollbar.grid(row=3, column=2, sticky="ns")

        # TextとScrollbarを連動させる
        self.text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_widget.yview)

        # ウィンドウサイズが変更されたときにTextウィジェットもリサイズされるように設定
        root2.grid_rowconfigure(2, weight=1)
        root2.grid_columnconfigure(1, weight=1)
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
            self._add_message_history(data)

            if self.is_echo_back:
                self.com_to_pc_socket.sendall(("cfd : " + data).encode())

    def _add_message_history(self, message: str):
        """受信メッセージの履歴の表示を追加する関数

        Args:
            message (str): 受け取ったメッセージ文字列
        """
        self.text_widget.config(state=tk.NORMAL)  # 編集可能にする
        self.text_widget.insert(tk.END, message)  # 末尾にデータを追加
        self.text_widget.see(tk.END)             # スクロールして末尾を表示
        self.text_widget.config(state=tk.DISABLED)

    def _connect(self):
        """こちらからPCに接続しに行き、接続が完了するまでループを回す
        """
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
