from queue import Queue
from GUIDesigner.GUIDesigner import GUIDesigner


def test_gui():
    send_queue = Queue()
    receive_queue = Queue()
    gui = GUIDesigner()
    gui.start_gui(send_queue, receive_queue)


if __name__ == "__main__":
    test_gui()
