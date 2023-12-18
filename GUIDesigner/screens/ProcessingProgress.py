import tkinter as tk
from tkinter import ttk
from typing import Dict, Union
from GUIDesigner.GUIRequestType import GUIRequestType
from GUIDesigner.GUISignalCategory import GUISignalCategory
from GUIDesigner.screens.ScreenBase import ScreenBase


class ProgressBar:

    default_font_title = ("AR丸ゴシック体M", 20)
    default_font_progress = ("AR丸ゴシック体M", 20)

    def __init__(self, root_frame, label_string: str, row, length=500) -> None:
        self.progress_ratio = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            root_frame, variable=self.progress_ratio, length=500, mode="determinate")
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

    def __init__(self, titel_label_string: str, row, col, on_off=False, font_name="AR丸ゴシック体M", font_size=14) -> None:
        if type(titel_label_string) is not str:
            titel_label_string = str(titel_label_string)
        titel_label_string += " " * LabelUnit.padding_space
        self.lamp_image = tk.Label(
            LabelUnit.root_frame,  text=titel_label_string, compound=tk.RIGHT,
            image=LabelUnit.on_lamp_image if on_off else LabelUnit.off_lamp_image,  font=(font_name, font_size))
        self.lamp_image.grid(row=row, column=col, sticky=tk.W)

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

        self.on_image = self.image_resource["green_lamp"].subsample(
            2, 2)  # 2倍縮小
        self.off_image = self.image_resource["red_lamp"].subsample(
            2, 2)

        self._create_widgets()
        self._create_sensor_status_labels()
        # self._update_connection_status_label()

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

    def _create_lamps(self, label_strings, col):
        # ラベルを作成して配置
        for i, label_text in enumerate(label_strings):
            LabelUnit(label_text, i, col)

    def _create_widgets(self):
        # 進捗フレームを作成
        self.label_strings = ["加工進捗", "良品率", "残り時間", "残り枚数"]
        self.progress_bar_frame = tk.Frame(self)
        self.progress_bar_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # ラベル用のフレーム
        self.label_frame = tk.Frame(self)
        self.label_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        LabelUnit.initial_variables(
            self.label_frame, self.on_image, self.off_image)
        # 要素のラベルを作成して配置
        for i, label_text in enumerate(self.label_strings):
            ProgressBar(self.progress_bar_frame, label_text, i+1)

        self.current_data_name = self.selected_items[0][0] if self.selected_items else "未選択"
        self.current_data_label = tk.Label(
            self.progress_bar_frame, text=f"現在加工中のデータ: {self.current_data_name}", font=("AR丸ゴシック体M", 18))
        self.current_data_label.grid(row=0, column=0, columnspan=2)  # ２列にまたがる
        # 選択されたデータの名前を取得
        # バックライト、バーライト、リングライトのラベルを作成
        # self.lighting_labels = self._create_lighting_status_labels()
        # ドアロックのラベルを作成
        # self.door_lock_labels = self._create_door_lock_status_labels()

        # # プログレスバー用の変数
        # self.progress_var = tk.DoubleVar()
        # self.quality_var = tk.DoubleVar()
        # self.remaining_time_var = tk.DoubleVar()
        # self.remaining_work_var = tk.DoubleVar()

        # # プログレスバー
        # self.progress_bar = ttk.Progressbar(
        #     self, variable=self.progress_var, length=500, mode="determinate")
        # self.quality_bar = ttk.Progressbar(
        #     self, variable=self.quality_var, length=500, mode="determinate")
        # self.remaining_time_bar = ttk.Progressbar(
        #     self, variable=self.remaining_time_var, length=500, mode="determinate")
        # self.remaining_work_bar = ttk.Progressbar(
        #     self, variable=self.remaining_work_var, length=500, mode="determinate")

        # 数値表示用のラベル
        self.progress_label = tk.Label(
            self, text="0%", font=("AR丸ゴシック体M", 20))
        self.quality_label = tk.Label(
            self, text="0%", font=("AR丸ゴシック体M", 20))
        self.remaining_time_label = tk.Label(
            self, text="2:30", font=("AR丸ゴシック体M", 20))
        self.remaining_work_label = tk.Label(
            self, text="0", font=("AR丸ゴシック体M", 20))

        # プログレスバー、ラベル、ボタンを配置
        # self.progress_bar.grid(row=1, column=1, padx=10, pady=10)
        # self.progress_label.grid(row=1, column=2, padx=10, pady=10)

        # self.quality_bar.grid(row=2, column=1, padx=10, pady=10)
        # self.quality_label.grid(row=2, column=2, padx=10, pady=10)

        # self.remaining_time_bar.grid(row=3, column=1, padx=10, pady=10)
        # self.remaining_time_label.grid(row=3, column=2, padx=10, pady=10)

        # self.remaining_work_bar.grid(row=4, column=1, padx=10, pady=10)
        # self.remaining_work_label.grid(row=4, column=2, padx=10, pady=10)

        # データ名を表示するラベル
        # self.current_data_label = tk.Label(
        #     self, text=f"現在加工中のデータ: {self.current_data_name}", font=("AR丸ゴシック体M", 18))
        # self.current_data_label.grid(row=0, column=0, columnspan=2, pady=40)

        # ネットワーク状況を表示するラベル
        # self.connection_status_label = tk.Label(
        #     self, text="Connection", image=self.off_image, compound=tk.BOTTOM)
        # self.connection_status_label.place(x=1500, y=400)
        # self._update_connection_status_label()  # 初期表示を更新

        # ステータスを確認し、適切な画像を設定
        self.ejector_status = "UR: attach" if self.robot_status[
            "ejector"]["attach"] else "UR: detach"
        self.ejector_image = self.on_image if self.robot_status[
            "ejector"]["attach"] else self.off_image

        # "green_lamp"または"red_lamp"の画像を表示し、画像の下にテキストを表示するためのラベル
        self.ejector_image_label = tk.Label(
            self, image=self.ejector_image, compound=tk.BOTTOM, text=self.ejector_status)
        self.ejector_image_label.place(x=1400, y=400)

        # センサーステータスラベルを更新
        # self._update_lighting_status_labels(self.lighting_labels)
        # ドアロックステータスラベルを更新
        # self._update_door_lock_status_labels(self.door_lock_labels)

    def _create_sensor_status_labels(self):
        # センサーステータス用のラベルを作成して配置
        self.sensor_status_labels = []
        self.row_index = 6  # 適切な行に配置するためのインデックス

        self.sensor_name_mapping = {
            1: "良品センサ", 2: "不良品センサ", 3: "搬入部在荷センサ",
            4: "加工部在荷センサ", 5: "検査部在荷センサ", 6: "URファイバセンサ"
        }

        self.cylinder_mapping = {
            1: {"forward": "加工部位置決め前進端", "backward": "加工部位置決め後進端"},
            2: {"forward": "加工部テーブル前進端", "backward": "加工部テーブル後進端"},
            3: {"forward": "検査部位置決め前進端", "backward": "検査部位置決め後進端"},
            4: {"forward": "ツールチェンジャー前進端", "backward": "ツールチェンジャー後進端"},
            5: {"forward": "検査部壁前進端", "backward": "検査部壁後進端"}
        }

        self._create_lamps(self.sensor_name_mapping, 0)

    def _create_lighting_status_labels(self):
        # ライトステータス用のラベルを作成して配置
        lighting_status_labels = []
        row_index = 8  # 適切な行に配置するためのインデックス

        lighting_name_mapping = {
            "back_light": "バックライト", "bar_light": "バーライト", "ring_light": "リングライト"
        }

        for light_name, light_value in self.robot_status["lighting"].items():
            light_label = tk.Label(
                self, text=lighting_name_mapping[light_name], font=("AR丸ゴシック体M", 14))
            light_label.place(x=1150, y=row_index*85)  # 任意のy座標に適した値を指定してください

            light_image = self.on_image if light_value else self.off_image
            light_status_label = tk.Label(
                self, text="On" if light_value else "Off", image=light_image)
            # 任意のy座標に適した値を指定してください
            light_status_label.place(x=1250, y=row_index*84)

            lighting_status_labels.append(light_status_label)
            row_index += 1

        return lighting_status_labels

    def _create_door_lock_status_labels(self):
        # ドアロックステータス用のラベルを作成して配置
        self.door_lock_status_labels = []
        row_index = 10  # 適切な行に配置するためのインデックス

        for door_num, door_lock_value in self.robot_status["door_lock"].items():
            self.door_lock_label = tk.Label(
                self, text=f"ドアロック{door_num}", font=("AR丸ゴシック体M", 14))
            # 任意のy座標に適した値を指定してください
            self.door_lock_label.place(x=1450, y=row_index*67)

            door_lock_image = self.on_image if door_lock_value else self.off_image
            door_lock_status_label = tk.Label(
                self, text="Locked" if door_lock_value else "Unlocked",
                image=door_lock_image, compound=tk.RIGHT, font=("AR丸ゴシック体M", 14))
            door_lock_status_label.place(
                x=1570, y=row_index*66)  # 任意のy座標に適した値を指定してください

            self.door_lock_status_labels.append(door_lock_status_label)
            row_index += 1

        return self.door_lock_status_labels

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
