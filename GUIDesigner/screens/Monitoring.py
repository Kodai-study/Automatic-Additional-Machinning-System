import tkinter as tk
from queue import Queue
from tkinter import PhotoImage
from typing import List, Tuple
from GUIDesigner.Frames import Frames
from GUIDesigner.GUIRequestType import GUIRequestType
from GUIDesigner.GUISignalCategory import GUISignalCategory
from GUIDesigner.screens.ScreenBase import ScreenBase
from common_data_type import CameraType, LightingType

CAMERA_IMAGE_UPDATE_RATE = 1000


class Monitoring(ScreenBase):
    def __init__(self, parent, robot_status: dict, send_to_integration_queue: Queue):
        super().__init__(parent)
        self.robot_status = robot_status
        self.send_to_integration_queue = send_to_integration_queue
        self._create_widgets()

        # TODO この画面にいるときだけリクエストするように変更
        self._request_inspection_camera_update()

    def _test_camera_views_update(self):
        self.after(1000, lambda: self._update_image_from_path(
            self.accuracy_camera_views, "./resource/images/test.png"))
        self.after(2000, lambda: self._update_image_from_path(
            self.tool_camera_views, "./resource/images/test.png"))
        self.after(3000, lambda: self._update_image_from_path(
            self.processing_camera_views, "./resource/images/test.png"))

    def _request_inspection_camera_update(self):
        self.send_to_integration_queue.put((GUIRequestType.CAMERA_FEED_REQUEST, [
            CameraType.TOOL_CAMERA, CameraType.PRE_PROCESSING_CAMERA, CameraType.ACCURACY_CAMERA]))
        self.after(CAMERA_IMAGE_UPDATE_RATE,
                   self._request_inspection_camera_update)

    def create_frame(self):
        self.tkraise()

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
        self.send_to_integration_queue.put(
            (GUIRequestType.ROBOT_OPERATION_REQUEST, command))

    def lightning_control_request(self, lightingtype, lightingstate):
        self.send_to_integration_queue.put(
            (GUIRequestType.LIGHTING_CONTROL_REQUEST, (lightingtype, lightingstate)))

    def button_state_update(self, on_button, off_button):
        on_button["state"] = "normal"
        off_button["state"] = "disable"

    def toggle_button(self, on_button, off_button):
        if on_button["state"] == "normal" or on_button["state"] == "active":
            on_button["state"] = "disabled"
            off_button["state"] = "normal"
        else:
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
        backlight_label = tk.Label(
            self, text="工具検査用のリング照明", font=("AR丸ゴシック体M", 18))
        barlight_label = tk.Label(
            self, text="加工前検査用のバー照明", font=("AR丸ゴシック体M", 18))
        ringlight_label = tk.Label(
            self, text="精度検査用のバックライト照明", font=("AR丸ゴシック体M", 18))
        UR_label = tk.Label(
            self, text="UR吸着", font=("AR丸ゴシック体M", 18))
        dlc0_label = tk.Label(
            self, text="ドアロック1", font=("AR丸ゴシック体M", 18))
        dlc1_label = tk.Label(
            self, text="ドアロック2", font=("AR丸ゴシック体M", 18))
        dlc2_label = tk.Label(
            self, text="ドアロック3", font=("AR丸ゴシック体M", 18))
        dlc3_label = tk.Label(
            self, text="ドアロック4", font=("AR丸ゴシック体M", 18))

        svm_label = tk.Label(
            self, text="サーボモータ", font=("AR丸ゴシック体M", 18))
        conv_label = tk.Label(
            self, text="ベルトコンベア", font=("AR丸ゴシック体M", 18))
        cyl_000_label = tk.Label(
            self, text="加工部位置決めシリンダ", font=("AR丸ゴシック体M", 18))
        cyl_001_label = tk.Label(
            self, text="検査部位置決めシリンダ", font=("AR丸ゴシック体M", 18))
        cyl_002_label = tk.Label(
            self, text="ツールチェンジャーシリンダ", font=("AR丸ゴシック体M", 18))
        cyl_003_label = tk.Label(
            self, text="検査部壁シリンダ", font=("AR丸ゴシック体M", 18))
        cyl_004_label = tk.Label(
            self, text="加工部テーブルシリンダ", font=("AR丸ゴシック体M", 18))

        kara_label1 = tk.Label(
            self, text="", font=("AR丸ゴシック体M", 18))
        kara_label2 = tk.Label(
            self, text="", font=("AR丸ゴシック体M", 18))

        back_button = tk.Button(self, text="戻る", command=lambda: self.change_frame(Frames.CREATE_SELECTION), font=(
            "AR丸ゴシック体M", 18), width=22)

        on_buttons: List[tk.Button] = []  # ONボタン用のリスト
        off_buttons: List[tk.Button] = []  # OFFボタン用のリスト
        forward_buttons: List[tk.Button] = []  # 正転ボタン用のリスト
        reverse_buttons: List[tk.Button] = []  # 後転ボタン用のリスト
        stop_buttons: List[tk.Button] = []

        # ボタンのコマンドリストを作成します
        on_commands = ["EJCT 0,ATTACH\n", "DLC 0,LOCK\n",
                       "DLC 1,LOCK\n", "DLC 2,LOCK\n", "DLC 3,LOCK\n"]
        off_commands = ["EJCT 0,DETACH\n", "DLC 0,UNLOCK\n",
                        "DLC 1,UNLOCK\n", "DLC 2,UNLOCK\n", "DLC 3,UNLOCK\n"]
        forward_commands = ["SVM 0,CW,1\n", "CONV 0,CW\n", "CYL 001,PUSH\n",
                            "CYL 002,PUSH\n", "CYL 003,PUSH\n", "CYL 004,PUSH\n", "CYL 005,PUSH\n"]
        reverse_commands = ["SVM 0,BREAK,0\n", "CONV 0,OFF\n", "CYL 001,PULL\n",
                            "CYL 002,PULL\n", "CYL 003,PULL\n", "CYL 004,PULL\n", "CYL 005,PULL\n"]
        stop_command = ["CONV 0,N\n", "CONV 0,N\n", "CONV 0,N\n"]

        # 証明ボタン作成
        self.tool_light_on_button = tk.Button(self, text="ON", state="normal", width=10, bg="#87de87",
                                              command=lambda: (self.lightning_control_request(LightingType.TOOL_LIGHTING, True)))
        self.tool_light_off_button = tk.Button(self, text="OFF", state="disable", width=10, bg="#de9687",
                                               command=lambda: (self.lightning_control_request(LightingType.TOOL_LIGHTING, False)))
        self.processing_light_on_button = tk.Button(self, text="ON", state="normal", width=10, bg="#87de87",
                                                    command=lambda: (self.lightning_control_request(LightingType.PRE_PROCESSING_LIGHTING, True)))
        self.processing_light_off_button = tk.Button(self, text="OFF", state="disable", width=10, bg="#de9687",
                                                     command=lambda: (self.lightning_control_request(LightingType.PRE_PROCESSING_LIGHTING, False)))
        self.accuracy_light_on_button = tk.Button(self, text="ON", state="normal", width=10, bg="#87de87",
                                                  command=lambda: (self.lightning_control_request(LightingType.ACCURACY_LIGHTING, True)))
        self.accuracy_light_off_button = tk.Button(self, text="OFF", state="disable", width=10, bg="#de9687",
                                                   command=lambda: (self.lightning_control_request(LightingType.ACCURACY_LIGHTING, False)))

        self.tool_light_on_button.grid(row=1, column=2)
        self.tool_light_off_button.grid(row=1, column=3)
        self.processing_light_on_button.grid(row=2, column=2)
        self.processing_light_off_button.grid(row=2, column=3)
        self.accuracy_light_on_button.grid(row=3, column=2)
        self.accuracy_light_off_button.grid(row=3, column=3)

        for i in range(5):
            on_button = tk.Button(self, text="ON", state="normal", width=10, bg="#87de87",
                                  command=lambda i=i: (self.robot_oprration_request(on_commands[i]), self.toggle_button(on_buttons[i], off_buttons[i])))
            off_button = tk.Button(self, text="OFF", state="disabled", width=10, bg="#de9687",
                                   command=lambda i=i: (self.robot_oprration_request(off_commands[i]), self.toggle_button(on_buttons[i], off_buttons[i])))
            on_buttons.append(on_button)
            off_buttons.append(off_button)

        # 同様に、正転と後転のボタンにも異なるコマンドを設定します
        for i in range(8):
            forward_button = tk.Button(self, text="正転", state="normal", width=10, bg="#87de87",
                                       command=lambda i=i: (self.robot_oprration_request(forward_commands[i]), self.toggle_button(forward_buttons[i], reverse_buttons[i])))
            reverse_button = tk.Button(self, text="後転", state="disabled", width=10, bg="#de9687",
                                       command=lambda i=i: (self.robot_oprration_request(reverse_commands[i]), self.toggle_button(forward_buttons[i], reverse_buttons[i])))
            forward_buttons.append(forward_button)
            reverse_buttons.append(reverse_button)

        for i in range(2):
            stop_button = tk.Button(self, text="停止", state="normal", width=10, bg="#ffb366",
                                    command=lambda: (self.robot_oprration_request(stop_command[i])))
            stop_buttons.append(stop_button)

        for i in range(5):
            on_buttons[i].grid(row=i + 4, column=2)
            off_buttons[i].grid(row=i + 4, column=3)

        for i in range(3):
            forward_buttons[i].grid(row=i + 9, column=2)
            reverse_buttons[i].grid(row=i + 9, column=3)

        for i in range(4):
            forward_buttons[i + 3].grid(row=i + 1, column=6)
            reverse_buttons[i + 3].grid(row=i + 1, column=7)

        for i in range(2):
            stop_buttons[i].grid(row=i + 9, column=4)

        kara_label1.grid(row=0, column=0, padx=40, pady=40)
        kara_label2.grid(row=0, column=4, padx=30, pady=40)
        backlight_label.grid(row=1, column=1, padx=30, pady=20)
        barlight_label.grid(row=2, column=1, padx=30, pady=20)
        ringlight_label.grid(row=3, column=1, padx=30, pady=20)
        UR_label.grid(row=4, column=1, padx=30, pady=20)
        dlc0_label.grid(row=5, column=1, padx=30, pady=20)
        dlc1_label.grid(row=6, column=1, padx=30, pady=20)
        dlc2_label.grid(row=7, column=1, padx=30, pady=20)
        dlc3_label.grid(row=8, column=1, padx=30, pady=20)

        svm_label.grid(row=9, column=1, padx=30, pady=20)
        conv_label.grid(row=10, column=1, padx=30, pady=20)
        cyl_000_label.grid(row=11, column=1, padx=30, pady=20)
        cyl_001_label.grid(row=1, column=5, padx=30, pady=20)
        cyl_002_label.grid(row=2, column=5, padx=30, pady=20)
        cyl_003_label.grid(row=3, column=5, padx=30, pady=20)
        cyl_004_label.grid(row=4, column=5, padx=30, pady=20)

        back_button.place(rely=0.85, relx=0.75)

    def _initial_camera_view_canvases(self):
        accuracy_camera_canvas = tk.Canvas(
            self, bg="#deb887", height=300, width=300)
        accuracy_camera_canvas.place(x=870, y=550)
        image_on_canvas = accuracy_camera_canvas.create_image(
            0, 0, anchor=tk.NW)
        self.accuracy_camera_views = accuracy_camera_canvas, image_on_canvas

        tool_camera_canvas = tk.Canvas(
            self, bg="#deb887", height=300, width=300)
        tool_camera_canvas.place(x=1200, y=550)
        image_on_canvas = tool_camera_canvas.create_image(
            0, 0, anchor=tk.NW)
        self.tool_camera_views = tool_camera_canvas, image_on_canvas

        processing_camera_canvas = tk.Canvas(
            self, bg="#deb887", height=500, width=300)
        image_on_canvas = processing_camera_canvas.create_image(
            0, 0, anchor=tk.NW)
        processing_camera_canvas.place(x=1530, y=350)
        self.processing_camera_views = processing_camera_canvas, image_on_canvas
