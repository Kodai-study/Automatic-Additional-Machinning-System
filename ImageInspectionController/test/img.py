from PIL import Image
import numpy as np


def save_numpy_array_as_png(numpy_array, file_path, scale_factor=0.5):
    # numpy arrayを8ビット整数に変換
    image_data = (numpy_array * 255).astype(np.uint8)

    # PIL Imageを作成
    image = Image.fromarray(image_data)

    # 画像サイズを縮小
    new_size = (int(image.width * scale_factor),
                int(image.height * scale_factor))
    resized_image = image.resize(new_size)

    # 画像を保存
    resized_image.save(file_path)


# 例として、ランダムな3x3のnumpy配列を生成し、半分のサイズで保存する
random_array = np.random.rand(3, 3)
save_numpy_array_as_png(
    random_array, "ImageInspectionController/output.png", scale_factor=10)
