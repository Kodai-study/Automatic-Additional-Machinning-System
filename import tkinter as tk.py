import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
import tkinter.font as f

class NumberPad(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Number Pad")
        self.geometry("200x300")

        self.result = tk.StringVar()
        self.result.set("0")

        entry = tk.Entry(self, textvariable=self.result, font=("Helvetica", 24), justify="right")
        entry.pack(fill="both", expand=True)

        number_frame = tk.Frame(self)
        number_frame.pack(fill="both", expand=True, padx=0, pady=0)  # パディングを0に設定

        buttons = [
            "7", "8", "9",
            "4", "5", "6",
            "1", "2", "3",
            "0", "C", "OK"
        ]

        row, col = 0, 0
        for button_text in buttons:
            button = tk.Button(number_frame, text=button_text, font=("Helvetica", 18), command=lambda b=button_text: self.on_button_click(b))
            button.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
            col += 1
            if col > 2:
                col = 0
                row += 1

    def on_button_click(self, button_text):
        current_value = self.result.get()

        if button_text.isdigit():
            if current_value == "0":
                self.result.set(button_text)
            else:
                self.result.set(current_value + button_text)
        elif button_text == "C":
            self.result.set("0")
        elif button_text == "OK":
            self.destroy()

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("ファイル選択とデータ入力")
        self.root.geometry("1920x1080+0+0")  # ウィンドウサイズと位置を設定

        self.selection_frame = None  # フレームを初期化
        self.data_list = []

        # フォントサイズを変更

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("AR丸ゴシック体M", 24))
        style.configure("Treeview", font=("AR丸ゴシック体M", 18), rowheight=40)
        
        # ログイン画面を表示lf_login_frame
        self.create_login_frame()

    def clear_frame(self):
        if self.selection_frame:
            self.selection_frame.destroy()

    def create_login_frame(self):
        # ログイン画面を作成
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(fill="both", expand=True)

        username_label = tk.Label(self.login_frame, text="ID:", font=("AR丸ゴシック体M", 24))
        username_label.pack()
        username_label.place(x=830, y=400)

        username_entry = tk.Entry(self.login_frame, font=("AR丸ゴシック体M", 24))
        username_entry.pack()
        username_entry.place(x=880, y=400)

        password_label = tk.Label(self.login_frame, text="pass:", font=("AR丸ゴシック体M", 24))
        password_label.pack()
        password_label.place(x=797, y=450)

        password_entry = tk.Entry(self.login_frame, show="*", font=("AR丸ゴシック体M", 24))
        password_entry.pack()
        password_entry.place(x=880, y=450)

        def perform_login():
            # ログインの処理を実行（ここではダミーのログイン処理を行います）
            username = username_entry.get()
            password = password_entry.get()
            if username == "aaa" and password == "aaa":
                print("ログイン成功")
                self.login_frame.destroy()     
                # ログイン画面を破棄
                self.create_selection_frame()  # データ選択画面を表示
            else:
                print("ログイン失敗")

        login_button = tk.Button(self.login_frame, text="Login", command=perform_login, font=("AR丸ゴシック体M", 21))
        login_button.pack()
        login_button.place(x=1270, y=550)

    def create_selection_frame(self):

        # データ選択画面を作成
        self.selection_frame = tk.Frame(self.root,pady=5, padx=5, bd=2)  # フレームを設定

        # データを表示する表（Treeview）
        self.table = ttk.Treeview(self.selection_frame, columns=("Data", "Quantity"), show="headings")

        #列の見出し設定
        self.table.heading("#0", text=" ")
        self.table.heading("Data", text="加工データ",anchor='center')
        self.table.heading("Quantity", text="個数",anchor='center')
        self.table.heading("#0", text=" ",anchor='center')
        
        # スクロールバーの追加
        scrollbar = ttk.Scrollbar(self.selection_frame, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)

        # ボタン
        go_monitor_button = tk.Button(self.selection_frame, text="モニタ画面", command=self.create_check_frame, font=("AR丸ゴシック体M", 18),width = 22)
        go_check_button = tk.Button(self.selection_frame, text="確認画面", command=self.create_monitor_frame, font=("AR丸ゴシック体M", 18),width = 22)
        add_data_button = tk.Button(self.selection_frame, text="ファイル参照", command=self.add_data_from_file, font=("AR丸ゴシック体M", 18),width = 22)        

        #ウィジェットの配置
        self.selection_frame.pack(fill="both", expand=True)
        self.table.place(relheigh=0.6, relwidth=0.7,x=130)
        scrollbar.place(relheigh=0.6,x=1464)    
        add_data_button.place(rely=0.2, x=1500)
        go_monitor_button.place(rely=0.85,relx=0.1)
        go_check_button.place(rely=0.85,relx=0.75)

        self.selection_frame.pack()  # フレームを表示

    def add_data_from_file(self):
        # ファイルを参照してデータを追加
        file_path = filedialog.askopenfilename(title="ファイルを選択してください", filetypes=(("テキストファイル", "*.txt"), ("すべてのファイル", "*.*")))
        if file_path:
            file_name = file_path.split("/")[-1]  # ファイル名を取得

            # NumberPadを表示して個数を入力
            number_pad = NumberPad(self.root)
            self.root.wait_window(number_pad)
            quantity = int(number_pad.result.get())

            self.data_list.append((file_name, quantity))

            # 表をクリア
            table = self.selection_frame.children["!treeview"]
            table.delete(*table.get_children())

            # データを再描画
            for data, quantity in self.data_list:
                table.insert("", "end", values=(data, quantity))
    
    def create_check_frame(self):

        self.selection_frame.destroy()  

        self.check_frame = tk.Frame(self.root,pady=5, padx=5, bd=2,bg="blue")  # フレームを設定
        self.check_frame.pack(fill="both", expand=True, padx=0, pady=0)
    
    def create_monitor_frame(self):

        self.selection_frame.destroy()  

        self.check_frame = tk.Frame(self.root,pady=5, padx=5, bd=2,bg="red")  # フレームを設定
        self.check_frame.pack(fill="both", expand=True, padx=0, pady=0)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()