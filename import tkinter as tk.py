import tkinter as tk
from itertools import cycle

# 2つの画像ファイルのリスト
image_files = ["red_lamp.png", "green_lamp.png"]
image_cycle = cycle(image_files)

# ボタンがクリックされたときの処理


def toggle_button():
    current_image = next(image_cycle)
    img = tk.PhotoImage(file=current_image)
    label.config(image=img)
    label.image = img  # ガベージコレクションを防ぐために画像をラベルに設定


# ウィンドウを作成
window = tk.Tk()
window.title("画像切り替え")

# 初期画像を設定
initial_image = next(image_cycle)
img = tk.PhotoImage(file=initial_image)

# 画像を表示するラベルを作成
label = tk.Label(window, image=img)
label.pack()

# トグルボタンを作成
toggle_button = tk.Button(window, text="切り替え", command=toggle_button)
toggle_button.pack()

# ウィンドウを表示
window.mainloop()
