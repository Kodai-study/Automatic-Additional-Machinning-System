from datetime import datetime, timedelta
import tkinter as tk
from GUIDesigner.ProcessingData import ProcessingData
from common_data_type import WorkPieceShape
from GUIDesigner.GUISignalCategory import GUISignalCategory
from GUIDesigner.screens.ScreenBase import ScreenBase


class WorkRequest(ScreenBase):
    def __init__(self, parent: tk.Tk, image_resources: dict, *args, **keywords):
        super().__init__(parent, *args, **keywords)
        self.work_img = image_resources["work"]
        self.processing_data_list = [
            ProcessingData(1, "ModelA", timedelta(
                minutes=30), WorkPieceShape.CIRCLE, 20.0, "John Doe", datetime.now()),
            ProcessingData(2, "ModelB", timedelta(
                hours=1), WorkPieceShape.SQUARE, 15.0, "Jane Smith", datetime.now()),
            ProcessingData(3, "ModelC", timedelta(
                minutes=45), WorkPieceShape.CIRCLE, 25.0, "Bob Johnson", datetime.now()),
            # Add more instances as needed
        ]
        self._create_widgets()

    def create_frame(self):
        self.tkraise()

    def handle_queued_request(self, request_type: GUISignalCategory, request_data=None):
        self.handle_pause_and_emergency(request_type, request_data)

    def _create_widgets(self):
        # 背景色を白に設定

        # 文を表示
        message_label1 = tk.Label(
            self, text="ワークが不足しています", font=("AR丸ゴシック体M", 18), bg="white")
        message_label2 = tk.Label(self, text=f"次に加工するデータは{self.processing_data_list[1].model_number}です", font=(
            "AR丸ゴシック体M", 18), bg="white")
        message_label3 = tk.Label(self, text=f"{self.processing_data_list[1].workpiece_dimension}の大きさのワークをストッカーに入れてください", font=(
            "AR丸ゴシック体M", 18), bg="white")

        # 画像の表示
        work_label = tk.Label(self, image=self.work_img, bg="white")

        # ボタンの配置
        kakunin_button = tk.Button(self, text="確認", font=(
            "AR丸ゴシック体M", 18), width=22, bg="white")

        # ガジェット配置

        # 文を上に配置
        message_label1.pack(pady=20)
        message_label2.pack(pady=10)
        message_label3.pack(pady=10)

        # 画像を中央に配置
        work_label.pack(pady=(1080 - self.work_img.height()) // 2)

        # ボタンを右下に配置
        kakunin_button.place(rely=0.85, relx=0.75)


if __name__ == "__main__":
    app = WorkRequest()
