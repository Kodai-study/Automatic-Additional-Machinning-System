from enum import Enum, auto
import serial.tools.list_ports


class Camera_type(Enum):
    Inspection = auto()
    Preprocessing = auto()
    # Accuracy = auto()
    Accuracy = auto()


class light_output(Enum):
    ON = auto()
    OFF = auto()


class Light_control:

    def __init__(self):
        self.IOBOARD_PID = 2050
        self.IOBOARD_VID = 10777
        # self.dic = {Camera_type.Accuracy: 1,
        self.dic = {Camera_type.Accuracy: 1,
                    Camera_type.Inspection: 2, Camera_type.Preprocessing: 3}

    def light_switch(self, camera: Camera_type, output: light_output):
        """
        任意の照明のON/OFFを制御する

        Args:
            camera (Camera_type): カメラの種類。
            output (light_output): 照明をON/OFFどちらに制御するか
        """
        # COMポートの一覧を取得
        ports = list(serial.tools.list_ports.comports())
        com_num = None

        for port in ports:
            if port.pid == self.IOBOARD_PID and port.vid == self.IOBOARD_VID:
                com_num = port.device

        if com_num is None:
            print("COMポートが見つかりませんでした。")
            return

        else:
            serPort = serial.Serial(com_num, 19200, timeout=1)
            print(f"COMポート {com_num} を使用します。")

        cmd = "gpio"

        if output == light_output.ON:
            cmd = cmd + " set "
        elif output == light_output.OFF:
            cmd = cmd + " clear "

        cmd = cmd + str(self.dic[camera])
        serPort.write((cmd + "\r").encode('utf-8'))


if __name__ == "__main__":
    l = Light_control()
    # l.light_switch(Camera_type.Accuracy, light_output.OFF)
    l.light_switch(camera=Camera_type.Accuracy, output=light_output.OFF)
