# coding: utf-8
from threading import Thread
import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from GUIDesigner.GUIRequestType import GUIRequestType

from RobotCommunicationHandler.RobotInteractionType import RobotInteractionType

# 　カスタムモジュールから必要なクラスをインポート
from .GUISignalCategory import GUISignalCategory
from .NumberPad import NumberPad
from queue import Queue


class GUIDesigner:
    """
    GUIのデザインを行うクラス
    GUIの画面を作成し、ユーザからの入力を受け付けて、それをキューに入れて統合ソフトに送ったり、
    統合ソフトから受け取ったデータをGUIに表示したりする
    """

    def __init__(self):
        # ルートウィンドウを作成
        self.root = tk.Tk()
        self.root.title("T5GUI")
        self.root.geometry("1920x1080+0+0")

        self.selection_frame = None
        self.check_frame = None
        self.data_list = []
        self.is_pochi_pressed = False

        # ttkスタイルの設定
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("AR丸ゴシック体M", 24))
        style.configure("Treeview", font=("AR丸ゴシック体M", 18), rowheight=40)

        # 画像ファイルの読み込み
        self.red_lamp_img = tk.PhotoImage(
            file="./resource/images/red_lamp.png")
        self.green_lamp_img = tk.PhotoImage(
            file="./resource/images/green_lamp.png")
        self.current_img = self.red_lamp_img

    def start_gui(self, send_queue: Queue, receive_queue: Queue):
        """
        GUIを起動し、ループを開始する。

        Args:
            send_queue (Queue): 統合ソフトに送るデータを入れるキュー\n
            receive_queue (Queue): 統合ソフトから受け取ったデータを入れるキュー
        """

        self.send_queue = send_queue
        self.receive_queue = receive_queue

        wait_connect_cfd_thread = Thread(
            target=self.create_connection_waiting_frame)
        wait_connect_cfd_thread.start()

        self.root.mainloop()

    # キューを受け取る関数
    def connection_is_successful(self):
        while True:
            if not self.send_queue.empty():
                received_data = self.send_queue.get()
                if received_data[0] == GUISignalCategory.ROBOT_CONNECTION_SUCCESS:
                    # self.create_login_frame()
                    return True

    def create_connection_waiting_frame(self):
        self.connection_waiting_frame = tk.Frame(self.root)
        self.connection_waiting_frame.pack(fill="both", expand=True)

        message_label = tk.Label(
            self.connection_waiting_frame, text="通信接続を待っています...", font=("AR丸ゴシック体M", 24))
        message_label.pack(pady=200)

        # 通信接続完了の確認を行う処理を追加
        def check_connection():
            if self.connection_is_successful():  # 通信接続が成功した場合
                self.connection_waiting_frame.destroy()  # 通信待ちフレームを破棄
                self.create_login_frame()  # ログイン画面を表示

            else:
                # 通信がまだ確立されていない場合、定期的に確認する
                self.root.after(1000, check_connection)

        # 通信確認をスタート
        check_connection()

    def create_login_frame(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(fill="both", expand=True)

        username_label = tk.Label(
            self.login_frame, text="ID:", font=("AR丸ゴシック体M", 24))
        username_label.pack()
        username_label.place(x=830, y=400)

        username_entry = tk.Entry(self.login_frame, font=("AR丸ゴシック体M", 24))
        username_entry.pack()
        username_entry.place(x=880, y=400)

        password_label = tk.Label(
            self.login_frame, text="pass:", font=("AR丸ゴシック体M", 24))
        password_label.pack()
        password_label.place(x=797, y=450)

        password_entry = tk.Entry(
            self.login_frame, show="*", font=("AR丸ゴシック体M", 24))
        password_entry.pack()
        password_entry.place(x=880, y=450)

        def perform_login():
            username = username_entry.get()
            password = password_entry.get()
            if username == "" and password == "":
                print("ログイン成功")
                self.login_frame.destroy()
                self.create_selection_frame()
            else:
                print("ログイン失敗")
                error_label.place(x=800, y=700)

        error_label = tk.Label(self.login_frame, text="IDかパスワードが間違っています",
                               font=("AR丸ゴシック体M", 24), fg="red")

        login_button = tk.Button(
            self.login_frame, text="Login", command=perform_login, font=("AR丸ゴシック体M", 21))
        login_button.pack()
        login_button.place(x=1270, y=550)

    def create_selection_frame(self, selected_items=None):
        if hasattr(self, 'check_frame') and self.check_frame:
            self.check_frame.destroy()

        self.selection_frame = tk.Frame(self.root)

        self.table = ttk.Treeview(self.selection_frame, columns=(
            "Data", "Quantity"), show="headings")

        self.table.heading("#0", text=" ")
        self.table.heading("Data", text="加工データ", anchor='center')
        self.table.heading("Quantity", text="個数", anchor='center')
        self.table.heading("#0", text=" ", anchor='center')

        self.table.column('Data', anchor='center')
        self.table.column('Quantity', anchor='center')

        scrollbar = ttk.Scrollbar(
            self.selection_frame, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)

        go_monitor_button = tk.Button(self.selection_frame, text="モニタ画面",
                                      command=self.create_monitor_frame, font=("AR丸ゴシック体M", 18), width=22)
        go_check_button = tk.Button(self.selection_frame, text="確認画面", command=lambda: self.create_check_frame(
            self.data_list), font=("AR丸ゴシック体M", 18), width=22)
        add_data_button = tk.Button(self.selection_frame, text="ファイル参照",
                                    command=self.add_data_from_file, font=("AR丸ゴシック体M", 18), width=22)

        if selected_items:
            for data, quantity in selected_items:
                self.table.insert("", "end", values=(data, quantity))

        self.selection_frame.pack(fill="both", expand=True)
        self.table.place(relheight=0.6, relwidth=0.7, x=130, y=70)
        scrollbar.place(relheight=0.6, x=1464, y=70)
        add_data_button.place(rely=0.2, x=1530, y=200)
        go_monitor_button.place(rely=0.85, relx=0.1)
        go_check_button.place(rely=0.85, relx=0.75)

    def add_data_from_file(self):
        file_path = filedialog.askopenfilename(
            title="ファイルを選択してください", filetypes=(("テキストファイル", "*.txt"), ("すべてのファイル", "*.*")))
        if file_path:
            file_name = file_path.split("/")[-1]

            number_pad = NumberPad(self.root)
            self.root.wait_window(number_pad)
            quantity = int(number_pad.result.get())

            self.data_list.append((file_name, quantity))

            table = self.selection_frame.children["!treeview"]
            table.delete(*table.get_children())

            for data, quantity in self.data_list:
                table.insert("", "end", values=(data, quantity))

    def create_check_frame(self, selected_items):
        if self.selection_frame:
            self.selection_frame.destroy()

        self.check_frame = tk.Frame(self.root)

        label = tk.Label(self.check_frame, text="選択した加工データ:",
                         font=("AR丸ゴシック体M", 24))
        decoy_label = tk.Label(
            self.check_frame, text="                                                 ", font=("AR丸ゴシック体M", 24))
        label_lamp = tk.Label(self.check_frame, image=self.current_img)

        listbox = tk.Listbox(self.check_frame, font=(
            "AR丸ゴシック体M", 18), selectmode=tk.MULTIPLE, width=80, height=25, justify="center")

        for item in selected_items:
            listbox.insert(tk.END, f"{item[0]} - 個数: {item[1]}")

        scrollbar = tk.Scrollbar(
            self.check_frame, orient=tk.VERTICAL, command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)

        def toggle_ready_state():
            if ready_button["text"] == "準備完了":
                ready_button["text"] = "準備取り消し"
                self.current_img = self.green_lamp_img
            else:
                ready_button["text"] = "準備完了"
                self.current_img = self.red_lamp_img
            label_lamp.config(image=self.current_img)

        back_button = tk.Button(self.check_frame, text="戻る", command=self.back_to_selection_frame, font=(
            "AR丸ゴシック体M", 18), width=22)
        go_monitor_button = tk.Button(
            self.check_frame, text="モニタ画面", command=self.create_monitor_frame, font=("AR丸ゴシック体M", 18), width=22)
        ready_button = tk.Button(self.check_frame, text="準備完了",
                                 command=toggle_ready_state, font=("AR丸ゴシック体M", 22), width=24)

        self.check_frame.pack(fill="both", expand=True)
        decoy_label.grid(row=0, column=0)
        label.grid(row=0, column=1, pady=40)
        listbox.grid(row=1, column=1)
        scrollbar.grid(row=1, column=2, sticky=(tk.N, tk.S))
        back_button.place(rely=0.85, relx=0.75)
        label_lamp.place(rely=0.80, relx=0.6)
        go_monitor_button.place(rely=0.85, relx=0.1)
        ready_button.place(rely=0.80, relx=0.37)

    def back_to_selection_frame(self):
        if hasattr(self, 'check_frame') and self.check_frame:
            self.check_frame.destroy()
        self.create_selection_frame(self.data_list)

    def update_button_state_with_queue(self):
        state = "READY_START"
        while True:
            if self.send_queue.empty():
                time.sleep(0.1)
                continue
            data = self.send_queue.get()
            if data[0] != RobotInteractionType.MESSAGE_RECEIVED:
                continue
            if data[1] == "SIG DET" or data[1] == "SIG 0,ATT_DRL_READY" or data[1] == "SIG 0,ATT_IMP_READY":
                if state == "READY_START" or state == "READY_DETACH":
                    state = "READY_ATTACH"
                    self.pochi_button["state"] = "disabled"
                    self.detach_button["state"] = "disabled"
                    self.attach_button["state"] = "normal"
                elif state == "READY_ATTACH":
                    state = "READY_DETACH"
                    self.detach_button["state"] = "normal"
                    self.pochi_button["state"] = "disabled"
                    self.attach_button["state"] = "disabled"
            elif data[1] == "FINISH":
                self.pochi_button["state"] = "normal"
                self.detach_button["state"] = "disabled"
                self.attach_button["state"] = "disabled"
                self.current_img = self.green_lamp_img
                self.label_lamp.config(image=self.current_img)
                state = "READY_START"

    def create_monitor_frame(self):
        if self.selection_frame:
            self.selection_frame.destroy()
        if self.check_frame:
            self.check_frame.destroy()

        def toggle_pochi_state(pochi_button, label_lamp):
            self.current_img = self.red_lamp_img
            label_lamp.config(image=self.current_img)
            # self.pochi_button["state"] = "disabled"
            self.receive_queue.put((
                GUIRequestType.ROBOT_OPERATION_REQUEST, "WRK 0,TAP_FIN\n"))

        def push_attach_button():
            self.receive_queue.put((
                GUIRequestType.ROBOT_OPERATION_REQUEST, "EJCT 0,ATTACH\n"))
            self.attach_button["state"] = "disabled"

        def push_detach_button():
            self.receive_queue.put((
                GUIRequestType.ROBOT_OPERATION_REQUEST, "EJCT 0,DETACH\n"))
            self.detach_button["state"] = "disabled"
        self.monitor_frame = tk.Frame(self.root)

        self.label_lamp = tk.Label(self.monitor_frame, image=self.current_img)
        self.pochi_button = tk.Button(self.monitor_frame, command=lambda: toggle_pochi_state(
            self.pochi_button, self.label_lamp), text="START", font=("AR丸ゴシック体M", 18), width=22)

        # デタッチボタンを作成
        self.detach_button = tk.Button(
            self.monitor_frame, text="デタッチ", width=30, font=("AR丸ゴシック体M", 22),  height=10, fg="white", bg="blue", state="disabled",
            command=push_detach_button)

        # アタッチボタンを作成
        self.attach_button = tk.Button(
            self.monitor_frame, text="アタッチ", width=30,  font=("AR丸ゴシック体M", 22), height=10, fg="white", bg="blue", state="disabled",
            command=push_attach_button)

        if self.is_pochi_pressed:
            self.current_img = self.green_lamp_img
            self.label_lamp.config(image=self.current_img)

        self.monitor_frame.pack(fill="both", expand=True)
        self.pochi_button.place(rely=0.50, relx=0.35)
        self.label_lamp.place(rely=0.48, relx=0.6)
        self.attach_button.place(rely=0.6, relx=0.5)
        self.detach_button.place(rely=0.8, relx=0.5)
        watching_queue_thread = Thread(
            target=self.update_button_state_with_queue)
        watching_queue_thread.start()
