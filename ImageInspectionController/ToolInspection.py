import cv2
import numpy as np
from ImageInspectionController.InspectionResults import ToolInspectionResult
from common_data_type import ToolType
import cv2
import numpy as np
import os


class ToolInspection:
    def __init__(self):
        self.PIXEL_TO_MM_RATIO = 0.037280701754385967
        self.HIDDEN_LENGTH_MM = 31.526315789473685
        DRILL_TEMPLATE_IMAGE_PATH = 'resource/images/tool_templete_tap.png'
        self.drill_template_image = cv2.imread(
            DRILL_TEMPLATE_IMAGE_PATH, cv2.IMREAD_GRAYSCALE)

    def _setup_image(self, image_path):
        # 画像を読み込む
        original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # 画像を反時計回りに90度回転
        rotateimg = cv2.rotate(original_image, cv2.ROTATE_90_COUNTERCLOCKWISE)

        start_y = 160
        end_y = 620 + start_y
        start_x = 280
        end_x = 380 + start_x
        # 画像を指定した範囲で切り取る
        cropped_image = rotateimg[start_y:end_y, start_x:end_x]

        return cropped_image, rotateimg

    def _drill_tap_categorizer(self, cropped_image):
        MATCHING_THRESHOLD = 0.8

        # テンプレートマッチングの実行
        result = cv2.matchTemplate(
            cropped_image, self.drill_template_image, cv2.TM_CCOEFF_NORMED)

        # 最大値とその位置を取得
        _, max_val, _, _ = cv2.minMaxLoc(result)

        # マッチング率が閾値以上の場合に判定
        if max_val >= MATCHING_THRESHOLD:
            return "TAP"
        else:
            return "DRILL"

    def _get_width_pixcel(self, cropped_image):
        BINARY_THRESHOLD = 128
        # 画像を2値化する
        _, binary_image = cv2.threshold(
            cropped_image, BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)
        max_width = 0
        # 1行ずつ黒色の最小と最大のピクセルを探し、横幅を計算する
        for y in range(binary_image.shape[0]):
            black_pixels = np.where(binary_image[y, :] == 0)[0]
            if len(black_pixels) > 0:
                min_x = np.min(black_pixels)
                max_x = np.max(black_pixels)
                width = max_x - min_x
                if width > max_width:
                    target_max_x = max_x
                    target_min_x = min_x
                    max_width = width
                    max_width_y = y
        # 描写
        cv2.line(cropped_image, (target_min_x, max_width_y),
                 (target_max_x, max_width_y), 125, 2)
        return max_width

    def _tool_type_detector(self, tool, width):
        M3_DRILL_min = 60
        M3_DRILL_max = 76
        M4_DRILL_min = 84
        M4_DRILL_max = 100
        M5_DRILL_min = 109
        M5_DRILL_max = 125
        M6_DRILL_min = 132
        M6_DRILL_max = 148
        M3_TAP_min = 68
        M3_TAP_max = 85
        M4_TAP_min = 92
        M4_TAP_max = 108
        M5_TAP_min = 124
        M5_TAP_max = 140
        M6_TAP_min = 145
        M6_TAP_max = 161

        if tool == "DRILL":
            if M3_DRILL_min <= width <= M3_DRILL_max:
                return ToolType.M3_DRILL
            elif M4_DRILL_min <= width <= M4_DRILL_max:
                return ToolType.M4_DRILL
            elif M5_DRILL_min <= width <= M5_DRILL_max:
                return ToolType.M5_DRILL
            elif M6_DRILL_min <= width <= M6_DRILL_max:
                return ToolType.M6_DRILL
        elif tool == "TAP":
            if M3_TAP_min <= width <= M3_TAP_max:
                return ToolType.M3_TAP
            elif M4_TAP_min <= width <= M4_TAP_max:
                return ToolType.M4_TAP
            elif M5_TAP_min <= width <= M5_TAP_max:
                return ToolType.M5_TAP
            elif M6_TAP_min <= width <= M6_TAP_max:
                return ToolType.M6_TAP
        return None

    def _get_tool_length(self, cropped_image):

        # 画像を2値化する
        _, binary_image = cv2.threshold(
            cropped_image, 128, 255, cv2.THRESH_BINARY)

        # 画像の高さと幅を取得
        height, width = binary_image.shape

        # 画像を下から上にスキャンして、一番最初に見つかった黒いピクセルの座標を取得
        for y in range(height-1, -1, -1):
            for x in range(width):
                if binary_image[y, x] == 0:  # 黒いピクセルを見つけたら
                    return y  # 座標を返す

        # 黒いピクセルが見つからなかった場合
        return None

    def exec_inspection(self, image_path):
        try:
            cropped_image, original_iamge = self._setup_image(image_path)

            color_image = cv2.cvtColor(original_iamge, cv2.COLOR_GRAY2BGR)
            tool_category = self._drill_tap_categorizer(original_iamge)
            width_pixcel = self._get_width_pixcel(cropped_image)
            tool_type = self._tool_type_detector(tool_category, width_pixcel)
            print(f"判定結果 : {tool_type}の{tool_category}")
            tool_length_pixcel = self._get_tool_length(cropped_image)
            tool_diameter = round(self.PIXEL_TO_MM_RATIO * width_pixcel, 2)
            tool_length_mm = tool_length_pixcel * \
                self.PIXEL_TO_MM_RATIO + self.HIDDEN_LENGTH_MM

            info_text1 = f"Tool Length     : {round(tool_length_mm, 2)}"
            info_text2 = f"Tool Type     : {tool_category}"
            info_text3 = f"Tool Diameter : {tool_diameter}"
            info_text4 = f"Tool Size : {tool_type}"
            print(f"Tool Length     : {round(tool_length_mm, 2)}")
            print(f"Tool Type     : {tool_category}")
            print(f"Tool Diameter : {tool_diameter}")
            print(f"Tool Size : {tool_type}")

            # テキストを追加
            cv2.putText(color_image, info_text1, (1, 500),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(color_image, info_text2, (1, 550),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(color_image, info_text3, (1, 600),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(color_image, info_text4, (1, 650),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # 追加するパス
            addpath = "_result"
            # パスを分割
            file_name, file_extension = os.path.splitext(image_path)
            newfile_name = file_name+addpath+file_extension
            cv2.imwrite(newfile_name, color_image)
        except:
             return ToolInspectionResult(result=False, error_items=[], tool_type="non", tool_length=0, drill_diameter=0)

        return ToolInspectionResult(result=True, error_items=None, tool_type=tool_type, tool_length=tool_length_mm, drill_diameter=tool_diameter)
