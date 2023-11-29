from queue import Queue
import tkinter as tk
from typing import Union
from GUIDesigner.Frames import Frames
from GUIDesigner.GUIRequestType import GUIRequestType
from GUIDesigner.GUISignalCategory import GUISignalCategory
from GUIDesigner.screens.ScreenBase import ScreenBase


class CheckSelection(ScreenBase):
    def __init__(self, parent: tk.Tk):
        super().__init__(parent)

    def handle_queued_request(self, request_type: Union[GUISignalCategory, GUIRequestType], request_data=None):
        self.handle_pause_and_emergency(request_type, request_data)

    def create_frame(self):
        self.tkraise()
