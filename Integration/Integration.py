from queue import Queue
from GUIDesigner.GUIDesigner import GUIDesigner

from RobotCommunicationHandler.RobotCommunicationHandler import RobotCommunicationHandler
from threading import Thread


class Integration:
    def __init__(self):
        self.ur_send_queue = Queue()
        self.cfd_send_queue = Queue()
        self.send_queue = Queue()
        self.receiv_queue = Queue()

    def main(self):

        communicationHandler = RobotCommunicationHandler()
        guiDesigner = GUIDesigner()
        self.communication_thread = Thread(
            target=communicationHandler.communication_loop,
            args=(self.ur_send_queue, self.cfd_send_queue))
        self.communication_thread.start()
        guiDesigner.start_gui(self.send_queue, self.receiv_queue)
