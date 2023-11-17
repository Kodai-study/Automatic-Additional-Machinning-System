from dataclasses import dataclass
from datetime import timedelta, datetime

from common_data_type import WorkPieceShape


@dataclass
class ProcessingData:
    """
    加工データのデータクラス
    GUIスレッドとこのリストを共有する。
    """
    model_id: int
    """
    データベースの型番に紐づけられたID
    """
    model_number: str
    """
    型番の名前
    """
    average_processing_time: timedelta
    """
    その型番の平均加工時間。 
    """
    work_shape: WorkPieceShape
    """
    ワークの形状
    """
    workpiece_dimension: float
    """
    ワークの大きさ。 円の場合は直径、正方形の場合は一辺の長さ
    """
    created_by: str
    """
    このデータを作成した人の名前
    """
    creation_timestamp: datetime
    """
    このデータを作成した日時
    """
