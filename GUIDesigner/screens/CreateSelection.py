from collections import defaultdict
import json
from queue import Queue
import textwrap
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
        self.tkraise()
        self.data_list = []
        self.send_to_integration_queue.put(
            (GUIRequestType.REQUEST_PROCESSING_DATA_LIST, ))

    def handle_queued_request(self, request_type: GUISignalCategory, request_data=None):
        self.handle_pause_and_emergency(request_type, request_data)
        if request_type == GUIRequestType.REQUEST_PROCESSING_DATA_LIST:
            if not request_data:
                self.after(500, lambda: self.send_to_integration_queue.put(
                    (GUIRequestType.REQUEST_PROCESSING_DATA_LIST, )))
                return
            self.update_option_menu(request_data)

    def update_option_menu(self, request_data):
        self.data_list = request_data
        self.combobox_options = [d["process_data"].model_number
                                 for d in self.data_list if 'process_data' in d]
        menu = self.model_select_combobox["menu"]
        menu.delete(0, 'end')  # 現在のメニュー項目をすべて削除
        for option in self.combobox_options:
            menu.add_command(
                label=option, command=lambda value=option: self.model_var.set(value))

    def _create_widgets(self):
        self.processed_data_treeview = self._create_registerd_table_list()
        self.process_detail_text_view = self._create_detail_view()
        self.model_select_combobox, self.model_var = self._create_data_select_combobox()

        go_monitor_button = tk.Button(self, text="モニタ画面",
                                      command=lambda: self.change_frame(Frames.MONITORING), font=("AR丸ゴシック体M", 18), width=22)
        add_data_button = tk.Button(self, text="加工データ追加",
                                    command=self._add_process_data, font=("AR丸ゴシック体M", 18), width=22)
        remove_button = tk.Button(self, text="削除", command=self._remove_selected_items,
                                  font=("AR丸ゴシック体M", 18), width=22)
        go_check_button = tk.Button(self, text="確認画面", command=lambda: (self._regist_processing_order(), self.change_frame(
            Frames.CHECK_SELECTION)), font=("AR丸ゴシック体M", 18), width=22)

        go_monitor_button.place(rely=0.75, relx=0.1)
        add_data_button.place(rely=0.8, relx=0.5)
        remove_button.place(rely=0.9, relx=0.5)
        go_check_button.place(rely=0.85, relx=0.1)  # テキストビューの配置

    def _create_data_select_combobox(self):
        COMBO_BOX_FONT = Font(family="Helvetica", size=30)
        style = ttk.Style()
        large_font = Font(family="Helvetica", size=30)
        text_view_x = 130 + (self.winfo_screenwidth() * 0.7)  # テーブルの幅の終わりの位置
        text_view_y = 70  # テーブルと同じy座標
        text_view_width = 1.0 - 0.8  # 残りの幅
        text_view_height = 0.6  # テーブルと同じ高さ
        selected_value = tk.StringVar(self)

        def view_process_data_detail(*args):
            print("value", selected_value.get())
            process_info = self._create_process_detail_str(self._search_data_with_name(
                selected_value.get()))
            self.process_detail_text_view.config(text=process_info)

        selected_value.trace("w", view_process_data_detail)
        model_select_optionmenu = tk.OptionMenu(
            self, selected_value, "hoge")
        model_select_optionmenu.config(font=COMBO_BOX_FONT)  # フォントサイズ設定
        # ドロップダウンメニューのフォントサイズも変更
        menu = model_select_optionmenu["menu"]
        menu.config(font=COMBO_BOX_FONT)
        model_select_optionmenu.place(
            relwidth=text_view_width, x=text_view_x, y=text_view_y)
        return model_select_optionmenu, selected_value

    def _create_registerd_table_list(self):
        processed_data_treeview = ttk.Treeview(self, columns=(
            "Data", "Quantity"), show="headings")
        processed_data_treeview.column("#0", width=0, stretch=tk.NO)
        processed_data_treeview.heading("#0", text="")
        processed_data_treeview.heading(
            "Data", text="加工データ", anchor='center')
        processed_data_treeview.heading(
            "Quantity", text="個数", anchor='center')
        processed_data_treeview.heading("#0", text=" ", anchor='center')

        processed_data_treeview.column('Data', anchor='center')
        processed_data_treeview.column('Quantity', anchor='center')

        scrollbar = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=processed_data_treeview.yview)
        scrollbar.place(relheight=0.6, x=1464, y=70)
        processed_data_treeview.configure(yscroll=scrollbar.set)
        processed_data_treeview.place(
            relheight=0.6, relwidth=0.5, x=130, y=70)
        return processed_data_treeview

    def _create_detail_view(self):
        text_view = tk.Label(self, font=(
            "AR丸ゴシック体M", 18), width=22, text="fda", anchor='nw', justify=tk.LEFT)
        text_view_x = 130 + (self.winfo_screenwidth() * 0.7)  # テーブルの幅の終わりの位置
        text_view_y = 70  # テーブルと同じy座標
        text_view_width = 1.0 - 0.7  # 残りの幅
        text_view_height = 0.6  # テーブルと同じ高さ
        text_view.place(relheight=text_view_height,
                        relwidth=text_view_width, x=text_view_x, y=text_view_y+100)
        return text_view

    def _add_process_data(self):
        target_process_data = self._search_data_with_name(self.model_var.get())
        self.number_pad = NumberPad(self)
        self.number_pad.attributes("-topmost", True)
        self.wait_window(self.number_pad)
        quantity = self.number_pad.input_number
        if quantity is None or quantity == 0:
            return
        del self.number_pad
        if target_process_data["regist_process_count"] != 0:
            self.processed_data_treeview.delete(
                target_process_data["process_data"].model_id)
        target_process_data["regist_process_count"] = quantity
        self.processed_data_treeview.insert("", "end", iid=target_process_data["process_data"].model_id, values=(
            target_process_data["process_data"].model_number, quantity))

    def _remove_selected_items(self):
        selected_items = self.processed_data_treeview.selection()
        for item in selected_items:
            for search_data in self.data_list:
                if search_data["process_data"].model_id == int(item):
                    search_data["regist_process_count"] = 0
                    break
        self._update_selection_table()

    # 削除後に選択テーブルを更新する新しい関数
    def _update_selection_table(self):
        self.processed_data_treeview.delete(
            *self.processed_data_treeview.get_children())
        for process_data in self.data_list:
            if process_data["regist_process_count"]:
                self.processed_data_treeview.insert("", "end",  iid=process_data["process_data"].model_id, values=(
                    process_data["process_data"].model_number, process_data["regist_process_count"]))

    def _regist_processing_order(self):
        order_number = 0
        for search_data in self.data_list:
            search_data["order_number"] = 0

        for id in self.processed_data_treeview.get_children():
            for search_data in self.data_list:
                if search_data["process_data"].model_id == int(id):
                    search_data["order_number"] = order_number
                    order_number += 1

    def _search_data_with_name(self, name):
        for search_data in self.data_list:
            if search_data["process_data"].model_number == name:
                return search_data
        return None

    def _create_process_detail_str(self, process_data):
        process_info = process_data["process_data"]
        with open(process_data["data_file_path"][1:], "r", encoding="utf-8") as f:
            hole_info = json.load(f)
        # 'size' ごとに辞書をまとめる
        grouped_by_size = defaultdict(list)
        for item in hole_info["holes"]:
            size = item['size']
            grouped_by_size[size].append(item)

        holes_info = ""
        for grouped_by_size in grouped_by_size.values():
            holes_info += f"""
            穴サイズ : {grouped_by_size[0]['size']}
                穴の数 : {len(grouped_by_size)}
            """

        info_str = f"""
            加工データ名 : {process_info.model_number}
            ワークの形状 : {process_info.work_shape}
            ワークのサイズ : {process_info.workpiece_dimension}
            平均加工時間 : {process_info.average_processing_time}
            {'-'*20}
            加工データ
            {holes_info}
            """

        return textwrap.dedent(info_str)
