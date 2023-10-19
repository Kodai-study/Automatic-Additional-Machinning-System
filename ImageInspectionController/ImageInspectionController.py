# coding: utf-8

from common_data_type import *
from typing import Union, List


class ImageInspectionController:

    def __init__(self):
        pass

    def perform_image_inspection(self, inspection_type: InspectionType, inspection_data: Union[PreProcessingInspectionData, ToolInspectionData, List[HoleCheckInfo]]):
        """
        画像検査を行って、結果を返す関数。

        Args:
            inspection_type (InspectionType): 画像検査の種類の列挙型\n
            inspection_data (Union[PreProcessingInspectionData, WorkPieceShape, List[HoleCheckInfo]]): 検査に必要なデータ。検査の種類によってデータの型が異なる
        """
        pass

