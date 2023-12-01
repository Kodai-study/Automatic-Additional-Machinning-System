# coding: utf-8

from ImageInspectionController.OperationType import OperationType
from ImageInspectionController.InspectDatas import PreProcessingInspectionData, ToolInspectionData
from ImageInspectionController.InspectionResults import CameraControlResult, LightningControlResult, PreProcessingInspectionResult, ToolInspectionResult
from ImageInspectionController.pre_PROCESSING_INSPECTION import process_qr_code
from ImageInspectionController.ProcessDatas import HoleCheckInfo, InspectionType
from ImageInspectionController.Taking import Taking
from common_data_type import CameraType, LightingType
from typing import Tuple, Union, List


class ImageInspectionController:

    def __init__(self):
        self.taking = Taking()

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
        if operation_type==OperationType.PRE_PROCESSING_INSPECTION:
            img_pass = self.taking.take_picuture(InspectionType.PRE_PROCESSING_INSPECTION)
            kekka = process_qr_code(img_pass)
        if operation_type==OperationType.ACCURACY_INSPECTION:
            img_pass = self.taking.take_picuture(InspectionType.ACCURACY_INSPECTION)
            kekka = (img_pass)
        return kekka 
    
    def test(kensamei:InspectionType):
        img_pass=Taking.take_picuture(kensamei)
        
        return img_pass       
    
     
