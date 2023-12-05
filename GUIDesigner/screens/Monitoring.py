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
                off_button["state"] = "disable"

        backlight_label = tk.Label(
            self, text="バックライト照明", font=("AR丸ゴシック体M", 18))
        barlight_label = tk.Label(
            self, text="バー照明", font=("AR丸ゴシック体M", 18))
        ringlight_label = tk.Label(
            self, text="リング照明", font=("AR丸ゴシック体M", 18))
        UR_label = tk.Label(
            self, text="UR吸着",font=("AR丸ゴシック体M", 18))
        dlc0_label = tk.Label(
            self, text="ドアロック1", font=("AR丸ゴシック体M", 18))
        dlc1_label = tk.Label(
            self, text="ドアロック2", font=("AR丸ゴシック体M", 18))
        dlc2_label = tk.Label(
            self, text="ドアロック3", font=("AR丸ゴシック体M", 18))
        dlc3_label = tk.Label(
            self, text="ドアロック4", font=("AR丸ゴシック体M", 18))

        svm_label = tk.Label(
            self, text="サーボモータ", font=("AR丸ゴシック体M", 18))
        conv_label = tk.Label(
            self, text="ベルトコンベア", font=("AR丸ゴシック体M", 18))
        cyl_000_label = tk.Label(
            self, text="加工部位置決めシリンダ", font=("AR丸ゴシック体M", 18))
        cyl_001_label = tk.Label(
            self, text="検査部位置決めシリンダ", font=("AR丸ゴシック体M", 18))
        cyl_002_label = tk.Label(
            self, text="ツールチェンジャーシリンダ", font=("AR丸ゴシック体M", 18))
        cyl_003_label = tk.Label(
            self, text="検査部壁シリンダ", font=("AR丸ゴシック体M", 18))
        cyl_004_label = tk.Label(
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
        stop_buttons: List[tk.Button] = []

        # ボタンのコマンドリストを作成します
        on_commands = ["backlight_on\n", "barlight_on\n", "ringlight_on\n", "EJCT 0,ATTACH\n",
                        "DLC 0,LOCK\n", "DLC 1,LOCK\n", "DLC 2,LOCK\n", "DLC 3,LOCK\n"]
        off_commands = ["backlight_off\n", "barlight_off\n", "ringlight_off\n", "EJCT 0,DETACH\n", 
                        "DLC 0,UNLOCK\n", "DLC 1,UNLOCK\n", "DLC 2,UNLOCK\n", "DLC 3,UNLOCK\n"]
        forward_commands = ["SVM 0,CW,1\n", "CONV 0,CW\n", "CYL 001,PUSH\n", "CYL 002,PUSH\n", "CYL 003,PUSH\n", "CYL 004,PUSH\n", "CYL 005,PUSH\n"]
        reverse_commands = ["SVM 0,BREAK,0\n", "CONV 0,OFF\n", "CYL 001,PULL\n", "CYL 002,PULL\n", "CYL 003,PULL\n", "CYL 004,PULL\n", "CYL 005,PULL\n"]
        stop_command = ["CONV 0,N\n", "CONV 0,N\n", "CONV 0,N\n"]

        # 各ボタンに対して異なるコマンドを設定します
        for i in range(8):
            on_button = tk.Button(self, text="ON", state="normal", width=10, bg="orange", 
                                  command=lambda i=i: (self.push_button(on_commands[i]), toggle_button(on_buttons[i], off_buttons[i])))
            off_button = tk.Button(self, text="OFF", state="disabled", width=10, bg="cyan", 
                                   command=lambda i=i: (self.push_button(off_commands[i]), toggle_button(on_buttons[i], off_buttons[i])))
            on_buttons.append(on_button)
            off_buttons.append(off_button)

        # 同様に、正転と後転のボタンにも異なるコマンドを設定します
        for i in range(8):
            forward_button = tk.Button(self, text="正転", state="normal", width=10, bg="orange", 
                                       command=lambda i=i: (self.push_button(forward_commands[i]), toggle_button(forward_buttons[i], reverse_buttons[i])))
            reverse_button = tk.Button(self, text="後転", state="disabled", width=10, bg="cyan", 
                                       command=lambda i=i: (self.push_button(reverse_commands[i]), toggle_button(forward_buttons[i], reverse_buttons[i])))
            forward_buttons.append(forward_button)
            reverse_buttons.append(reverse_button)

        for i in range(3):
            stop_button_state = {"on": "normal", "off": "disabled"}
            stop_button = tk.Button(self, text="停止", state="normal", width=10, bg="yellow",
                                    command=lambda: (self.push_button(stop_command[i])))
            stop_buttons.append(stop_button)

        for i in range(8):
            on_buttons[i].grid(row=i + 1, column=2)
            off_buttons[i].grid(row=i + 1, column=3)

        for i in range(3):
            forward_buttons[i].grid(row=i + 9, column=2)
            reverse_buttons[i].grid(row=i + 9, column=3)

        for i in range(4):
            forward_buttons[i + 3].grid(row=i + 1, column=6)
            reverse_buttons[i + 3].grid(row=i + 1, column=7)
        
        for i in range(3):
            stop_buttons[i].grid(row=i + 9, column=4)

        kara_label1.grid(row=0, column=0, padx=40, pady=40)
        kara_label2.grid(row=0, column=4, padx=30, pady=40)
        backlight_label.grid(row=1, column=1, padx=30, pady=20)
        barlight_label.grid(row=2, column=1, padx=30, pady=20)
        ringlight_label.grid(row=3, column=1, padx=30, pady=20)
        UR_label.grid(row=4, column=1, padx=30, pady=20)
        dlc0_label.grid(row=5, column=1, padx=30, pady=20)
        dlc1_label.grid(row=6, column=1, padx=30, pady=20)
        dlc2_label.grid(row=7, column=1, padx=30, pady=20)
        dlc3_label.grid(row=8, column=1, padx=30, pady=20)

        svm_label.grid(row=9, column=1, padx=30, pady=20)
        conv_label.grid(row=10, column=1, padx=30, pady=20)
        cyl_000_label.grid(row=11, column=1, padx=30, pady=20)
        cyl_001_label.grid(row=1, column=5, padx=30, pady=20)
        cyl_002_label.grid(row=2, column=5, padx=30, pady=20)
        cyl_003_label.grid(row=3, column=5, padx=30, pady=20)
        cyl_004_label.grid(row=4, column=5, padx=30, pady=20)

        back_button.place(rely=0.85, relx=0.75)
