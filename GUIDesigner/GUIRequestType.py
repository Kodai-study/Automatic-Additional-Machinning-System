from enum import Enum, auto


class GUIRequestType(Enum):
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
    UPLOAD_PROCESSING_DETAILS = auto()
    """
    加工データが入力され、加工開始の準備ができたことを通知する
    加工データを送信する
    """
    REQUEST_PROCESSING_DATA_LIST = auto()
    """
    加工データ(型番)の一覧を要求する
    """
