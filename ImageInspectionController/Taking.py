import configparser
import os
from typing import Tuple
import numpy as np
import pytelicam
import cv2
from ImageInspectionController.ProcessDatas import InspectionType
import datetime as dt


NUM_REQUIRED_CAMERAS = 3
USE_TOOL_INSPECTION_CAMERA = True
USE_PRE_PROCESSING_INSPECTION_CAMERA = True
USE_ACCURACY_INSPECTION_CAMERA = True

cam_count = 1 if USE_TOOL_INSPECTION_CAMERA else 0
if USE_PRE_PROCESSING_INSPECTION_CAMERA:
    cam_count += 1
if USE_ACCURACY_INSPECTION_CAMERA:
    cam_count += 1


class CaseSensitiveConfigParser(configparser.ConfigParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def optionxform(self, optionstr):
        return optionstr


cam_count = 1 if USE_TOOL_INSPECTION_CAMERA else 0
if USE_PRE_PROCESSING_INSPECTION_CAMERA:
    cam_count += 1
if USE_ACCURACY_INSPECTION_CAMERA:
    cam_count += 1


class CaseSensitiveConfigParser(configparser.ConfigParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def optionxform(self, optionstr):
        return optionstr


class Taking:
    def __init__(self):
        self.config = CaseSensitiveConfigParser()
        file_path = 'kensa.conf'
        self.cam_system = self._initial_cam_setting(cam_count)
        self.toggle_flag = True
        self.config.read(file_path, encoding='utf-8')
        if not self.cam_system:
            print("カメラの初期化がうまくできませんでした。 カメラの接続を確認してください")
            return

        if USE_TOOL_INSPECTION_CAMERA:
            self.cam_device_tool, self.receive_signal_tool = self._get_camera_device(
                "TOOL_INSPECTION")

        if USE_PRE_PROCESSING_INSPECTION_CAMERA:
            self.cam_device_kakou, self.receive_signal_kakou = self._get_camera_device(
                "PRE_PROCESSING_INSPECTION")

        if USE_ACCURACY_INSPECTION_CAMERA:
            self.cam_device_seido, self.receive_signal_seido = self._get_camera_device(
                "ACCURACY_INSPECTION")

    def _get_camera_device(self, inspection_type):
        try:
            serial_number, model_number, section_name = self._get_serial_and_model(
                inspection_type)
            return self._setting_cam(
                inspection_type, serial_number, model_number)
        except configparser.NoSectionError:
            raise ValueError(f"指定されたセクションが存在しません: {section_name}")

    def _get_serial_and_model(self, inspection_type: str):
        section_name = f"{inspection_type}"
        serial_number = self.config.get(section_name, "serial_number")
        model_number = self.config.get(section_name, "model_number")
        return serial_number, model_number, section_name

    def _setting_cam(self, camera_section, serial_num: str, model: str)\
            -> Tuple[pytelicam.pytelicam.CameraDevice, pytelicam.pytelicam.SignalHandle]:
        ignore_config_list = ["serial_number", "model_number"]
        cam_device = self.cam_system.create_device_object_from_info(
            serial_num, model, "")

        cam_device.open()
        # res = cam_device.genapi.set_enum_str_value("ExposureMode","Timed")
        # res = cam_device.genapi.set_enum_str_value("ExposureAuto","Off")
        # 設定された項目の一覧とその値のペアのリストを取得
        for key, value in self.config.items(camera_section):
            if not key in ignore_config_list:
                setting_result = cam_device.genapi.set_feature_value(
                    key, value)
                if int(setting_result):
                    print(f"""カメラの設定でエラーです コマンド : {key}={value} \
                          エラーコード : {setting_result} \
                           メッセージ : {cam_device.get_last_genicam_error()} """)

        res = cam_device.genapi.set_enum_str_value('TriggerMode', 'Off')
        if res != pytelicam.CamApiStatus.Success:
            raise Exception("Can't set TriggerMode.")

        res = cam_device.genapi.set_enum_str_value('TriggerSource', 'Software')
        if res != pytelicam.CamApiStatus.Success:
            raise Exception("Can't set TriggerSource.")

        # res = cam_device.genapi.set_enum_str_value(
        #     'TriggerSequence', 'TriggerSequence0')
        receive_signal = self.cam_system.create_signal()

        # ここより前に設定を書くと間違いない？
        cam_device.cam_stream.open(receive_signal)
        return cam_device, receive_signal

    def take_picture(self, kensamei: InspectionType, base_directory: str, is_test_snapshot=False) -> str:
        if self.cam_system == None:
            return "era"

        PREPROCESS_PICTURE_FILENAME = "PREPROCESS_ORIGINAL.png"
        ACCURACT_PICTURE_FILENAME = "ACCURACY_ORIGINAL.png"
        TEST_TOOL_PICTURE_FILENAME = "TOOL_ORIGINAL.png"

        try:
            if kensamei == InspectionType.TOOL_INSPECTION:
                if not USE_TOOL_INSPECTION_CAMERA:
                    raise Exception("カメラを使わない設定になっています", kensamei)
                np_arr = self._get_image_data(
                    self.cam_device_tool,  self.receive_signal_tool)
                if is_test_snapshot:
                    save_path = os.path.join(
                        base_directory, ("a"if self.toggle_flag else "b") + TEST_TOOL_PICTURE_FILENAME)
                else:
                    save_path = os.path.join(
                        base_directory, dt.datetime.now().strftime('%Y/%m/%d/%H_%M_%S.png'))
                directory = os.path.dirname(save_path)
                if not os.path.exists(directory):
                    os.makedirs(directory)

            elif kensamei == InspectionType.PRE_PROCESSING_INSPECTION:
                if not USE_PRE_PROCESSING_INSPECTION_CAMERA:
                    raise Exception("カメラを使わない設定になっています", kensamei)
                np_arr = self._get_image_data(
                    self.cam_device_kakou,  self.receive_signal_kakou)
                save_path = os.path.join(
                    base_directory, ("a"if self.toggle_flag else "b")+PREPROCESS_PICTURE_FILENAME)

            elif kensamei == InspectionType.ACCURACY_INSPECTION:
                if not USE_ACCURACY_INSPECTION_CAMERA:
                    raise Exception("カメラを使わない設定になっています", kensamei)
                np_arr = self._get_image_data(
                    self.cam_device_seido,  self.receive_signal_seido)
                save_path = os.path.join(
                    base_directory, ("a"if self.toggle_flag else "b")+ACCURACT_PICTURE_FILENAME)
                directory = os.path.dirname(save_path)
                if not os.path.exists(directory):
                    os.makedirs(directory)
            self.toggle_flag = not self.toggle_flag
            if not cv2.imwrite(save_path, np_arr):
                print("hosonFailed")
                return None
        except Exception as e:
            print("カメラ撮影でエラーです", e)
            return None

        return save_path

    def check_camera_connection(self) -> bool:
        if not self.cam_system:
            return False

        if USE_PRE_PROCESSING_INSPECTION_CAMERA:
            if not (self.cam_device_kakou and self.cam_device_kakou.cam_stream.is_open):
                return False
            if not (self.cam_device_kakou and self.cam_device_kakou.is_open):
                return False

        if USE_TOOL_INSPECTION_CAMERA:
            if not (self.cam_device_tool and self.cam_device_tool.cam_stream.is_open):
                return False
            if not (self.cam_device_tool and self.cam_device_tool.is_open):
                return False

        if USE_ACCURACY_INSPECTION_CAMERA:
            if not (self.cam_device_seido and self.cam_device_seido.cam_stream.is_open):
                return False
            if not (self.cam_device_seido and self.cam_device_seido.is_open):
                return False

        return True

    def _initial_cam_setting(self, cam_num=3) -> pytelicam.pytelicam.CameraSystem:
        cam_system = pytelicam.get_camera_system(
            int(pytelicam.CameraType.U3v) |
            int(pytelicam.CameraType.Gev))
        find_cam_num = cam_system.get_num_of_cameras()
        if find_cam_num != cam_num:
            print(f"Camera number is{find_cam_num}")
            return None
        return cam_system

    def _get_image_data(self, cam_device,  receive_signal) -> np.ndarray:

        cam_device.cam_stream.start()
        with cam_device.cam_stream.get_next_image() as image_data:
            if image_data.status != pytelicam.CamApiStatus.Success:
                print('Grab error! status = {0}'.format(image_data.status))
                return
            else:
                return image_data.get_ndarray(pytelicam.OutputImageType.Bgr24)

    def close(self):

        if USE_PRE_PROCESSING_INSPECTION_CAMERA:
            if self.cam_device_kakou and self.cam_device_kakou.cam_stream.is_open:
                self.cam_device_kakou.cam_stream.stop()
                self.cam_device_kakou.cam_stream.close()

            if self.cam_device_kakou and self.cam_device_kakou.is_open:
                self.cam_device_kakou.close()

            if self.receive_signal_kakou:
                self.cam_system.close_signal(self.receive_signal_kakou)

        if USE_TOOL_INSPECTION_CAMERA:
            if self.cam_device_tool and self.cam_device_tool.cam_stream.is_open:
                self.cam_device_tool.cam_stream.stop()
                self.cam_device_tool.cam_stream.close()

                if self.cam_device_tool and self.cam_device_tool.is_open:
                    self.cam_device_tool.close()

                if self.receive_signal_tool:
                    self.cam_system.close_signal(self.receive_signal_tool)

        if USE_ACCURACY_INSPECTION_CAMERA:
            if self.cam_device_seido and self.cam_device_seido.cam_stream.is_open:
                self.cam_device_seido.cam_stream.stop()
                self.cam_device_seido.cam_stream.close()

            if self.cam_device_seido and self.cam_device_seido.is_open:
                self.cam_device_seido.close()

            if self.receive_signal_seido:
                self.cam_system.close_signal(self.receive_signal_seido)

        self.cam_system.terminate()
