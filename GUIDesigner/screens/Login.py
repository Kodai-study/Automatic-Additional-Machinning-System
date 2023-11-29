import tkinter as tk
from GUIDesigner.screens.ScreenBase import ScreenBase


class Login(ScreenBase):
    def __init__(self, parent):
        super().__init__(parent)
        # self.pack(fill="both", expand=True)

        self.username_label = tk.Label(
            self, text="ID:", font=("AR丸ゴシック体M", 24))
        self.username_label.place(relx=0.5, rely=0.5, anchor="center")
        # 位置を中央上部に割合で指定


        self.username_entry = tk.Entry(
            self, font=("AR丸ゴシック体M", 24))
        self.username_entry.pack()
        self.username_entry.place(relx=0.5, rely=0.5, anchor="center")

        self.password_label = tk.Label(
            self, text="pass:", font=("AR丸ゴシック体M", 24))
        self.password_label.pack()
        self.password_label.place(relx=0.5, rely=0.5, anchor="center")

        self.password_entry = tk.Entry(
            self, show="*", font=("AR丸ゴシック体M", 24))
        self.password_entry.pack()
        self.password_entry.place(relx=0.5, rely=0.5, anchor="center")

        self.error_label = tk.Label(self, text="IDかパスワードが間違っています",
                                    font=("AR丸ゴシック体M", 24), fg="red")

        login_button = tk.Button(
            self, text="Login", command=self._perform_login, font=("AR丸ゴシック体M", 21))
        login_button.pack()
        login_button.place(x=1270, y=550)

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
