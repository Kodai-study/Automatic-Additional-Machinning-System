import datetime
from DBAccessHandler.DBAccessHandler import DBAccessHandler
from GUIDesigner.ProcessingData import ProcessingData
from common_data_type import WorkPieceShape


class ProcessDataManager:
    def __init__(self, database_accesser: DBAccessHandler):
        self.database_accesser = database_accesser

    def get_process_datas(self) -> list:
        return ProcessDataManager._test_create_process_data()

    @staticmethod
    def _test_create_process_data():
        return [
            {"process_data": ProcessingData(1, "加工データ(型番)1", datetime.timedelta(minutes=2, seconds=34), WorkPieceShape.CIRCLE, 10.0, "加工者1", datetime.datetime.now()),
             "regist_process_count": 10,
             "process_time": datetime.timedelta(minutes=12, seconds=34),
             "good_count": 7,
             "data_file_path": "/test/test.json",
             "remaining_count": 2},
            {"process_data": ProcessingData(2, "加工データ(型番)2", datetime.timedelta(minutes=2, seconds=34), WorkPieceShape.SQUARE, 10.0, "加工者2", datetime.datetime.now()),
             "average_time": datetime.timedelta(minutes=2, seconds=34),
             "regist_process_count": 20,
             "process_time": datetime.timedelta(minutes=23, seconds=45),
             "good_count": 8,
             "data_file_path": "/test/test.json",
             "remaining_count": 10}
        ]
