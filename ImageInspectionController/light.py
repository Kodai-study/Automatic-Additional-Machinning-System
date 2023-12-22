from test_flags import TEST_CFD_CONNECTION_LOCAL, TEST_UR_CONNECTION_LOCAL, TEST_FEATURE_GUI, TEST_FEATURE_IMAGE_PROCESSING
import configparser
if TEST_FEATURE_IMAGE_PROCESSING:
    import serial
    import yaml
    from light_control import Light_control
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
        pin_numbers = self.data['Light_information']['pinnumbers']
        if camera == InspectionType.ACCURACY_INSPECTION:
            pinnum = pin_numbers['ACCURACY_INSPECTION']
        elif camera == InspectionType.PRE_PROCESSING_INSPECTION:
            pinnum = pin_numbers['PRE_PROCESSING_INSPECTION']
        elif camera == InspectionType.TOOL_INSPECTION:
            pinnum = pin_numbers['TOOL_INSPECTION']
        return pinnum

    def light_onoff(self, camera: InspectionType, ONorOFF) -> str:
        if ONorOFF == "ON":
            cmd = "set"
        elif ONorOFF == "OFF":
            cmd = "clear"
        gpio_pin_number = self._getpinnum(camera)
        self.serPort.write(f"gpio {cmd} {gpio_pin_number}\r".encode('utf-8'))
        return "OK"
