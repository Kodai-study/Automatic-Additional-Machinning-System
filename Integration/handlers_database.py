
from DBAccessHandler.DBAccessHandler import DBAccessHandler


def write_database(database_accesser: DBAccessHandler, message: str):
    database_accesser.write_data_to_database()
