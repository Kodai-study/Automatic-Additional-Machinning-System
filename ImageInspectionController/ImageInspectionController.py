# coding: utf-8
from test_flags import TEST_CFD_CONNECTION_LOCAL, TEST_UR_CONNECTION_LOCAL, TEST_FEATURE_GUI, TEST_FEATURE_IMAGE_PROCESSING
if TEST_FEATURE_IMAGE_PROCESSING:
    from ImageInspectionController.light import Light
    from ImageInspectionController.pre_processing_inspection import process_qr_code
    from ImageInspectionController.Taking import Taking
from ImageInspectionController.OperationType import OperationType
from ImageInspectionController.ProcessDatas import HoleCheckInfo, InspectionType
from ImageInspectionController.InspectDatas import PreProcessingInspectionData, ToolInspectionData
from ImageInspectionController.InspectionResults import CameraControlResult, LightningControlResult, PreProcessingInspectionResult, ToolInspectionResult
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
        if TEST_FEATURE_IMAGE_PROCESSING:
            self.taking = Taking()
            self.lighting = Light()

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
            img_pass = self.taking.take_picuture(
                InspectionType.PRE_PROCESSING_INSPECTION)
            kekka = process_qr_code(img_pass)
        elif operation_type == OperationType.ACCURACY_INSPECTION:
            img_pass = self.taking.take_picuture(
                InspectionType.ACCURACY_INSPECTION)
            kekka = (img_pass)
        elif operation_type == OperationType.TOOL_INSPECTION:
            img_pass = self.taking.take_picuture(
                InspectionType.TOOL_INSPECTION)
            kekka = (img_pass)

        return kekka
