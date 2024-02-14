import copy
import tkinter as tk
from queue import Queue
from typing import List, Tuple
from GUIDesigner.Frames import Frames
from GUIDesigner.GUIRequestType import GUIRequestType
from GUIDesigner.GUISignalCategory import GUISignalCategory
from GUIDesigner.screens.ScreenBase import ScreenBase
from common_data_type import CameraType, LightingType

CAMERA_IMAGE_UPDATE_RATE = 1000
LABEL_FONT_SIZE = 22
BUTTON_FONT_SIZE = 14


class Monitoring(ScreenBase):
    def __init__(self, parent, robot_status: dict, send_to_integration_queue: Queue):
        super().__init__(parent)
        self.robot_status = robot_status
        self.old_robot_status = copy.deepcopy(robot_status)
        self.send_to_integration_queue = send_to_integration_queue
        self._create_widgets()
        self.is_currentScreen = lambda: parent.current_screen == Frames.MONITORING
        self.stm_motor_turn = 1
        self._request_inspection_camera_update()

    def _request_inspection_camera_update(self):
        self.send_to_integration_queue.put((GUIRequestType.CAMERA_FEED_REQUEST, [
            CameraType.TOOL_CAMERA, CameraType.PRE_PROCESSING_CAMERA, CameraType.ACCURACY_CAMERA]))
        if self.is_currentScreen():
            self.after(CAMERA_IMAGE_UPDATE_RATE,
                       self._request_inspection_camera_update)

    def create_frame(self):
        self.tkraise()
        self._request_inspection_camera_update()

    def _update_image_from_path(self, canvas_datas: Tuple[tk.Canvas, int], img_path: str):
        target_canvas = canvas_datas[0]
        img_width = target_canvas.winfo_reqwidth()
        img_height = target_canvas.winfo_reqheight()
        original_image = tk.PhotoImage(file=img_path)
        view_image = self.resize_image(img_width, img_height, original_image)
        target_canvas.itemconfig(canvas_datas[1], image=view_image)
        target_canvas.image = view_image  # これが重要です

    def handle_queued_request(self, request_type: GUISignalCategory, request_data=None):
        self.handle_pause_and_emergency(request_type, request_data)

        if request_type == GUIRequestType.LIGHTING_CONTROL_REQUEST:
            self._handle_lightning_control_responce(request_data)

        elif request_type == GUIRequestType.CAMERA_FEED_REQUEST:
            for camera_type, img_path in request_data:
                target_camera_view = None
                if camera_type == CameraType.ACCURACY_CAMERA:
                    target_camera_view = self.accuracy_camera_views
                elif camera_type == CameraType.PRE_PROCESSING_CAMERA:
                    target_camera_view = self.processing_camera_views
                elif camera_type == CameraType.TOOL_CAMERA:
                    target_camera_view = self.tool_camera_views

                if target_camera_view:
                    self._update_image_from_path(target_camera_view, img_path)

        elif request_type == GUISignalCategory.SENSOR_STATUS_UPDATE:
            self._update_button_enables(request_data)

    def _handle_lightning_control_responce(self, request_data):
        if request_data['target'] == LightingType.TOOL_LIGHTING:
            if request_data['state'] == True:
                self.button_state_update(
                    self.tool_light_off_button, self.tool_light_on_button)
            else:
                self.button_state_update(
                    self.tool_light_on_button, self.tool_light_off_button)
        if request_data['target'] == LightingType.PRE_PROCESSING_LIGHTING:
            if request_data['state'] == True:
                self.button_state_update(
                    self.processing_light_off_button, self.processing_light_on_button)
            else:
                self.button_state_update(
                    self.processing_light_on_button, self.processing_light_off_button)
        if request_data['target'] == LightingType.ACCURACY_LIGHTING:
            if request_data['state'] == True:
                self.button_state_update(
                    self.accuracy_light_off_button, self.accuracy_light_on_button)
            else:
                self.button_state_update(
                    self.accuracy_light_on_button, self.accuracy_light_off_button)

    def robot_oprration_request(self, command):
        # 改行で終わっていなかった場合、改行を追加する
        if command[-1] != "\n":
            command += "\n"
        self.send_to_integration_queue.put(
            (GUIRequestType.ROBOT_OPERATION_REQUEST, command))

    def lightning_control_request(self, lightingtype, lightingstate):
        self.send_to_integration_queue.put(
            (GUIRequestType.LIGHTING_CONTROL_REQUEST, (lightingtype, lightingstate)))

    def button_state_update(self, on_button, off_button):
        on_button["state"] = "normal"
        off_button["state"] = "disable"

    def resize_image(self, width, height, image):
        new_width = width
        new_height = height

        resized_image = image.subsample(
            int(image.width() / new_width), int(image.height() / new_height))
        return resized_image

    def _create_widgets(self):

        self._initial_camera_view_canvases()

        # ラベル作成
        backlight_label = tk.Label(
            self, text="工具検査用のリング照明", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))
        barlight_label = tk.Label(
            self, text="加工前検査用のバー照明", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))
        ringlight_label = tk.Label(
            self, text="精度検査用のバックライト照明", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))
        UR_label = tk.Label(
            self, text="UR吸着", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))
        dlc0_label = tk.Label(
            self, text="ドアロック", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))
        stm_label = tk.Label(
            self, text="ステッピングモータ", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))
        conv_label = tk.Label(
            self, text="ベルトコンベア", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))
        cyl_000_label = tk.Label(
            self, text="加工部位置決めシリンダ", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))
        cyl_001_label = tk.Label(
            self, text="検査部位置決めシリンダ", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))
        cyl_002_label = tk.Label(
            self, text="ツールチェンジャーシリンダ", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))
        cyl_003_label = tk.Label(
            self, text="検査部壁シリンダ", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))
        cyl_004_label = tk.Label(
            self, text="加工部テーブルシリンダ", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))
        kara_label1 = tk.Label(
            self, text="", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))

        # ボタンのコマンドリスト作成
        self.on_buttons: List[tk.Button] = []
        self.off_buttons: List[tk.Button] = []
        self.pull_buttons: List[tk.Button] = []
        self.push_buttons: List[tk.Button] = []

        on_commands = ["EJCT 0,ATTACH", "DLC 0,LOCK"]
        off_commands = ["EJCT 0,DETACH", "DLC 0,UNLOCK"]
        pull_commands = ["CYL 0,PULL", "CYL 3,PULL", "CYL 2,PULL",
                         "CYL 4,PULL", "CYL 1,PULL"]
        push_commands = ["CYL 0,PUSH", "CYL 3,PUSH", "CYL 2,PUSH",
                         "CYL 4,PUSH", "CYL 1,PUSH"]
        conv_n_commands = ["CONV 0,N", "CONV 0,N", "CONV 0,N"]

        # 照明ボタン作成
        self.tool_light_on_button = tk.Button(self, text="ON", state="normal", width=10, font=("MSゴシック", BUTTON_FONT_SIZE, "bold"), bg="#87de87",
                                              command=lambda: self.lightning_control_request(LightingType.TOOL_LIGHTING, True))
        self.tool_light_off_button = tk.Button(self, text="OFF", state="disable", width=10, font=("MSゴシック", BUTTON_FONT_SIZE, "bold"), bg="#de9687",
                                               command=lambda: self.lightning_control_request(LightingType.TOOL_LIGHTING, False))
        self.processing_light_on_button = tk.Button(self, text="ON", state="normal", width=10, font=("MSゴシック", BUTTON_FONT_SIZE, "bold"), bg="#87de87",
                                                    command=lambda: self.lightning_control_request(LightingType.PRE_PROCESSING_LIGHTING, True))
        self.processing_light_off_button = tk.Button(self, text="OFF", state="disable", width=10, font=("MSゴシック", BUTTON_FONT_SIZE, "bold"), bg="#de9687",
                                                     command=lambda: self.lightning_control_request(LightingType.PRE_PROCESSING_LIGHTING, False))
        self.accuracy_light_on_button = tk.Button(self, text="ON", state="normal", width=10, font=("MSゴシック", BUTTON_FONT_SIZE, "bold"), bg="#87de87",
                                                  command=lambda: self.lightning_control_request(LightingType.ACCURACY_LIGHTING, True))
        self.accuracy_light_off_button = tk.Button(self, text="OFF", state="disable", width=10, font=("MSゴシック", BUTTON_FONT_SIZE, "bold"), bg="#de9687",
                                                   command=lambda: self.lightning_control_request(LightingType.ACCURACY_LIGHTING, False))

        # シリンダボタン
        for i in range(5):
            push_button = tk.Button(self, text="PUSH", state="normal", width=10, bg="#87de87", font=("MSゴシック", BUTTON_FONT_SIZE, "bold"),
                                    command=lambda i=i: self.robot_oprration_request(push_commands[i]))
            pull_button = tk.Button(self, text="PULL", state="disabled", width=10, bg="#de9687", font=("MSゴシック", BUTTON_FONT_SIZE, "bold"),
                                    command=lambda i=i: self.robot_oprration_request(pull_commands[i]))
            self.push_buttons.append(push_button)
            self.pull_buttons.append(pull_button)

        # URドアロックボタン
        for i in range(len(on_commands)):
            on_button = tk.Button(self, text="ON", state="normal", width=10, bg="#87de87", font=(
                "MSゴシック", BUTTON_FONT_SIZE, "bold"))
            off_button = tk.Button(self, text="OFF", state="disabled", width=10, bg="#de9687", font=(
                "MSゴシック", BUTTON_FONT_SIZE, "bold"))

            on_button["command"] = lambda i=i: self.robot_oprration_request(on_commands[i])
            off_button["command"] = lambda i=i: self.robot_oprration_request(off_commands[i])
            self.on_buttons.append(on_button)
            self.off_buttons.append(off_button)

        def enable_stm_button(flag):
            if flag == 0:  # 原点サーチ
                stm_turn_button["state"] = "disabled"
                stm_search_button["state"] = "disabled"
                stm_plus_button["state"] = "disabled"
                stm_minus_button["state"] = "disabled"
                stm_value_label["fg"] = "#666666"
                stm_value_label["bg"] = "#cccccc"
            elif flag == 1:  # STM 0,TURNED受信時
                stm_turn_button["state"] = "normal"
                stm_search_button["state"] = "normal"
                stm_value_label["fg"] = "#000000"
                stm_value_label["bg"] = "#ffffff"
                if self.stm_motor_turn <= 1:
                    stm_plus_button["state"] = "normal"
                elif 7 <= self.stm_motor_turn:
                    stm_minus_button["state"] = "normal"
                else:
                    stm_plus_button["state"] = "normal"
                    stm_minus_button["state"] = "normal"

        def stm_turn_controller(change_number):
            self.stm_motor_turn += change_number
            if self.stm_motor_turn >= 7:
                self.stm_motor_turn = 7
                stm_plus_button["state"] = "disabled"
            elif self.stm_motor_turn <= 1:
                self.stm_motor_turn = 1
                stm_minus_button["state"] = "disabled"
            else:
                stm_plus_button["state"] = "normal"
                stm_minus_button["state"] = "normal"
            stm_value_label["text"] = str(self.stm_motor_turn)

        def enable_conveyor_button(button_kind_list):

            conveyor_rotato_good_button["state"] = "disabled"
            conveyor_rotato_bad_button["state"] = "disabled"
            conveyor_stop_button["state"] = "disabled"
            for button_kind in button_kind_list:
                if button_kind == "GOOD":
                    conveyor_rotato_good_button["state"] = "normal"
                elif button_kind == "BAD":
                    conveyor_rotato_bad_button["state"] = "normal"
                elif button_kind == "STOP":
                    conveyor_stop_button["state"] = "normal"

        # ベルトコンベアボタン
        conveyor_rotato_good_button = tk.Button(
            self, text="正転", state="normal", width=10, bg="#87de87", font=("MSゴシック", BUTTON_FONT_SIZE, "bold"))

        conveyor_rotato_bad_button = tk.Button(
            self, text="後転", state="normal", width=10, bg="#de9687", font=("MSゴシック", BUTTON_FONT_SIZE, "bold"))

        conveyor_stop_button = tk.Button(
            self, text="停止", state="normal", width=10, bg="#ffb366", font=("MSゴシック", BUTTON_FONT_SIZE, "bold"))

        conveyor_rotato_good_button["command"] = lambda: (self.robot_oprration_request("CONV 0,GOOD"),
                                                          enable_conveyor_button(["STOP"]))
        conveyor_rotato_bad_button["command"] = lambda: (self.robot_oprration_request("CONV 0,BAD"),
                                                         enable_conveyor_button(["STOP"]))
        conveyor_stop_button["command"] = lambda: (self.robot_oprration_request("CONV 0,N"),
                                                   enable_conveyor_button(["GOOD", "BAD"]))
        # ステッピングモータボタン
        stm_plus_button = tk.Button(
            self, text="+1", state="normal", width=10, bg="#7ab0ff", font=("MSゴシック", BUTTON_FONT_SIZE, "bold"))

        stm_minus_button = tk.Button(
            self, text="-1", state="disabled", width=10, bg="#7ab0ff", font=("MSゴシック", BUTTON_FONT_SIZE, "bold"))

        stm_value_label = tk.Label(  # いくつ回すかの数値表示ラベル(かテキストボックスのdisable)
            self, text="1", state="normal", width=10, height=1, bg="#ffffff", relief="solid", bd=1, font=("MSゴシック", BUTTON_FONT_SIZE, "bold"))

        stm_search_button = tk.Button(
            self, text="原点", state="normal", width=10, bg="#87de87", font=("MSゴシック", BUTTON_FONT_SIZE, "bold"))

        stm_turn_button = tk.Button(
            self, text="回転", state="normal", width=10, bg="#87de87", font=("MSゴシック", BUTTON_FONT_SIZE, "bold"))

        stm_plus_button["command"] = lambda: (stm_turn_controller(1))
        stm_minus_button["command"] = lambda: (stm_turn_controller(-1))
        stm_search_button["command"] = lambda: (self.robot_oprration_request("STM 0,SEARCH"),
                                                print("STM 0,SEARCH"),
                                                enable_stm_button(0))
        stm_turn_button["command"] = lambda: (self.robot_oprration_request("STM 0,R,"+str(self.stm_motor_turn)),
                                              print("STM 0,R," +
                                                    str(self.stm_motor_turn)),
                                              enable_stm_button(0))
        # 戻るボタン
        back_button = tk.Button(self, text="戻る", command=lambda: (self.change_frame(Frames.CREATE_SELECTION), enable_stm_button(1)),
                                font=("AR丸ゴシック体M", 18), width=22)

        kara_label1.grid(row=0, column=0)
        backlight_label.grid(row=1, column=1, pady=10)
        barlight_label.grid(row=2, column=1, pady=10)
        ringlight_label.grid(row=3, column=1, pady=10)
        
        for i, (on_button, off_button) in enumerate(zip(self.on_buttons, self.off_buttons)):
            # ボタン配置
            on_button.grid(row=i + 4, column=2)
            off_button.grid(row=i + 4, column=3)

        stm_plus_button.grid(row=9, column=4)
        stm_value_label.grid(row=10, column=4)
        stm_minus_button.grid(row=11, column=4)
        stm_turn_button.grid(row=10, column=3)
        stm_search_button.grid(row=10, column=2)

        conveyor_rotato_good_button.grid(row=13, column=2)
        conveyor_rotato_bad_button.grid(row=13, column=3)
        conveyor_stop_button.grid(row=13, column=4)

        for i in range(5):
            self.push_buttons[i].grid(row=i + 14, column=2)
            self.pull_buttons[i].grid(row=i + 14, column=3)

        UR_label.grid(row=4, column=1, pady=10)
        dlc0_label.grid(row=5, column=1, pady=10)
        stm_label.grid(row=10, column=1, pady=10)
        conv_label.grid(row=13, column=1, pady=10)
        cyl_000_label.grid(row=14, column=1, pady=10)
        cyl_001_label.grid(row=15, column=1, pady=10)
        cyl_002_label.grid(row=16, column=1, pady=10)
        cyl_003_label.grid(row=17, column=1, pady=10)
        cyl_004_label.grid(row=18, column=1, pady=10)

        self.tool_light_on_button.grid(row=1, column=2)
        self.tool_light_off_button.grid(row=1, column=3)
        self.processing_light_on_button.grid(row=2, column=2)
        self.processing_light_off_button.grid(row=2, column=3)
        self.accuracy_light_on_button.grid(row=3, column=2)
        self.accuracy_light_off_button.grid(row=3, column=3)
        back_button.place(rely=0.88, relx=0.75)

    def _compare_dicts(self, old_dict, new_dict, path="") -> dict:
        differences = {}
        for key in old_dict:
            # キーがdict2にない場合
            if key not in new_dict:
                differences[f"{path}{key}"] = (old_dict[key], None)
            # 両方の値が辞書の場合、再帰的に比較
            elif isinstance(old_dict[key], dict) and isinstance(new_dict[key], dict):
                deeper_differences = self._compare_dicts(
                    old_dict[key], new_dict[key], path=f"{path}{key}.")
                differences.update(deeper_differences)
            # 値が異なる場合、変更された値のみを記録
            elif old_dict[key] != new_dict[key]:
                differences[f"{path}{key}"] = new_dict[key]  # 変更後の値のみを保存
        self.old_robot_status = copy.deepcopy(new_dict)
        return differences

    def _update_button_enables(self, differences):
        changed_colums = self._compare_dicts(
            self.old_robot_status, self.robot_status)
        if "ejector" in changed_colums:
            if changed_colums["ejector"]:
                self.button_state_update(
                    self.off_buttons[0], self.on_buttons[0])
            else:
                self.off_buttons[0]["state"] = "normal"
                self.on_buttons[0]["state"] = "normal"
        if "door_lock" in changed_colums:
            if changed_colums["door_lock"]:
                self.button_state_update(
                    self.off_buttons[1], self.on_buttons[1])
            else:
                self.button_state_update(
                    self.on_buttons[1], self.off_buttons[1])

    def _initial_camera_view_canvases(self):
        accuracy_camera_canvas = tk.Canvas(
            self, bg="#deb887", height=250, width=370)
        accuracy_camera_canvas.place(x=820, y=630)
        image_on_canvas = accuracy_camera_canvas.create_image(
            0, 0, anchor=tk.NW)
        self.accuracy_camera_views = accuracy_camera_canvas, image_on_canvas

        tool_camera_canvas = tk.Canvas(
            self, bg="#deb887", height=240, width=240)
        tool_camera_canvas.place(x=1580, y=630)
        image_on_canvas = tool_camera_canvas.create_image(
            0, 0, anchor=tk.NW)
        self.tool_camera_views = tool_camera_canvas, image_on_canvas

        processing_camera_canvas = tk.Canvas(
            self, bg="#deb887", height=250, width=370)
        image_on_canvas = processing_camera_canvas.create_image(
            0, 0, anchor=tk.NW)
        processing_camera_canvas.place(x=1200, y=630)
        self.processing_camera_views = processing_camera_canvas, image_on_canvas
