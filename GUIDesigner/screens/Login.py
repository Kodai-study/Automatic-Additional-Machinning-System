import tkinter as tk
from GUIDesigner.screens.ScreenBase import ScreenBase

FORM_FONT_SIZE = 50

class Login(ScreenBase):
    def __init__(self, parent: tk.Tk):
        super().__init__(parent)

        # 位置を中央上部に割合で指定
        self._create_widgets(parent)
        self.grid(sticky="nsew")

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
        self.username_label.grid(row=0, column=0, sticky="e")

        # ID entry
        self.username_entry = tk.Entry(
            self, font=("Arial", FORM_FONT_SIZE))
        # Increased vertical padding
        self.username_entry.grid(row=0, column=1, sticky="ew", ipady=10)

        # Password label
        self.password_label = tk.Label(
            self, text="Pass:", font=("Arial", FORM_FONT_SIZE))
        self.password_label.grid(row=1, column=0, sticky="e")

        # Password entry
        self.password_entry = tk.Entry(
            self, show="*", font=("Arial", FORM_FONT_SIZE))
        # Increased vertical padding
        self.password_entry.grid(row=1, column=1, sticky="ew", ipady=10)

        # Login button
        login_button = tk.Button(
            self, text="Login", font=("Arial", FORM_FONT_SIZE))
        login_button.grid(row=2, column=0, columnspan=3, sticky="ew", padx=200)

    def create_frame(self):
        self.tkraise()

    def _perform_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "" and password == "":
            print("ログイン成功")
            self.destroy()
            self.create_selection_frame()
        else:
            print("ログイン失敗")
            self.error_label.place(x=800, y=700)
