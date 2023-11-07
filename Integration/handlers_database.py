
import datetime
from DBAccessHandler.DBAccessHandler import DBAccessHandler

instruction_table_dictionary = {
    "SNS": "t_sensor_tracking",
    "PROCESS": "t_work_tracking"
}


def write_database(database_accesser: DBAccessHandler, instruction, dev_num, detail, sensor_date_time: datetime.datetime, serial_num: int):
    database_accesser.write_data_to_database(create_sql(
        instruction, dev_num, detail, sensor_date_time, serial_num))


def create_sql(instruction, dev_num, detail, sensor_date_time: datetime.datetime, serial_num: int):
    if instruction == "SNS":
        return _create_sql_sns(dev_num, detail, sensor_date_time, serial_num)


def _single_insert(instruction):
    return f"INSERT INTO {instruction_table_dictionary[instruction]} "


def _create_sql_sns(dev_num, detail: str, sensor_date_time: datetime.datetime, serial_num: int):
    sql = _single_insert("SNS")
    sensor_status = 1 if detail == "ON" else 0
    sql += f"""(sensor_id,sensor_status,sensor_date_time) VALUES ({
        dev_num},{sensor_status},'{sensor_date_time.strftime('%Y-%m-%d %H:%M:%S')}');"""

    is_write_process = False
    if dev_num == 3 and detail == "ON":
        process_num = 1
        is_write_process = True
    elif dev_num == 4 and detail == "ON":
        process_num = 4
        is_write_process = True

    if is_write_process:
        sql += "\n"
        sql += f"""INSERT INTO {instruction_table_dictionary["PROCESS"]} (serial_number,process_id,process_time) VALUES ({serial_num},{process_num},
       '{sensor_date_time.strftime('%Y-%m-%d %H:%M:%S')}');"""

    return sql
