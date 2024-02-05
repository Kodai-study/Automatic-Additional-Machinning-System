import math
from typing import List
from ImageInspectionController.InspectDatas import PreProcessingInspectionData
from ImageInspectionController.InspectionResults import AccuracyInspectionResult
from ImageInspectionController.ProcessDatas import HoleCheckInfo, HoleType
from common_data_type import Point, WorkPieceShape
import cv2
import numpy as np
from pyzbar.pyzbar import decode


class AccuracyInspection:

    def __init__(self):
        self.OFFSET_X = 427

    def exec_inspection(self, image_path: str, inspect_data: List[HoleCheckInfo]) -> AccuracyInspectionResult:
        hole_informations, work_dimension = inspect_data
        circles = self._detect_holes(
            self._get_preprocessed_image(image_path))[0]
        hole_check_informations = []
        for circle in circles:
            centor, radius = self._get_hole_informations(
                circle, inspect_data[1])
            target_hole = self._find_closest_hole(centor, hole_informations)
            hole_check_informations.append(self._check_hole(
                centor, radius, target_hole))

        return AccuracyInspectionResult(True, None, hole_check_informations)

    def _get_preprocessed_image(self, image_path):
        # 画像の読み込み
        CROPP_WIDTH = 2048
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        image = image[0:CROPP_WIDTH, self.OFFSET_X:]
        # image = image[start_y:end_y, start_x:end_x]
        # グレースケール変換
        # 画像の平滑化
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        return blurred

    def _detect_holes(self, image, result_image=None):
        # ハフ変換を用いて円を検出
        PARAMETER_1 = 50
        PARAMETER_2 = 30
        MIN_RADIUS = 10
        MAX_RADIUS = 100

        circles = cv2.HoughCircles(
            image,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=20,
            param1=PARAMETER_1,
            param2=PARAMETER_2,
            minRadius=MIN_RADIUS,
            maxRadius=MAX_RADIUS
        )

        if result_image:
            for i in circles[0, :]:
                center = (i[0], i[1])
                cv2.circle(result_image, center,
                           i[2], (0, 255, 0), 2)  # 円を描画

        return circles

    def _get_hole_informations(self, circle, work_dimension):
        # 1ピクセル当たりのミリメートル
        PIXEL_PER_MILLI = 0.05
        ORIGIN_X = 2513
        ORIGIN_Y = 36

        centor_mills_x = (ORIGIN_X - circle[0]) * PIXEL_PER_MILLI
        centor_mills_y = (ORIGIN_Y - circle[1]) * PIXEL_PER_MILLI
        radius_mills = circle[2] * PIXEL_PER_MILLI
        cercle_position_mills = Point(
            centor_mills_x, work_dimension - centor_mills_y)
        return cercle_position_mills, radius_mills

    def _check_hole(self, centor: Point, radius, target_data: HoleCheckInfo):
        # 座標の誤差の範囲
        TOLERANCE = 0.5

        THRESHOLD_M3 = 3.7
        THRESHOLD_M4 = 4.7
        THRESHOLD_M5 = 5.7
        THRESHOLD_M6 = 6.7

        min_x = target_data.hole_position.x_potision - TOLERANCE
        max_x = target_data.hole_position.x_potision + TOLERANCE
        is_position_ok = (min_x <= centor.x_potision <= max_x)

        if radius < THRESHOLD_M3:
            hole_type = HoleType.M3_HOLE
        elif radius < THRESHOLD_M4:
            hole_type = HoleType.M4_HOLE
        elif radius < THRESHOLD_M5:
            hole_type = HoleType.M5_HOLE
        elif radius < THRESHOLD_M6:
            hole_type = HoleType.M6_HOLE
        else:
            hole_type = None
            is_position_ok = False

        return HoleCheckInfo(target_data.hole_id, centor, hole_type, is_position_ok)

    def _find_closest_hole(self, target_hole: Point, holes: List[HoleCheckInfo]):
        def calculate_distance(point1: Point, point2: Point):
            return ((point1.x_potision - point2.x_potision) ** 2 + (point1.y_potision - point2.y_potision) ** 2) ** 0.5

        closest_distance = float('inf')
        closest_hole = None

        for hole in holes:
            distance = calculate_distance(target_hole,
                                          hole.hole_position)
            if distance < closest_distance:
                closest_distance = distance
                closest_hole = hole

        return closest_hole


if __name__ == "__main__":
    accuracy_inspection = AccuracyInspection()
    accuracy_inspection.exec_inspection(
        "Z:/source/Automatic Additional Machinning System/ImageInspectionController/test/accuracy_inspection/sample_images/multi_type_EXP500.png", [])
