from queue import Queue

from ..RobotCommunicationHandler.RobotCommunicationHandler import RobotCommunicationHandler
from threading import Thread

class Integration:
    def __init__(self):
        pass

    def main(self):

        self.ur_send_queue = Queue()
        self.cfd_send_queue = Queue()
        self.communication_thread = Thread(
            target=RobotCommunicationHandler.communication_loop)
