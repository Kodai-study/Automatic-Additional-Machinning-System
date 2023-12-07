from queue import Queue
import time
from GUIDesigner.GUIDesigner import GUIDesigner
from ImageInspectionController.ProcessDatas import InspectionType
from ImageInspectionController.Taking import Taking
from ImageInspectionController.light import Light
from ImageInspectionController.ImageInspectionController import ImageInspectionController
from ImageInspectionController.InspectDatas import PreProcessingInspectionData, ToolInspectionData
from ImageInspectionController.OperationType import OperationType
from Integration.Integration import Integration
from RobotCommunicationHandler.RobotCommunicationHandler import RobotCommunicationHandler
import light_control
from common_data_type import CameraType, LightingType, WorkPieceShape


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


def test_inspections():
    image_inspection_controller = ImageInspectionController()

    result = image_inspection_controller.perform_image_operation(
        OperationType.PRE_PROCESSING_INSPECTION, PreProcessingInspectionData(WorkPieceShape.CIRCLE, work_dimension=30))
    print(f"PRE_PROCESSING_INSPECTION: {result}")

    result = image_inspection_controller.perform_image_operation(
        OperationType.ACCURACY_INSPECTION, 5)
    print(f"ACCURACY_INSPECTION: {result}")

    result = image_inspection_controller.perform_image_operation(
        OperationType.TOOL_INSPECTION, ToolInspectionData(is_initial_phase=True, tool_position_number=1))
    print(f"TOOL_INSPECTION: {result}")


def test_lighting():
    image_inspection_controller = ImageInspectionController()

    result = image_inspection_controller.perform_image_operation(
        OperationType.CONTROL_LIGHTING, (LightingType.PRE_PROCESSING_LIGHTING, True))
    print(f"加工前検査照明テスト: {result}")

    result = image_inspection_controller.perform_image_operation(
        OperationType.CONTROL_LIGHTING, (LightingType.ACCURACY_LIGHTING, True))
    print(f"精度検査照明テスト: {result}")

    result = image_inspection_controller.perform_image_operation(
        OperationType.CONTROL_LIGHTING, (LightingType.TOOL_LIGHTING, False))
    print(f"工具検査照明テスト: {result}")


if __name__ == "__main__":
    # test_camera_snapshot()
    test_lighting()
