#引数
#画像パス
#返り値
#画像処理を施した画像、良否判定
import cv2
import numpy as np

def detect_circles(image_path):
    image = cv2.imread(image_path)

    # グレースケール変換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # ガウシアンブラーによるノイズ低減
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Cannyエッジ検出
    edges = cv2.Canny(blurred, 50, 150)

    circles = cv2.HoughCircles(
        edges,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=50,
        param1=50,
        param2=30,
        minRadius=20,
        maxRadius=50
    )

    detected_circles = []

    if circles is not None:
        detected_circles = np.uint16(np.around(circles))

    return detected_circles

# 以下の部分は変更がありません

def detect_squares(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)

    gray_canny = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(gray_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected_squares = []

    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4:
            detected_squares.append(approx)

    return detected_squares

def measure_dimensions(square):
    side1 = np.linalg.norm(square[0] - square[1])
    side2 = np.linalg.norm(square[1] - square[2])
    
    return side1, side2

def main():
    image_path = 'ImageInspectionController/img21.png'

    detected_circles = detect_circles(image_path)
    detected_squares = detect_squares(image_path)

    image = cv2.imread(image_path)

    if len(detected_circles) > 0:
        for i, circle in enumerate(detected_circles[0, :]):
            center = (circle[0], circle[1])
            radius = circle[2]
            cv2.circle(image, center, radius, (0, 0, 255), 2)
            cv2.circle(image, center, 2, (0, 255, 0), 3)
            print(f"円 {i + 1}: 中心 = {center}, 半径 = {radius}")
    else:
        print('円が見つかりませんでした.')

    if len(detected_squares) > 0:
        for i, square in enumerate(detected_squares):
            print(f"四角形 {i + 1}: ", end="")
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
            for j, point in enumerate(square):
                color = colors[j]
                cv2.circle(image, tuple(point[0]), 5, color, -1)
            print()
            side1, side2 = measure_dimensions(square)
            print(f"  縦の寸法: {side1}, 横の寸法: {side2}")
    else:
        print('四角形が見つかりませんでした.')

    cv2.imshow('検出された形状', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
