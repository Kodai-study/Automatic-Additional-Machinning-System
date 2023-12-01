from PIL import Image

def resize_image(input_path, output_path, new_size):
    try:
        # 画像を開く
        with Image.open(input_path) as img:
            # 画像を指定されたサイズにリサイズ
            resized_img = img.resize(new_size)
            
            # リサイズされた画像を保存
            resized_img.save(output_path)
            
            print(f"画像をリサイズしました。保存先: {output_path}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

# 例: リサイズする画像のパス、保存先のパス、新しいサイズ
input_image_path = "ImageInspectionController/img3.png"
output_image_path = "ImageInspectionController/output_resized.png"
new_size = (1000, 750)

# 関数を呼び出して画像をリサイズ
resize_image(input_image_path, output_image_path, new_size)
