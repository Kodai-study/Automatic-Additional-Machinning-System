from threading import Thread
import time
import tkinter as tk
from tkinter import ttk
from GUIDesigner import GUIDesigner

class ProcessingProgress:
    def __init__(self, root,create_result_frame):

        self.root = root
        self.create_result_frame = create_result_frame
        self.robot_status = {
            "is_connection": True,
            "limit_switch": False,
            "lighting": {
                "back_light": False, "bar_light": False, "ring_light": False
            },
            "sensor": {
                1: False, 2: True, 3: True, 4: False, 5: False, 6: False
            },
            "reed_switch": {
                1: {"forward": True, "backward": False}, 2: {"forward": False, "backward": False},
                3: {"forward": False, "backward": False}, 4: {"forward": False, "backward": False}, 5: {"forward": False, "backward": False}
            },
            # "door_status": {
            #     1: False, 2: False, 3: False, 4: False
            # },
            "door_lock": {
                1: True, 2: True, 3: True, 4: True
            },
            "ejector": {
                "attach": True, "detach": False
            }
        }

        self.on_image = tk.PhotoImage(
            file="./resource/images/red_lamp.png").subsample(2, 2)  # 2倍縮小
        self.off_image = tk.PhotoImage(
            file="./resource/images/green_lamp.png").subsample(2, 2)  # 2倍縮小
        self.connection_status_label = None  # coneection のステータスラベル
        self.create_frame([])  # Pass your selected_items list here
        self.sensor_status_labels = self.create_sensor_status_labels()

        self.update_connection_status_label()
        # 1000ミリ秒ごとにupdate_ui_threadを呼び出す
        self.root.after(1000, self.update_ui_thread)

    def create_frame(self, selected_items):
        # 進捗フレームを作成
        self.progress_frame = tk.Frame(self.root)

        # 要素のラベル
        labels = ["", "加工進捗", "良品率", "残り時間", "残り枚数"]

        # 要素のラベルを作成して配置
        for i, label_text in enumerate(labels):
            label = tk.Label(self.progress_frame,
                             text=label_text, font=("AR丸ゴシック体M", 20))
            label.grid(row=i, column=0, padx=50, pady=10, sticky=tk.W)

        # 選択されたデータの名前を取得
        current_data_name = selected_items[0][0] if selected_items else "未選択"

        # バックライト、バーライト、リングライトのラベルを作成
        lighting_labels = self.create_lighting_status_labels()
        # ドアロックのラベルを作成
        door_lock_labels = self.create_door_lock_status_labels()

        # プログレスバー用の変数
        self.progress_var = tk.DoubleVar()
        quality_var = tk.DoubleVar()
        remaining_time_var = tk.DoubleVar()
        remaining_work_var = tk.DoubleVar()

        # プログレスバー
        progress_bar = ttk.Progressbar(
            self.progress_frame, variable=self.progress_var, length=500, mode="determinate")
        quality_bar = ttk.Progressbar(
            self.progress_frame, variable=quality_var, length=500, mode="determinate")
        remaining_time_bar = ttk.Progressbar(
            self.progress_frame, variable=remaining_time_var, length=500, mode="determinate")
        remaining_work_bar = ttk.Progressbar(
            self.progress_frame, variable=remaining_work_var, length=500, mode="determinate")

        # 数値表示用のラベル
        self.progress_label = tk.Label(
            self.progress_frame, text="0%", font=("AR丸ゴシック体M", 20))
        quality_label = tk.Label(
            self.progress_frame, text="0%", font=("AR丸ゴシック体M", 20))
        remaining_time_label = tk.Label(
            self.progress_frame, text="2:30", font=("AR丸ゴシック体M", 20))
        remaining_work_label = tk.Label(
            self.progress_frame, text="0", font=("AR丸ゴシック体M", 20))
        
        # ボタン作成
        result_button = tk.Button(self.progress_frame, text="結果表示", font=("AR丸ゴシック体M", 18), width=22, command=self.show_result)

        # プログレスバー、ラベル、ボタンを配置
        progress_bar.grid(row=1, column=1, padx=10, pady=10)
        self.progress_label.grid(row=1, column=2, padx=10, pady=10)

        quality_bar.grid(row=2, column=1, padx=10, pady=10)
        quality_label.grid(row=2, column=2, padx=10, pady=10)

        remaining_time_bar.grid(row=3, column=1, padx=10, pady=10)
        remaining_time_label.grid(row=3, column=2, padx=10, pady=10)

        remaining_work_bar.grid(row=4, column=1, padx=10, pady=10)
        remaining_work_label.grid(row=4, column=2, padx=10, pady=10)

        result_button.place(rely=0.87, relx=0.75)

        # データ名を表示するラベル
        current_data_label = tk.Label(
            self.progress_frame, text=f"現在加工中のデータ: {current_data_name}", font=("AR丸ゴシック体M", 18))
        current_data_label.grid(row=0, column=0, columnspan=2, pady=40)

        # ネットワーク状況を表示するラベル
        self.connection_status_label = tk.Label(
            self.progress_frame, text="Connection", image=self.on_image, compound=tk.BOTTOM)
        self.connection_status_label.place(x=1500, y=400)

        # ステータスを確認し、適切な画像を設定
        ejector_status = "UR: attach" if self.robot_status["ejector"]["attach"] else "UR: detach"
        ejector_image = self.on_image if self.robot_status["ejector"]["attach"] else self.off_image

        # "green_lamp"または"red_lamp"の画像を表示し、画像の下にテキストを表示するためのラベル
        ejector_image_label = tk.Label(
            self.progress_frame, image=ejector_image, compound=tk.BOTTOM, text=ejector_status)
        ejector_image_label.place(x=1400, y=400)

        # センサーステータスラベルを更新
        self.update_lighting_status_labels(lighting_labels)
        # ドアロックステータスラベルを更新
        self.update_door_lock_status_labels(door_lock_labels)

        self.progress_frame.pack(fill="both", expand=True)

    def create_sensor_status_labels(self):
        # センサーステータス用のラベルを作成して配置
        sensor_status_labels = []
        row_index = 6  # 適切な行に配置するためのインデックス

        sensor_name_mapping = {
            1: "良品センサ", 2: "不良品センサ", 3: "搬入部在荷センサ",
            4: "加工部在荷センサ", 5: "検査部在荷センサ", 6: "URファイバセンサ"
        }

        cylinder_mapping = {
            1: {"forward": "加工部位置決め前進端", "backward": "加工部位置決め後進端"},
            2: {"forward": "加工部テーブル前進端", "backward": "加工部テーブル後進端"},
            3: {"forward": "検査部位置決め前進端", "backward": "検査部位置決め後進端"},
            4: {"forward": "ツールチェンジャー前進端", "backward": "ツールチェンジャー後進端"},
            5: {"forward": "検査部壁前進端", "backward": "検査部壁後進端"}
        }

        for sensor_num, sensor_value in self.robot_status["sensor"].items():
            if sensor_num in cylinder_mapping:
                sensor_label = tk.Label(
                    self.progress_frame, text=sensor_name_mapping[sensor_num], font=("AR丸ゴシック体M", 14))
                # 任意のy座標に適した値を指定してください
                sensor_label.place(x=100, y=row_index*85)

                sensor_image = self.on_image if sensor_value else self.off_image
                sensor_status_label = tk.Label(
                    self.progress_frame, text="On" if sensor_value else "Off", image=sensor_image)
                sensor_status_label.place(
                    x=260, y=row_index*84)  # 任意のy座標に適した値を指定してください

                reed_switch_labels = []
                for direction in ["forward", "backward"]:
                    reed_switch_value = self.robot_status["reed_switch"][sensor_num][direction]
                    reed_switch_image = self.on_image if reed_switch_value else self.off_image
                    reed_switch_label = tk.Label(
                        self.progress_frame, text=cylinder_mapping[sensor_num][direction], font=("AR丸ゴシック体M", 12))

                    # 新しい配置の設定
                    column_index = 2 if direction == "forward" else 3
                    padx_value = 10 if direction == "forward" else 50
                    # 任意のy座標に適した値を指定してください
                    reed_switch_label.place(
                        x=column_index*240 + padx_value, y=row_index*85)

                    reed_switch_image_label = tk.Label(
                        self.progress_frame, image=reed_switch_image)
                    # 新しい配置の設定
                    column_index = 3 if direction == "forward" else 4
                    padx_value = 10 if direction == "forward" else 50
                    reed_switch_image_label.place(
                        x=column_index*225 + padx_value, y=row_index*84)  # 任意のy座標に適した値を指定してください

                    reed_switch_labels.extend(
                        [reed_switch_label, reed_switch_image_label])

                sensor_status_labels.extend(
                    [sensor_status_label] + reed_switch_labels)
                row_index += 1

        return sensor_status_labels

    def create_lighting_status_labels(self):
        # ライトステータス用のラベルを作成して配置
        lighting_status_labels = []
        row_index = 8  # 適切な行に配置するためのインデックス

        lighting_name_mapping = {
            "back_light": "バックライト", "bar_light": "バーライト", "ring_light": "リングライト"
        }

        for light_name, light_value in self.robot_status["lighting"].items():
            light_label = tk.Label(
                self.progress_frame, text=lighting_name_mapping[light_name], font=("AR丸ゴシック体M", 14))
            light_label.place(x=1150, y=row_index*85)  # 任意のy座標に適した値を指定してください

            light_image = self.on_image if light_value else self.off_image
            light_status_label = tk.Label(
                self.progress_frame, text="On" if light_value else "Off", image=light_image)
            # 任意のy座標に適した値を指定してください
            light_status_label.place(x=1250, y=row_index*84)

            lighting_status_labels.append(light_status_label)
            row_index += 1

        return lighting_status_labels

    def create_door_lock_status_labels(self):
        # ドアロックステータス用のラベルを作成して配置
        door_lock_status_labels = []
        row_index = 10  # 適切な行に配置するためのインデックス

        for door_num, door_lock_value in self.robot_status["door_lock"].items():
            door_lock_label = tk.Label(
                self.progress_frame, text=f"ドアロック{door_num}", font=("AR丸ゴシック体M", 14))
            # 任意のy座標に適した値を指定してください
            door_lock_label.place(x=1450, y=row_index*67)

            door_lock_image = self.on_image if door_lock_value else self.off_image
            door_lock_status_label = tk.Label(
                self.progress_frame, text="Locked" if door_lock_value else "Unlocked", image=door_lock_image)
            door_lock_status_label.place(
                x=1570, y=row_index*66)  # 任意のy座標に適した値を指定してください

            door_lock_status_labels.append(door_lock_status_label)
            row_index += 1

        return door_lock_status_labels
    
    def show_result(self):
        self.create_result_frame()

    def update_door_lock_status_labels(self, door_lock_labels):
        for door_lock_label in door_lock_labels:
            door_lock_label.grid_forget()
        self.door_lock_status_labels = self.create_door_lock_status_labels()

    def update_lighting_status_labels(self, lighting_labels):
        for lighting_label in lighting_labels:
            lighting_label.grid_forget()
        self.lighting_status_labels = self.create_lighting_status_labels()

    def update_sensor_status_labels(self, sensor_labels):
        for sensor_label in sensor_labels:
            sensor_label.grid_forget()
        self.sensor_status_labels = self.create_sensor_status_labels()

    def update_connection_status_label(self):
        if self.connection_status_label:
            if self.robot_status["is_connection"]:
                self.connection_status_label.config(
                    text="Connection: On", image=self.on_image)
            else:
                self.connection_status_label.config(
                    text="Connection: Off", image=self.off_image)

    def update_ui_thread(self):
        # このメソッドはメインスレッドで実行されるようになりました
        self.update_ui()
        self.root.after(1000, self.update_ui_thread)  # 再度このメソッドを1000ミリ秒後に呼び出す

    def update_ui(self):
        # プログレスバーなどの UI を更新する処理をここに追加
        progress_value = 50  # 例として50%の進捗を設定
        self.progress_var.set(progress_value)
        self.progress_label.config(text=f"{progress_value}%")
        # 他の要素も同様に更新

        # センサーステータスラベルを更新
        self.update_sensor_status_labels(self.sensor_status_labels)


if __name__ == "__main__":
    app = ProcessingProgress()
