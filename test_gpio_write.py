
# License
# -------
# This code is published and shared by Numato Systems Pvt Ltd under GNU LGPL
# license with the hope that it may be useful. Read complete license at
# http://www.gnu.org/licenses/lgpl.html or write to Free Software Foundation,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

# Simplicity and understandability is the primary philosophy followed while
# writing this code. Sometimes at the expence of standard coding practices and
# best practices. It is your responsibility to independantly assess and implement
# coding practices that will satisfy safety and security necessary for your final
# application.

# This demo code demonstrates how to write to a GPIO
import sys
import serial

# コマンドライン引数の数をチェック
if len(sys.argv) < 4:
    print("Usage: gpiowrite.py <PORT> <GPIONUM> <COMMAND> \nEg: gpiowrite.py COM1 0 set")
    sys.exit(0)
else:
    portName = sys.argv[1]
    gpioNum = sys.argv[2]
    command = sys.argv[3]

# 通信のためのポートを開く
serPort = serial.Serial(portName, 19200, timeout=1)

# "gpio write" コマンドを送信。GPIO番号10以上は、
# Aから始まるアルファベットで参照されます。
# 例: GPIO10はA、GPIO11はB、など。
# 16進数表記ではありませんので、Fを超えることもあります。

if int(gpioNum) < 10:
    gpioIndex = str(gpioNum)
else:
    gpioIndex = chr(55 + int(gpioNum))

# Python 3では、バイト列に変換する必要があります。
serPort.write(("gpio " + command + " " + gpioIndex + "\r").encode('utf-8'))

print("gpio " + command + " " + gpioIndex + "\r")
# serPort.write("gpio "+ command +" "+ gpioIndex  + "\r")
print("Command sent...")

# ポートを閉じる
serPort.close()
