from ImageInspectionController.ProcessDatas import InspectionType
from ImageInspectionController.light import Light


class Taking:
    def take_picuture(kensamei:InspectionType)->str:
        if(kensamei==InspectionType.PRE_PROCESSING_INSPECTION):
            ONorOFF="ON"
            houkoku = Light.light_on(kensamei,ONorOFF)
            if(houkoku=="OK"):
                print("satuei")
                return "/home/kuga/ソフトウェア/Automatic-Additional-Machinning-System/img/drill.png"
        return 0

       
 