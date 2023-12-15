import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def detect_and_draw_shapes(image_path, max_circles=5, max_rectangles=5):
    image = cv2.imread(image_path)

    # グレースケール変換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 画像を2値化
    _, threshold = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)
    cv2.imwrite("ImageInspectionController/test/threshold.png",threshold)
    # ガウシアンブラーによるノイズ低減
    blurred = cv2.GaussianBlur(threshold, (5, 5), 0)

    # Cannyエッジ検出
    edges = cv2.Canny(blurred, 20, 50)
    edges = cv2.bitwise_not(edges)
    cv2.imshow("Edge Detection", edges)

    # 円の検出
    circles = cv2.HoughCircles(
        edges,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=10,
        param1=10,
        param2=1,
        minRadius=5,
        maxRadius=110
    )

    detected_circles = []

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i, circle in enumerate(circles[0, :]):
            if i >= max_circles:
                break  # 検出する円の最大数に達したら終了

            center = (circle[0], circle[1])
            radius = int(circle[2])  # 半径を整数に変換

            # 他の円との重なりを確認
            overlap = False
            for existing_circle in detected_circles:
                existing_center = existing_circle["center"]
                existing_radius = existing_circle["radius"]
                distance = np.sqrt((center[0] - existing_center[0])**2 + (center[1] - existing_center[1])**2)
                if distance < (radius + existing_radius):
                    overlap = True
                    break

            if not overlap:
                detected_circles.append({
                    "center": center,
                    "radius": radius,
                })

                # TTFフォントを指定して読み込む
                font_path = "ImageInspectionController/test/NotoSansJP-VariableFont_wght.ttf"  # フォントのパスを指定してください
                font_size = 14
                font = ImageFont.truetype(font_path, font_size)

                # 検出された円の情報を画像に描画
                image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                draw = ImageDraw.Draw(image_pil)
                text = f"円{i + 1}: 中心 = {center}, 半径 = {radius} px"
                text_position = (center[0] + radius + 10, center[1] - radius - 10)
                draw.text(text_position, text, font=font, fill=(255, 0, 0))  # 赤い文字

                image = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

                cv2.circle(image, center, radius, (0, 0, 255), 2)
                cv2.circle(image, center, 2, (0, 255, 0), 3)

    # 黒い四角形の検出
    contours, _ = cv2.findContours(blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected_black_rectangles = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # 画像の淵は検出対象外
        if x > 0 and y > 0 and x + w < image.shape[1] and y + h < image.shape[0]:
            if w > 20 and h > 20:  # 面積が一定以上のものを四角形として扱う
                if len(detected_black_rectangles) >= max_rectangles:
                    break  # 検出する四角形の最大数に達したら終了

                detected_black_rectangles.append((x, y, x+w, y+h))

                # 検出された四角形を描画
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

                # 四角形の頂点に色でマーク
                color_list = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
                for j, color in enumerate(color_list):
                    vertex = (x + int(j % 2) * w, y + int(j / 2) * h)
                    cv2.circle(image, vertex, 5, color, -1)

    # 画像を保存
    output_image_path = 'ImageInspectionController/test/output_shapes.png'
    cv2.imwrite(output_image_path, image)
    cv2.imwrite("ImageInspectionController/test/output_edges.png",edges)
    cv2.imshow('検出された形状', image)
    cv2.waitKey(0)

    return detected_circles, detected_black_rectangles, output_image_path

def main():
    image_path = 'ImageInspectionController/test/threshold2.png'
    detected_circles, detected_black_rectangles, output_image_path = detect_and_draw_shapes(image_path, max_circles=5, max_rectangles=5)

    if not detected_circles:
        print("円は検出されませんでした。")

    if not detected_black_rectangles:
        print("黒い四角形は検出されませんでした。")

    if detected_circles or detected_black_rectangles:
        for i, circle in enumerate(detected_circles):
            center = circle["center"]
            radius = circle["radius"]
            print(f"円 {i + 1}: 中心座標 = {center}, 半径 = {radius} px")

        for i, rectangle in enumerate(detected_black_rectangles):
            print(f"黒い四角形 {i + 1}: 座標 = {rectangle}")

        print(f"検出結果の画像を保存しました: {output_image_path}")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
