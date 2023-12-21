import numpy as np
import cv2

# 画像データの生成
image_data = np.random.randint(0, 256, size=(512, 512), dtype=np.uint8)

# グレースケール画像の保存
cv2.imwrite('img/grayscale_image.jpg', image_data)

# グレースケール画像の読み込み
loaded_image_data = cv2.imread('img/grayscale_image.jpg', cv2.IMREAD_GRAYSCALE)

# データの比較
if np.array_equal(image_data, loaded_image_data):
    print("データは一致しています。")
else:
    print("データが一致しません。")

# 必要に応じて、元のデータと読み込んだデータを表示して確認することもできます
# cv2.imshow('Original Image', image_data)
# cv2.imshow('Loaded Image', loaded_image_data)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
