from enum import Enum, auto


class Frames(Enum):
    WAIT_CONNECTION = auto()
    LOGIN = auto()
    EMERGENCY_STOP = auto()
    WORK_REQUEST_OVERVIEW = auto()
    TOOL_REQUEST_OVERVIEW = auto()
    CREATE_SELECTION = auto()
    CHECK_SELECTION = auto()
    PROCESSING_PROGRESS = auto()
    WORK_RESULT_OVERVIEW = auto()
