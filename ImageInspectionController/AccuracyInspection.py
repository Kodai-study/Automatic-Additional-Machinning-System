from typing import List
from ImageInspectionController.InspectDatas import AccuracyInspectionData
from ImageInspectionController.InspectionResults import AccuracyInspectionResult
from ImageInspectionController.ProcessDatas import HoleCheckInfo, HoleType
from common_data_type import Point
import cv2


class AccuracyInspection:

    def __init__(self):
        self.OFFSET_X = 427

    def exec_inspection(self, image_path: str, inspect_data: AccuracyInspectionData) -> AccuracyInspectionResult:
        inspect_image= self._get_preprocessed_image(image_path)
        result_image = cv2.cvtColor(inspect_image,cv2.COLOR_GRAY2BGR)
        circles = self._detect_holes(
            inspect_image,result_image)
        if circles is None:
            return AccuracyInspectionResult(False, None, None)
        circles = circles[0]
        hole_check_informations = []
        for circle in circles:
            centor, radius = self._get_hole_informations(
                circle, inspect_data.work_dimension)
            target_hole = self._find_closest_hole(
                centor, inspect_data.hole_informations)
            hole_check_informations.append(self._check_hole(
                centor, radius, target_hole))

        # hole_check_informationsの要素に検査不合格があるか判定
        is_check_ok = True
        error_messages = []
        for hole_check_information in hole_check_informations:
            if hole_check_information.hole_check_info == False:
                is_check_ok = False
                error_messages.append(
                    f"hole_id: {hole_check_information.hole_id}の位置が不正です。")

        return AccuracyInspectionResult(is_check_ok, None, hole_check_informations)

    def _get_preprocessed_image(self, image_path):
        BINARY_THRESHOLD = 180
        # 画像の読み込み
        CROPP_WIDTH = 2048
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        image = image[0:CROPP_WIDTH, self.OFFSET_X:]
        _, image = cv2.threshold(
            image, BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)
        # グレースケール変換
        # 画像の平滑化
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        return blurred

    def _detect_holes(self, image, result_image=None):
        # ハフ変換を用いて円を検出
        PARAMETER_1 = 200
        PARAMETER_2 = 15
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

        if result_image is not None and circles:
            for i in circles[0, :]:
                center = (int(i[0]), int(i[1]))
                cv2.circle(result_image, center,
                           int(i[2]), ((0, 255, 0)), 2)  # 円を描画

        cv2.imshow("hofg",result_image)
        cv2.waitKey(-1)
        cv2.destroyAllWindows()
        return circles

    def _get_hole_informations(self, circle, work_dimension):
        # 1ピクセル当たりのミリメートル
        PIXEL_PER_MILLI = 0.05
        ORIGIN_X = 2513 - self.OFFSET_X
        ORIGIN_Y = 36

        centor_mills_x = (ORIGIN_X - circle[0]) * PIXEL_PER_MILLI
        centor_mills_y = (circle[1] - ORIGIN_Y) * PIXEL_PER_MILLI
        radius_mills = circle[2] * PIXEL_PER_MILLI * 2
        cercle_position_mills = Point(
            work_dimension - centor_mills_x, work_dimension - centor_mills_y)
        return cercle_position_mills, radius_mills

    def _check_hole(self, centor: Point, radius, target_data: HoleCheckInfo):
        # 座標の誤差の範囲
        TOLERANCE = 4

        THRESHOLD_M3 = 2.5
        THRESHOLD_M4 = 3.5
        THRESHOLD_M5 = 4.5
        THRESHOLD_M6 = 5.5

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
