import datetime
from queue import Queue
from DBAccessHandler.DBAccessHandler import DBAccessHandler
from GUIDesigner.GUIDesigner import GUIDesigner
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


def test_dbAccessHandler():
    dbAccess_handler = DBAccessHandler()
    # sql_query = "SELECT * FROM t_event WHERE error_code = %s"
    # result = dbAccess_handler.fetch_data_from_database(sql_query, 2)
    # print(result)
    current_time = datetime.datetime.now()
    sql_query = "INSERT INTO t_sensor_tracking (sensor_id,sensor_status,sensor_date_time ) VALUES (%s, %s, %s)"
    is_success, error_message = dbAccess_handler.write_data_to_database(
        sql_query, (1, 1, current_time))
    print(is_success, error_message)
    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print(dbAccess_handler.fetch_data_from_database(
        "SELECT * FROM t_sensor_tracking WHERE sensor_date_time = %s", current_time))


if __name__ == "__main__":
    # test_integration()
    test_dbAccessHandler()
