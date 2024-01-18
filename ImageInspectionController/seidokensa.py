import cv2
import numpy as np

def preprocess_image(image_path, threshold_value=127):
    # 画像の読み込み
    image = cv2.imread(image_path)
    
    # グレースケール変換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 画像の平滑化
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    cv2.imwrite("result_gray.png",blurred)
    return blurred

def detect_circles(image_path, min_radius=10, max_radius=100, param1=50, param2=30, threshold_value=127,Tolerance=1.7,realvalue=0.05):
    # 画像の前処理
    preprocessed_image = preprocess_image(image_path, threshold_value)
    
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
            radius = i[2]
            cv2.circle(result_image, center, radius, (0, 255, 0), 2)  # 円を描画
            #合否結果判定
            Tolerancemin=Tolerance-0.05
            Tolerancemax=Tolerance+0.05
            #pxをmmに変換する
            realvalue_radius=radius*2*0.05 #実際の寸法＝直径(半径×2)×1pxの長さ
            if realvalue_radius < Tolerancemax and realvalue_radius > Tolerancemin:
                gouhi="o"
            else:
                gouhi="x"
            
            # 座標と直径を表示
            text = f"(x_{center[0]}px, y_{center[1]}px, center{Tolerance}+-0.05mm,center{realvalue_radius}mm, {gouhi})"
            cv2.putText(result_image, text, (i[0] - 9*radius, i[1] - radius), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.imwrite('result_image.png', result_image)
        #cv2.imshow('Detected Circles', result_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("円が検出されませんでした。")

# 使用例
detect_circles('exptime1000.png', min_radius=10, max_radius=100, param1=50, param2=30, threshold_value=240,realvalue=0.05)
