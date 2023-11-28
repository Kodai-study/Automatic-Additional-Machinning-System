from threading import Thread
import time
import tkinter as tk
from tkinter import ttk

class EmergencyStop:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1920x1080+0+0")
        self.create_emergency_frame()
        self.root.mainloop()

    def create_emergency_frame(self):
        self.emergency_frame = tk.Frame(self.root, bg="yellow")
        self.emergency_label = tk.Label(self.emergency_frame, text="非常停止", font=("AR丸ゴシック体M", 150), fg="red", bg="yellow")

        back_button = tk.Button(self.emergency_frame, text="戻る",font=("AR丸ゴシック体M", 18), width=22,bg="yellow")
        self.emergency_frame.pack(fill="both", expand=True)

        # ガジェット配置
        self.emergency_frame.pack(fill="both", expand=True)
        self.emergency_label.pack(pady=300)
        back_button.place(rely=0.85, relx=0.75)


if __name__ == "__main__":
    app = EmergencyStop()
