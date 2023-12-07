from queue import Queue
import time
from GUIDesigner.GUIDesigner import GUIDesigner
from ImageInspectionController.ProcessDatas import InspectionType
from ImageInspectionController.Taking import Taking
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
    L = Light()
    T = Taking()
    time.sleep(1)
    L.light_onoff(InspectionType.TOOL_INSPECTION, "ON")
    time.sleep(1)
    L.light_onoff(InspectionType.PRE_PROCESSING_INSPECTION, "ON")
    time.sleep(1)
    L.light_onoff(InspectionType.ACCURACY_INSPECTION, "ON")
    T.take_picture(InspectionType.TOOL_INSPECTION)
    L.light_onoff(InspectionType.TOOL_INSPECTION, "OFF")
    time.sleep(1)
    L.light_onoff(InspectionType.PRE_PROCESSING_INSPECTION, "OFF")
    time.sleep(1)
    L.light_onoff(InspectionType.ACCURACY_INSPECTION, "OFF")
