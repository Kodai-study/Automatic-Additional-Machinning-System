from datetime import datetime, timedelta
import tkinter as tk
from GUIDesigner.Frames import Frames
from GUIDesigner.ProcessingData import ProcessingData
from common_data_type import WorkPieceShape
from GUIDesigner.GUISignalCategory import GUISignalCategory
from GUIDesigner.screens.ScreenBase import ScreenBase


class WorkRequest(ScreenBase):
    def __init__(self, parent: tk.Tk, image_resources: dict, request_work_data_getter, *args, **keywords):
        super().__init__(parent, *args, **keywords)
        self.work_img = image_resources["work"]
        self._create_widgets()
        self.request_work_data_getter = request_work_data_getter

    def create_frame(self):
        self.tkraise()
        request_work_data = self.request_work_data_getter()
        self._display_image_center()
        self.message_label1["text"] = f"""\
            次の加工データ
                型番: {request_work_data["process_data"].model_number}
                ワークの形: {request_work_data["process_data"].work_shape}
                大きさ: {request_work_data["process_data"].workpiece_dimension}mm"""

    def handle_queued_request(self, request_type: GUISignalCategory, request_data=None):
        self.handle_pause_and_emergency(request_type, request_data)

    def _create_widgets(self):
        self.message_label1 = tk.Label(
            self, text="ワークが不足しています", font=("AR丸ゴシック体M", 18), bg="white")
        # 画像の表示
        # ボタンの配置
        kakunin_button = tk.Button(self, text="確認", font=(
            "AR丸ゴシック体M", 18), width=22, bg="white", command=lambda:self.change_frame(Frames.PROCESSING_PROGRESS))

        # 文を上に配置
        self.message_label1.pack(pady=20)
        # 画像を中央に配置
        kakunin_button.place(rely=0.85, relx=0.75)

    def _display_image_center(self):
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        work_label = tk.Label(self, image=self.work_img, bg="white")
        # 画像サイズの取得
        image_width, image_height = self.work_img.width(), self.work_img.height()
        # 画像を中央に配置するための座標を計算
        x = (window_width - image_width) // 2
        y = (window_height - image_height) // 2
        # 画像の配置
        work_label.place(x=x, y=y)
        # ボタンを右下に配置


if __name__ == "__main__":
    app = WorkRequest()
