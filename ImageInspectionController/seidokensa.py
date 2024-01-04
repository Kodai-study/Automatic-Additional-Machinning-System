import cv2
import numpy as np

def preprocess_image(image_path):
    # 画像の読み込み
    image = cv2.imread(image_path)
    
    # グレースケール変換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 画像の平滑化
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    return blurred

def detect_circles(image_path, min_radius=10, max_radius=100, param1=50, param2=30):
    # 画像の前処理
    preprocessed_image = preprocess_image(image_path)
    
    # ハフ変換を用いて円を検出
    circles = cv2.HoughCircles(
        preprocessed_image,
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
        result_image = cv2.imread(image_path)
        for i in circles[0, :]:
            center = (i[0], i[1])
            cv2.circle(result_image, center, i[2], (0, 255, 0), 2)  # 円を描画

        cv2.imshow('Detected Circles', result_image)
        cv2.imwrite("circle.png",result_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("円が検出されませんでした。")

# 使用例
detect_circles('seido.png', min_radius=10, max_radius=100, param1=50, param2=30)
