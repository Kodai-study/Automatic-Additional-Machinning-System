from enum import Enum, auto


class GUISignalCategory(Enum):
    """
    統合スレッドからGUIスレッドに、通知や信号を送るときに、その種類を表す列挙型\n
    統合 → GUIのキューに入るデータの第1要素に入れる
    """

    ROBOT_CONNECTION_SUCCESS = auto()
    """
    ロボットとの接続に成功したことを通知する (接続されないと次に)
    """
    SENSOR_STATUS_UPDATE = auto()
    """
    センサの状態が更新されたことを通知する。 
    これが送られたときには、共通変数のセンサ状態が後進されている
    """
    CANNOT_CONTINUE_PROCESSING = auto()
    """
    処理を続行できないことを通知する。クリティカルなエラーではなく、
    ストッカの交換などが必要なときに送る
    """
    INSPECTION_COMPLETED = auto()
    """
    検査の時に、画像のキャプチャに成功したことを通知する
    その時に撮られた画像をGUI画面に表示する
    """
    PROCESSING_OUTCOME = auto()
    """
    加工が完了したことを通知する。画面に表示を出し、残りの加工個数などを更新する
    """
    CANNOT_PROCESS_MISSING_TOOL = auto()
    """
    工具の不足や種類が違うことにより、加工ができないことを通知する
    """
    CRITICAL_FAILURE = auto()
    """
    エラー画面を表示させる必要があるような、致命的なエラーが発生したことを通知する
    """
