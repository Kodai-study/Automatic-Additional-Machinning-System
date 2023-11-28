from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from common_data_type import WorkPieceShape
from GUIDesigner.ProcessingData import ProcessingData

class WorkResultOverview:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1920x1080+0+0")
        self.processing_data_list = [
            ProcessingData(1, "ModelA", timedelta(minutes=30), WorkPieceShape.CIRCLE, 20.0, "John Doe", datetime.now()),
            ProcessingData(2, "ModelB", timedelta(hours=1), WorkPieceShape.SQUARE, 15.0, "Jane Smith", datetime.now()),
            ProcessingData(3, "ModelC", timedelta(minutes=45), WorkPieceShape.CIRCLE, 25.0, "Bob Johnson", datetime.now()),
            # Add more instances as needed
        ]
        self.create_frame(self.processing_data_list)
        self.root.mainloop()

    def create_frame(self, selected_items):
        self.frame = tk.Frame(self.root)

        # Set a custom row height
        custom_row_height = 40  # 必要に応じて行の高さを変更してください

        # Treeview のカスタムフォントを定義
        custom_font = ("AR丸ゴシック体M", 18)  # 必要に応じてフォント名やサイズを変更してください
        style = ttk.Style()
        style.configure("Treeview.Heading", font=custom_font)  # カラム見出しのフォントを設定
        style.configure("Treeview", font=custom_font, rowheight=custom_row_height)  # Treeview アイテムのフォントと行の高さを設定

        label = tk.Label(self.frame, text="加工結果", font=("AR丸ゴシック体M", 36))

        tree = ttk.Treeview(self.frame, columns=("ID", "Model", "Processing Time", "Shape", "Dimension", "Created By", "Timestamp"), show="headings", height=18, style="Treeview")
        tree.heading("ID", text="ID", anchor=tk.CENTER)
        tree.heading("Model", text="Model", anchor=tk.CENTER)
        tree.heading("Processing Time", text="Processing Time", anchor=tk.CENTER)
        tree.heading("Shape", text="Shape", anchor=tk.CENTER)
        tree.heading("Dimension", text="Dimension", anchor=tk.CENTER)
        tree.heading("Created By", text="Created By", anchor=tk.CENTER)
        tree.heading("Timestamp", text="Timestamp", anchor=tk.CENTER)

        tree.column("#0", stretch=tk.NO, minwidth=0, width=0)  # デフォルトの最初の列を非表示

        # 各列の幅を設定
        tree.column("ID", width=50)  # 例: 幅 50 ピクセル
        tree.column("Model", width=200)  # 例: 幅 100 ピクセル
        tree.column("Processing Time", width=250)  # 例: 幅 150 ピクセル
        tree.column("Shape", width=150)  # 例: 幅 80 ピクセル
        tree.column("Dimension", width=100)  # 例: 幅 100 ピクセル
        tree.column("Created By", width=300)  # 例: 幅 120 ピクセル
        tree.column("Timestamp", width=360)  # 例: 幅 150 ピクセル

        for item in selected_items:
            tree.insert("", "end", values=(item.model_id, item.model_number, str(item.average_processing_time), 
                            item.work_shape, item.workpiece_dimension, item.created_by, item.creation_timestamp))

        scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=tree.yview)
        tree.config(yscrollcommand=scrollbar.set)

        kakunin_button = tk.Button(self.frame, text="確認", command=self.back_to_selection_frame, font=("AR丸ゴシック体M", 24), width=22)

        self.frame.pack(fill="both", expand=True)
        label.place(relx=0.5, rely=0.02, anchor="n")  # ラベルを画面上部に配置
        tree.place(relx=0.5, rely=0.1, anchor="n")  # Treeview を画面中央に配置

        # スクロールバーを右側に合わせて配置
        scrollbar.place(relx=0.877, rely=0.1, relheight=0.71, anchor="ne")  # relheight の値を適切な値に変更

        kakunin_button.place(rely=0.85, relx=0.75)

    def back_to_selection_frame(self):
        # Implement the logic to go back to the selection frame
        # For example, you can destroy the current frame and recreate the selection frame
        pass

if __name__ == "__main__":
    app = WorkResultOverview()
