import datetime
from queue import Queue
import time
from DBAccessHandler.DBAccessHandler import DBAccessHandler
from GUIDesigner.GUIDesigner import GUIDesigner
from ImageInspectionController.ImageInspectionController import ImageInspectionController
from ImageInspectionController.InspectDatas import PreProcessingInspectionData, ToolInspectionData
from ImageInspectionController.OperationType import OperationType
from Integration.Integration import Integration
from Integration.WorkManager import WorkManager
from Integration.process_number import Processes
from RobotCommunicationHandler.RobotCommunicationHandler import RobotCommunicationHandler
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


def test_dbAccessHandler():
    dbAccess_handler = DBAccessHandler()
    # sql_query = "SELECT * FROM t_event WHERE error_code = %s"
    # result = dbAccess_handler.fetch_data_from_database(sql_query, 2)
    # print(result)
    current_time = datetime.datetime.now()
    sql_query = "INSERT INTO t_sensor_tracking (sensor_id,sensor_status,sensor_date_time ) VALUES (%s, %s, %s)"
    is_success, error_message = dbAccess_handler.write_data_to_database(
        sql_query, (1, 1, current_time))
    print(is_success, error_message)
    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print(dbAccess_handler.fetch_data_from_database(
        "SELECT * FROM t_sensor_tracking WHERE sensor_date_time = %s", current_time))


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


if __name__ == "__main__":
    # work_manager_test()
    test_integration()
