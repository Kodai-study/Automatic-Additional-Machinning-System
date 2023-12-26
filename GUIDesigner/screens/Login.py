from queue import Queue
import tkinter as tk
from typing import Union
from GUIDesigner.Frames import Frames
from GUIDesigner.GUIRequestType import GUIRequestType
from GUIDesigner.GUISignalCategory import GUISignalCategory
from GUIDesigner.screens.ScreenBase import ScreenBase

FORM_FONT_SIZE = 30

class Login(ScreenBase):
    def __init__(self, parent: tk.Tk, send_to_integration_queue: Queue):
        super().__init__(parent)
        self.send_to_integration_queue = send_to_integration_queue
        # 位置を中央上部に割合で指定
        self._create_widgets(parent)
        self.grid(sticky="nsew")

        def _simulate_login_with_static_data():
            OK_ID = ""
            OK_PASSWORD = ""
            login_request = self.send_to_integration_queue.get()
            if not login_request[0] == GUIRequestType.LOGIN_REQUEST:
                print("ログイン要求が来ていません")
                return

            if login_request[1]["id"] == OK_ID and login_request[1]["password"] == OK_PASSWORD:
                parent.get_request_queue.put(  # 統合ソフトにログイン成功を通知
                    (GUIRequestType.LOGIN_REQUEST, {"is_success": True, "permission_type": "admin"}))

        self._simulate_login_with_static_data = _simulate_login_with_static_data

    def handle_queued_request(self, request_type: Union[GUISignalCategory, GUIRequestType], request_data=None):
        self.handle_pause_and_emergency(request_type, request_data)
        if not request_type == GUIRequestType.LOGIN_REQUEST:
            return
        if request_data["is_success"]:
            self._success_login(request_data)

    def _success_login(self, request_data):
        print(f"ログイン成功 : ユーザの権限は{request_data['permission_type']}です。")
        self.change_frame(Frames.CREATE_SELECTION)

    def create_frame(self):
        self.tkraise()

    def _create_widgets(self, parent: tk.Tk):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Configure the row heights
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # ID label
        self.username_label = tk.Label(
            self, text="ID:", font=("Arial", FORM_FONT_SIZE))
        self.username_label.place(x=814, y=400)

        # ID entry
        self.username_entry = tk.Entry(
            self, font=("Arial", FORM_FONT_SIZE))
        # Increased vertical padding
        self.username_entry.place(x=880, y=400)

        # Password label
        self.password_label = tk.Label(
            self, text="Pass:", font=("Arial", FORM_FONT_SIZE))
        self.password_label.place(x=767, y=450)

        # Password entry
        self.password_entry = tk.Entry(
            self, show="*", font=("Arial", FORM_FONT_SIZE))
        # Increased vertical padding
        self.password_entry.place(x=880, y=450)

        # Login button
        self.login_button = tk.Button(
            self, text="Login", font=("Arial", 24), command=self._perform_login, width=13)
        self.login_button.place(x=1270, y=600)

    def _perform_login(self):
        self.send_to_integration_queue.put(
            (GUIRequestType.LOGIN_REQUEST, {"id": self.username_entry.get(), "password": self.password_entry.get()}))

        # DEBUG 決められたID、パスワードを入力するとログイン成功する
        self._simulate_login_with_static_data()
