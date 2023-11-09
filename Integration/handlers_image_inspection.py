
from ImageInspectionController.ImageInspectionController import ImageInspectionController
from ImageInspectionController.InspectDatas import PreProcessingInspectionData, ToolInspectionData
from ImageInspectionController.OperationType import OperationType
from ImageInspectionController.ProcessDatas import HoleCheckInfo, HoleType
from Integration.handlers_database import write_database_process
from common_data_type import Point, WorkPieceShape


def _start_accuracy_inspection_inspection(image_inspection_controller: ImageInspectionController):
    test_list = [HoleCheckInfo(hole_id=1, hole_position=Point(
        50.0, 50.0), hole_type=HoleType.M3_HOLE)]
    accuracy_inspection_result = image_inspection_controller.perform_image_operation(
        OperationType.ACCURACY_INSPECTION, test_list)
    print("加工後の精度検査を行いました。 \n", accuracy_inspection_result)


def _start_pre_processing_inspection(image_inspection_controller: ImageInspectionController, work_list: list, process_list: list, database_accesser):
    pre_processing_inspection_result = image_inspection_controller.perform_image_operation(
        OperationType.PRE_PROCESSING_INSPECTION, PreProcessingInspectionData(workpiece_shape=WorkPieceShape.SQUARE, work_dimension=30.0))
    max_process_item = max(
        (item for item in work_list if item["serial_number"] is None),
        key=lambda x: x["process"].value,
        default=None
    )
    max_process_item["serial_number"] = pre_processing_inspection_result.serial_number
    if not pre_processing_inspection_result.result:
        process_list.clear()
    else:
        for item in process_list:
            write_database_process(
                database_accesser, item["process_type"], pre_processing_inspection_result.serial_number)
        process_list.clear()

    
    print("加工前の検査を行いました。 \n", pre_processing_inspection_result)


def _start_tool_inspeciton(image_inspection_controller: ImageInspectionController):
    inspection_result = image_inspection_controller.perform_image_operation(
        OperationType.TOOL_INSPECTION, ToolInspectionData(is_initial_phase=True, tool_position_number=1))
    print("工具の検査を行いました。 \n", inspection_result)
