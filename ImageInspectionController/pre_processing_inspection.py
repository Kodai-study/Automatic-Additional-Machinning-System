import cv2
import numpy as np
from pyzbar.pyzbar import decode


def process_qr_code(image_path):
    # 画像の読み込み
    image = cv2.imread(image_path)

    # グレースケールに変換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # エッジ検出
    edges = cv2.Canny(gray, 50, 150)

    # 輪郭検出
    contours, _ = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    qr_code_info = None
    rectangle_coords = []
    for contour in contours:
        # 四角形の検出
        approx = cv2.approxPolyDP(
            contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:
            # 四角形の大きさを表示
            x, y, w, h = cv2.boundingRect(approx)
            print("四角形の大きさ: 幅 =", w, ", 高さ =", h)

            # 四角形の枠線を描画
            cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)

            # この四角形の座標を保存
            rectangle_coords = [x, y, w, h]

    # QRコードの検出
    qr_codes = decode(gray)

    if qr_codes:
        for qr_code in qr_codes:
            # QRコードの内容を保存
            qr_code_info = qr_code.data.decode('utf-8')
            print("QRコードの内容:", qr_code_info)

    return rectangle_coords, qr_code_info


if __name__ == "__main__":
    # 画像ファイルのパスを指定
    image_path = 'ImageInspectionController/QR.png'

    # 関数を呼び出して結果を取得
    rectangle_coords, qr_code_info = process_qr_code(image_path)

    # 結果を表示
    print("四角形の座標:", rectangle_coords)
    print("QRコードの内容:", qr_code_info)
