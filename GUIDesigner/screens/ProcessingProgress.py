import copy
import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Union
from GUIDesigner.Frames import Frames
from GUIDesigner.GUIRequestType import GUIRequestType
from GUIDesigner.GUISignalCategory import GUISignalCategory
from GUIDesigner.screens.ScreenBase import ScreenBase

FRAME_PADDING_X = 40
FRAME_PADDING_Y = 40
DOOR_LOCK_NUMBER = 4


class ProgressBar:

    default_font_title = ("AR丸ゴシック体M", 20)
    default_font_progress = ("AR丸ゴシック体M", 20)

    def __init__(self, root_frame, label_string: str, row, view_update_handler, length=700) -> None:
        self.progress_ratio = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            root_frame, variable=self.progress_ratio, length=length, mode="determinate")
        self.title_label = tk.Label(
            root_frame, text=label_string, font=ProgressBar.default_font_title)
        self.progress_level = tk.Label(
            root_frame, text="0", font=ProgressBar.default_font_progress)
        self.view_update_handler = view_update_handler

        self.progress_bar.grid(row=row, column=1, padx=10, pady=20)
        self.title_label.grid(row=row, column=0, padx=40, pady=10)
        self.progress_level.grid(row=row, column=2, padx=10, pady=10)

    def update_progress(self, **args):
        ratio, label_str = self.view_update_handler(**args)
        self.progress_ratio.set(ratio)
        self.progress_level.config(text=label_str)


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
            LabelUnit.root_frame, compound=tk.RIGHT, text=titel_label_string, font=(
                font_name, font_size),
            image=LabelUnit.on_lamp_image if on_off else LabelUnit.off_lamp_image, anchor=tk.E
        )

    def set_grid(self, row_, col):
        self.lamp_image.grid(row=row_, column=col,
                             padx=10, pady=10, sticky="nsew")

    def update_lamp(self, is_on: bool):
        self.lamp_image.config(
            image=LabelUnit.on_lamp_image if is_on else LabelUnit.off_lamp_image)


