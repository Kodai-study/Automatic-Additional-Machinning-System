# ライセンス
# -------
# このコードはNumato Systems Pvt LtdによってGNU LGPLライセンスの下で公開・共有されています。
# このコードが役立つことを願っています。完全なライセンスについては
# http://www.gnu.org/licenses/lgpl.html を参照してください。

# このコードを書く際の主な哲学は、シンプルさと理解しやすさです。
# これは、標準的なコーディング慣習やベストプラクティスを犠牲にする場合もあります。
# 最終的なアプリケーションで必要な安全性とセキュリティを確保するためのコーディング慣習を
# 独自に評価し、実装する責任はあなたにあります。

# このデモコードは、GPIOの状態を読み取る方法を示しています。

import sys
import serial

# コマンドライン引数の数をチェック
if len(sys.argv) < 3:
    print("使用法: gpioread.py <PORT> <GPIONUM>\n例: gpioread.py COM1 0")
    sys.exit(0)
else:
    portName = sys.argv[1]
    gpioNum = sys.argv[2]

# 通信のためのポートを開く
serPort = serial.Serial(portName, 19200, timeout=1)

print(serPort)

# "gpio read" コマンドを送信。GPIO番号10以上は、
# Aから始まるアルファベットで参照されます。
# 例: GPIO10はA、GPIO11はB、など。
# 16進数表記ではありませんので、Fを超えることもあります。

if int(gpioNum) < 10:
    gpioIndex = str(gpioNum)
else:
    gpioIndex = chr(55 + int(gpioNum))

# Python 3では、バイト列に変換する必要があります。
serPort.write(("gpio read " + gpioIndex + "\r").encode('utf-8'))

response = serPort.read(25).decode('utf-8')

if response[-4] == "1":
    print("GPIO " + str(gpioNum) + " はONです")
elif response[-4] == "0":
    print("GPIO " + str(gpioNum) + " はOFFです")

# ポートを閉じる
serPort.close()
