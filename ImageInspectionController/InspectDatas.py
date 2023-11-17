
from dataclasses import dataclass

from common_data_type import WorkPieceShape


@dataclass
class ToolInspectionData:
    """
    工具検査を行うときに必要な情報を格納するデータクラス
    """
    is_initial_phase: bool
    """
    検査が1回目で、工具の種類と長さを登録する段階かどうか
    True:共有変数のリストに、種類と長さを登録する
    False:リストの項目と比べ、工具が破損していないかどうかを判断する
    """
    tool_position_number: int
    """
    検査・登録を行う工具のストッカの位置番号
    (ストッカに記述されている番号)
    """


@dataclass
class PreProcessingInspectionData:
    """
    加工前検査を行うときに必要な情報を格納するデータクラス\n
    検査を行うときには引数として渡し、このインスタンスと比較して合否を出す
    """
    workpiece_shape: WorkPieceShape
    """
    ワークの形。
    """
    work_dimension: float
    """
    ワークの大きさ。この大きさと比較して合否を出す\n
    ・正方形の場合:1辺の長さ\n
    ・円の場合:直径
    """
