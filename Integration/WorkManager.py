
class WorkManager:
    def __init__(self, workQueue):
        self.work_list = []
        # プロセスの書き込みをためておくリスト
        self.write_waiting_list = []
