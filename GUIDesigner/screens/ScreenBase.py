import tkinter as tk
from abc import ABC, abstractmethod

from GUIDesigner.Frames import Frames
from GUIDesigner.GUISignalCategory import GUISignalCategory


class ScreenBase(tk.Frame, ABC):
    """GUIの画面を作成する際の基底クラス

    インスタンス化するときは、親ウィンドゥを引数に渡し、
    画面を表示させるときは、create_frame()を呼び出す。
    その画面を表示させている時に、統合ソフトからキューで要求を受け取った場合は、
    handle_queued_request()を呼び出す。
    """

    def __init__(self, parent, *args, **keywords):
        super().__init__(parent, *args, **keywords)
        self.change_frame = parent.change_frame

    @abstractmethod
    def create_frame(self):
        """画面を表示・再表示させるときに呼び出すメソッド。
        仮想メソッドなので、サブクラスでオーバーライドしてください
        """
        pass

    @abstractmethod
    def handle_queued_request(self, request_type: GUISignalCategory, request_data=None):
        """統合ソフトからキューで要求を受け取った場合に呼び出すメソッド。"""
        pass

    def handle_pause_and_emergency(self, request_type: GUISignalCategory, request_data=None):
        """一時停止と非常停止の通信を受け取ったときに、それを処理して非常停止または一時停止画面に遷移する。
        必要に応じて呼び出す"""
        if request_type == GUISignalCategory.CRITICAL_FAILURE:
            self.change_frame(Frames.EMERGENCY_STOP)
        elif request_type == GUISignalCategory.CANNOT_CONTINUE_PROCESSING:
            if request_data:
                self._handle_pause_request(request_data)

    def _handle_pause_request(self, request_data):
        if request_data == "stock_empty":
            self.change_frame(Frames.WORK_REQUEST_OVERVIEW)
        elif request_data == "tool_not_found":
            self.change_frame(Frames.TOOL_REQUEST_OVERVIEW)
