from queue import Queue
import time
from GUIDesigner.GUIDesigner import GUIDesigner
from RobotCommunicationHandler.RobotCommunicationHandler \
    import TEST_PORT1, TEST_HOST, RobotCommunicationHandler, TransmissionTarget
from threading import Thread
from RobotCommunicationHandler.test_ur import _test_ur


TEST_UR_CONN = True


class Integration:

    def __init__(self):
        self.ur_send_queue = Queue()
        self.cfd_send_queue = Queue()
        self.send_queue = Queue()
        self.receiv_queue = Queue()
        if (TEST_UR_CONN):
            self.test_ur = _test_ur(TEST_PORT1)

    def test_send(self):
        while True:
            self.ur_send_queue.put(
                {"target": TransmissionTarget.TEST_TARGET_1, "message": "test"})
            time.sleep(5)

    def test_watching_send_queue(self):
        while True:
            if not self.send_queue.empty():
                # send_queueから値を取り出す
                send_data = self.send_queue.get()
                self.ur_send_queue.put(
                    {"target": TransmissionTarget.TEST_TARGET_1, "message": str(send_data)})
            time.sleep(0.1)

    def main(self):
        communicationHandler = RobotCommunicationHandler()
        guiDesigner = GUIDesigner()
        self.communication_thread = Thread(
            target=communicationHandler.communication_loop,
            args=(self.ur_send_queue, self.cfd_send_queue))
        self.communication_thread.start()

        if (TEST_UR_CONN):
            test_ur_thread = Thread(target=self.test_ur.start)
            test_ur_thread.start()
            test_send_thread = Thread(target=self.test_watching_send_queue)

        test_send_thread.start()
        guiDesigner.start_gui(self.send_queue, self.receiv_queue)
