import cv2
import numpy as np

def detect_circles(image_path):
    # 画像の読み込み
    image = cv2.imread(image_path)

    # グレースケールに変換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 画像のぼかしを適用（ノイズの軽減のため）
    gray = cv2.medianBlur(gray, 5)

    # ハフ変換を使用して円を検出
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=30,
        param1=100,
        param2=45,
        minRadius=1,
        maxRadius=1000
    )

    detected_circles = []

    if circles is not None:
        # 検出された円を整数に変換
        detected_circles = np.uint16(np.around(circles))

    return detected_circles

def detect_squares(image_path):
    # 画像の読み込み
    image = cv2.imread(image_path)

    # グレースケールに変換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 画像のぼかしを適用（ノイズの軽減のため）
    gray = cv2.medianBlur(gray, 5)

    # 四角形を検出
    gray_canny = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(gray_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected_squares = []

    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4:  # 近似された輪郭が四角形である場合
            detected_squares.append(approx)

    return detected_squares

def main():
    image_path = 'ImageInspectionController/img3.png'

    # 円の検出
    detected_circles = detect_circles(image_path)

    # 四角形の検出
    detected_squares = detect_squares(image_path)

    # 画像の読み込み
    image = cv2.imread(image_path)

    # 検出された円を赤色で描画
    if len(detected_circles) > 0:
        for circle in detected_circles[0, :]:
            center = (circle[0], circle[1])
            radius = circle[2]
            cv2.circle(image, center, radius, (0, 0, 255), 2)
            
            # 円の中心を描画
            cv2.circle(image, center, 2, (0, 255, 0), 3)
    else:
        print('円が見つかりませんでした。')

    # 検出された四角形を緑色で描画
    if len(detected_squares) > 0:
        for square in detected_squares:
            cv2.polylines(image, [square], True, (0, 255, 0), 2)
    else:
        print('四角形が見つかりませんでした。')

    # 結果の表示
    cv2.imshow('Detected Shapes', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
