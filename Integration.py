from queue import Queue
from test_classes import RobotCommunicationHandler, stop_flag
from threading import Thread
from test_gui import GUIDesigner


class Integration:
    def __init__(self):
        pass

    def main(self):
        self.test_module_control()
        

    def test_module_control(self):
        self.send_queue = Queue()
        self.receiv_queue = Queue()

        robot_communication_handler = RobotCommunicationHandler()
        gui_designer = GUIDesigner()

        self.communication_thread = Thread(
            target=robot_communication_handler.communication_loop,args=(self.send_queue, self.receiv_queue))
        self.gui_thread = Thread(target=gui_designer.start_gui,args=(self.send_queue, self.receiv_queue))

        self.communication_thread.start()
        self.gui_thread.start()

        while(input() != "bye"):
            pass
        



if __name__ == "__main__":
    integration = Integration()
    integration.main()