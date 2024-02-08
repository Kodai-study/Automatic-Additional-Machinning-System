import configparser
import serial.tools.list_ports
from ImageInspectionController.ProcessDatas import InspectionType


class Light:
    def __init__(self):
        self.config = configparser.ConfigParser()
        file_path = 'kensa.conf'
        self.config.read(file_path, encoding='utf-8')
        ports = list(serial.tools.list_ports.comports())
        section_name = "gpio"
        self.IOBOARD_PID = self.config.getint(section_name, "IOBOARD_PID")
        self.IOBOARD_VID = self.config.getint(section_name, "IOBOARD_VID")
        self.pin_number_dict = {
            InspectionType.ACCURACY_INSPECTION: self.config.getint("Light_information", "ACCURACY_INSPECTION_pinnumber"),
            InspectionType.TOOL_INSPECTION: self.config.getint("Light_information", "TOOL_INSPECTION_pinnumber"),
            InspectionType.PRE_PROCESSING_INSPECTION: [
                self.config.getint("Light_information",
                                   "PRE_PROCESSING_INSPECTION_pinnumber1"),
                self.config.getint("Light_information",
                                   "PRE_PROCESSING_INSPECTION_pinnumber2")
            ]
        }
        com_num = None
        for port in ports:
            if port.pid == self.IOBOARD_PID and port.vid == self.IOBOARD_VID:
                com_num = port.device

        if com_num is None:
            print("COMポートが見つかりませんでした。")
        else:
            self.serPort = serial.Serial(com_num, 19200, timeout=1)
            print(f"COMポート {com_num} を使用します。")

    def _getpinnum(self, camera: InspectionType):
        return self.pin_number_dict[camera]

    def light_onoff(self, camera: InspectionType, ONorOFF) -> str:
        if ONorOFF == "ON":
            cmd = "set"
        elif ONorOFF == "OFF":
            cmd = "clear"

        gpio_pin_number = self._getpinnum(camera)
        if camera == InspectionType.PRE_PROCESSING_INSPECTION:
            self.serPort.write(
                f"gpio {cmd} {gpio_pin_number[0]}\r".encode('utf-8'))
            self.serPort.write(
                f"gpio {cmd} {gpio_pin_number[1]}\r".encode('utf-8'))
        else:
            self.serPort.write(
                f"gpio {cmd} {gpio_pin_number}\r".encode('utf-8'))

        return "OK"
