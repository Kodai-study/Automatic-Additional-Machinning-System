import cv2
import numpy as np

def measure_drill_width(drill_image_path):
    # 画像の読み込み
    image = cv2.imread(drill_image_path)

    if image is None:
        print(f"Error: Failed to load image from {drill_image_path}")
        return

    # グレースケール変換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # エッジ検出（適切なパラメータを調整してください）
    edges = cv2.Canny(gray, 30, 100)

    # 輪郭検出
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print("Error: No contours found.")
        return

    # 面積最大の輪郭選択
    max_contour = max(contours, key=cv2.contourArea)

    # 外接矩形を取得
    x, y, w, h = cv2.boundingRect(max_contour)

    # 外形を囲む四角形を描画
    cv2.drawContours(image, [max_contour], 0, (0, 255, 0), 2)

    # 外形の幅（直径）を計算
    width = w

    # 結果を表示
    print(f"ドリルの外形の幅（直径）: {width} ピクセル")

    # 矩形を画像上に表示
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.putText(image, f"Width: {width:.2f} px", (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow("Drill Width Measurement", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# ドリルの画像ファイルのパスを指定して呼び出し
drill_image_path = "ImageInspectionController/drill.png"
measure_drill_width(drill_image_path)
