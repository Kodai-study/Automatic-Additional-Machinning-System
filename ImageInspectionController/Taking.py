#
# grab_software_trigger_ndarray.py (for Python 3)
#
# Copyright (c) 2020 Toshiba-Teli Corporation
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
#

import sys
from typing import Tuple
import numpy as np
import pytelicam
import yaml
import cv2
from ImageInspectionController.ProcessDatas import InspectionType
from ImageInspectionController.light import Light


class Taking:
    def __init__(self):
        self.light = Light()
        file_path = 'ImageInspectionController/kensa_config.yaml'
        with open(file_path, 'r') as yaml_file:
            self.data = yaml.safe_load(yaml_file)
        self.cam_system = self.initial_cam_setting(1)

        self.cam_device_tool, self.receive_signal_tool = self._get_camera_device(
            "TOOL_INSPECTION")
        self.cam_device_kakou, self.receive_signal_kakou = self._get_camera_device(
            "PRE_PROCESSING_INSPECTION")
        self.cam_device_seido, self.receive_signal_seido = self._get_camera_device(
            "ACCURACY_INSPECTION")

    def _get_camera_device(self, camera_type: str):
        serial_number, model_number = self._get_serial_and_model(camera_type)
        return self.setting_cam(
            serial_number, model_number, self.cam_system)

    def _get_serial_and_model(self, camera_type: str):
        setting_data = self.data['Camera_information'][camera_type]
        return setting_data['serial_number'], setting_data['model_number']

    def take_picuture(self, kensamei: InspectionType) -> str:
        self.light.light_onoff(kensamei)

        if kensamei == InspectionType.TOOL_INSPECTION:
            np_arr = self.take_picture(
                self.cam_device_tool, self.cam_system, self.receive_signal_tool)
        if kensamei == InspectionType.PRE_PROCESSING_INSPECTION:
            np_arr = self.take_picture(
                self.cam_device_kakou, self.cam_system, self.receive_signal_kakou)
        if kensamei == InspectionType.ACCURACY_INSPECTION:
            np_arr = self.take_picture(
                self.cam_device_seido, self.cam_system, self.receive_signal_seido)

        cv2.imwrite('img/grayscale_image.png', np_arr)
        return 'img/grayscale_image.png'

    def initial_cam_setting(self, cam_num=3) -> pytelicam.pytelicam.CameraSystem:
        cam_system = pytelicam.get_camera_system(
            int(pytelicam.CameraType.U3v) |
            int(pytelicam.CameraType.Gev))
        find_cam_num = cam_system.get_num_of_cameras()
        if find_cam_num != cam_num:
            print('Camera number is No')
            return None
        return cam_system

    def setting_cam(self, serial_num: str, model: str, cam_system: pytelicam.pytelicam.CameraSystem)\
            -> Tuple[pytelicam.pytelicam.CameraDevice, pytelicam.pytelicam.SignalHandle]:
        cam_device = cam_system.create_device_object_from_info(
            serial_num, model, "")
        cam_device.open()

        res = cam_device.genapi.set_enum_str_value('TriggerMode', 'On')
        if res != pytelicam.CamApiStatus.Success:
            raise Exception("Can't set TriggerMode.")

        res = cam_device.genapi.set_enum_str_value('TriggerSource', 'Software')
        if res != pytelicam.CamApiStatus.Success:
            raise Exception("Can't set TriggerSource.")

        res = cam_device.genapi.set_enum_str_value(
            'TriggerSequence', 'TriggerSequence0')
        receive_signal = cam_system.create_signal()

        cam_device.cam_stream.open(receive_signal)
        return cam_device, receive_signal

    def take_picture(self, cam_device, cam_system, receive_signal) -> np.ndarray:

        cam_device.cam_stream.start()

        res = cam_device.genapi.execute_command('TriggerSoftware')
        if res != pytelicam.CamApiStatus.Success:
            raise Exception("Can't execute TriggerSoftware.")

        res = cam_system.wait_for_signal(receive_signal)
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
