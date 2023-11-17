import serial
from ImageInspectionController.ProcessDatas import InspectionType
from light_control import Light_control


class Light:
    def __init__(self):
        self.IOBOARD_PID = 2050
        self.IOBOARD_VID = 10777
        # self.dic = {Camera_type.Accuracy: 1,
        #             Camera_type.Inspection: 2, Camera_type.Preprocessing: 3}
        self.IT = {InspectionType.ACCURACY_INSPECTION: 1,
                   InspectionType.PRE_PROCESSING_INSPECTION:2,InspectionType.TOOL_INSPECTION:3}
    '''def light_on(kensamei:InspectionType,ONorOFF)->str:
        if(kensamei==InspectionType.ACCURACY_INSPECTION):
            ONorOFF="ON"
            Light_control.light_switch(kensamei,ONorOFF)
            
        return "OK"
    '''
    def light_switch(self, camera: InspectionType, ONorOFF="NONE"):
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

        if ONorOFF == "ON":
            cmd = cmd + " set "
        elif ONorOFF == "OFF":
            cmd = cmd + " clear "

        cmd = cmd + str(self.IT[camera])
        serPort.write((cmd + "\r").encode('utf-8'))
if __name__ == "__main__":
    Light.light_switch(InspectionType.ACCURACY_INSPECTION,"ON")