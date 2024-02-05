# coding: utf-8

from ImageInspectionController.AccuracyInspection import AccuracyInspection
from ImageInspectionController.OperationType import OperationType
from ImageInspectionController.InspectDatas import PreProcessingInspectionData, ToolInspectionData
from ImageInspectionController.InspectionResults import AccuracyInspectionResult, CameraControlResult, LightningControlResult, PreProcessingInspectionResult, ToolInspectionResult
from ImageInspectionController.light import Light
from ImageInspectionController.PreProcessInspection import PreProcessInspection
from ImageInspectionController.ProcessDatas import HoleCheckInfo, InspectionType
from ImageInspectionController.Taking import Taking
from common_data_type import CameraType, LightingType
from typing import Tuple, Union, List

camera_type_dict = {
    InspectionType.TOOL_INSPECTION: CameraType.TOOL_CAMERA,
    InspectionType.ACCURACY_INSPECTION: CameraType.ACCURACY_CAMERA,
    InspectionType.PRE_PROCESSING_INSPECTION: CameraType.PRE_PROCESSING_CAMERA
}


def get_inspectionType_with_camera(camera_type: CameraType) -> InspectionType:
    for key, value in camera_type_dict.items():
        if value == camera_type:
            return key


class ImageInspectionController:

    def __init__(self):
        self.taking = Taking()
        self.lighting = Light()
        self.pre_process_inspection = PreProcessInspection()
        self.accuracy_inspection = AccuracyInspection()

    def _take_inspection_snapshot(self, camera_type):
        inspection_type = get_inspectionType_with_camera(camera_type)
        img_pass = self.taking.take_picuture(inspection_type)

        if img_pass is None:
            return CameraControlResult(is_success=False, camera_type=camera_type, image_path=None)

        return CameraControlResult(is_success=True, camera_type=camera_type, image_path=img_pass)

    def perform_image_operation(self, operation_type: OperationType, inspection_data: Union[PreProcessingInspectionData, ToolInspectionData, List[HoleCheckInfo], Tuple[LightingType, bool], List[CameraType]]) \
            -> Union[PreProcessingInspectionResult, ToolInspectionResult, List[HoleCheckInfo], LightningControlResult, CameraControlResult]:
        """
        画像検査を行って、結果を返す関数。
        Args:
            inspection_type (OperationType): 画像検査モジュールに送る命令の種類の列挙型\n
            inspection_data (Union[PreProcessingInspectionData, ToolInspectionData, List[HoleCheckInfo]]): 検査に必要なデータ。検査の種類によってデータの型が異なる

        Returns:
            Union[PreProcessingInspectionResult, ToolInspectionResult, List[HoleCheckInfo]]: 検査の結果。合否と、検査で出された様々な値。検査の種類によって型が異なる
        """
        if operation_type == OperationType.TAKE_INSPECTION_SNAPSHOT:
            request_result = [self._take_inspection_snapshot(
                camera_type) for camera_type in inspection_data]
            return request_result

        elif operation_type == OperationType.CONTROL_LIGHTING:
            lightning_type, is_on = inspection_data
            lightning_control_result = self.lighting.light_on(
                lightning_type, is_on)
            if lightning_control_result == "OK":
                return LightningControlResult(is_success=True, lighting_type=lightning_type, lighting_state=is_on)
            else:
                return LightningControlResult(is_success=False, lighting_type=lightning_type, lighting_state=not is_on)

        elif operation_type == OperationType.PRE_PROCESSING_INSPECTION:
            img_pass = self.taking.take_picuture(
                InspectionType.PRE_PROCESSING_INSPECTION)
            kekka = self.pre_process_inspection.exec_inspection(
                img_pass, inspection_data)
        elif operation_type == OperationType.ACCURACY_INSPECTION:
            img_pass = self.taking.take_picuture(
                InspectionType.ACCURACY_INSPECTION)
            img_pass = "ImageInspectionController/test/accuracy_inspection/sample_images/multi_type_EXP500.png"
            self.accuracy_inspection.exec_inspection(
                img_pass, inspection_data)
            kekka = (img_pass)
        elif operation_type == OperationType.TOOL_INSPECTION:
            img_pass = self.taking.take_picuture(
                InspectionType.TOOL_INSPECTION)
            kekka = (img_pass)

        return kekka
