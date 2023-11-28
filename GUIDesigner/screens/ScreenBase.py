import tkinter as tk
from abc import ABC, abstractmethod


class ScreenBase(tk.Frame, ABC):
    def __init__(self, parent):
        tk.Frame.__init__(parent)
        self.change_frame = parent.change_frame

    @abstractmethod
    def create_frame(self):
        pass
