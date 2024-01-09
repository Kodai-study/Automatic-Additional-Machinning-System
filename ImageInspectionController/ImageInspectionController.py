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
from common_data_type import CameraType, LightingType,ToolType
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
            return self._test_return_inspection_result(operation_type, inspection_data)

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
    
    
    def _test_return_inspection_result(self,operation_type: OperationType, inspection_data):
        
        if (operation_type == OperationType.PRE_PROCESSING_INSPECTION):
            return self._test_pass_preprocessing()

        elif (operation_type == OperationType.TOOL_INSPECTION):
            return self._test_pass_TOOL_INSPECTION(inspection_data)

        elif (operation_type == OperationType.ACCURACY_INSPECTION):
            return self._test_pass_accuracy_inspection()

        elif (operation_type == OperationType.CONTROL_LIGHTING):
            return self._test_pass_control_lighting()

        elif (operation_type == OperationType.TAKE_INSPECTION_SNAPSHOT):
            return self._test_pass_take_inspection_snapshot()

    def _test_pass_preprocessing(self):
        return PreProcessingInspectionResult(result=True, error_items=None, serial_number=0, dimensions=30.0)

    def _test_fail_preprocessing(self):
        return PreProcessingInspectionResult(result=False, error_items=["ワークの大きさが一致していません", "QRコードの読み取りに失敗しました"], serial_number=None, dimensions=28.0)

    def _test_pass_TOOL_INSPECTION(self, inspection_data: ToolInspectionData = None, return_tool_type: ToolType = ToolType.M3_DRILL, tool_length: float = 10.0, drill_diameter: float = 3.0):
        return ToolInspectionResult(result=True, error_items=None, tool_type=return_tool_type, tool_length=tool_length, drill_diameter=drill_diameter)

    def _test_fail_TOOL_INSPECTION(self, inspection_data: ToolInspectionData = None, return_tool_type: ToolType = ToolType.M3_DRILL, tool_length: float = 10.0, drill_diameter: float = 3.0):
        return ToolInspectionResult(result=False, error_items=["工具の種類が一致していません", "工具の長さが一致していません"], tool_type=return_tool_type, tool_length=tool_length, drill_diameter=drill_diameter)

    def _test_pass_accuracy_inspection(self):
        holecheck_list = [HoleCheckInfo(hole_id=1, hole_position=Point(
            50.0, 50.0), hole_type=HoleType.M3_HOLE, hole_check_info=True)]
        holecheck_list.append(HoleCheckInfo(hole_id=2, hole_position=Point(
            60.0, 60.0), hole_type=HoleType.M3_HOLE, hole_check_info=True))

        return AccuracyInspectionResult(result=True, error_items=None, hole_result=holecheck_list)

    def _test_fail_accuracy_inspection(self):
        holecheck_list = [HoleCheckInfo(hole_id=1, hole_position=Point(
            55.0, 55.0), hole_type=HoleType.M3_HOLE, hole_check_info=True)]
        holecheck_list.append(HoleCheckInfo(hole_id=2, hole_position=Point(
            65.0, 65.0), hole_type=HoleType.M4_HOLE, hole_check_info=False))

        return AccuracyInspectionResult(result=False, error_items=["穴の位置が一致していません", "穴の種類が一致していません"], hole_check_infos=holecheck_list)

    def _test_pass_control_lighting(self, lighting_type: LightingType = LightingType.ACCURACY_LIGHTING):
        return LightningControlResult(result=True,  lighting_type=lighting_type, lighting_state=True)

    def _test_fail_control_lighting(self, lighting_type: LightingType = LightingType.ACCURACY_LIGHTING):
        return LightningControlResult(is_success=False,  lighting_type=lighting_type, lighting_state=False)

    def _test_pass_take_inspection_snapshot(self, camera_type: CameraType = CameraType.ACCURACY_CAMERA):
        return CameraControlResult(is_success=True, camera_type=camera_type, image_path="../test/inspection_image.png")

    def _test_fail_take_inspection_snapshot(self, camera_type: CameraType = CameraType.ACCURACY_CAMERA):
        return CameraControlResult(result=False, camera_type=camera_type, image_path=None)

