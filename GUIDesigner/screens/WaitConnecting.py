from queue import Queue
import time
import tkinter as tk
from GUIDesigner.Frames import Frames
from GUIDesigner.GUISignalCategory import GUISignalCategory
from GUIDesigner.screens.ScreenBase import ScreenBase


class WaitConnecting(ScreenBase):
    def __init__(self, parent, request_queue: Queue):
        super().__init__(parent)
        self.gui_request_queue = request_queue
        self.is_connection_ur = False
        self.is_connection_cfd = False

        message_label = tk.Label(
            self, text="通信接続を待っています...", font=("AR丸ゴシック体M", 24))
        message_label.pack(pady=200)

    def create_frame(self):
        self.tkraise()

    def handle_queued_request(self, request_type: GUISignalCategory, request_data=None):
        self.handle_pause_and_emergency(request_type, request_data)
        if not request_type[0] == GUISignalCategory.ROBOT_CONNECTION_SUCCESS:
            return
        self.is_connection_ur = True
        self.is_connection_cfd = True

        if self.is_connection_ur and self.is_connection_cfd:
            self.change_frame(Frames.LOGIN)
