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
            self.dropdown["values"] = combobox_options

    def _create_widgets(self, selected_items=None):

        self.table = ttk.Treeview(self, columns=(
            "Data", "Quantity"), show="headings")
        self.table.heading("#0", text=" ")
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
        add_data_button = tk.Button(self, text="ファイル参照",
                                    command=self._add_data_from_file, font=("AR丸ゴシック体M", 18), width=22)
        remove_button = tk.Button(self, text="削除", command=self._remove_selected_items,
                                  font=("AR丸ゴシック体M", 18), width=22)

        go_check_button = tk.Button(self, text="確認画面", command=lambda: self.change_frame(
            Frames.CHECK_SELECTION), font=("AR丸ゴシック体M", 18), width=22)
        go_check_button.place(rely=0.85, relx=0.1)
        if selected_items:
            for data, quantity in selected_items:
                self.table.insert("", "end", values=(data, quantity))

        self.table.place(relheight=0.6, relwidth=0.7, x=130, y=70)
        scrollbar.place(relheight=0.6, x=1464, y=70)
        add_data_button.place(rely=0.2, x=1530, y=200)
        remove_button.place(rely=0.2, x=1530, y=400)
        go_monitor_button.place(rely=0.75, relx=0.1)
        large_font = Font(family="Helvetica", size=14)

        # Add dropdown box
        self.dropdown = ttk.Combobox(self, font=large_font, state="readonly")
        self.dropdown.place(relx=0.8, rely=0.9, anchor="center")
        self.dropdown.config(width=15)

    def _add_data_from_file(self):
        file_path = filedialog.askopenfilename(
            title="ファイルを選択してください", filetypes=(("すべてのファイル", "*.*"), ("テキストファイル", "*.txt")))
        if file_path:
            file_name = file_path.split("/")[-1]
            self.number_pad = NumberPad(self)
            self.number_pad.attributes("-topmost", True)
            self.wait_window(self.number_pad)
            quantity = int(self.number_pad.result.get())
            del self.number_pad
            self.data_list.append((file_name, quantity))
            self._update_selection_table()

    # 選択されたアイテムを削除する新しい関数
    def _remove_selected_items(self):
        selected_items = self.table.selection()

        for item in selected_items:
            item_values = self.table.item(item, 'values')
            if item_values:
                data, quantity = item_values[0], int(
                    item_values[1])  # 数量を整数に変換

                # data_list から削除する対象を見つけて削除
                for i, (existing_data, existing_quantity) in enumerate(self.data_list):
                    if (data, quantity) == (existing_data, existing_quantity):
                        print("Found in the list. Removing.")
                        del self.data_list[i]
                        break  # 見つかったらループを抜ける
                else:
                    print("Not found in the list.")

        self._update_selection_table()

    # 削除後に選択テーブルを更新する新しい関数
    def _update_selection_table(self):
        self.table.delete(*self.table.get_children())
        for process_data in self.data_list:
            self.table.insert("", "end", values=(
                process_data["data_file_path"], process_data["regist_process_count"]))
