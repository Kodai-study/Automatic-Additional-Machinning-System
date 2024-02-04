from ImageInspectionController.ProcessDatas import InspectionType


class Taking:
    def take_picuture(self, kensamei: InspectionType) -> str:
        return self._test_takepicture_ok(kensamei)

    def _test_takepicture_ok(self, kensamei: InspectionType) -> str:
        if (kensamei == InspectionType.PRE_PROCESSING_INSPECTION):
            ONorOFF = "ON"
            return "ImageInspectionController/test/pre_process_inspection/sample_images/circle_r0.png"

        elif kensamei == InspectionType.ACCURACY_INSPECTION:
            ONorOFF = "ON"
            return "ImageInspectionController/test/ana.png"

        elif kensamei == InspectionType.TOOL_INSPECTION:
            ONorOFF = "ON"
            return "ImageInspectionController/test/drill.png"
        return None
