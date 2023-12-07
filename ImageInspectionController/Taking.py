from ImageInspectionController.ProcessDatas import InspectionType
from ImageInspectionController.light import Light


class Taking:
    def take_picuture(self, kensamei: InspectionType) -> str:
        if (kensamei == InspectionType.PRE_PROCESSING_INSPECTION):
            ONorOFF = "ON"
            houkoku = Light.light_on(kensamei, ONorOFF)
            if (houkoku == "OK"):
                print("satuei")
                return "ImageInspectionController/QR.png"

        elif kensamei == InspectionType.ACCURACY_INSPECTION:
            ONorOFF = "ON"
            houkoku = Light.light_on(kensamei, ONorOFF)
            if (houkoku == "OK"):
                print("satuei")
                return "ImageInspectionController/test/ana.png"

        elif kensamei == InspectionType.TOOL_INSPECTION:
            ONorOFF = "ON"
            houkoku = Light.light_on(kensamei, ONorOFF)
            if (houkoku == "OK"):
                print("satuei")
                return "ImageInspectionController/test/drill.png"
        return None
