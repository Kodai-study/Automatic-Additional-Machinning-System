import cv2
import numpy as np
import matplotlib.pyplot as plt

def detect_and_draw_circles(image_path, param1=50, param2=30, min_radius=10, max_radius=100):
    # 画像の読み込み
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    if image is None:
        print(f"Error: Unable to read the image at {image_path}")
        return

    # グレースケール変換
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # cv2.HoughCirclesを使用して円を検出
    circles = cv2.HoughCircles(
        gray_image,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=20,
        param1=param1,
        param2=param2,
        minRadius=min_radius,
        maxRadius=max_radius
    )

    if circles is not None:
        circles = np.uint16(np.around(circles))
        
        # 検出された円を描画
        for i in circles[0, :]:
            center = (i[0], i[1])
            radius = i[2]
            cv2.circle(image, center, radius, (0, 0, 255), 2)  # 赤色で描画

        # 画像の表示
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title('Detected Circles')
        plt.show()

        return circles[0, :]
    else:
        print("No circles detected.")
        return []

def main():
    image_path = 'ImageInspectionController/img.png'
    detected_circles = detect_and_draw_circles(image_path)

    print("Detected Circles:")
    for circle in detected_circles:
        print(circle)

if __name__ == "__main__":
    main()
