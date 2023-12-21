import cv2
import numpy as np
from matplotlib import pyplot as plt

def binary_threshold(image_path, threshold_value):
    # 画像の読み込み
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # しきい値処理
    _, binary_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)

    # 結果の表示
    plt.subplot(121), plt.imshow(image, cmap='gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])

    plt.subplot(122), plt.imshow(binary_image, cmap='gray')
    plt.title('Binary Image'), plt.xticks([]), plt.yticks([])

    plt.show()

# 画像ファイルのパスと2値化のためのしきい値を指定
image_path = 'ImageInspectionController/test/kakou.png'
threshold_value = 240

# 2値化の関数呼び出し
binary_threshold(image_path, threshold_value)
