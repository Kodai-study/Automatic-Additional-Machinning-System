from queue import Queue
import time
import tkinter as tk
from GUIDesigner.Frames import Frames
from GUIDesigner.GUISignalCategory import GUISignalCategory
from GUIDesigner.screens.ScreenBase import ScreenBase


class WaitConnecting(ScreenBase):
    def __init__(self, parent, request_queue: Queue):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.gui_request_queue = request_queue

        message_label = tk.Label(
            self, text="通信接続を待っています...", font=("AR丸ゴシック体M", 24))
        message_label.pack(pady=200)

    def create_frame(self):
        self.tkraise()
    # 通信確認をスタート
        self.check_connection()

    def connection_is_successful(self):
        while True:
            if not self.gui_request_queue.empty():
                received_data = self.gui_request_queue.get()
                if received_data[0] == GUISignalCategory.ROBOT_CONNECTION_SUCCESS:
                    return True
            else:
                time.sleep(0.1)

        # 通信接続完了の確認を行う処理を追加
    def check_connection(self):
        if self.connection_is_successful():  # 通信接続が成功した場合
            print("通信接続が確立されました")
            self.change_frame(Frames.WAIT_CONNECTION)

        else:
            # 通信がまだ確立されていない場合、定期的に確認する
            self.after(1000, self.check_connection)
