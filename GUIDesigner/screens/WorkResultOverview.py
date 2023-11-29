from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from GUIDesigner.Frames import Frames
from GUIDesigner.screens.ScreenBase import ScreenBase
from common_data_type import WorkPieceShape
from GUIDesigner.ProcessingData import ProcessingData
from typing import Union
from GUIDesigner.GUIRequestType import GUIRequestType
from GUIDesigner.GUISignalCategory import GUISignalCategory


class WorkResultOverview(ScreenBase):
    def __init__(self, parent, selected_items):
        super().__init__(parent)
        self.selected_items = [
            ProcessingData(1, "ModelA", timedelta(
                minutes=30), WorkPieceShape.CIRCLE, 20.0, "John Doe", datetime.now()),
            ProcessingData(2, "ModelB", timedelta(
                hours=1), WorkPieceShape.SQUARE, 15.0, "Jane Smith", datetime.now()),
            ProcessingData(3, "ModelC", timedelta(
                minutes=45), WorkPieceShape.CIRCLE, 25.0, "Bob Johnson", datetime.now()),
            # Add more instances as needed
        ]
        self._create_widgets()

    def handle_queued_request(self, request_type: Union[GUISignalCategory, GUIRequestType], request_data=None):
        self.handle_pause_and_emergency(request_type, request_data)

    def create_frame(self):
        self.tkraise()

    def _create_widgets(self):
        # Set a custom row height
        custom_row_height = 40  # 必要に応じて行の高さを変更してください

        # Treeview のカスタムフォントを定義
        custom_font = ("AR丸ゴシック体M", 18)  # 必要に応じてフォント名やサイズを変更してください
        style = ttk.Style()
        style.configure("Treeview.Heading", font=custom_font)  # カラム見出しのフォントを設定
        # Treeview アイテムのフォントと行の高さを設定
        style.configure("Treeview", font=custom_font,
                        rowheight=custom_row_height)

        self.label = tk.Label(self, text="加工結果", font=("AR丸ゴシック体M", 36))

        self.tree = ttk.Treeview(self, columns=("ID", "Model", "Processing Time", "Shape",
                                                "Dimension", "Created By", "Timestamp"), show="headings", height=18, style="Treeview")
        self.tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.tree.heading("Model", text="Model", anchor=tk.CENTER)
        self.tree.heading("Processing Time",
                          text="Processing Time", anchor=tk.CENTER)
        self.tree.heading("Shape", text="Shape", anchor=tk.CENTER)
        self.tree.heading("Dimension", text="Dimension", anchor=tk.CENTER)
        self.tree.heading("Created By", text="Created By", anchor=tk.CENTER)
        self.tree.heading("Timestamp", text="Timestamp", anchor=tk.CENTER)

        self.tree.column("#0", stretch=tk.NO, minwidth=0,
                         width=0)  # デフォルトの最初の列を非表示

        # 各列の幅を設定
        self.tree.column("ID", width=50)  # 例: 幅 50 ピクセル
        self.tree.column("Model", width=200)  # 例: 幅 100 ピクセル
        self.tree.column("Processing Time", width=250)  # 例: 幅 150 ピクセル
        self.tree.column("Shape", width=150)  # 例: 幅 80 ピクセル
        self.tree.column("Dimension", width=100)  # 例: 幅 100 ピクセル
        self.tree.column("Created By", width=300)  # 例: 幅 120 ピクセル
        self.tree.column("Timestamp", width=360)  # 例: 幅 150 ピクセル

        for item in self.selected_items:
            self.tree.insert("", "end", values=(item.model_id, item.model_number, str(item.average_processing_time),
                                                item.work_shape, item.workpiece_dimension, item.created_by, item.creation_timestamp))

        scrollbar = tk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.config(yscrollcommand=scrollbar.set)

        kakunin_button = tk.Button(
            self, text="確認", command=self.back_to_selection_frame, font=("AR丸ゴシック体M", 24), width=22)

        self.label.place(relx=0.5, rely=0.02, anchor="n")  # ラベルを画面上部に配置
        self.tree.place(relx=0.5, rely=0.1, anchor="n")  # Treeview を画面中央に配置

        # スクロールバーを右側に合わせて配置
        scrollbar.place(relx=0.877, rely=0.1, relheight=0.71,
                        anchor="ne")  # relheight の値を適切な値に変更

        kakunin_button.place(rely=0.85, relx=0.75)

    def back_to_selection_frame(self):
        self.change_frame(Frames.CREATE_SELECTION)


if __name__ == "__main__":
    app = WorkResultOverview()
