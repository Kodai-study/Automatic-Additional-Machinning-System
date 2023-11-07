# coding: utf-8

from threading import Lock
import time
from ImageInspectionController.OperationType import OperationType
from ImageInspectionController.InspectDatas import PreProcessingInspectionData, ToolInspectionData
from ImageInspectionController.InspectionResults import AccuracyInspectionResult, CameraControlResult, LightningControlResult, PreProcessingInspectionResult, ToolInspectionResult
from ImageInspectionController.ProcessDatas import HoleCheckInfo, HoleType
from common_data_type import CameraType, LightingType, Point, ToolType
from typing import Tuple, Union, List


class ImageInspectionController:

    def __init__(self):
        self.thread_lock = Lock()

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
        with self.thread_lock:
            time.sleep(5)
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

    def _test_pass_preprocessing(self, serial_number: int = 123):
        return PreProcessingInspectionResult(result=True, error_items=None, serial_number=serial_number, dimensions=30.0)

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
        return CameraControlResult(result=True, camera_type=camera_type, image_path="../test/inspection_image.png")

    def _test_fail_take_inspection_snapshot(self, camera_type: CameraType = CameraType.ACCURACY_CAMERA):
        return CameraControlResult(result=False, camera_type=camera_type, image_path=None)
