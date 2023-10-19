from queue import Queue
from GUIDesigner.GUIDesigner import GUIDesigner
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


if __name__ == "__main__":
    test_communicaion()
