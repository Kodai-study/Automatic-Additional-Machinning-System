from GUIDesigner.GUISignalCategory import GUISignalCategory
from ImageInspectionController.InspectDatas import ToolInspectionData
from ImageInspectionController.OperationType import OperationType
from Integration.Integration import Integration
from common_data_type import TransmissionTarget
from test_flags import TEST_CFD_CONNECTION_LOCAL,TEST_UR_CONNECTION_LOCAL

def start_process():
    print("加工を開始します")


def reservation_process():
    print("加工の予約が行われました")


def change_robot_first_position():
    print("ロボットが初期位置に移動しました")
    
def _test_regist_process_count(integration_instance):
    integration_instance.process_list = integration_instance.process_data_manager.refresh_process_data()
    integration_instance.process_list[0]["regist_process_count"] = 1
    integration_instance.process_list[2]["regist_process_count"] = 2
    integration_instance.process_list[5]["regist_process_count"] = 7
    integration_instance.process_data_manager.register_process_number()


def _start_process(integration_instance:Integration):
    for stock_number in range(1, 9):
        if TEST_CFD_CONNECTION_LOCAL:
            integration_instance.send_request_queue.put(
                {"target": TransmissionTarget.TEST_TARGET_2, "message": "STM 0,R,1"})
            condition = integration_instance._regist_wait_command(
                TransmissionTarget.TEST_TARGET_2, "STM 0,TURNED")
            with condition:
                condition.wait()
        else:
            integration_instance.send_request_queue.put(
                {"target": TransmissionTarget.CFD, "message": "STM 0,R,1"})
            integration_instance._regist_wait_command(
                TransmissionTarget.CFD, "STM 0,TURNED")
            with condition:
                condition.wait()
        result = integration_instance.image_inspection_controller.perform_image_operation(
            OperationType.TOOL_INSPECTION, ToolInspectionData(is_initial_phase=True, tool_position_number=stock_number))
        print(f"工具{stock_number}個めの検査 : 結果 {result}")
        if not result.result:
            integration_instance.gui_request_queue.put(
                GUISignalCategory.CANNOT_CONTINUE_PROCESSING, f"{stock_number}個の工具がエラーです")
            return
    # TODO ワークの個数を取得する
    _test_regist_process_count(integration_instance)
    m = integration_instance.process_data_manager.get_next_process_data()
    integration_instance._regist_wait_command(
        TransmissionTarget.TEST_TARGET_1 if TEST_UR_CONNECTION_LOCAL else TransmissionTarget.UR, "SIZE 0,ST")
    