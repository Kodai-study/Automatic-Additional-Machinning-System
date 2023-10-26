# 工具検査のデータクラス
from ast import List
from ctypes import Union
from dataclasses import dataclass

from ImageInspectionController.ProcessDatas import HoleCheckInfo, ToolType


@dataclass
class ToolInspectionResult:
    """
    ツール検査の結果を格納するデータクラス
    """

    result: bool
    """
    不合格か否かを表す
    """
    error_items: Union[None, str]
    """
    不合格や検査エラーの項目を格納する\n
    合格出会った場合はNoneとなる
    """
    tool_type: ToolType
    """
    ツールの種類を判別して返す
    """
    tool_length: float
    """
    検査したツールの長さを返す
    """
    drill_diameter: float
    """
    検査によって出てきたドリルの直径。
    検査結果には直接関係しない
    """
# 加工前検査のデータクラス


@dataclass
class PreProcessingInspectionResult:
    """
    加工前検査の結果を格納するデータクラス
    """
    result: bool
    """
    検査結果の合否
    """
    error_items: Union[None, List[str]]
    """
    不合格や検査エラーの項目を格納する\n
    合格出会った場合はNoneとなる
    """
    serial_number: int
    """"""
    dimensions: float
    """
    実際に検査したワークの大きさ
    """
# 精度検査のデータクラス


@dataclass
class AccuracyInspectionResult:
    """
    加工穴の精度検査の結果を格納するデータクラス
    """
    result: bool
    """
    検査結果の合否
    """
    error_items: Union[None, List[str]]
    """
    不合格や検査エラーの項目を格納する\n
    合格出会った場合はNoneとなる
    """
    hole_result: List[HoleCheckInfo]
    """
    各穴の検査結果を格納する
    """