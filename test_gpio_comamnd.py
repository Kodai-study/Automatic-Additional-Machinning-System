import serial


serPort = serial.Serial("COM4", 19200, timeout=1)

while True:
    str = input()
    if (str == "bye"):
        break

    serPort.write((str + "\r").encode('utf-8'))
    print((str + "\r"))
