from queue import Queue
from typing import List
from GUIDesigner.Frames import Frames
from GUIDesigner.GUIRequestType import GUIRequestType
from GUIDesigner.GUISignalCategory import GUISignalCategory
from GUIDesigner.screens.ScreenBase import ScreenBase
import tkinter as tk


class Monitoring(ScreenBase):
    def __init__(self, parent, robot_status: dict,send_to_integration_queue: Queue):
        super().__init__(parent)
        self.robot_status = robot_status
        self.send_to_integration_queue = send_to_integration_queue
        self._create_widgets()

    def create_frame(self):
        self.tkraise()

    def handle_queued_request(self, request_type: GUISignalCategory, request_data=None):
        self.handle_pause_and_emergency(request_type, request_data)

    def push_button(self,command):
        self.send_to_integration_queue.put((GUIRequestType.ROBOT_OPERATION_REQUEST, command))

    def _create_widgets(self):
        def toggle_button(on_button, off_button):
            if on_button["state"] == "normal" or on_button["state"] == "active":
                on_button["state"] = "disabled"
                off_button["state"] = "normal"
            else:
                on_button["state"] = "normal"
                off_button["state"] = "disabled"

        backlight_label = tk.Label(
            self, text="バックライト照明", font=("AR丸ゴシック体M", 18))
        barlight_label = tk.Label(
            self, text="バー照明", font=("AR丸ゴシック体M", 18))
        ringlight_label = tk.Label(
            self, text="リング照明", font=("AR丸ゴシック体M", 18))
        UR_label = tk.Label(self, text="UR吸着",
                            font=("AR丸ゴシック体M", 18))
        doorlock1_label = tk.Label(
            self, text="ドアロック1", font=("AR丸ゴシック体M", 18))
        doorlock2_label = tk.Label(
            self, text="ドアロック2", font=("AR丸ゴシック体M", 18))
        doorlock3_label = tk.Label(
            self, text="ドアロック3", font=("AR丸ゴシック体M", 18))
        doorlock4_label = tk.Label(
            self, text="ドアロック4", font=("AR丸ゴシック体M", 18))

        servomotor_label = tk.Label(
            self, text="サーボモータ", font=("AR丸ゴシック体M", 18))
        beltconveyor_label = tk.Label(
            self, text="ベルトコンベア", font=("AR丸ゴシック体M", 18))
        processing_cylinder_label = tk.Label(
            self, text="加工部位置決めシリンダ", font=("AR丸ゴシック体M", 18))
        inspection_cylinder_label = tk.Label(
            self, text="検査部位置決めシリンダ", font=("AR丸ゴシック体M", 18))
        toolchanger_cylinder_label = tk.Label(
            self, text="ツールチェンジャーシリンダ", font=("AR丸ゴシック体M", 18))
        inspectionwall_cylinder_label = tk.Label(
            self, text="検査部壁シリンダ", font=("AR丸ゴシック体M", 18))
        processing_table_cylinder_label = tk.Label(
            self, text="加工部テーブルシリンダ", font=("AR丸ゴシック体M", 18))

        kara_label1 = tk.Label(
            self, text="", font=("AR丸ゴシック体M", 18))
        kara_label2 = tk.Label(
            self, text="", font=("AR丸ゴシック体M", 18))

        back_button = tk.Button(self, text="戻る", command=lambda: self.change_frame(Frames.CREATE_SELECTION), font=(
            "AR丸ゴシック体M", 18), width=22)

        on_buttons: List[tk.Button] = []  # ONボタン用のリスト
        off_buttons: List[tk.Button] = []  # OFFボタン用のリスト
        forward_buttons: List[tk.Button] = []  # 正転ボタン用のリスト
        reverse_buttons: List[tk.Button] = []  # 後転ボタン用のリスト

        button = tk.Button(self, text="OFF", width=10, bg="red",command=lambda: self.push_button("test"))
        button.grid(row=6,column=1)

        for i in range(8):
            # ONボタンとOFFボタンを作成
            on_button = tk.Button(
                self, text="ON", state="normal", width=10, bg="orange")
            off_button = tk.Button(
                self, text="OFF", state="disabled", width=10, bg="cyan")
            on_buttons.append(on_button)
            off_buttons.append(off_button)

        for i in range(8):
            forward_button = tk.Button(
                self, text="正転", state="normal", width=10, bg="orange")
            reverse_button = tk.Button(
                self, text="後転", state="disabled", width=10, bg="cyan")
            forward_buttons.append(forward_button)
            reverse_buttons.append(reverse_button)

        for i in range(8):
            on_buttons[i].config(command=lambda i=i: toggle_button(
                on_buttons[i], off_buttons[i]))
            off_buttons[i].config(command=lambda i=i: toggle_button(
                on_buttons[i], off_buttons[i]))
            forward_buttons[i].config(command=lambda i=i: self.push_button(
                forward_buttons[i], reverse_buttons[i]))
            reverse_buttons[i].config(command=lambda i=i: self.push_button(
                forward_buttons[i], reverse_buttons[i]))
        


        for i in range(8):
            on_buttons[i].grid(row=i + 1, column=2)
            off_buttons[i].grid(row=i + 1, column=3)

        for i in range(3):
            forward_buttons[i].grid(row=i + 9, column=2)
            reverse_buttons[i].grid(row=i + 9, column=3)

        for i in range(4):
            forward_buttons[i + 3].grid(row=i + 1, column=6)
            reverse_buttons[i + 3].grid(row=i + 1, column=7)

        kara_label1.grid(row=0, column=0, padx=40, pady=40)
        kara_label2.grid(row=0, column=4, padx=30, pady=40)
        backlight_label.grid(row=1, column=1, padx=30, pady=20)
        barlight_label.grid(row=2, column=1, padx=30, pady=20)
        ringlight_label.grid(row=3, column=1, padx=30, pady=20)
        UR_label.grid(row=4, column=1, padx=30, pady=20)
        doorlock1_label.grid(row=5, column=1, padx=30, pady=20)
        doorlock2_label.grid(row=6, column=1, padx=30, pady=20)
        doorlock3_label.grid(row=7, column=1, padx=30, pady=20)
        doorlock4_label.grid(row=8, column=1, padx=30, pady=20)

        servomotor_label.grid(row=9, column=1, padx=30, pady=20)
        beltconveyor_label.grid(row=10, column=1, padx=30, pady=20)
        processing_cylinder_label.grid(row=11, column=1, padx=30, pady=20)

        inspection_cylinder_label.grid(row=1, column=5, padx=30, pady=20)
        toolchanger_cylinder_label.grid(row=2, column=5, padx=30, pady=20)
        inspectionwall_cylinder_label.grid(row=3, column=5, padx=30, pady=20)
        processing_table_cylinder_label.grid(row=4, column=5, padx=30, pady=20)

        back_button.place(rely=0.85, relx=0.75)
