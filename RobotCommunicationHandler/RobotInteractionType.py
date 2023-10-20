from enum import Enum, auto


class RobotInteractionType(Enum):
    """
    通信ソフト → 統合ソフトに渡すメッセージの種類を定義したEnum
    """
    MESSAGE_RECEIVED = auto()
    """
    通信ソフトからメッセージを受信したことを表す
    """
    SOCKET_CONNECTED = auto()
    """
    ロボットとのソケット通信が確立したことを表す
    """
    CONNECTION_LOST = auto()
    """
    ロボットとのソケット通信が切断されたことを表す
    """
    SEND_FAILURE = auto()
    """
    ロボットへのコマンド送信に失敗したことを表す
    """
    RESPOND_REQUEST = auto()
    """
    ロボットからの応答を要求することを表す
    """
