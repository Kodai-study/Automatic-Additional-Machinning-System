# coding: utf-8
from ImageInspectionController.AccuracyInspection import AccuracyInspection
from test_flags import TEST_CFD_CONNECTION_LOCAL, TEST_UR_CONNECTION_LOCAL, TEST_FEATURE_GUI, TEST_FEATURE_IMAGE_PROCESSING
if TEST_FEATURE_IMAGE_PROCESSING:
    from ImageInspectionController.light import Light
    from ImageInspectionController.Taking import Taking
from ImageInspectionController.OperationType import OperationType
from ImageInspectionController.ProcessDatas import HoleCheckInfo, InspectionType
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

light_to_inspect_dict = {
    LightingType.ACCURACY_LIGHTING: InspectionType.ACCURACY_INSPECTION,
    LightingType.PRE_PROCESSING_LIGHTING: InspectionType.PRE_PROCESSING_INSPECTION,
    LightingType.TOOL_LIGHTING: InspectionType.TOOL_INSPECTION
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
        img_pass = self.taking.take_picture(inspection_type)

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
        if not TEST_FEATURE_IMAGE_PROCESSING:
            return

        if operation_type == OperationType.TAKE_INSPECTION_SNAPSHOT:
            request_result = [self._take_inspection_snapshot(
                camera_type) for camera_type in inspection_data]
            return request_result

        elif operation_type == OperationType.CONTROL_LIGHTING:
            lightning_type, is_on = inspection_data
            lightning_control_result = self.lighting.light_onoff(
                light_to_inspect_dict[lightning_type], "ON" if is_on else "OFF")
            if lightning_control_result == "OK":
                return LightningControlResult(is_success=True, lighting_type=lightning_type, lighting_state=is_on)
            else:
                return LightningControlResult(is_success=False, lighting_type=lightning_type, lighting_state=not is_on)

        elif operation_type == OperationType.PRE_PROCESSING_INSPECTION:
            lighting_return_code = self.lighting.light_onoff(
                InspectionType.PRE_PROCESSING_INSPECTION, "ON")
            if lighting_return_code != "OK":
                return PreProcessingInspectionResult(is_check_ok=False, error_message=["照明の点灯に失敗しました。"], serial_number=None, dimensions=None)

            img_pass = self.taking.take_picture(
                InspectionType.PRE_PROCESSING_INSPECTION)

            lighting_return_code = self.lighting.light_onoff(
                InspectionType.PRE_PROCESSING_INSPECTION, "OFF")
            if lighting_return_code != "OK":
                lighting_return_code = self.lighting.light_onoff(
                    InspectionType.PRE_PROCESSING_INSPECTION, "OFF")
            kekka = self.pre_process_inspection.exec_inspection(
                img_pass, inspection_data)

        elif operation_type == OperationType.ACCURACY_INSPECTION:
            lighting_return_code = self.lighting.light_onoff(
                InspectionType.ACCURACY_INSPECTION, "ON")
            if lighting_return_code != "OK":
                return AccuracyInspectionResult(result=False, error_items=["照明の点灯に失敗しました。"], hole_result=None)

            img_pass = self.taking.take_picture(
                InspectionType.ACCURACY_INSPECTION)

            lighting_return_code = self.lighting.light_onoff(
                InspectionType.ACCURACY_INSPECTION, "OFF")
            if lighting_return_code != "OK":
                lighting_return_code = self.lighting.light_onoff(
                    InspectionType.ACCURACY_INSPECTION, "OFF")

            kekka = self.accuracy_inspection.exec_inspection(
                img_pass, inspection_data)

        elif operation_type == OperationType.TOOL_INSPECTION:
            lighting_return_code = self.lighting.light_onoff(
                InspectionType.TOOL_INSPECTION, "ON")
            if lighting_return_code != "OK":
                return ToolInspectionResult(result=False, error_items=["照明の点灯に失敗しました。"],
                                            tool_type=None, tool_length=None, drill_diameter=None)

            img_pass = self.taking.take_picture(
                InspectionType.TOOL_INSPECTION)

            lighting_return_code = self.lighting.light_onoff(
                InspectionType.TOOL_INSPECTION, "OFF")
            if lighting_return_code != "OK":
                lighting_return_code = self.lighting.light_onoff(
                    InspectionType.TOOL_INSPECTION, "OFF")
            kekka = (img_pass)

        return kekka
