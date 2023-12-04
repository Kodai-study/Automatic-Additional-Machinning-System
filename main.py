from queue import Queue
from GUIDesigner.GUIDesigner import GUIDesigner
from ImageInspectionController.ProcessDatas import InspectionType
from ImageInspectionController.Taking import Taking
from Integration.Integration import Integration
from RobotCommunicationHandler.RobotCommunicationHandler import RobotCommunicationHandler


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
    taking=Taking()
    a=taking.take_picuture(InspectionType.TOOL_INSPECTION)
    print(a)