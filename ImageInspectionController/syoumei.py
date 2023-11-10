import serial.tools.list_ports

IOBOARD_PID = 2050
IOBOARD_VID = 10777

# COMポートの一覧を取得
ports = list(serial.tools.list_ports.comports())
com_num = None

for port in ports:
    if port.pid == IOBOARD_PID and port.vid == IOBOARD_VID:
        com_num = port.device

if com_num is None:
    print("COMポートが見つかりませんでした。")
    exit()

else:
    serPort = serial.Serial(com_num, 19200, timeout=1)
    print(f"COMポート {com_num} を使用します。")


str = "gpio "+"clear "+"1"
serPort.write((str + "\r").encode('utf-8'))
print((str + "\r"))
