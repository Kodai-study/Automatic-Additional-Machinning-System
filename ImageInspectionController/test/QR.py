import cv2
import numpy as np
from pyzbar.pyzbar import decode

def read_qr_code(image_path):
    # 画像の読み込み
    image = cv2.imread(image_path)

    # グレースケールに変換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # エッジ検出
    edges = cv2.Canny(gray, 50, 150)

    # 輪郭検出
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # 四角形の検出
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:
            # 四角形の大きさを表示
            x, y, w, h = cv2.boundingRect(approx)
            print("四角形の大きさ: 幅 =", w, ", 高さ =", h)

            # 四角形の枠線を描画
            cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)

    # QRコードの検出
    qr_codes = decode(gray)

    if qr_codes:
        for qr_code in qr_codes:
            # QRコードの位置を取得
            rect_points = qr_code.polygon
            if rect_points:
                # numpy.array に変換
                rect_points = np.array(rect_points, dtype=np.int32)

                # QRコードの位置に矩形を描画
                rect = cv2.convexHull(rect_points)
                cv2.drawContours(image, [rect], -1, (0, 255, 0), 2)

                # 四角形の外側に矩形を描画
                x, y, w, h = cv2.boundingRect(rect)
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # QRコードの内容を表示
                print("QRコードの内容:", qr_code.data.decode('utf-8'))
    else:
        # QRコードが見つからない場合のメッセージ
        print("QRコードが見つかりませんでした。")

    # 画像の表示
    cv2.imshow('QR Code Reader', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # 画像ファイルのパスを指定
    image_path = 'ImageInspectionController/QR.png'

    # QRコードを読み取り、内容を表示
    read_qr_code(image_path)
