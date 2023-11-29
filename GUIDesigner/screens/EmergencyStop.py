import tkinter as tk
from typing import Union
from GUIDesigner.Frames import Frames
from GUIDesigner.GUIRequestType import GUIRequestType
from GUIDesigner.GUISignalCategory import GUISignalCategory
from GUIDesigner.screens.ScreenBase import ScreenBase


class EmergencyStop(ScreenBase):
    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self._create_widgets()
        self.configure(bg="yellow")

    def create_frame(self):
        self.tkraise()

    def handle_queued_request(self, request_type: GUISignalCategory, request_data=None):
        self.handle_pause_and_emergency(request_type, request_data)

    def _create_widgets(self):
        self.emergency_label = tk.Label(self, text="非常停止", font=(
            "AR丸ゴシック体M", 150), fg="red", bg="yellow")

        self.back_button = tk.Button(self, text="戻る", font=(
            "AR丸ゴシック体M", 18), width=22, bg="yellow")

        # ガジェット配置
        self.emergency_label.pack(pady=300)
        self.back_button.place(rely=0.85, relx=0.75)
