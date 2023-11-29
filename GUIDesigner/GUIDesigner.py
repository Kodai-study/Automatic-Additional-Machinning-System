# coding: utf-8
import time
import tkinter as tk
from tkinter import ttk
from typing import Dict
from GUIDesigner.screens.CheckSelection import CheckSelection
from GUIDesigner.screens.CreateSelection import CreateSelection
from GUIDesigner.screens.Login import Login
from GUIDesigner.screens.ScreenBase import ScreenBase
from GUIDesigner.screens.WaitConnecting import WaitConnecting
from RobotCommunicationHandler.RobotInteractionType import RobotInteractionType
from queue import Queue


# 　カスタムモジュールから必要なクラスをインポート
from .screens.ProcessingProgress import ProcessingProgress
from .screens.WorkResultOverview import WorkResultOverview
from .Frames import Frames


class GUIDesigner(tk.Tk):
    """
    GUIのデザインを行うクラス
    GUIの画面を作成し、ユーザからの入力を受け付けて、それをキューに入れて統合ソフトに送ったり、
    統合ソフトから受け取ったデータをGUIに表示したりする
    """

    def __init__(self):
        super().__init__()
        self.title("T5GUI")
        self.geometry("1920x1080+0+0")

        # ttkスタイルの設定
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("AR丸ゴシック体M", 24))
        style.configure("Treeview", font=("AR丸ゴシック体M", 18), rowheight=40)

        self.image_resources: Dict[str, tk.PhotoImage] = {}
        self.previous_screen = None
        self.screens: Dict[Frames, ScreenBase] = {}
        self.current_screen = Frames.WAIT_CONNECTION
        self.data_list = []
        self.robot_status = {}
        self._initial_variables()

    def _initial_variables(self):
        self.image_resources["red_lamp"] = tk.PhotoImage(
            file="./resource/images/red_lamp.png")
        # 画像ファイルの読み込み
        self.image_resources["green_lamp"] = tk.PhotoImage(
            file="./resource/images/green_lamp.png")

        self.robot_status = {
            "is_connection": True,
            "limit_switch": False,
            "lighting": {
                "back_light": False, "bar_light": False, "ring_light": False
            },
            "sensor": {
                1: False, 2: True, 3: True, 4: False, 5: False, 6: False
            },
            "reed_switch": {
                1: {"forward": True, "backward": False}, 2: {"forward": False, "backward": False},
                3: {"forward": False, "backward": False}, 4: {"forward": False, "backward": False}, 5: {"forward": False, "backward": False}
            },
            # "door_status": {
            #     1: False, 2: False, 3: False, 4: False
            # },
            "door_lock": {
                1: True, 2: True, 3: True, 4: True
            },
            "ejector": {
                "attach": True, "detach": False
            }
        }

    def _initial_screens(self):
        self.screens[Frames.WAIT_CONNECTION] = WaitConnecting(
            self, self.get_request_queue)
        self.screens[Frames.LOGIN] = Login(self, self.send_message_queue)
        self.screens[Frames.CREATE_SELECTION] = CreateSelection(
            self, self.data_list)
        self.screens[Frames.CHECK_SELECTION] = CheckSelection(
            self, self.data_list, self.image_resources)

        # screensのvalue全てで.grid(0,0)を実行
        for screen in self.screens.values():
            screen.grid(row=0, column=0, sticky="nsew")

    def _check_queue(self):
        if not self.get_request_queue.empty():
            request_type, request_data = self.get_request_queue.get()
            self.screens[self.current_screen].handle_queued_request(
                request_type, request_data)

        self.after(10, self._check_queue)

    def change_frame(self, frame: Frames):
        self.current_screen = frame
        self.screens[frame].create_frame()

    def start_gui(self, get_request_queue: Queue, send_message_queue: Queue):
        """
        GUIを起動し、ループを開始する。

        Args:
            get_request_queue (Queue): 統合ソフトから受け取ったデータを入れるキュー\n
            send_message_queue (Queue): 統合ソフトに送るデータを入れるキュー
        """

        self.get_request_queue = get_request_queue
        self.send_message_queue = send_message_queue

        self._initial_screens()
        # 画面作成のクラスのインスタンス化のテスト
        self.screens[self.current_screen].create_frame()
        self._check_queue()
        self.mainloop()

    def update_button_state_with_queue(self):
        state = "READY_START"
        while True:
            if self.get_request_queue.empty():
                time.sleep(0.1)
                continue
            data = self.get_request_queue.get()
            if data[0] != RobotInteractionType.MESSAGE_RECEIVED:
                continue
            if data[1] == "READY":
                self.create_progress_frame()

    def create_monitor_frame(self):
        if self.monitor_frame:
            self.monitor_frame.destroy()
        if self.check_frame:
            self.check_frame.destroy()
        if self.selection_frame:
            self.selection_frame.destroy()

        def toggle_button(on_button, off_button):
            if on_button["state"] == "normal" or on_button["state"] == "active":
                on_button["state"] = "disabled"
                off_button["state"] = "normal"
            else:
                on_button["state"] = "normal"
                off_button["state"] = "disabled"

        def toggle_forward_button(forward_button, reverse_button):
            toggle_button(forward_button, reverse_button)

        def toggle_reverse_button(forward_button, reverse_button):
            toggle_button(reverse_button, forward_button)

        self.monitor_frame = tk.Frame(self.root)

        backlight_label = tk.Label(
            self.monitor_frame, text="バックライト照明", font=("AR丸ゴシック体M", 18))
        barlight_label = tk.Label(
            self.monitor_frame, text="バー照明", font=("AR丸ゴシック体M", 18))
        ringlight_label = tk.Label(
            self.monitor_frame, text="リング照明", font=("AR丸ゴシック体M", 18))
        UR_label = tk.Label(self.monitor_frame, text="UR吸着",
                            font=("AR丸ゴシック体M", 18))
        doorlock1_label = tk.Label(
            self.monitor_frame, text="ドアロック1", font=("AR丸ゴシック体M", 18))
        doorlock2_label = tk.Label(
            self.monitor_frame, text="ドアロック2", font=("AR丸ゴシック体M", 18))
        doorlock3_label = tk.Label(
            self.monitor_frame, text="ドアロック3", font=("AR丸ゴシック体M", 18))
        doorlock4_label = tk.Label(
            self.monitor_frame, text="ドアロック4", font=("AR丸ゴシック体M", 18))

        servomotor_label = tk.Label(
            self.monitor_frame, text="サーボモータ", font=("AR丸ゴシック体M", 18))
        beltconveyor_label = tk.Label(
            self.monitor_frame, text="ベルトコンベア", font=("AR丸ゴシック体M", 18))
        processing_cylinder_label = tk.Label(
            self.monitor_frame, text="加工部位置決めシリンダ", font=("AR丸ゴシック体M", 18))
        inspection_cylinder_label = tk.Label(
            self.monitor_frame, text="検査部位置決めシリンダ", font=("AR丸ゴシック体M", 18))
        toolchanger_cylinder_label = tk.Label(
            self.monitor_frame, text="ツールチェンジャーシリンダ", font=("AR丸ゴシック体M", 18))
        inspectionwall_cylinder_label = tk.Label(
            self.monitor_frame, text="検査部壁シリンダ", font=("AR丸ゴシック体M", 18))
        processing_table_cylinder_label = tk.Label(
            self.monitor_frame, text="加工部テーブルシリンダ", font=("AR丸ゴシック体M", 18))

        kara_label1 = tk.Label(
            self.monitor_frame, text="", font=("AR丸ゴシック体M", 18))
        kara_label2 = tk.Label(
            self.monitor_frame, text="", font=("AR丸ゴシック体M", 18))

        back_button = tk.Button(self.monitor_frame, text="戻る", command=self.back_to_selection_frame, font=(
            "AR丸ゴシック体M", 18), width=22)

        on_buttons = []  # ONボタン用のリスト
        off_buttons = []  # OFFボタン用のリスト
        forward_buttons = []  # 正転ボタン用のリスト
        reverse_buttons = []  # 後転ボタン用のリスト

        for i in range(8):
            # ONボタンとOFFボタンを作成
            on_button = tk.Button(
                self.monitor_frame, text="ON", state="normal", width=10, bg="orange")
            off_button = tk.Button(
                self.monitor_frame, text="OFF", state="disabled", width=10, bg="cyan")
            on_buttons.append(on_button)
            off_buttons.append(off_button)

        for i in range(8):
            forward_button = tk.Button(
                self.monitor_frame, text="正転", state="normal", width=10, bg="orange")
            reverse_button = tk.Button(
                self.monitor_frame, text="後転", state="disabled", width=10, bg="cyan")
            forward_buttons.append(forward_button)
            reverse_buttons.append(reverse_button)

        for i in range(8):
            on_buttons[i].config(command=lambda i=i: toggle_button(
                on_buttons[i], off_buttons[i]))
            off_buttons[i].config(command=lambda i=i: toggle_button(
                on_buttons[i], off_buttons[i]))
            forward_buttons[i].config(command=lambda i=i: toggle_forward_button(
                forward_buttons[i], reverse_buttons[i]))
            reverse_buttons[i].config(command=lambda i=i: toggle_reverse_button(
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

        self.monitor_frame.pack(fill="both", expand=True)

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

    def create_progress_frame(self, selected_items):

        if self.check_frame:
            self.check_frame.destroy()

        self.processing = ProcessingProgress(
            self.root, self.create_result_frame)
        self.processing.create_frame(selected_items=self.data_list)

        print("hi")

    def create_emergency_frame(self):
        ()

    def create_requirements_frame(self):
        ()

    def create_result_frame(self):

        self.processing.progress_frame.destroy()

        # if  processing.progress_frame:
        #         processing.progress_frame.destroy()

        resulting = WorkResultOverview()
        resulting.create_frame(selected_items=self.data_list)
