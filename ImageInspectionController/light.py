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

    def light_on(self, camera: InspectionType, ONorOFF="NONE")->str:
        """指定された検査名から指定の照明をONまたはOFFする。
        引数から検査の種類とONまたはOFFを受け取り、返り値としてOKもしくは
        エラーを示すERを返す。

        Args:
            camera (InspectionType): _description_
            ONorOFF (str, optional): "ON"or"OFF". Defaults to "NONE".

        Returns:
            str:"OK" 
                "ER"
        """
        # COMポートの一覧を取得
        ports = list(serial.tools.list_ports.comports())
        com_num = None

        for port in ports:
            if port.pid == self.IOBOARD_PID and port.vid == self.IOBOARD_VID:
                com_num = port.device

        if com_num is None:
            print("COMポートが見つかりませんでした。")
            return "ER"

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
        return "OK"
