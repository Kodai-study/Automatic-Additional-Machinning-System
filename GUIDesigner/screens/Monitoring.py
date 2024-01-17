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
LABEL_FONT_SIZE = 22
BUTTON_FONT_SIZE = 14


class Monitoring(ScreenBase):
    def __init__(self, parent, robot_status: dict, send_to_integration_queue: Queue):
        super().__init__(parent)
        self.robot_status = robot_status
        self.send_to_integration_queue = send_to_integration_queue
        self._create_widgets()
        self.is_currentScreen = lambda: parent.current_screen == Frames.MONITORING

        # TODO この画面にいるときだけリクエストするように変更
        self._request_inspection_camera_update()

    def _test_camera_views_update(self):
        self.after(1000, lambda: self._update_image_from_path(
            self.accuracy_camera_views, "./test/c.png"))
        self.after(2000, lambda: self._update_image_from_path(
            self.tool_camera_views, "./test/a.png"))
        self.after(3000, lambda: self._update_image_from_path(
            self.processing_camera_views, "./test/b.png"))

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
        svm_label = tk.Label(
            self, text="サーボモータ", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))
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
        tool_label = tk.Label(
            self, text="工具使用回数", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))
        tool1_label = tk.Label(
            self, text="工具1 : ", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))
        tool2_label = tk.Label(
            self, text="工具2 : ", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))
        tool3_label = tk.Label(
            self, text="工具3 : ", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))
        tool4_label = tk.Label(
            self, text="工具4 : ", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))
        tool5_label = tk.Label(
            self, text="工具5 : ", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))
        tool6_label = tk.Label(
            self, text="工具6 : ", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))
        tool7_label = tk.Label(
            self, text="工具7 : ", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))
        tool8_label = tk.Label(
            self, text="工具8 : ", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))
        kara_label1 = tk.Label(
            self, text="", font=("AR丸ゴシック体M", LABEL_FONT_SIZE))

        tool1_entry = tk.Entry(
            self, font=("Arial", LABEL_FONT_SIZE), width=10, state="readonly")
        tool2_entry = tk.Entry(
            self, font=("Arial", LABEL_FONT_SIZE), width=10, state="readonly")
        tool3_entry = tk.Entry(
            self, font=("Arial", LABEL_FONT_SIZE), width=10, state="readonly")
        tool4_entry = tk.Entry(
            self, font=("Arial", LABEL_FONT_SIZE), width=10, state="readonly")
        tool5_entry = tk.Entry(
            self, font=("Arial", LABEL_FONT_SIZE), width=10, state="readonly")
        tool6_entry = tk.Entry(
            self, font=("Arial", LABEL_FONT_SIZE), width=10, state="readonly")
        tool7_entry = tk.Entry(
            self, font=("Arial", LABEL_FONT_SIZE), width=10, state="readonly")
        tool8_entry = tk.Entry(
            self, font=("Arial", LABEL_FONT_SIZE), width=10, state="readonly")

        # ボタンのコマンドリスト作成
        on_buttons: List[tk.Button] = []
        off_buttons: List[tk.Button] = []
        forward_buttons: List[tk.Button] = []
        reverse_buttons: List[tk.Button] = []
        pull_buttons: List[tk.Button] = []
        push_buttons: List[tk.Button] = []
        stop_buttons: List[tk.Button] = []

        on_commands = ["EJCT 0,ATTACH\n", "DLC 0,LOCK\n"]
        off_commands = ["EJCT 0,DETACH\n", "DLC 0,UNLOCK\n"]
        forward_commands = ["SVM 0,CW,1\n", "CONV 0,CW\n"]
        reverse_commands = ["SVM 0,BREAK,0\n", "CONV 0,OFF\n"]
        pull_commands = ["CYL 0,PULL\n", "CYL 3,PULL\n", "CYL 2,PULL\n",
                         "CYL 4,PULL\n", "CYL 1,PULL\n"]
        push_commands = ["CYL 0,PUSH\n", "CYL 3,PUSH\n", "CYL 2,PUSH\n",
                         "CYL 4,PUSH\n", "CYL 1,PUSH\n"]
        stop_command = ["CONV 0,N\n", "CONV 0,N\n", "CONV 0,N\n"]

        # 照明ボタン作成
        self.tool_light_on_button = tk.Button(self, text="ON", state="normal", width=10, font=("MSゴシック", BUTTON_FONT_SIZE, "bold"), bg="#87de87",
                                              command=lambda: (self.lightning_control_request(LightingType.TOOL_LIGHTING, True)))
        self.tool_light_off_button = tk.Button(self, text="OFF", state="disable", width=10, font=("MSゴシック", BUTTON_FONT_SIZE, "bold"), bg="#de9687",
                                               command=lambda: (self.lightning_control_request(LightingType.TOOL_LIGHTING, False)))
        self.processing_light_on_button = tk.Button(self, text="ON", state="normal", width=10, font=("MSゴシック", BUTTON_FONT_SIZE, "bold"), bg="#87de87",
                                                    command=lambda: (self.lightning_control_request(LightingType.PRE_PROCESSING_LIGHTING, True)))
        self.processing_light_off_button = tk.Button(self, text="OFF", state="disable", width=10, font=("MSゴシック", BUTTON_FONT_SIZE, "bold"), bg="#de9687",
                                                     command=lambda: (self.lightning_control_request(LightingType.PRE_PROCESSING_LIGHTING, False)))
        self.accuracy_light_on_button = tk.Button(self, text="ON", state="normal", width=10, font=("MSゴシック", BUTTON_FONT_SIZE, "bold"), bg="#87de87",
                                                  command=lambda: (self.lightning_control_request(LightingType.ACCURACY_LIGHTING, True)))
        self.accuracy_light_off_button = tk.Button(self, text="OFF", state="disable", width=10, font=("MSゴシック", BUTTON_FONT_SIZE, "bold"), bg="#de9687",
                                                   command=lambda: (self.lightning_control_request(LightingType.ACCURACY_LIGHTING, False)))

        # シリンダボタン
        for i in range(5):
            push_button = tk.Button(self, text="PUSH", state="normal", width=10, bg="#87de87", font=("MSゴシック", BUTTON_FONT_SIZE, "bold"),
                                    command=lambda i=i: (self.robot_oprration_request(push_commands[i]), self.toggle_button(push_buttons[i], pull_buttons[i])))
            pull_button = tk.Button(self, text="PULL", state="disabled", width=10, bg="#de9687", font=("MSゴシック", BUTTON_FONT_SIZE, "bold"),
                                    command=lambda i=i: (self.robot_oprration_request(pull_commands[i]), self.toggle_button(push_buttons[i], pull_buttons[i])))
            push_buttons.append(push_button)
            pull_buttons.append(pull_button)
        # URドアロックボタン
        for i in range(len(on_commands)):
            on_button = tk.Button(self, text="ON", state="normal", width=10, bg="#87de87", font=(
                "MSゴシック", BUTTON_FONT_SIZE, "bold"))
            off_button = tk.Button(self, text="OFF", state="disabled", width=10, bg="#de9687", font=(
                "MSゴシック", BUTTON_FONT_SIZE, "bold"))

            on_button["command"] = command = lambda i=i: (self.robot_oprration_request(
                on_commands[i]), self.toggle_button(on_buttons[i], off_buttons[i]))
            off_button["command"] = command = lambda i=i: (self.robot_oprration_request(
                off_commands[i]), self.toggle_button(off_buttons[i], on_buttons[i]))
            on_buttons.append(on_button)
            off_buttons.append(off_button)

        # サーボモータベルトコンベアボタン
        for i in range(2):
            forward_button = tk.Button(self, text="正転", state="normal", width=10, bg="#87de87", font=("MSゴシック", BUTTON_FONT_SIZE, "bold"),
                                       command=lambda i=i: (self.robot_oprration_request(forward_commands[i]), self.toggle_button(forward_buttons[i], reverse_buttons[i])))
            reverse_button = tk.Button(self, text="後転", state="disabled", width=10, bg="#de9687", font=("MSゴシック", BUTTON_FONT_SIZE, "bold"),
                                       command=lambda i=i: (self.robot_oprration_request(reverse_commands[i]), self.toggle_button(forward_buttons[i], reverse_buttons[i])))
            forward_buttons.append(forward_button)
            reverse_buttons.append(reverse_button)
        # 停止ボタン
        for i in range(2):
            stop_button = tk.Button(self, text="停止", state="normal", width=10, bg="#ffb366", font=("MSゴシック", BUTTON_FONT_SIZE, "bold"),
                                    command=lambda: (self.robot_oprration_request(stop_command[i])))
            stop_buttons.append(stop_button)
        # 戻るボタン
        back_button = tk.Button(self, text="戻る", command=lambda: self.change_frame(Frames.CREATE_SELECTION),
                                font=("AR丸ゴシック体M", 18), width=22)

        for i, (on_button, off_button) in enumerate(zip(on_buttons, off_buttons)):
            # ボタン配置
            on_button.grid(row=i + 4, column=2)
            off_button.grid(row=i + 4, column=3)

        for i in range(2):
            forward_buttons[i].grid(row=i + 9, column=2)
            reverse_buttons[i].grid(row=i + 9, column=3)

        for i in range(5):
            push_buttons[i].grid(row=i + 11, column=2)
            pull_buttons[i].grid(row=i + 11, column=3)

        for i in range(2):
            stop_buttons[i].grid(row=i + 9, column=4)

        kara_label1.grid(row=0, column=0)
        backlight_label.grid(row=1, column=1, pady=10)
        barlight_label.grid(row=2, column=1, pady=10)
        ringlight_label.grid(row=3, column=1, pady=10)
        UR_label.grid(row=4, column=1, pady=10)
        dlc0_label.grid(row=5, column=1, pady=10)
        svm_label.grid(row=9, column=1, pady=10)
        conv_label.grid(row=10, column=1, pady=10)
        cyl_000_label.grid(row=11, column=1, pady=10)
        cyl_001_label.grid(row=12, column=1, pady=10)
        cyl_002_label.grid(row=13, column=1, pady=10)
        cyl_003_label.grid(row=BUTTON_FONT_SIZE, column=1, pady=10)
        cyl_004_label.grid(row=15, column=1, pady=10)
        tool_label.grid(row=1, column=5, columnspan=2)
        tool1_label.grid(row=2, column=5)
        tool2_label.grid(row=2, column=7)
        tool3_label.grid(row=2, column=9)
        tool4_label.grid(row=2, column=11)
        tool5_label.grid(row=3, column=5)
        tool6_label.grid(row=3, column=7)
        tool7_label.grid(row=3, column=9)
        tool8_label.grid(row=3, column=11)

        self.tool_light_on_button.grid(row=1, column=2)
        self.tool_light_off_button.grid(row=1, column=3)
        self.processing_light_on_button.grid(row=2, column=2)
        self.processing_light_off_button.grid(row=2, column=3)
        self.accuracy_light_on_button.grid(row=3, column=2)
        self.accuracy_light_off_button.grid(row=3, column=3)
        back_button.place(rely=0.88, relx=0.75)

        tool1_entry.grid(row=2, column=6)
        tool2_entry.grid(row=2, column=8)
        tool3_entry.grid(row=2, column=10)
        tool4_entry.grid(row=2, column=12)
        tool5_entry.grid(row=3, column=6)
        tool6_entry.grid(row=3, column=8)
        tool7_entry.grid(row=3, column=10)
        tool8_entry.grid(row=3, column=12)

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
