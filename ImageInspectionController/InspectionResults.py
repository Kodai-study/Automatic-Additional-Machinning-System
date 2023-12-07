from dataclasses import dataclass

from ImageInspectionController.ProcessDatas import HoleCheckInfo
from common_data_type import CameraType, LightingType, ToolType
from typing import Union, List


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


@dataclass
class LightningControlResult:
    """
    照明のON/OFF操作の結果を格納するデータクラス
    """
    is_success: bool
    """
    操作が成功したかどうか
    """
    lighting_type: LightingType
    """
    操作した照明の種類
    """
    lighting_state: bool
    """
    操作によって変化した後の照明の状態(ON/OFF)\n
    操作が失敗してそのままの場合は、変化前の状態が入ってくることになる
    """


@dataclass
class CameraControlResult:
    """
    検査カメラの画像撮影の結果を格納するデータクラス\n
    カメラごとに結果を返す
    """
    is_success: bool
    """
    撮影とファイル保存が成功したかどうか
    """
    camera_type: CameraType
    """
    撮影したカメラの種類
    """
    image_path: str
    """
    撮影後の画像の保存先のパス
    """
