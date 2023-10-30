# coding: utf-8
from enum import Enum, auto
from dataclasses import dataclass


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


@dataclass
class Point:
    """
    2次元の座標を表すデータクラス
    """
    x_potision: float
    y_potision: float


class TransmissionTarget(Enum):
    """
    送信先を表す列挙型
    """
    TEST_TARGET_1 = auto()

    TEST_TARGET_2 = auto()

    UR = auto()
    """
    URに送信する
    """
    CFD = auto()
    """
    CFDに送信する
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


class CameraType(Enum):
    """
    検査カメラの種類を表す列挙型
    """
    TOOL_CAMERA = auto()
    """
    工具検査用のカメラ
    """
    PRE_PROCESSING_CAMERA = auto()
    """
    加工前検査用のカメラ
    """
    ACCURACY_CAMERA = auto()
    """
    加工穴の精度検査用のカメラ
    """


class LightingType(Enum):
    """
    照明の種類を表す列挙型
    """
    TOOL_LIGHTING = auto()
    """
    工具検査用のリング照明
    """
    PRE_PROCESSING_LIGHTING = auto()
    """
    加工前検査用のバー照明
    """
    ACCURACY_LIGHTING = auto()
    """
    精度検査用のバックライト照明
    """
