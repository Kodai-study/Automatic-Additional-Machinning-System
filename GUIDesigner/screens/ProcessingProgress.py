import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Union
from GUIDesigner.GUIRequestType import GUIRequestType
from GUIDesigner.GUISignalCategory import GUISignalCategory
from GUIDesigner.screens.ScreenBase import ScreenBase

FRAME_PADDING_X = 40
FRAME_PADDING_Y = 40
DOOR_LOCK_NUMBER = 4


class ProgressBar:

    default_font_title = ("AR丸ゴシック体M", 20)
    default_font_progress = ("AR丸ゴシック体M", 20)

    def __init__(self, root_frame, label_string: str, row, length=500) -> None:
        self.progress_ratio = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            root_frame, variable=self.progress_ratio, length=length, mode="determinate")
        self.title_label = tk.Label(
            root_frame, text=label_string, font=ProgressBar.default_font_title)
        self.progress_level = tk.Label(
            root_frame, text="0", font=ProgressBar.default_font_progress)

        self.progress_bar.grid(row=row, column=1, padx=10, pady=10)
        self.title_label.grid(row=row, column=0, padx=10, pady=10)
        self.progress_level.grid(row=row, column=2, padx=10, pady=10)


class LabelUnit:

    on_lamp_image: tk.PhotoImage = None
    off_lamp_image: tk.PhotoImage = None
    root_frame: tk.Tk = None
    default_font = ("AR丸ゴシック体M", 14)
    padding_space = 5

    @staticmethod
    def initial_variables(root_frame_resource: tk.Tk, on_lamp_image_resouce: tk.PhotoImage, off_lamp_image_resource: tk.PhotoImage):
        LabelUnit.on_lamp_image = on_lamp_image_resouce
        LabelUnit.off_lamp_image = off_lamp_image_resource
        LabelUnit.root_frame = root_frame_resource

    def __init__(self, titel_label_string: str, on_off=False, font_name="AR丸ゴシック体M", font_size=14) -> None:
        if type(titel_label_string) is not str:
            titel_label_string = str(titel_label_string)
        titel_label_string += " " * LabelUnit.padding_space
        self.lamp_image = tk.Label(
            LabelUnit.root_frame,  text=titel_label_string, compound=tk.RIGHT,
            image=LabelUnit.on_lamp_image if on_off else LabelUnit.off_lamp_image,
            font=(font_name, font_size), anchor=tk.E)

    def set_grid(self, row_, col):
        self.lamp_image.grid(row=row_, column=col,
                             padx=10, pady=10, sticky="nsew")

    def update_lamp(self, is_on: bool):
        self.lamp_image.config(
            image=LabelUnit.on_lamp_image if is_on else LabelUnit.off_lamp_image)


