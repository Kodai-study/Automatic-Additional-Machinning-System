import cv2
import numpy as np
from matplotlib import pyplot as plt

def mark_90_degree_intersection(image_path, threshold_value):
    # 画像の読み込み
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2値化
    _, binary_image = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

    # Hough変換で直線を検出
    lines = cv2.HoughLinesP(binary_image, 1, np.pi / 180, threshold=50, minLineLength=100, maxLineGap=10)

    # 角度が90度に近い線分を抽出
    angle_threshold = 10  # 90度からの許容誤差
    detected_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        if abs(angle - 90) < angle_threshold:
            detected_lines.append(line)

    # 検出された線分の交点を計算
    intersection_points = []
    for i in range(len(detected_lines)):
        for j in range(i + 1, len(detected_lines)):
            line1 = detected_lines[i][0]
            line2 = detected_lines[j][0]
            x, y = calculate_intersection(line1, line2)
            intersection_points.append((x, y))

    # 交点にマークを付ける
    for point in intersection_points:
        x, y = point
        # 有効な座標かどうかをチェック
        if not (np.isnan(x) or np.isinf(x) or np.isnan(y) or np.isinf(y)):
            cv2.drawMarker(image, (int(x), int(y)), (0, 255, 0), markerType=cv2.MARKER_CROSS, markerSize=10)

    # 結果の表示
    cv2.imwrite("ImageInspectionController/test/gray.png",binary_image)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('Marked 90 Degree Intersections')
    plt.show()

def calculate_intersection(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
    y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator

    return x, y

# 画像ファイルのパスと2値化のためのしきい値を指定
image_path = 'ImageInspectionController/test/kakou.png'
threshold_value = 254

# 90度で交わっている点にマークを付ける関数呼び出し
mark_90_degree_intersection(image_path, threshold_value)
