
import datetime
from DBAccessHandler.DBAccessHandler import DBAccessHandler
from Integration.process_number import Processes, get_process_number

instruction_table_dictionary = {
    "SNS": "t_sensor_tracking",
    "PROCESS": "t_work_tracking"
}


def write_database(database_accesser: DBAccessHandler, instruction, dev_num, detail, sensor_date_time: datetime.datetime, serial_num: int):
    database_accesser.write_data_to_database(create_sql(
        instruction, dev_num, detail, sensor_date_time, serial_num))


def write_database_process(database_accesser: DBAccessHandler, process_num: Processes, serial_num: int):
    sql = _single_insert("PROCESS")
    sql += f""" (serial_number,process_id,process_time) VALUES ({serial_num},{process_num.value[0]},
    '{_change_mysql_time(datetime.datetime.now())}');"""
    database_accesser.write_data_to_database(sql)


def create_sql(instruction, dev_num, detail, sensor_date_time: datetime.datetime, serial_num: int):
    if instruction == "SNS":
        return _create_sql_sns(dev_num, detail, sensor_date_time, serial_num)
    elif instruction == "SIG":
        return _create_sql_sig(dev_num, detail, sensor_date_time, serial_num)


def _single_insert(instruction: str): return f"INSERT INTO {
    instruction_table_dictionary[instruction]} "


def _change_mysql_time(sensor_date_time: datetime.datetime): return sensor_date_time.strftime(
    '%Y-%m-%d %H:%M:%S')


def _create_sql_sns(dev_num, detail: str, sensor_date_time: datetime.datetime, serial_num: int):
    sql = _single_insert("SNS")
    sensor_status = 1 if detail == "ON" else 0
    sql += f"""(sensor_id,sensor_status,sensor_date_time) VALUES ({
        dev_num},{sensor_status},'{_change_mysql_time(sensor_date_time)}');"""

    process_num = get_process_number("SNS", dev_num, detail)

    if process_num is not None:
        sql += "\n"
        sql += _single_insert("PROCESS")
        sql += f""" (serial_number,process_id,process_time) VALUES ({serial_num},{process_num.value[0]},
       '{_change_mysql_time(sensor_date_time)}');"""

    return sql


def _create_sql_sig(dev_num, detail: str, sensor_date_time: datetime.datetime, serial_num: int):
    sql = _single_insert("PROCESS")
    process_num = get_process_number("SIG", dev_num, detail)

    if process_num is None:
        return ""

    sql += f""" (serial_number,process_id,process_time) VALUES \
    ({serial_num},{process_num.value[0]},'{_change_mysql_time(sensor_date_time)}');"""
    return sql
