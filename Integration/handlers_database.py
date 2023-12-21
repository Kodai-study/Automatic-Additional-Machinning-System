import datetime
from DBAccessHandler.DBAccessHandler import DBAccessHandler
from Integration.process_number import Processes, get_process_number


def write_database(database_accesser: DBAccessHandler, instruction, dev_num, detail, sensor_date_time: datetime.datetime, serial_num: int):
    database_accesser.write_data_to_database(create_sql(
        instruction, dev_num, detail, sensor_date_time, serial_num))


def write_database_process(database_accesser: DBAccessHandler, process_num: Processes, serial_num: int):
    write_processing_sql = """\
    INSERT INTO t_work_tracking(
        serial_number,
        process_id,
        process_time
    )
    VALUES(
        ?,
        ?,
        ?
    );
    """
    database_accesser.write_data_to_database(
        write_processing_sql, serial_num, process_num.value[0], _change_mysql_time(datetime.datetime.now()))


def create_sql(instruction, dev_num, detail, sensor_date_time: datetime.datetime, serial_num: int):
    if instruction == "SNS":
        return insert_sns_update(dev_num, detail, sensor_date_time, serial_num)
    elif instruction == "SIG":
        return _create_sql_sig(dev_num, detail, sensor_date_time, serial_num)


def _change_mysql_time(sensor_date_time: datetime.datetime):
    return sensor_date_time.strftime(
        '%Y-%m-%d %H:%M:%S')


def insert_sns_update(database_accesser: DBAccessHandler, dev_num, detail: str, sensor_date_time: datetime.datetime):
    tracking_sensor_sql = """\
        INSERT INTO t_sensor_tracking(
            sensor_id,
            sensor_status,
            sensor_date_time
        )
        VALUES(
            ?,
            ?,
            ?
        );
    """
    sensor_status = 1 if detail == "ON" else 0
    database_accesser.write_data_to_database(
        tracking_sensor_sql, dev_num, sensor_status, _change_mysql_time(sensor_date_time))


def _create_sql_sig(dev_num, detail: str, sensor_date_time: datetime.datetime, serial_num: int):
    process_num = get_process_number("SIG", dev_num, detail)

    if process_num is None:
        return ""

    sql += f""" (serial_number,process_id,process_time) VALUES \
    ({serial_num},{process_num.value[0]},'{_change_mysql_time(sensor_date_time)}');"""
    return sql
