
from enum import Enum, auto


class GUIRequestType(Enum):
    REQUEST_LOGIN = auto()
    FETCH_CAMERA_VIEW = auto()
    SEND_ROBOT_COMMAND = auto()
    FETCH_ROBOT_CONDITION = auto()
    TOGGLE_LIGHTING = auto()
    FETCH_PROCESSING_AVG_TIME = auto()
    UPLOAD_PROCESSING_DETAILS = auto()
    FETCH_WORK_DATA_LIST = auto()
