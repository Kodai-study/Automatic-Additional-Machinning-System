import cv2

def crop_image(image, x, y, width, height):
    cropped_image = image[y:y+height, x:x+width]
    return cropped_image

# 画像を読み込む
image = cv2.imread('ImageInspectionController/test/threshold.png')

# 切り取る領域の座標とサイズ（例: x, y, width, height）
x, y, width, height = 100, 50, 200, 150

# 画像を切り取る
cropped = crop_image(image, x, y, width, height)

# 切り取られた画像を表示
cv2.imshow('Cropped Image', cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()
