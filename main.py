import datetime
import json
from queue import Queue
import time
from DBAccessHandler.DBAccessHandler import DBAccessHandler
from GUIDesigner.GUIDesigner import GUIDesigner
from GUIDesigner.ProcessingData import ProcessingData
from ImageInspectionController.ImageInspectionController import ImageInspectionController
from ImageInspectionController.InspectDatas import PreProcessingInspectionData, ToolInspectionData
from ImageInspectionController.InspectionResults import ToolInspectionResult
from ImageInspectionController.OperationType import OperationType
from Integration.Integration import Integration
from Integration.ProcessManager import ProcessManager
from Integration.WorkManager import WorkManager
from Integration.process_number import Processes
from RobotCommunicationHandler.RobotCommunicationHandler import RobotCommunicationHandler
from common_data_type import CameraType, LightingType, ToolType, WorkPieceShape


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


def work_manager_test():
    work_manager = WorkManager(DBAccessHandler())
    work_manager.regist_new_process(Processes.start, datetime.datetime.now())
    work_manager.regist_new_process(
        Processes.attach_work_delivery, datetime.datetime.now())
    work_manager.regist_new_process(
        Processes.move_to_process, datetime.datetime.now())
    work_manager.preprocess_inspection(1)
    work_manager.regist_new_process(Processes.start, datetime.datetime.now())
    work_manager.regist_new_process(
        Processes.attach_work_delivery, datetime.datetime.now())
    work_manager.regist_new_process(
        Processes.start_process, datetime.datetime.now())
    work_manager.regist_new_process(
        Processes.end_process, datetime.datetime.now())
    work_manager.regist_new_process(
        Processes.move_to_process, datetime.datetime.now())
    work_manager.preprocess_inspection(1)
    work_manager.regist_new_process(
        Processes.attach_work_move_inspection, datetime.datetime.now())
    work_manager.regist_new_process(
        Processes.start_process, datetime.datetime.now())
    work_manager.regist_new_process(
        Processes.move_inspection, datetime.datetime.now())
    work_manager.regist_new_process(
        Processes.end_inspection, datetime.datetime.now())
    work_manager.regist_new_process(
        Processes.carry_out, datetime.datetime.now())


def test_process_manager():
    test_tool_stock_data = [
        None,
        ToolInspectionResult(result=True, error_items=None,
                             tool_type=ToolType.M3_DRILL, tool_length=10.0, drill_diameter=3.0),
        ToolInspectionResult(result=True, error_items=None,
                             tool_type=ToolType.M2_TAP, tool_length=10.0, drill_diameter=3.0),
        ToolInspectionResult(result=True, error_items=None,
                             tool_type=ToolType.M3_TAP, tool_length=10.0, drill_diameter=3.0),
        ToolInspectionResult(result=True, error_items=None,
                             tool_type=ToolType.M4_DRILL, tool_length=10.0, drill_diameter=3.0),
        ToolInspectionResult(result=True, error_items=None,
                             tool_type=ToolType.M4_TAP, tool_length=10.0, drill_diameter=3.0),
        ToolInspectionResult(result=True, error_items=None,
                             tool_type=ToolType.M5_DRILL, tool_length=10.0, drill_diameter=3.0),
        ToolInspectionResult(result=True, error_items=None,
                             tool_type=ToolType.M6_TAP, tool_length=10.0, drill_diameter=3.0),
        ToolInspectionResult(result=True, error_items=None,
                             tool_type=ToolType.M2_DRILL, tool_length=10.0, drill_diameter=3.0),
    ]
    process_manager = ProcessManager(test_tool_stock_data)
    with open("test/test.json", "r") as f:
        process_data = json.load(f)
    process_manager.start_process(process_data)
    a = process_manager.get_first_tool_degrees()
    while True:
        next_process_data = process_manager.get_next_position()
        if next_process_data is None:
            break
        (x_position, y_position,
         drill_speed), tool_degree = next_process_data
    process_data = None


if __name__ == "__main__":
    # work_manager_test()
    # test_integration()
    test_process_manager()
