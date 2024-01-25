from threading import Thread
import time
from GUIDesigner.GUISignalCategory import GUISignalCategory
from ImageInspectionController.InspectDatas import PreProcessingInspectionData, ToolInspectionData
from ImageInspectionController.InspectionResults import PreProcessingInspectionResult
from ImageInspectionController.OperationType import OperationType
from Integration.ProcessDataManager import ProcessDataManager
from common_data_type import TransmissionTarget, WorkPieceShape
from test_flags import TEST_CFD_CONNECTION_LOCAL, TEST_UR_CONNECTION_LOCAL
from ImageInspectionController.ProcessDatas import HoleCheckInfo, HoleType
from common_data_type import Point

TEST_WAIT_COMMAND = True
CYLINDRE_WAIT_TIME = 2


def reservation_process():
    print("加工の予約が行われました")


def _test_regist_process_count(integration_instance):
    integration_instance.process_list = integration_instance.process_data_manager.refresh_process_data()
    integration_instance.process_list[0]["regist_process_count"] = 1
    integration_instance.process_list[1]["regist_process_count"] = 2
    integration_instance.process_list[5]["regist_process_count"] = 7
    integration_instance.process_data_manager.register_process_number()


def start_process(integration_instance):
    send_to_CFD(integration_instance, "STM 0,SEARCH")
    # initial_tool_inspection(integration_instance)
    # TODO ワークの個数を取得する
    time.sleep(1)
    send_to_CFD(integration_instance, "MODE 0,RESERVE_SET")
    _test_regist_process_count(integration_instance)
    process_data_manager: ProcessDataManager = integration_instance.process_data_manager

    while not work_process(integration_instance, process_data_manager):
        pass


def initial_tool_inspection(integration_instance):
    for stock_number in range(1, 9):
        send_to_CFD(integration_instance, "STM 0,R,1")
        wait_command(integration_instance, "CFD", "STM 0,TURNED")

        result = integration_instance.image_inspection_controller.perform_image_operation(
            OperationType.TOOL_INSPECTION, ToolInspectionData(is_initial_phase=True, tool_position_number=stock_number))
        print(f"工具{stock_number}個めの検査 : 結果 {result}")
        if not result.result:
            integration_instance.gui_request_queue.put(
                GUISignalCategory.CANNOT_CONTINUE_PROCESSING, f"{stock_number}個の工具がエラーです")
            return


skip_wait_size = False


def work_process(integration_instance, process_data_manager):
    global skip_wait_size
    is_last_work, m = process_data_manager.get_next_process_data()
    if m is None:
        return True
    integration_instance.process_manager.start_process(m)
    if not integration_instance.process_manager.check_tool_ok():
        print("工具が足りません")
        return True

    if not skip_wait_size:
        wait_command(integration_instance, "UR", "SIZE 0,ST")
    else:
        skip_wait_size = False
    size = integration_instance.process_manager.get_work_size()
    send_to_UR(integration_instance, f"SIZE 0,{size}")
    wait_command(integration_instance, "UR", "CYL 0,PUSH")
    send_to_CFD(integration_instance, "CYL 0,PUSH")
    time.sleep(CYLINDRE_WAIT_TIME)
    send_to_CFD(integration_instance, "CYL 0,PULL")
    # TODO 加工前検査
    time.sleep(CYLINDRE_WAIT_TIME)
    print("加工前検査をします")
    workShape = WorkPieceShape.get_work_shape_from_str(m["workShape"])

    preprocess_inspection_result = integration_instance.image_inspection_controller.perform_image_operation(
        OperationType.PRE_PROCESSING_INSPECTION, PreProcessingInspectionData(workShape, m["holes"]))

    if not preprocess_inspection_result.result:
        print("加工前検査に失敗しました")

    send_to_CFD(integration_instance, "CYL 0,PUSH")
    tool_degrees = integration_instance.process_manager.get_first_tool_degrees()
    rotato_tool_stock(integration_instance, tool_degrees)

    drill_process(integration_instance)

    # send_to_CFD(integration_instance, "DRL 0,0,0,8")
    wait_command(integration_instance, "CFD", "DRL 0,TOOL_DETACHED")
    send_to_CFD(integration_instance, "CYL 0,PULL")
    send_to_UR(integration_instance, "WRK 0,TAP_FIN")
    wait_command(integration_instance, "UR", "WRK 0,ATT_POSE")
    grip_position = integration_instance.process_manager.get_grip_position()
    send_to_UR(integration_instance,
               f"WRK 0,{grip_position[0]},{grip_position[1]}")
    wait_command(integration_instance, "UR", "CYL 4,PUSH")

    if is_last_work:
        is_switch_model = inspect_and_carry_out(
            integration_instance, process_data_manager, m)
        wait_command(integration_instance, "UR", "SIZE 0,ST")
        if is_switch_model:
            print("ワークの交換を行います")
            send_to_UR(integration_instance, "SIZE 0,0")
        else:
            skip_wait_size = True
    else:
        inspect_and_carry_out(
            integration_instance, process_data_manager, m)