class ProcessingProgress(ScreenBase):

    def __init__(self, parent: tk.Tk, image_resource: Dict[str, tk.PhotoImage],  selected_items: list, robot_status):
        super().__init__(parent)
        self.image_resource: dict = image_resource
        self.robot_status: dict = robot_status
        self.sensor_status_labels = []
        self.selected_items = selected_items
        self.rabel_col_num = 0

        self.on_image = self.image_resource["green_lamp"].subsample(
            2, 2)  # 2倍縮小
        self.off_image = self.image_resource["red_lamp"].subsample(
            2, 2)

        self._create_widgets()
        self._create_sensor_status_labels()
        self._create_lighting_status_labels()
        self._create_door_lock_status_labels()
        self.connection_status_label = None

    def handle_queued_request(self, request_type: Union[GUISignalCategory, GUIRequestType], request_data=None):
        self.handle_pause_and_emergency(request_type, request_data)
        if request_type == GUISignalCategory.SENSOR_STATUS_UPDATE:
            self._update_connection_status_label()
            self._update_door_lock_status_labels(self.door_lock_status_labels)
            self._update_lighting_status_labels(self.lighting_status_labels)
            self._update_sensor_status_labels(self.sensor_status_labels)

    def create_frame(self):
        self.tkraise()

    def _add_label_column(self, label_units: List[LabelUnit]):
        for i, label_unit in enumerate(label_units):
            label_unit.set_grid(
                i, self.rabel_col_num)
            self.label_frame.rowconfigure(i, weight=1)
        self.label_frame.columnconfigure(self.rabel_col_num, weight=1)
        self.rabel_col_num += 1

    def _create_widgets(self):
        # 進捗フレームを作成
        self.label_strings = ["加工進捗", "良品率", "残り時間", "残り枚数"]
        self.progress_bar_frame = tk.Frame(self)
        self.progress_bar_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # ラベル用のフレーム
        self.label_frame = tk.Frame(self)
        self.label_frame.pack(side=tk.TOP, fill=tk.BOTH,
                              expand=True, padx=FRAME_PADDING_X, pady=FRAME_PADDING_Y)

        LabelUnit.initial_variables(
            self.label_frame, self.on_image, self.off_image)
        # 要素のラベルを作成して配置
        for i, label_text in enumerate(self.label_strings):
            ProgressBar(self.progress_bar_frame, label_text, i+1)

        self.current_data_name = self.selected_items[0][0] if self.selected_items else "未選択"
        self.current_data_label = tk.Label(
            self.progress_bar_frame, text=f"現在加工中のデータ: {self.current_data_name}", font=("AR丸ゴシック体M", 18))
        self.current_data_label.grid(row=0, column=0, columnspan=2)  # ２列にまたがる

        # ステータスを確認し、適切な画像を設定
        self.ejector_status = "UR: attach" if self.robot_status[
            "ejector"]["attach"] else "UR: detach"
        self.ejector_image = self.on_image if self.robot_status[
            "ejector"]["attach"] else self.off_image

    def _create_sensor_status_labels(self):
        # センサーステータス用のラベルを作成して配置
        self.sensor_status_labels = []
        self.row_index = 6  # 適切な行に配置するためのインデックス

        # リストにする
        sensor_names = [
            "良品センサ", "不良品センサ", "搬入部在荷センサ",
            "加工部在荷センサ", "検査部在荷センサ", "URファイバセンサ"
        ]

        self.sensor_labels = {}
        self.cylinder_labels = {}

        sensor_label_row_list = []
        for i, sensor_name in enumerate(sensor_names):
            label_unit = LabelUnit(sensor_name)
            sensor_label_row_list.append(label_unit)
            self.sensor_labels[i] = label_unit
        self._add_label_column(sensor_label_row_list)

        cylinder_label_names = [
            "加工部位置決め", "加工部テーブル", "検査部位置決め", "検査部位置決め",
            "ツールチェンジャー", "検査部"
        ]

        cylinder_forward_ravel_list = []
        cylinder_backward_ravel_list = []
        for i, cylinder_name in enumerate(cylinder_label_names):
            label_unit_positive_edge = LabelUnit(cylinder_name+"前進端")
            label_unit_negative_edge = LabelUnit(cylinder_name+"後進端")
            cylinder_forward_ravel_list.append(label_unit_positive_edge)
            cylinder_backward_ravel_list.append(label_unit_negative_edge)
            self.cylinder_labels[i] = {}
            self.cylinder_labels[i]["forward"] = label_unit_positive_edge
            self.cylinder_labels[i]["backward"] = label_unit_negative_edge
        self._add_label_column(cylinder_forward_ravel_list)
        self._add_label_column(cylinder_backward_ravel_list)

    def _create_lighting_status_labels(self):

        self.lighting_name_mapping = {}
        self.lighting_name_mapping["back_light"] = LabelUnit("バックライト")
        self.lighting_name_mapping["bar_light"] = LabelUnit("バーライト")
        self.lighting_name_mapping["ring_light"] = LabelUnit("リングライト")

        self._add_label_column(self.lighting_name_mapping.values())

    def _create_door_lock_status_labels(self):
        # ドアロックステータス用のラベルを作成して配置
        self.door_lock_status = {}
        door_lock_label_list = []
        for i in range(DOOR_LOCK_NUMBER):
            label_unit = LabelUnit(f"ドアロック{i+1}")
            self.door_lock_status[i] = label_unit
            door_lock_label_list.append(label_unit)
        self._add_label_column(door_lock_label_list)

    def _update_door_lock_status_labels(self, door_lock_labels):
        for door_lock_label in door_lock_labels:
            door_lock_label.grid_forget()
        self.door_lock_status_labels = self._create_door_lock_status_labels()

    def _update_lighting_status_labels(self, lighting_labels):
        for lighting_label in lighting_labels:
            lighting_label.grid_forget()
        self.lighting_status_labels = self._create_lighting_status_labels()

    def _update_sensor_status_labels(self, sensor_labels):
        for sensor_label in sensor_labels:
            sensor_label.grid_forget()

    def _update_connection_status_label(self):
        if self.connection_status_label:
            connection_text = "Connection: On" if self.robot_status[
                "is_connection"] else "Connection: Off"
            connection_image = self.on_image if self.robot_status["is_connection"] else self.off_image

            self.connection_status_label.config(
                text=connection_text, image=connection_image)

    def update_ui_thread(self):
        # このメソッドはメインスレッドで実行されるようになりました
        self._update_ui()
        self._update_connection_status_label()  # ネットワーク状況を更新
        self.root.after(1000, self.update_ui_thread)  # 再度このメソッドを1000ミリ秒後に呼び出す

    def _update_ui(self):
        # プログレスバーなどの UI を更新する処理をここに追加
        progress_value = 50  # 例として50%の進捗を設定
        self.progress_var.set(progress_value)
        self.progress_label.config(text=f"{progress_value}%")
        # 他の要素も同様に更新

        # センサーステータスラベルを更新
        self._update_sensor_status_labels(self.sensor_status_labels)


if __name__ == "__main__":
    app = ProcessingProgress()
