import math
import os
import shutil
from ImageInspectionController.InspectDatas import PreProcessingInspectionData
from ImageInspectionController.InspectionResults import PreProcessingInspectionResult
from common_data_type import WorkPieceShape
from test_flags import TEST_FEATURE_IMAGE_PROCESSING
if TEST_FEATURE_IMAGE_PROCESSING:
    import cv2
    import numpy as np
    from pyzbar.pyzbar import decode


class PreProcessInspection:
    def __init__(self):
        self.OFFSET_X = 427

    def exec_inspection(self, img_path: str, inspect_data: PreProcessingInspectionData, base_dir) -> PreProcessingInspectionResult:
        """
        画像の前処理検査を行う関数
        Args:
            img_path (str): 画像のパス
        Returns:
            bool: 検査の合否
        """
        TORELANCE = 5
        ORIGINAL_IMAGE_FILE_NAME = "PreProcess_Original.png"
        PROCESSED_IMAGE_FILE_NAME = "PreProcess_Result.png"

        inspection_image = self._get_preprocessed_image(img_path)
        output_image = cv2.imread(img_path, cv2.IMREAD_COLOR)
        contor, width = self._get_contor_and_width(
            inspection_image, output_image)
        is_circle, output_image = self._check_circle(contor, output_image)
        width_millis = self._get_mills_with_picxel(width)
        is_qr_ok, qr_data = self._search_qr_code(inspection_image)
        print(width_millis, "円形" if is_circle else "正方形")

        error_items = []
        if is_circle and inspect_data.workpiece_shape != WorkPieceShape.CIRCLE:
            is_success = False
            error_items.append("正方形ではないワークが検出されました")
        elif not is_circle and inspect_data.workpiece_shape == WorkPieceShape.CIRCLE:
            is_success = False
            error_items.append("正方形が検出されました")
        else:
            is_success = True
        # 誤差の範囲内での最小幅と最大幅を計算
        min_width = inspect_data.work_dimension - TORELANCE
        max_width = inspect_data.work_dimension + TORELANCE

        # 横幅が範囲内でなければエラー  変数を1つ使う
        if not (min_width <= width_millis <= max_width):
            is_success = False
            error_items.append("ワークの大きさが範囲外です")

        if is_qr_ok:
            model, serial_str = qr_data[:3], qr_data[3:]
            save_dir = os.path.join(
                base_dir, f"{model}/{serial_str}")
            directory = os.path.dirname(save_dir)
            if not os.path.exists(directory):
                os.makedirs(directory)
            save_path_original = os.path.join(
                save_dir, ORIGINAL_IMAGE_FILE_NAME)
            save_path_result = os.path.join(
                save_dir, PROCESSED_IMAGE_FILE_NAME)

            shutil.move(img_path, save_path_original)
            cv2.imwrite(save_path_result, output_image)

        else:
            is_success = False
            error_items.append(qr_data)

        return PreProcessingInspectionResult(is_success, error_items, 0, width_millis), save_path_result

    def _get_preprocessed_image(self, img_path):
        # 2値画像を読み込む
        CROPP_HEIGHT = 1970
        CROPP_WIDTH = 1973
        # 2値化の閾値
        THRESHOLD = 140
        # ノイズ除去のためのカーネルサイズ
        NOISE_REMOVAL_KERNEL_SIZE = (5, 5)

        image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        cropped_image = image[0:CROPP_HEIGHT,
                              self.OFFSET_X:self.OFFSET_X + CROPP_WIDTH]

        # 2値化する
        _, binary_img = cv2.threshold(
            cropped_image, THRESHOLD, 255, cv2.THRESH_BINARY)

        # ノイズの除去
        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, NOISE_REMOVAL_KERNEL_SIZE)
        return cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel)

    def _get_contor_and_width(self, image, draw_information_image=None):
        contours, _ = cv2.findContours(
            image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            print("物体が見つかりませんでした")
            return None

        # 最大の輪郭を取得
        max_contour = max(contours, key=cv2.contourArea)
        # 輪郭の外接矩形を取得
        x, y, w, h = cv2.boundingRect(max_contour)

        if draw_information_image is not None:
            # max_countorをオフセット分だけずらす
            max_contour = max_contour + np.array([self.OFFSET_X, 0])
            cv2.drawContours(draw_information_image, [max_contour], -
                             1, (0, 0, 255), 2, )  # 元の輪郭を赤色で描画
            x += self.OFFSET_X
            cv2.rectangle(draw_information_image, (x, y), (x + w, y + h),
                          (255, 0, 0), 5)  # 外接矩形に青色の枠線を引く
        return max_contour, w

    def _get_mills_with_picxel(self, pixcel_width):
        PIXELS_PER_MILLIMETER = 20.1
        # 右側に隠れているミリ数の変数
        HIDDEN_MILLMETERS = 5.920398009950251

        mill_width = pixcel_width / PIXELS_PER_MILLIMETER
        real_width = mill_width + HIDDEN_MILLMETERS
        return round(real_width, 2)

    def _search_qr_code(self, image):
        # QRコードの検出
        qr_codes = decode(image)
        if not qr_codes:
            return False, "QRコードが見つかりませんでした。"
        if len(qr_codes) >= 2:
            return False, "error:QRコードが2個以上検出された"
        return True, qr_codes[0].data.decode('utf-8')

    def _check_circle(self, contour, draw_information_image=None):
        # 最小外接円を取得
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)

        # 最小外接円と輪郭の適合度を評価するロジック（カスタマイズが必要）
        # 例: 輪郭の面積と最小外接円の面積の比較
        contour_area = cv2.contourArea(contour)
        circle_area = math.pi * (radius ** 2)
        area_ratio = contour_area / circle_area

        if 0.7 < area_ratio < 1.3:
            return True, draw_information_image
        else:
            return False, draw_information_image
