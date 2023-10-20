# BEGIN: 5z8j7d9f3x2a
import tkinter as tk
from enum import Enum
from dataclasses import dataclass
from common_data_type import *
from queue import Queue
from typing import Union, List, Tuple

from test_classes import TransmissionTarget





class GUIDesigner:
    """
    GUIのデザインを行うクラス
    GUIの画面を作成し、ユーザからの入力を受け付けて、それをキューに入れて統合ソフトに送ったり、
    統合ソフトから受け取ったデータをGUIに表示したりする
    """

    def __init__(self):
        pass

    def start_gui(self, send_queue: Queue, receive_queue: Queue):
        """
        GUIを起動し、ループを開始する。

        Args:
            send_queue (Queue): 統合ソフトに送るデータを入れるキュー\n
            receive_queue (Queue): 統合ソフトから受け取ったデータを入れるキュー
        """
        self.send_queue = send_queue
        self.receive_queue = receive_queue

        # Create the main window
        self.root = tk.Tk()
        self.root.title("My GUI")

        # Create a label
        self.label = tk.Label(self.root, text="Hello, world!")
        self.label.pack()

        # Create a button
        self.button = tk.Button(self.root, text="Click me!", command=self.button_click)
        self.button.pack()

        # Start the GUI loop
        self.root.mainloop()

    def button_click(self):
        """
        The function to be called when the button is clicked
        """
        # print("Button clicked!")
        self.send_queue.put({"target": TransmissionTarget.TEST_TARGET_1, "message": "button1 clicked"})
# END: 5z8j7d9f3x2a


if __name__ == "__main__":
    gui = GUIDesigner()
    gui.start_gui(None, None)