import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog


class NumberPad(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Number Pad")
        self.geometry("200x300")

        self.result = tk.StringVar()
        self.result.set("0")

        entry = tk.Entry(self, textvariable=self.result,
                         font=("Helvetica", 24), justify="right")
        entry.pack(fill="both", expand=True)

        number_frame = tk.Frame(self)
        number_frame.pack(fill="both", expand=True)

        buttons = [
            "7", "8", "9",
            "4", "5", "6",
            "1", "2", "3",
            "0", "C", "OK"
        ]

        row, col = 0, 0
        for button_text in buttons:
            button = tk.Button(number_frame, text=button_text, font=(
                "Helvetica", 18), command=lambda b=button_text: self.on_button_click(b))
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
        self.root.geometry("800x600")

        self.current_frame = None
        self.data_list = []

        self.create_selection_frame()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def add_data_from_file(self):
        file_path = filedialog.askopenfilename(
            title="ファイルを選択してください", filetypes=(("テキストファイル", "*.txt"), ("すべてのファイル", "*.*")))
        if file_path:
            file_name = file_path.split("/")[-1]  # ファイル名を取得

            # NumberPadを表示して個数を入力
            number_pad = NumberPad(self.root)
            self.root.wait_window(number_pad)
            quantity = int(number_pad.result.get())

            self.data_list.append((file_name, quantity))
            self.update_table()

    def create_selection_frame(self):
        self.clear_frame()
        self.current_frame = tk.Frame(self.root)

        # データを表示する表（Treeview）
        table = ttk.Treeview(self.current_frame, columns=(
            "Data", "Quantity"), show="headings", selectmode="extended")
        table.heading("Data", text="データ")
        table.heading("Quantity", text="個数")
        table.pack(padx=10, pady=10)

        # 選択したデータと個数を取得するボタン
        get_selected_button = tk.Button(
            self.current_frame, text="選択したデータと個数を取得", command=self.get_selected_data, font=("Helvetica", 18))
        get_selected_button.pack(padx=10, pady=10)

        # ファイルを参照してデータを追加するボタン
        add_data_button = tk.Button(self.current_frame, text="ファイルを参照してデータを追加",
                                    command=self.add_data_from_file, font=("Helvetica", 18))
        add_data_button.pack(padx=10, pady=10)

        self.current_frame.pack()

    def update_table(self):
        table = self.current_frame.children["!treeview"]
        table.delete(*table.get_children())
        for data, quantity in self.data_list:
            table.insert("", "end", values=(data, quantity))

    def get_selected_data(self):
        selected_items = []
        selected_rows = self.current_frame.children["!treeview"].selection()
        for row in selected_rows:
            data = self.current_frame.children["!treeview"].item(row)[
                "values"][0]
            quantity = self.current_frame.children["!treeview"].item(row)[
                "values"][1]
            selected_items.append((data, quantity))
        print(selected_items)


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
