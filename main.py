from queue import Queue
from GUIDesigner.GUIDesigner import GUIDesigner
from ImageInspectionController.ImageInspectionController import ImageInspectionController
from ImageInspectionController.InspectDatas import PreProcessingInspectionData, ToolInspectionData
from ImageInspectionController.OperationType import OperationType
from ImageInspectionController.ProcessDatas import InspectionType
from Integration.Integration import Integration
from RobotCommunicationHandler.RobotCommunicationHandler import RobotCommunicationHandler
from common_data_type import WorkPieceShape


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


if __name__ == "__main__":
    # img_pass=ImageInspectionController.test(InspectionType.PRE_PROCESSING_INSPECTION)
    # print(img_pass) 
    image_inspection_controller = ImageInspectionController()
    #a=image_inspection_controller.perform_image_operation(OperationType.PRE_PROCESSING_INSPECTION,PreProcessingInspectionData(WorkPieceShape.CIRCLE,work_dimension=30) )
    #a=image_inspection_controller.perform_image_operation(OperationType.ACCURACY_INSPECTION,5)
    # image_inspection_controller.perform_image_operation(OperationType.CONTROL_LIGHTING)
    # image_inspection_controller.perform_image_operation(OperationType.TAKE_INSPECTION_SNAPSHOT)
    a=image_inspection_controller.perform_image_operation(OperationType.TOOL_INSPECTION,ToolInspectionData(is_initial_phase=True,tool_position_number=1))
    print(a)