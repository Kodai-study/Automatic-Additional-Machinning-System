import torch
from PIL import Image, ImageDraw
from IPython.display import display

# yolov5 モデルを読み込みます
model = torch.hub.load('ultralytics/yolov5:v5.0', 'yolov5s')

# 画像のパス
image_path = 'path/to/your/image.jpg'  

# 画像の読み込み
img = Image.open(image_path)

# 推論
results = model(img)

# 円を検出した場合、結果を表示
if results.xyxy[0].shape[0] > 0:
    # 円を検出した場合の処理
    draw = ImageDraw.Draw(img)
    for det in results.xyxy[0]:
        label, conf, xyxy = int(det[5]), det[4], det[:4].cpu().numpy()
        
        # 検出された円を描画
        draw.ellipse(xy=xyxy, outline='red', width=3)

    # 結果の表示
    display(img)
else:
    print("円は検出されませんでした。")
