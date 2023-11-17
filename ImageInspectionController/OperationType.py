from enum import Enum, auto


class OperationType(Enum):
    """
    画像検査システムへの操作の種類を表す列挙型   
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
    CONTROL_LIGHTING = auto()
    """
    (手動操作モード)照明のON/OFFの操作を行う
    """
    TAKE_INSPECTION_SNAPSHOT = auto()
    """
    (手動操作モード)検査カメラの監視で、画像を撮影する。
    """
