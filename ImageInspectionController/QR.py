import cv2
import numpy as np
from pyzbar.pyzbar import decode

def read_qr_code(image_path):
    # 画像の読み込み
    image = cv2.imread(image_path)

    # グレースケールに変換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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

            # QRコードの内容を表示
            print("QRコードの内容:", qr_code.data.decode('utf-8'))

    # 画像の表示
    cv2.imshow('QR Code Reader', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

if __name__ == "__main__":
    # 画像ファイルのパスを指定
    image_path = 'ImageInspectionController/QR2.png'

    # QRコードを読み取り、内容を表示
    read_qr_code(image_path)
