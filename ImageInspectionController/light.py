import serial
import yaml
from ImageInspectionController.ProcessDatas import InspectionType
from light_control import Light_control


class Light:
    def __init__(self):
        ports = list(serial.tools.list_ports.comports())
        file_path = 'ImageInspectionController/kensa_config.yaml'
        with open(file_path, 'r') as yaml_file:
            self.data = yaml.safe_load(yaml_file)
        gpio_setting = self.data['Light_information']['gpio']
        self.IOBOARD_PID = gpio_setting['IOBOARD_PID']
        self.IOBOARD_VID = gpio_setting['IOBOARD_VID']        # COMポートの一覧を取得
        com_num = None

        for port in ports:
            if port.pid == self.IOBOARD_PID and port.vid == self.IOBOARD_VID:
                com_num = port.device

        if com_num is None:
            print("COMポートが見つかりませんでした。")
            return "ER"

        else:
            self.serPort = serial.Serial(com_num, 19200, timeout=1)
            print(f"COMポート {com_num} を使用します。")
        return
    
    def getpinnum(self, camera: InspectionType):
        pinnum = self.data['Light_information']['pinnumbers']
        if camera == InspectionType.ACCURACY_INSPECTION:
            pinnum = pinnum['ACCURACY_INSPECTION']
        elif camera == InspectionType.PRE_PROCESSING_INSPECTION:
            pinnum = pinnum['PRE_PROCESSING_INSPECTION']
        elif camera == InspectionType.TOOL_INSPECTION:
            pinnum = pinnum['TOOL_INSPECTION']
        return pinnum

    def light_onoff(self, camera: InspectionType, ONorOFF)->str:
        if ONorOFF == "ON":
            cmd = "set"
        elif ONorOFF == "OFF":
            cmd = "clear"
        gpio_pin_number = self.getpinnum(camera)
        self.serPort.write(f"gpio {cmd} {gpio_pin_number}\r".encode('utf-8'))
        return "OK"
