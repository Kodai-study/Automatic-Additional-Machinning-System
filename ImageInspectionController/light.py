from ImageInspectionController.ProcessDatas import InspectionType


class Light:
    def light_on(self, kensamei: InspectionType, ONorOFF) -> str:
        self._test_control_light_ok(kensamei, ONorOFF)

    def _test_control_light_ok(self, kensamei: InspectionType, ONorOFF) -> str:
        if (kensamei == InspectionType.PRE_PROCESSING_INSPECTION):
            if (ONorOFF == "ON"):
                print("ON")
            else:
                print("OFF")
        return "OK"
