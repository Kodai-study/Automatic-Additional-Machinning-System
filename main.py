from queue import Queue
from GUIDesigner.GUIDesigner import GUIDesigner
from ImageInspectionController.ProcessDatas import InspectionType
from ImageInspectionController.light import Light
from Integration.Integration import Integration
from RobotCommunicationHandler.RobotCommunicationHandler import RobotCommunicationHandler
import light_control


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
    L=Light()
    L.light_switch(InspectionType.ACCURACY_INSPECTION,"OFF")
