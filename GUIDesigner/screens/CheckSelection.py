from queue import Queue
import tkinter as tk
from typing import Union
from GUIDesigner.Frames import Frames
from GUIDesigner.GUIRequestType import GUIRequestType
from GUIDesigner.GUISignalCategory import GUISignalCategory
from GUIDesigner.screens.ScreenBase import ScreenBase


class CheckSelection(ScreenBase):
    def __init__(self, parent: tk.Tk, selected_items: list, image_resource: dict, send_to_integration_queue: Queue):
        super().__init__(parent)
        self.selected_items = selected_items
        self.image_resource = image_resource
        self.ready_lamp_img = self.image_resource["green_lamp"]
        self.preparation_lamp_img = self.image_resource["red_lamp"]
        self.send_to_integration_queue = send_to_integration_queue
        self._create_widgets()

    def handle_queued_request(self, request_type: Union[GUISignalCategory, GUIRequestType], request_data=None):
        self.handle_pause_and_emergency(request_type, request_data)

    def create_frame(self):
        self.listbox.delete(0, tk.END)
        for item in self.selected_items:
            self.listbox.insert(tk.END, f"{item['process_data'].model_number} - 個数: {item['regist_process_count']}")
        self.tkraise()

    def _create_widgets(self):
        self.label = tk.Label(self, text="選択した加工データ",
                              font=("AR丸ゴシック体M", 24))
        self.decoy_label = tk.Label(
            self, text=" "*50, font=("AR丸ゴシック体M", 24))
        self.label_lamp = tk.Label(self, image=self.preparation_lamp_img)

        self.listbox = tk.Listbox(self, font=(
            "AR丸ゴシック体M", 18), selectmode=tk.MULTIPLE, width=80, height=25, justify="center")

        self.scrollbar = tk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        def toggle_ready_state():
            if self.ready_button["text"] == "準備完了":
                self.ready_button["text"] = "準備取り消し"
                # ここでlabel_lampの画像を更新
                self.label_lamp.config(image=self.ready_lamp_img)
                self.send_to_integration_queue.put(
                    (GUIRequestType.UPLOAD_PROCESSING_DETAILS, True))
            else:
                self.ready_button["text"] = "準備完了"
                # ここでlabel_lampの画像を更新
                self.label_lamp.config(image=self.preparation_lamp_img)
                self.send_to_integration_queue.put(
                    (GUIRequestType.UPLOAD_PROCESSING_DETAILS, False))

        self.ready_button = tk.Button(self, text="準備完了",
                                      command=toggle_ready_state, font=("AR丸ゴシック体M", 22), width=24)

        back_button = tk.Button(self, text="戻る", command=self.back_to_selection_frame, font=(
            "AR丸ゴシック体M", 18), width=22)
        back_button.place(rely=0.85, relx=0.75)
        go_monitor_button = tk.Button(
            self, text="モニタ画面", command=lambda: self.change_frame(Frames.MONITORING), font=("AR丸ゴシック体M", 18), width=22)
        go_check_button = tk.Button(self, text="進捗画面", command=lambda: self.change_frame(
            Frames.PROCESSING_PROGRESS), font=("AR丸ゴシック体M", 18), width=22)
        
        go_monitor_button.place(rely=0.85, relx=0.1)
        # go_check_button.place(rely=0.65, relx=0.1)

        self.decoy_label.grid(row=0, column=0)
        self.label.grid(row=0, column=1, pady=40)
        self.listbox.grid(row=1, column=1)
        self.scrollbar.grid(row=1, column=2, sticky=(tk.N, tk.S))
        self.label_lamp.place(rely=0.80, relx=0.6)
        self.ready_button.place(rely=0.80, relx=0.37)

    def back_to_selection_frame(self):
        self.change_frame(Frames.CREATE_SELECTION)