def inspect_and_carry_out(integration_instance, process_data_manager, m):
    preprocess_inspection_result = integration_instance.image_inspection_controller.perform_image_operation(
        OperationType.ACCURACY_INSPECTION, create_inspection_information(m))
    process_data_manager.processing_finished(
        preprocess_inspection_result.result)
    send_to_CFD(integration_instance,
                f"INSPCT 0,{'OK' if preprocess_inspection_result.result else 'NG'}")
    return preprocess_inspection_result.result


def create_inspection_information(json_data):
    hole_information_data = json_data["holes"]
    hole_check_informations = []
    for hole_id, hole in enumerate(hole_information_data):
        point = Point(hole["position"]["x"], hole["position"]["y"])
        hole_check_informations.append(HoleCheckInfo(
            hole_id, point,
            HoleType.get_hole_type_from_str(hole["size"]), None)
        )
    return hole_check_informations


def drill_process(integration_instance):
    previous_x_position = 0
    previous_y_position = 0
    while True:
        next_process_data = integration_instance.process_manager.get_next_position()
        if next_process_data is None:
            print("加工終了\n")
            break
        (x_position, y_position,
         drill_speed), tool_degree = next_process_data

        if tool_degree:
            send_to_CFD(integration_instance, "DRL 0,0,0,8")
            wait_command(integration_instance, "CFD", "DRL 0,TOOL_DETACHED")
            preprocess_inspection_result = integration_instance.image_inspection_controller.perform_image_operation(
                OperationType.TOOL_INSPECTION, ToolInspectionData(False, integration_instance.process_manager.current_tool_type))
            if not preprocess_inspection_result.result:
                print("工具検査に失敗しました")
                return
            rotato_tool_stock(integration_instance, tool_degree)
            previous_x_position = 0
            previous_y_position = 0

        send_to_CFD(integration_instance,
                    f"DRL 0,{x_position-previous_x_position},{y_position-previous_y_position},{drill_speed}")
        wait_command(integration_instance, "CFD", "DRL 0,XYT_IS_SET")
        previous_x_position = x_position
        previous_y_position = y_position
        print(f"{x_position} , {y_position}にM{drill_speed}の穴をあけた")
    send_to_CFD(integration_instance, "DRL 0,0,0,8")


def send_to_CFD(integration_instance, message):
    if not message.endswith("\n") and not message.endswith("\r"):
        message += "\n"
    integration_instance.send_request_queue.put(
        {"target": TransmissionTarget.TEST_TARGET_2 if TEST_CFD_CONNECTION_LOCAL else TransmissionTarget.CFD,
         "message": message})


def send_to_UR(integration_instance, message):
    if not message.endswith("\n") and not message.endswith("\r"):
        message += "\n"
    integration_instance.send_request_queue.put(
        {"target": TransmissionTarget.TEST_TARGET_1 if TEST_UR_CONNECTION_LOCAL else TransmissionTarget.UR,
         "message": message})


def rotato_tool_stock(integration_instance, degress_number):
    send_to_CFD(integration_instance, f"STM 0,R,{degress_number}")
    time.sleep(3)
    # wait_command(integration_instance, "CFD", "STM 0,TURNED")
    print(f"工具ストッカを{degress_number}個分回転させた")


def wait_command(integration, robot, command):
    if not TEST_WAIT_COMMAND:
        return

    print(f"次のコマンドを待機中…    {robot}からのコマンド : {command}")
    if not command.endswith("\n"):
        command += "\n"

    if robot == "CFD":
        target = TransmissionTarget.TEST_TARGET_2 if TEST_CFD_CONNECTION_LOCAL else TransmissionTarget.CFD
    elif robot == "UR":
        target = TransmissionTarget.TEST_TARGET_1 if TEST_UR_CONNECTION_LOCAL else TransmissionTarget.UR
    condition = integration._regist_wait_command(target, command)
    with condition:
        condition.wait()
