import datetime
from DBAccessHandler.DBAccessHandler import DBAccessHandler
from Integration.handlers_database import write_database_process
from Integration.process_number import Processes


class WorkManager:
    def __init__(self, database_accesser: DBAccessHandler):
        self.work_list = []
        # プロセスの書き込みをためておくリスト
        self.write_waiting_list = []
        self.database_accesser = database_accesser

    def regist_new_process(self, process_type: Processes, process_time: datetime.datetime):
        if process_type == Processes.start:
            self.work_list.append(
                {"process": Processes.start, "serial_number": None})
            self.write_waiting_list.append(
                {"process_type": Processes.start, "process_time": process_time})
            return

        max_progress_item = self._get_newest_work_data(process_type)
        serial_number = max_progress_item["serial_number"]
        if serial_number is None:
            self.write_waiting_list.append(
                {"process_type": process_type, "process_time": process_time})
        else:
            write_database_process(self.database_accesser,
                                   process_type, serial_number, process_time)

        max_progress_item["process"] = process_type
        if process_type == Processes.end_process:
            self._delete_finished_process()

    def preprocess_inspection(self, serial_number: int):
        while self.write_waiting_list:
            waiting_item = self.write_waiting_list.pop(0)
            write_database_process(self.database_accesser,
                                   waiting_item["process_type"], serial_number, time=waiting_item["process_time"])

    def _delete_finished_process(self):
        self.work_list = [d for d in self.work_list if d.get(
            'process') != Processes.end_process]

    def _get_newest_work_data(self, new_process: Processes) -> dict:
        filtered_progress = [
            item for item in self.work_list if item["process"].value < new_process.value]

        # filtered_progress の要素がない場合
        if not filtered_progress:
            self.work_list.append(
                {"process": new_process, "serial_number": None})
            return False, None

        max_progress_item = max(
            filtered_progress, key=lambda item: item["process"].value, default=None)

        if max_progress_item is None:
            print("ワーク管理の部分でエラーです")
        return max_progress_item

    def _test_insert_work_datas(self):
        self.write_waiting_list = [{"process_type": Processes.start,
                                    "process_time": datetime.datetime.now()},
                                   {"process_type": Processes.move_to_process,
                                    "process_time": datetime.datetime.now() + datetime.timedelta(seconds=10)}]
