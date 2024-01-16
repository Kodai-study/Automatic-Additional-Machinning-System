import tkinter as tk


class NumberPad(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Number Pad")
        self.geometry("200x300")

        self.result = tk.StringVar()
        self.result.set("0")
        self.input_number = None

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
                
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # 「×」ボタンの処理を追加

    def on_close(self):
        # 「×」ボタンが押されたときに呼ばれる
        self.result.set(None)
        self.input_number = None
        self.destroy()

    def on_button_click(self, button_text):
        current_value = self.result.get()
        if button_text == "OK":
            self.destroy()
            return
        
        if button_text.isdigit():
            if current_value == "0":
                self.result.set(button_text)
            else:
                self.result.set(current_value + button_text)
        elif button_text == "C":
            self.result.set("0")
        self.input_number = int(self.result.get())
