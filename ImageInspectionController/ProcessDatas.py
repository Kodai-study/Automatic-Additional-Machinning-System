from dataclasses import dataclass
from enum import Enum, auto

from common_data_type import Point, ToolType


class HoleType(Enum):
    """
    穴の種類を表す列挙型
    """
    M2_HOLE = auto()
    M3_HOLE = auto()
    M4_HOLE = auto()
    M5_HOLE = auto()
    M6_HOLE = auto()
    M7_HOLE = auto()
    M8_HOLE = auto()


@dataclass
class HoleCheckInfo:
    """
    加工穴のデータを格納するデータクラス\n
    """
    hole_id: int
    """
    どの穴かを識別するID   加工の順番とは関係なく、
    加工データファイル、検査時にのみ有効
    """
    hole_position: Point
    """
    加工穴の座標\n
    データを渡すときには、加工穴の座標であり
    検査結果を格納するときには、実際の座標である
    """

    hole_type: HoleType
    """
    加工穴の種類
    穴の大きさを判別する
    """

    hole_check_info: bool = None
    """
    チェックが通ったかどうかを表す\n
    渡されるときはNoneになっており、検査結果を格納するときにTrue/Falseになる
    """


@dataclass
class ToolsInfo:
    """
    工具の情報を格納するデータクラス。
    """
    stock_position_number: int
    """
    工具が入っているストッカの位置番号\n
    (ストッカに記述されている番号と一致する)
    """
    tool_type: ToolType
    """
    工具の種類  穴径:ドリルorタップ
    """
    tool_length: float
    """
    ツールの長さ 検査した値
    """
class InspectionType(Enum):
    ACCURACY_INSPECTION = auto(),
    PRE_PROCESSING_INSPECTION = auto(),
    TOOL_INSPECTION = auto()