import tkinter as tk
from tkinter import simpledialog


class NumberPad(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("テンキーパッド")
        self.geometry("200x250")

        self.result = tk.StringVar()
        self.result.set("0")

        self.create_number_buttons()
        self.create_clear_button()
        self.create_ok_button()

    def create_number_buttons(self):
        buttons = [
            "7", "8", "9",
            "4", "5", "6",
            "1", "2", "3",
            "0"
        ]

        row_val = 1
        col_val = 0

        for button in buttons:
            tk.Button(self, text=button, width=5, height=2, command=lambda b=button: self.add_digit(
                b)).grid(row=row_val, column=col_val)
            col_val += 1
            if col_val > 2:
                col_val = 0
                row_val += 1

    def create_clear_button(self):
        tk.Button(self, text="C", width=5, height=2,
                  command=self.clear).grid(row=4, column=0)

    def create_ok_button(self):
        tk.Button(self, text="OK", width=5, height=2,
                  command=self.ok).grid(row=4, column=2)

    def add_digit(self, digit):
        current_value = self.result.get()
        if current_value == "0":
            self.result.set(digit)
        else:
            self.result.set(current_value + digit)

    def clear(self):
        self.result.set("0")

    def ok(self):
        self.destroy()


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("テンキーパッドを表示する例")
        self.root.geometry("400x300")

        self.quantity = 0  # 初期値

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="個数を入力してください:").pack(pady=10)

        self.quantity_label = tk.Label(self.root, text=str(self.quantity))
        self.quantity_label.pack()

        tk.Button(self.root, text="テンキーパッドを表示",
                  command=self.show_number_pad).pack()

    def show_number_pad(self):
        number_pad = NumberPad(self.root)
        self.root.wait_window(number_pad)

        entered_value = number_pad.result.get()
        try:
            self.quantity = int(entered_value)
        except ValueError:
            self.quantity = 0

        self.quantity_label.config(text=str(self.quantity))


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
