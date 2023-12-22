import datetime
from Integration.process_number import Processes


class WorkManager:
    def __init__(self):
        self.work_list = []
        # プロセスの書き込みをためておくリスト
        self.write_waiting_list = []

    def regist_new_process(self, process_type: Processes, process_time: datetime.datetime):
        if process_type == Processes.start:
            self.work_list.append(
                {"process": Processes.start, "serial_number": None})
            self.write_waiting_list.append(
                {"process_type": Processes.start, "process_time": process_time})
            return

        max_progress_item = self._get_newest_work_data(process_type)
        max_progress_item["process"] = process_type
        if process_type == Processes.end_process:
            self._delete_finished_process()

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
