from queue import Queue
import time
from GUIDesigner.GUIDesigner import GUIDesigner
from ImageInspectionController.ImageInspectionController import ImageInspectionController
from ImageInspectionController.InspectDatas import PreProcessingInspectionData, ToolInspectionData
from ImageInspectionController.OperationType import OperationType
from ImageInspectionController.ProcessDatas import HoleCheckInfo, HoleType, InspectionType
from ImageInspectionController.Taking import Taking
from Integration.Integration import Integration
from RobotCommunicationHandler.RobotCommunicationHandler import RobotCommunicationHandler
from common_data_type import CameraType, LightingType, Point, WorkPieceShape


def test_gui():
    send_queue = Queue()
    receive_queue = Queue()
    gui = GUIDesigner()
    gui.start_gui(send_queue, receive_queue)


def test_communicaion():
    send_queue = Queue()
    receive_queue = Queue()
    communication_handler = RobotCommunicationHandler()
    communication_handler.communication_loop(send_queue, receive_queue)


def test_integration():
    integration = Integration()
    integration.main()


def test_camera_snapshot():
    camera_list = [CameraType.ACCURACY_CAMERA,
                   CameraType.PRE_PROCESSING_CAMERA, CameraType.TOOL_CAMERA]
    image_inspection_controller = ImageInspectionController()

    list = image_inspection_controller.perform_image_operation(
        OperationType.TAKE_INSPECTION_SNAPSHOT, camera_list)
    print(list)


def test_take_picture():
    taking = Taking()
    inspection_types = [
        InspectionType.TOOL_INSPECTION,
        InspectionType.ACCURACY_INSPECTION,
        InspectionType.PRE_PROCESSING_INSPECTION
    ]
    for inspection in inspection_types:
        print(taking.take_picture(inspection))


def test_inspections():
    image_inspection_controller = ImageInspectionController()

    result = image_inspection_controller.perform_image_operation(
        OperationType.PRE_PROCESSING_INSPECTION, PreProcessingInspectionData(WorkPieceShape.SQUARE, work_dimension=30))
    print(f"PRE_PROCESSING_INSPECTION: {result}")
    test_hole_infos = [
        HoleCheckInfo(1, Point(20.003, 20.115),
                      HoleType.M3_HOLE, None),
        HoleCheckInfo(2, Point(19.964, 30.096),
                      HoleType.M4_HOLE, None),
        HoleCheckInfo(3, Point(20.007, 40.092),
                      HoleType.M5_HOLE, None),
        HoleCheckInfo(4, Point(19.994, 50.077),
                      HoleType.M6_HOLE, None),
        HoleCheckInfo(5, Point(40.017, 20.1),
                      HoleType.M3_HOLE, None),
        HoleCheckInfo(6, Point(40.018, 30.105),
                      HoleType.M4_HOLE, None),
        HoleCheckInfo(7, Point(40.02, 40.097),
                      HoleType.M5_HOLE, None),
        HoleCheckInfo(8, Point(40.021, 50.061),
                      HoleType.M6_HOLE, None)
    ]
    result = image_inspection_controller.perform_image_operation(
        OperationType.ACCURACY_INSPECTION, (test_hole_infos, 100))

    print(f"ACCURACY_INSPECTION: {result}")

    result = image_inspection_controller.perform_image_operation(
        OperationType.TOOL_INSPECTION, ToolInspectionData(is_initial_phase=True, tool_position_number=1))
    print(f"TOOL_INSPECTION: {result}")


def test_lighting():
    light_state = True
    image_inspection_controller = ImageInspectionController()
    while True:

        result = image_inspection_controller.perform_image_operation(
            OperationType.CONTROL_LIGHTING, (LightingType.PRE_PROCESSING_LIGHTING, light_state))
        print(f"加工前検査照明テスト: {result}")

        result = image_inspection_controller.perform_image_operation(
            OperationType.CONTROL_LIGHTING, (LightingType.ACCURACY_LIGHTING, light_state))
        print(f"精度検査照明テスト: {result}")

        result = image_inspection_controller.perform_image_operation(
            OperationType.CONTROL_LIGHTING, (LightingType.TOOL_LIGHTING, light_state))
        print(f"工具検査照明テスト: {result}")
        light_state = not light_state
        time.sleep(5)


if __name__ == "__main__":
    # test_integration()
    # test_camera_snapshot()
    test_inspections()
    # test_take_picture()
