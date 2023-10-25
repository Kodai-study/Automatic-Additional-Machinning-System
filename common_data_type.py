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
