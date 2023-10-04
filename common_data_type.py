# coding: utf-8
from typing import List, Union
from enum import Enum, auto
from dataclasses import dataclass


class InspectionType(Enum):
    """
    画像検査の種類を表す列挙型   
    ImageInspectionController.perform_image_inspection()の引数に使用する
    """
    TOOL_INSPECTION = auto()
    """
    ドリル・タップが破損していないかを検査する工具検査
    """
    PRE_PROCESSING_INSPECTION = auto()
    """
    外形の大きさを判別してQRコードを読み取る加工前検査
    """
    ACCURACY_INSPECTION = auto()
    """
    穴の位置と大きさを検査する精度検査
    """


class WorkPieceShape(Enum):
    """
    ワークの形を表す列挙型
    """
    SQUARE = auto()
    """
    ワークの形:四角。今回だと正方形
    """
    CIRCLE = auto()
    """
    ワークの形:円
    """


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


class Request(Enum):
    """
    GUIスレッドから受け取って処理するリクエストの種類を表す列挙型
    """
    LOGIN_REQUEST = auto()
    """
    ログイン要求する。
    IDとパスワードを送信する。
    """
    CAMERA_FEED_REQUEST = auto()
    """
    カメラの映像を要求
    カメラの種類を送信する
    """
    ROBOT_OPERATION_REQUEST = auto()
    """
    ロボットの動作を要求する
    ロボットに送信する命令の文字列を送信する
    """
    STATUS_REQUEST = auto()
    """
    ロボットの状態の取得を要求する\n
    共有変数に格納されている、ロボットの状態を編集する
    """
    LIGHTING_CONTROL_REQUEST = auto()
    """
    照明の制御を要求する
    照明の種類と、ON/OFFを送信する
    """
    AVERAGE_PROCESSING_TIME_REQUEST = auto()
    """
    残りの加工時間を推測するために、ある型番の加工時間の平均を要求する
    型番を送信する
    """
    INPUT_PROCESSING_DATA = auto()
    """
    加工データが入力され、加工開始の準備ができたことを通知する
    加工データを送信する
    """
    REQUEST_PROCESSING_DATA_LIST = auto()
    """
    加工データ(型番)の一覧を要求する
    """


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


@dataclass
class Point:
    """
    2次元の座標を表すデータクラス
    """
    x_potision: float
    y_potision: float


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


# 工具検査のデータクラス
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
    """"""
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
