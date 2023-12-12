import cv2
import numpy as np

def detect_circles(image_path, max_circles=5):
    image = cv2.imread(image_path)

    # グレースケール変換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # ガウシアンブラーによるノイズ低減
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Cannyエッジ検出
    edges = cv2.Canny(blurred, 20, 50)
    edges = cv2.bitwise_not(edges)
    cv2.imshow("Edge Detection", edges)
    circles = cv2.HoughCircles(
        edges,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=50,
        param1=50,
        param2=30,
        minRadius=20,
        maxRadius=109
    )

    detected_circles = []

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i, circle in enumerate(circles[0, :]):
            if len(detected_circles) >= max_circles:
                break  # 検出する円の最大数に達したら終了

            center = (circle[0], circle[1])
            radius = int(circle[2])  # 半径を整数に変換

            # 既存の円との重なりを確認
            overlap = False
            for existing_circle in detected_circles:
                existing_center = existing_circle["center"]
                existing_radius = existing_circle["radius"]
                distance = np.sqrt((center[0] - existing_center[0])**2 + (center[1] - existing_center[1])**2)
                if distance < (radius + existing_radius):
                    overlap = True
                    break

            if not overlap:
                cv2.circle(image, center, radius, (0, 0, 255), 2)
                cv2.circle(image, center, 2, (0, 255, 0), 3)
                detected_circles.append({
                    "center": center,
                    "radius": radius,
                })
                print(f"円 {i + 1}: 中心 = {center}, 半径 = {radius}")

    # 画像を保存
    output_image_path = 'ImageInspectionController/test/output_circles.png'
    cv2.imwrite(output_image_path, image)

    cv2.imshow('検出された形状', image)
    cv2.waitKey(0)

    return detected_circles, output_image_path

def main():
    image_path = 'ImageInspectionController/test/c.png'
    max_circles_to_detect = 5  # 検出する円の最大数

    detected_circles, output_image_path = detect_circles(image_path, max_circles_to_detect)

    for i, circle in enumerate(detected_circles):
        center = circle["center"]
        radius = circle["radius"]
        print(f"円 {i + 1}: 中心座標 = {center}, 直径 = {radius * 2} px")

    print(f"検出結果の画像を保存しました: {output_image_path}")
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
