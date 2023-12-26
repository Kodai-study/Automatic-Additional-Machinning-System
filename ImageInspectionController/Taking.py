
# grab_software_trigger_ndarray.py (for Python 3)
#
# Copyright (c) 2020 Toshiba-Teli Corporation
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
#

import configparser
from typing import Tuple
import numpy as np
import pytelicam
import yaml
import cv2
from ImageInspectionController.ProcessDatas import InspectionType
from ImageInspectionController.light import Light

NUM_REQUIRED_CAMERAS = 3
USE_TOOL_INSPECTION_CAMERA = True
USE_PRE_PROCESSING_INSPECTION_CAMERA = True
USE_ACCURACY_INSPECTION_CAMERA = True


class Taking:
    def __init__(self):
        self.config = configparser.ConfigParser()
        file_path = 'kensa.conf'
        # with open(file_path, 'r') as yaml_file:
        #     self.data = yaml.safe_load(yaml_file)
        self.cam_system = self._initial_cam_setting(NUM_REQUIRED_CAMERAS)
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
                serial_number, model_number)
        except configparser.NoSectionError:
            raise ValueError(f"指定されたセクションが存在しません: {section_name}")

    def _get_serial_and_model(self, inspection_type: str):
        section_name = f"{inspection_type}"
        serial_number = self.config.get(section_name, "serial_number")
        model_number = self.config.get(section_name, "model_number")
        return serial_number, model_number, section_name
    # def _get_camera_device(self, camera_type: str):
    #     serial_number, model_number = self._get_serial_and_model(camera_type)
    #     return self._setting_cam(
    #         serial_number, model_number)

    # def _get_serial_and_model(self, camera_type: str):
    #     setting_data = self.data['Camera_information'][camera_type]
    #     return setting_data['serial_number'], setting_data['model_number']

    def _setting_cam(self, serial_num: str, model: str)\
            -> Tuple[pytelicam.pytelicam.CameraDevice, pytelicam.pytelicam.SignalHandle]:
          
        cam_device = self.cam_system.create_device_object_from_info(
            serial_num, model, "")
        cam_device.open()

        # 設定された項目の一覧とその値のペアのリストを取得
        sections = self.config.sections()
        # 1項目ずつ処理
        for section in sections:
            print(f"Section: {section}")
            for key, value in self.config.items(section):
                print(f"{key} = {value}")
                if serial_num == value:
                    Width = self.config.get(section, "Width")
                    OffsetX = self.config.get(section, "OffsetX")
                    OffsetY = self.config.get(section, "OffsetY")     
                    cam_device.genapi.set_feature_value("Width",Width)
                    cam_device.genapi.set_feature_value("OffsetX",OffsetX)
                    cam_device.genapi.set_feature_value("OffsetY",OffsetY)                                   
            print("\n")

        res = cam_device.genapi.set_enum_str_value('TriggerMode', 'On')
        if res != pytelicam.CamApiStatus.Success:
            raise Exception("Can't set TriggerMode.")

        res = cam_device.genapi.set_enum_str_value('TriggerSource', 'Software')
        if res != pytelicam.CamApiStatus.Success:
            raise Exception("Can't set TriggerSource.")

        res = cam_device.genapi.set_enum_str_value(
            'TriggerSequence', 'TriggerSequence0')
        receive_signal = self.cam_system.create_signal()


        # ここより前に設定を書くと間違いない？
        cam_device.cam_stream.open(receive_signal)
        return cam_device, receive_signal

    def take_picture(self, kensamei: InspectionType) -> str:
        if self.cam_system == None:
            return "era"
        # self.light.light_onoff(kensamei)
        image_file_name = None
        if kensamei == InspectionType.TOOL_INSPECTION:
            np_arr = self._get_image_data(
                self.cam_device_tool,  self.receive_signal_tool)

            image_file_name = "a.png" if self.toggle_flag else "a_2.png"
        elif kensamei == InspectionType.PRE_PROCESSING_INSPECTION:
            np_arr = self._get_image_data(
                self.cam_device_kakou,  self.receive_signal_kakou)
            image_file_name = "b.png" if self.toggle_flag else "b_2.png"

        elif kensamei == InspectionType.ACCURACY_INSPECTION:
            np_arr = self._get_image_data(
                self.cam_device_seido,  self.receive_signal_seido)
            image_file_name = "c.png" if self.toggle_flag else "c_2.png"

        self.toggle_flag = not self.toggle_flag
        write_image_path = f"/home/kuga/img/{image_file_name}"
        if not cv2.imwrite(write_image_path, np_arr):
            print("hosonFailed")

        return write_image_path

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
            print('Camera number is No')
            return None
        return cam_system

    def _get_image_data(self, cam_device,  receive_signal) -> np.ndarray:

        cam_device.cam_stream.start()

        res = cam_device.genapi.execute_command('TriggerSoftware')

        if res != pytelicam.CamApiStatus.Success:
            raise Exception("Can't execute TriggerSoftware.")

        res = self.cam_system.wait_for_signal(receive_signal)
        if res != pytelicam.CamApiStatus.Success:
            print('Grab error! status = {0}'.format(res))
            return
        else:
            with cam_device.cam_stream.get_current_buffered_image() as image_data:
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
