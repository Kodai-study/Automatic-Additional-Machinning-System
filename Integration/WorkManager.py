
class WorkManager:
    def __init__(self):
        self.work_list = []
        # プロセスの書き込みをためておくリスト
        self.write_waiting_list = []

    def _test_insert_work_datas(self):
        self.write_waiting_list = [{"process_type": Processes.start,
                                    "process_time": datetime.datetime.now()},
                                   {"process_type": Processes.move_to_process,
                                    "process_time": datetime.datetime.now()}]
