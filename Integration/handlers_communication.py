from queue import Queue
from GUIDesigner.GUISignalCategory import GUISignalCategory
from RobotCommunicationHandler.RobotInteractionType import RobotInteractionType
from common_data_type import TransmissionTarget
from test_flags import TEST_UR_CONNECTION_LOCAL


def _send_message_to_cfd(message: str, send_request_queue: Queue):
    """
    メッセージのハンドラ。CFDにメッセージを送信する

    Args:
        message (str): 送信するコマンド文字列
    """
    if TEST_UR_CONNECTION_LOCAL:
        send_request_queue.put(
            {"target": TransmissionTarget.TEST_TARGET_2, "message": message})
    else:
        print("send to cfd: ", message)


def _send_message_to_ur(message: str, send_request_queue: Queue):
    """
    メッセージのハンドラ。URにメッセージを送信する

    Args:
        message (str): 送信するコマンド文字列
    """
    send_request_queue.put(
        {"target": TransmissionTarget.TEST_TARGET_1 if TEST_UR_CONNECTION_LOCAL else TransmissionTarget.UR,
            "message": message})


def _change_gui_status(gui_request_queue: Queue, robot_status: dict, device_type: str, device_num: int, status: bool):
    """GUIの状態を変更する

    Args:
        message (str): メッセージの文字列
    """
    robot_status[device_type][device_num] = status
    notice_change_status(gui_request_queue)


def notice_change_status(gui_request_queue: Queue):
    gui_request_queue.put(
        (GUISignalCategory.SENSOR_STATUS_UPDATE,))


def _handle_connection_success(gui_request_queue: Queue, target: TransmissionTarget):
    """接続成功時に呼び出されるハンドラ

    Args:
        target (TransmissionTarget): 接続成功した相手
    """
    gui_request_queue.put(
        (GUISignalCategory.ROBOT_CONNECTION_SUCCESS, target))


def _send_to_gui(gui_request_queue: Queue, message: str):
    """GUIに、ロボットから受け取ったメッセージをそのまま送信する

    Args:
        message (str): ロボットから受け取ったメッセージ
    """
    gui_request_queue.put(
        (RobotInteractionType.MESSAGE_RECEIVED, message))


def _notice_finish_process(gui_request_queue: Queue, result: bool):
    """処理が終了したことをGUIに通知する

    Args:
        message (str): ロボットから受け取ったメッセージ
    """
    gui_request_queue.put(
        (GUISignalCategory.CANNOT_CONTINUE_PROCESSING, result))
