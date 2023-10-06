import tkinter as tk
from tkinter import Scrollbar

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("ログイン画面")
        self.root.geometry("1980x1020")  # 画面サイズを固定

        self.current_frame = None
        self.create_login_frame()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def create_login_frame(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root)

        # ログイン画面の要素を中央配置
        decoi_id = tk.Label(self.current_frame, text=" ")
        decoi_password = tk.Label(self.current_frame, text=" ")
        label_id = tk.Label(self.current_frame, text="ID:",
                            font=("Helvetica", 24))
        label_password = tk.Label(
            self.current_frame, text="パスワード:", font=("Helvetica", 24))
        entry_id = tk.Entry(self.current_frame, font=(
            "Helvetica", 24), width=20)  # 幅を調整
        entry_password = tk.Entry(
            self.current_frame, show="*", font=("Helvetica", 24), width=20)  # 幅を調整
        login_button = tk.Button(self.current_frame, text="ログイン",
                                 command=self.create_selection_frame, font=("Helvetica", 24))

        decoi_id.grid(row=0, column=0, padx=10, pady=200, sticky="e")
        decoi_id.grid(row=0, column=1, padx=10, pady=200)
        label_id.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        entry_id.grid(row=1, column=1, padx=10, pady=10)
        label_password.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        entry_password.grid(row=2, column=1, padx=10, pady=10)

        # ログインボタンを右寄せに配置
        login_button.grid(row=3, column=1, padx=10, pady=20, sticky="e")

        self.current_frame.pack()

    def create_selection_frame(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root)

         

        confirm_button = tk.Button(self.current_frame, text="確認画面へ", command=self.create_confirmation_frame, font=("Helvetica", 24))
        confirm_button.grid(row=2, column=0, columnspan=2, padx=10, pady=20)

        self.current_frame.pack()
        
    def create_confirmation_frame(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root)

        # 確認画面の要素
        confirmation_label = tk.Label(
            self.current_frame, text="以下の情報で確認してください:", font=("Helvetica", 24))
        confirmation_label.pack()

        data_text = self.data_entry.get()
        quantity_text = self.quantity_entry.get()

        confirmation_info = f"加工データ: {data_text}\n個数: {quantity_text}"

        confirmation_text = tk.Text(
            self.current_frame, height=10, width=40, font=("Helvetica", 24))
        confirmation_text.insert(tk.END, confirmation_info)
        confirmation_text.pack()

        finish_button = tk.Button(
            self.current_frame, text="終了", command=self.root.quit, font=("Helvetica", 24))
        finish_button.pack()

        self.current_frame.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
