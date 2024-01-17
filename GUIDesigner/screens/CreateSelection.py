from queue import Queue
from tkinter import filedialog, ttk
from tkinter.font import Font
from GUIDesigner.Frames import Frames
from GUIDesigner.GUIRequestType import GUIRequestType
from GUIDesigner.GUISignalCategory import GUISignalCategory
from GUIDesigner.NumberPad import NumberPad
from GUIDesigner.screens.ScreenBase import ScreenBase
import tkinter as tk


class CreateSelection(ScreenBase):
    def __init__(self, parent, send_to_integration_queue: Queue):
        super().__init__(parent)
        self.number_pad = None
        self.data_list = []
        self._create_widgets()
        self.send_to_integration_queue = send_to_integration_queue

    def create_frame(self):
        self.send_to_integration_queue.put(
            (GUIRequestType.REQUEST_PROCESSING_DATA_LIST, ))
        self.data_list = []
        self.tkraise()

    def handle_queued_request(self, request_type: GUISignalCategory, request_data=None):
        self.handle_pause_and_emergency(request_type, request_data)
        if request_type == GUIRequestType.REQUEST_PROCESSING_DATA_LIST:
            if not request_data:
                self.after(500, lambda: self.send_to_integration_queue.put(
                    (GUIRequestType.REQUEST_PROCESSING_DATA_LIST, )))
                return

            self.data_list = request_data
            combobox_options = [d["process_data"].model_number
                                for d in self.data_list if 'process_data' in d]
            self.model_select_combobox["values"] = combobox_options

    def _create_widgets(self):
        self.table = ttk.Treeview(self, columns=(
            "Data", "Quantity"), show="headings")
        self.table.column("#0", width=0, stretch=tk.NO)
        self.table.heading("#0", text="")
        self.table.heading("Data", text="加工データ", anchor='center')
        self.table.heading("Quantity", text="個数", anchor='center')
        self.table.heading("#0", text=" ", anchor='center')

        self.table.column('Data', anchor='center')
        self.table.column('Quantity', anchor='center')

        scrollbar = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)

        go_monitor_button = tk.Button(self, text="モニタ画面",
                                      command=lambda: self.change_frame(Frames.MONITORING), font=("AR丸ゴシック体M", 18), width=22)
        add_data_button = tk.Button(self, text="加工データ追加",
                                    command=self._add_data_from_file, font=("AR丸ゴシック体M", 18), width=22)
        remove_button = tk.Button(self, text="削除", command=self._remove_selected_items,
                                  font=("AR丸ゴシック体M", 18), width=22)

        go_check_button = tk.Button(self, text="確認画面", command=lambda: self.change_frame(
            Frames.CHECK_SELECTION), font=("AR丸ゴシック体M", 18), width=22)
        go_check_button.place(rely=0.85, relx=0.1)

        self.table.place(relheight=0.6, relwidth=0.7, x=130, y=70)
        scrollbar.place(relheight=0.6, x=1464, y=70)
        add_data_button.place(rely=0.8, relx=0.8)
        remove_button.place(rely=0.9, relx=0.8)
        go_monitor_button.place(rely=0.75, relx=0.1)

        conbobox_font = Font(family="Helvetica", size=30)
        # Add dropdown box
        self.model_select_combobox = ttk.Combobox(
            self, font=conbobox_font, state="readonly")
        self.model_select_combobox.place(relx=0.8, rely=0.9, anchor="center")
        self.model_select_combobox.config(width=15)

    def _add_data_from_file(self):
        target_index = self.model_select_combobox.current()
        target_process_data = self.data_list[target_index]
        self.number_pad = NumberPad(self)
        self.number_pad.attributes("-topmost", True)
        self.wait_window(self.number_pad)
        quantity = self.number_pad.input_number
        if quantity is None or quantity == 0:
            return
        del self.number_pad
        if target_process_data["regist_process_count"] != 0:
            self.table.delete(target_process_data["process_data"].model_id)
        target_process_data["regist_process_count"] = quantity
        self.table.insert("", "end", iid=target_process_data["process_data"].model_id, values=(
            target_process_data["process_data"].model_number, quantity))

    # 選択されたアイテムを削除する新しい関数

    def _remove_selected_items(self):
        selected_items = self.table.selection()
        for item in selected_items:
            for search_data in self.data_list:
                if search_data["process_data"].model_id == int(item):
                    search_data["regist_process_count"] = 0
                    break

        self._update_selection_table()

    # 削除後に選択テーブルを更新する新しい関数
    def _update_selection_table(self):
        self.table.delete(*self.table.get_children())
        for process_data in self.data_list:
            if process_data["regist_process_count"]:
                self.table.insert("", "end",  iid=process_data["process_data"].model_id, values=(
                    process_data["process_data"].model_number, process_data["regist_process_count"]))
