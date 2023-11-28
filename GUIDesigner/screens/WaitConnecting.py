from GUIDesigner.Frames import Frames
from GUIDesigner.screens.ScreenBase import ScreenBase


class WaitConnecting(ScreenBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_frame()
        self.change_frame(Frames.WAIT_CONNECTION)

    def create_frame(self):
        print("WaitConnecting")
