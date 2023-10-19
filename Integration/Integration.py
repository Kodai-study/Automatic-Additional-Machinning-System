from queue import Queue
import time
from GUIDesigner.GUIDesigner import GUIDesigner
from RobotCommunicationHandler.RobotCommunicationHandler \
    import TEST_PORT1, TEST_HOST, RobotCommunicationHandler, TransmissionTarget
from threading import Thread
from RobotCommunicationHandler.test_ur import _test_ur


TEST_FLAG = True


class Integration:

    def __init__(self):
        self.ur_send_queue = Queue()
        self.cfd_send_queue = Queue()
        self.send_queue = Queue()
        self.receiv_queue = Queue()
        if (TEST_FLAG):
            self.test_ur = _test_ur(TEST_PORT1)

    def test_send(self):
        while True:
            self.ur_send_queue.put(
                {"target": TransmissionTarget.TEST_TARGET_1, "message": "test"})
            time.sleep(5)

    def main(self):
        communicationHandler = RobotCommunicationHandler()
        guiDesigner = GUIDesigner()
        self.communication_thread = Thread(
            target=communicationHandler.communication_loop,
            args=(self.ur_send_queue, self.cfd_send_queue))
        self.communication_thread.start()

        if (TEST_FLAG):
            test_ur_thread = Thread(target=self.test_ur.start)
            test_ur_thread.start()
            test_send_thread = Thread(target=self.test_send)
            test_send_thread.start()
            
        guiDesigner.start_gui(self.send_queue, self.receiv_queue)
