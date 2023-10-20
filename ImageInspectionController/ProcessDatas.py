from dataclasses import dataclass
from enum import Enum, auto

from common_data_type import Point


class ToolType(Enum):
    """
    工具の種類を表す列挙型
    ストッカに、この中のいずれかの工具が入っている
    """
    M2_DRILL = auto()
    M3_DRILL = auto()
    M4_DRILL = auto()
    M5_DRILL = auto()
    M6_DRILL = auto()
    M7_DRILL = auto()
    M8_DRILL = auto()
    M2_TAP = auto()
    M3_TAP = auto()
    M4_TAP = auto()
    M5_TAP = auto()
    M6_TAP = auto()
    M7_TAP = auto()
    M8_TAP = auto()


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
    hole_check_info: bool
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