class ProcessingProgress(ScreenBase):

    def __init__(self, parent: tk.Tk, image_resource: Dict[str, tk.PhotoImage],  selected_items, robot_status, request_work_data_setter):
        super().__init__(parent)
        self.image_resource: dict = image_resource
        self.robot_status: dict = robot_status
        self.sensor_status_labels = []
        self.selected_items = selected_items
        self.rabel_col_num = 0
        self.label_status_dict = {}
        self.old_robot_status = {}
        self.request_work_data_setter = request_work_data_setter

        self.on_image = self.image_resource["green_lamp"].subsample(
            2, 2)  # 2倍縮小
        self.off_image = self.image_resource["red_lamp"].subsample(
            2, 2)

        self._create_widgets()
        self.connection_status_label = None
        self.is_initial_process = False

    def _test_update_ui(self, new_state=True):
        # 上のものを全てTrueにした
        new_robot_status = {
            "is_connection": new_state,
            "ejector": new_state,
            "lighting": {
                "back_light": new_state, "bar_light": new_state, "ring_light": new_state
            },
            "sensor": {
                0: new_state, 1: new_state, 2: new_state, 3: new_state, 4: new_state, 5: new_state
            },
            "reed_switch": {
                0: {"forward": new_state, "backward": new_state}, 1: {"forward": new_state, "backward": new_state}, 2: {"forward": new_state, "backward": new_state},
                3: {"forward": new_state, "backward": new_state}, 4: {"forward": new_state, "backward": new_state}, 5: {"forward": new_state, "backward": new_state}
            },
            "door_lock": {
                0: new_state, 1: new_state, 2: new_state, 3: new_state
            }
        }
        self._update_ui(new_robot_status)

    def handle_queued_request(self, request_type: Union[GUISignalCategory, GUIRequestType], request_data=None):
        self.handle_pause_and_emergency(request_type, request_data)
        if request_type == GUISignalCategory.SENSOR_STATUS_UPDATE:
            self._update_ui(self.robot_status)
        elif request_type == GUISignalCategory.PROCESSING_OUTCOME:
            self._update_progress_state()
        elif request_type == GUISignalCategory.CANNOT_CONTINUE_PROCESSING:
            self.request_work_data_setter(request_data)
            self.change_frame(Frames.WORK_REQUEST_OVERVIEW)

    def create_frame(self):
        self.tkraise()
        self.old_robot_status = copy.deepcopy(self.robot_status)
        if not self.is_initial_process:
            self.process_data_manager = self.selected_items()
            self.process_count_sum = self.process_data_manager.get_process_count_sum()
            self.reaming_second_sum = self.process_data_manager.get_reaming_time_sum().total_seconds()
            self.is_initial_process = True
        self._set_robot_status(self.robot_status, self.label_status_dict)
        self._update_progress_state()

    def _update_progress_state(self):
        if not len(self.process_data_manager.process_data_list):
            print("全ての加工が終了しました")
            self.change_frame(Frames.WORK_RESULT_OVERVIEW)
            self.is_initial_process = False
            return
        self._update_current_data_label()
        good_sum, bad_sum = self.process_data_manager.get_good_and_bad_count()
        self.progress_percent.update_progress(sum_count=self.process_count_sum,
                                              current_count=good_sum)
        self.good_rate.update_progress(good_sum=good_sum, bad_sum=bad_sum)
        self.remaining_time.update_progress(
            reaming_time_second=self.process_data_manager.get_reaming_time_sum().total_seconds())
        self.remaining_count.update_progress(
            process_data=self.process_data_manager.process_data_list[0])
        # self.after(1000, self._update_progress_state)

    def _update_current_data_label(self):
        current_data_name = self.process_data_manager.process_data_list[
            0]["process_data"].model_number
        self.current_data_label.config(
            text=f"現在加工中のデータ: {current_data_name}")

    def _add_label_column(self, label_units: List[LabelUnit]):
        for i, label_unit in enumerate(label_units):
            if not label_unit:
                continue
            label_unit.set_grid(
                i, self.rabel_col_num)
            self.label_frame.rowconfigure(i, weight=1)
        self.label_frame.columnconfigure(self.rabel_col_num, weight=1)
        self.rabel_col_num += 1

    def _create_widgets(self):
        # 進捗フレームを作成
        progress_bar_frame = self._create_progress_bars()

        # ラベル用のフレーム
        self.label_frame = tk.Frame(self)
        self.label_frame.pack(side=tk.TOP, fill=tk.BOTH,
                              expand=True, padx=FRAME_PADDING_X, pady=FRAME_PADDING_Y)
        LabelUnit.initial_variables(
            self.label_frame, self.on_image, self.off_image)
        self.label_status_dict["sensor"] = self._create_sensor_status_labels()
        self.label_status_dict["reed_switch"] = self._create_cylinder_status_labels(
        )
        self.label_status_dict["lighting"] = self._create_lighting_status_labels(
        )
        self.label_status_dict["door_lock"] = self._create_door_lock_status_labels(
        )

        self.current_data_label = tk.Label(progress_bar_frame)
        self.current_data_label.grid(
            row=0, column=0, columnspan=2, padx=40, pady=40)

    def _create_progress_bars(self):
        def update_progress_percent(sum_count, current_count):
            progress_percent = (current_count/sum_count) * 100
            progress_percent = round(progress_percent, 1)
            return progress_percent, f"{progress_percent:.1f}% ({sum_count}個中{current_count}個加工済み)"

        def update_good_rate(good_sum, bad_sum):
            if good_sum == 0 and bad_sum == 0:
                return 0, "0%"
            good_rate = (good_sum/(good_sum+bad_sum)) * 100
            good_rate = round(good_rate, 1)
            return good_rate, f"{good_rate:.1f}%"

        def update_remaining_time(reaming_time_second):
            hours, remainder = divmod(int(reaming_time_second), 3600)
            minutes, seconds = divmod(remainder, 60)
            if hours:
                time_str = f"{hours:2d}時間{minutes:2d}分{seconds:2d}秒"
            else:
                time_str = f"{minutes:2d}分{seconds:2d}秒"
            reaming_rate = (reaming_time_second/self.reaming_second_sum) * 100
            return 100-reaming_rate, time_str

        def update_reaming_count(process_data):
            reaming_rate = (
                process_data["good_count"] / process_data["regist_process_count"]) * 100
            return reaming_rate, f"{reaming_rate:.1f}%"

        progress_bar_frame = tk.Frame(self)
        progress_bar_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.progress_percent = ProgressBar(
            progress_bar_frame, "加工進捗", 1, update_progress_percent)
        self.good_rate = ProgressBar(
            progress_bar_frame, "良品率", 2, update_good_rate)
        self.remaining_time = ProgressBar(
            progress_bar_frame, "残り時間", 3, update_remaining_time)
        self.remaining_count = ProgressBar(
            progress_bar_frame, "残り枚数", 4, update_reaming_count)
        return progress_bar_frame

    def _create_sensor_status_labels(self):
        # センサーステータス用のラベルを作成して配置
        sensor_labels = {}
        sensor_names = [
            "良品センサ", "不良品センサ", "搬入部在荷センサ",
            "加工部在荷センサ", "検査部在荷センサ", "URファイバセンサ"
        ]
        sensor_label_row_list = []
        for i, sensor_name in enumerate(sensor_names):
            label_unit = LabelUnit(sensor_name)
            sensor_label_row_list.append(label_unit)
            sensor_labels[i] = label_unit
        self._add_label_column(sensor_label_row_list)
        return sensor_labels

    def _create_cylinder_status_labels(self):
        cylinder_labels = {}
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
            cylinder_labels[i] = {}
            cylinder_labels[i]["forward"] = label_unit_positive_edge
            cylinder_labels[i]["backward"] = label_unit_negative_edge
        self._add_label_column(cylinder_forward_ravel_list)
        self._add_label_column(cylinder_backward_ravel_list)
        return cylinder_labels

    def _create_lighting_status_labels(self):
        lighting_name_mapping = {}
        lighting_name_mapping["back_light"] = LabelUnit("バックライト")
        lighting_name_mapping["bar_light"] = LabelUnit("バーライト")
        lighting_name_mapping["ring_light"] = LabelUnit("リングライト")
        self.label_status_dict["lighting"] = lighting_name_mapping

        ejector_label = LabelUnit("ワーク吸着")
        self.label_status_dict["ejector"] = ejector_label
        label_list = [ejector_label, None, None]
        label_list.extend(lighting_name_mapping.values())
        self._add_label_column(label_list)
        return lighting_name_mapping

    def _create_door_lock_status_labels(self):
        # ドアロックステータス用のラベルを作成して配置
        door_lock_status = {}
        connection_status_label = LabelUnit("ロボットとの接続")
        self.label_status_dict["is_connection"] = connection_status_label
        door_lock_label_list = [connection_status_label, None]
        for i in range(DOOR_LOCK_NUMBER):
            label_unit = LabelUnit(f"ドアロック{i}")
            door_lock_status[i] = label_unit
            door_lock_label_list.append(label_unit)
        self._add_label_column(door_lock_label_list)
        return door_lock_status

    def _update_ui(self, new_robot_status):
        robot_status_differences = self.compare_dicts(
            self.old_robot_status, new_robot_status)
        for key_str in robot_status_differences.keys():
            self._get_unit_from_keystr(key_str).update_lamp(
                robot_status_differences[key_str])

    def _get_unit_from_keystr(self, key_str):
        keys = key_str.split('.')
        # 辞書の要素にアクセス
        current_element = self.label_status_dict
        for key in keys:
            # 数値に変換できる場合は変換する
            if key.isdigit():
                key = int(key)
            current_element = current_element[key]
        return current_element

    def compare_dicts(self, old_dict, new_dict, path="") -> dict:
        differences = {}
        for key in old_dict:
            # キーがdict2にない場合
            if key not in new_dict:
                differences[f"{path}{key}"] = (old_dict[key], None)
            # 両方の値が辞書の場合、再帰的に比較
            elif isinstance(old_dict[key], dict) and isinstance(new_dict[key], dict):
                deeper_differences = self.compare_dicts(
                    old_dict[key], new_dict[key], path=f"{path}{key}.")
                differences.update(deeper_differences)
            # 値が異なる場合、変更された値のみを記録
            elif old_dict[key] != new_dict[key]:
                differences[f"{path}{key}"] = new_dict[key]  # 変更後の値のみを保存
        self.old_robot_status = copy.deepcopy(new_dict)
        return differences

    def _set_robot_status(self, values_dict, instances_dict):
        for key, value in values_dict.items():
            if isinstance(value, dict) and key in instances_dict:
                # 対応するキーが辞書の場合、再帰的に処理
                self._set_robot_status(value, instances_dict[key])
            elif key in instances_dict:
                # インスタンスに値を設定
                # ここでは `set_value` メソッドを使って値を設定すると仮定
                instances_dict[key].update_lamp(value)


if __name__ == "__main__":
    app = ProcessingProgress()
