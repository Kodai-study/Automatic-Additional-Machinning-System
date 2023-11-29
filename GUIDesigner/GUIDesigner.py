# coding: utf-8
import tkinter as tk
from tkinter import ttk
from typing import Dict
from GUIDesigner.screens.CheckSelection import CheckSelection
from GUIDesigner.screens.CreateSelection import CreateSelection
from GUIDesigner.screens.Login import Login
from GUIDesigner.screens.Monitoring import Monitoring
from GUIDesigner.screens.ScreenBase import ScreenBase
from GUIDesigner.screens.WaitConnecting import WaitConnecting
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
        self.current_screen = Frames.MONITORING
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
        self.screens[Frames.PROCESSING_PROGRESS] = ProcessingProgress(
            self, self.image_resources, self.data_list, self.robot_status)
        self.screens[Frames.WORK_RESULT_OVERVIEW] = WorkResultOverview(
            self, self.data_list)
        self.screens[Frames.MONITORING] = Monitoring(
            self, self.robot_status)
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
