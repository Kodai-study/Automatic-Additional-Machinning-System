from ImageInspectionController.ProcessDatas import InspectionType


class Light:
    def light_on(kensamei:InspectionType,ONorOFF)->str:
        if(kensamei==InspectionType.ACCURACY_INSPECTION):
            if(ONorOFF=="ON"):
                print("ON")
            else:
                print("OFF")
        return "OK"