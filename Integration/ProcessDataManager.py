import random
import datetime
import json
from DBAccessHandler.DBAccessHandler import DBAccessHandler
from GUIDesigner.ProcessingData import ProcessingData
from common_data_type import WorkPieceShape
from test_flags import TEST_FEATURE_DB

FETCH_PROCESS_DATA_SQL = """\
SELECT 
    *,
    CAST(AVG(TIME_TO_SEC(TIMEDIFF(subquery.max_process_time, subquery.min_process_time))) AS SIGNED) AS average_time_diff
FROM 
    m_model 
LEFT JOIN (
    SELECT 
        m_work.serial_number,
        m_work.model_number,
        MIN(t_work_tracking.process_time) AS min_process_time,
        MAX(t_work_tracking.process_time) AS max_process_time
    FROM 
        m_work
    JOIN 
        t_work_tracking ON t_work_tracking.serial_number = m_work.serial_number
    JOIN 
        m_process ON t_work_tracking.process_id = m_process.process_id
    JOIN 
        (SELECT MIN(process_id) AS min_id, MAX(process_id) AS max_id FROM m_process) AS process_range
    WHERE 
        m_process.process_id = process_range.min_id OR m_process.process_id = process_range.max_id
    GROUP BY 
        m_work.serial_number
) AS subquery ON m_model.model_number = subquery.model_number
JOIN 
	m_processing ON m_model.processing_id = m_processing.processing_id 
WHERE 
	m_processing.invisible = 1
GROUP BY 
    m_model.model_number;
"""


class ProcessDataManager:
    def __init__(self, database_accesser: DBAccessHandler):
        self.database_accesser = database_accesser
        self.process_data_list = []

    def refresh_process_data(self) -> list:
        """DBから加工データのリストを(再)取得する

        Returns:
            list: 加工データのリスト
        """
        # 既存のリストを model_id でインデックス化
        existing_data_index = {d["process_data"]['model_id']: d for d in self.process_data_list}

        # データベースからの新しいデータを処理
        for new_item in self._get_process_datas():
            if new_item["process_data"]['model_id'] in existing_data_index:
                # model_id が一致する場合、number を保持して他のデータを更新
                existing_item = existing_data_index[new_item['model_id']]
                existing_item.update({k: v for k, v in new_item.items() if k != 'model_id'})
            else:
            # model_id が存在しない場合、新しい要素を追加
                return self.process_data_list

    def register_process_number(self):
        """加工数を登録したことを通知する
        process_data_listのregist_process_count  を変更した後に呼び出す
        """
        self.process_data_list = [
            item for item in self.process_data_list if item["regist_process_count"] != 0]
        for item in self.process_data_list:
            json_data = self._get_processing_data_from_json(
                item["data_file_path"])
            item["hole_informations"] = json_data

    def get_next_process_data(self):
        """次の加工データを取得する
        全ての加工データが終了した場合はNoneを返す
        """

        if len(self.process_data_list) == 0:
            return None
        # 残りの個数
        is_last_work = self.process_data_list[0]["regist_process_count"] - \
            self.process_data_list[0]["good_count"] == 1
        return is_last_work, self.process_data_list[0]["hole_informations"]

    def processing_finished(self, is_good: bool) -> bool:
        """加工が終了したことを通知する

        Args:
            is_good (bool): 良品であればTrue, 不良品であればFalse

        Returns:
            bool: 今加工している型番の加工が終了した場合はTrue, まだ終了していない場合はFalse
        """
        if is_good:
            self.process_data_list[0]["good_count"] += 1
        else:
            self.process_data_list[0]["bad_count"] += 1

        if self.process_data_list[0]["regist_process_count"] - self.process_data_list[0]["good_count"] == 0:
            self.process_data_list.pop(0)
            return True
        return False

    def _get_processing_data_from_json(self, json_file_path: str):
        """
        jsonファイルを読み込む
        """
        with open(json_file_path) as f:
            json_data = json.load(f)
            return json_data

    def _create_processData_from_db(self, data_from_db):
        process_data_file = self._get_processing_data_from_json(
            data_from_db["file_pass"])
        work_shape = None
        if process_data_file["workShape"] == "CIRCLE":
            work_shape = WorkPieceShape.CIRCLE
        elif process_data_file["workShape"] == "SQUARE":
            work_shape = WorkPieceShape.SQUARE

        workpiece_dimension = process_data_file["workSize"]

        return ProcessingData(
            model_id=data_from_db['model_number'],
            model_number=data_from_db['model_name'],
            average_processing_time=data_from_db['average_time_diff'],
            work_shape=work_shape,
            workpiece_dimension=workpiece_dimension,
            created_by=data_from_db['create_user'],
            creation_timestamp=data_from_db['create_date'],
        )

    def _get_process_datas(self) -> list:
        if not TEST_FEATURE_DB:
            li = []
            for i in range(10):
                process_info = {
                    "regist_process_count": 0,
                    "process_time": datetime.timedelta(seconds=0),
                    "good_count": 0,
                    "data_file_path": f"test/test{i%10 + 1}.json",
                    "remaining_count": 0,
                    "bad_count": 0,
                    "average_time": datetime.timedelta(seconds=random.randint(1, 1000))
                }
                li.append(process_info)
            return li

        processing_datas_database = self.database_accesser.fetch_data_from_database(
            FETCH_PROCESS_DATA_SQL)
        processing_data_list = []
        for data in processing_datas_database:
            process_info = {
                "regist_process_count": 0,
                "process_time": datetime.timedelta(seconds=0),
                "good_count": 0,
                "data_file_path": data["file_pass"],
                "remaining_count": 0,
                "bad_count": 0,
                "average_time": datetime.timedelta(seconds=data["average_time_diff"])
            }
            process_info["process_data"] = self._create_processData_from_db(
                data)
            processing_data_list.append(process_info)
        return processing_data_list

    @staticmethod
    def _test_create_process_data():
        return [
            {"process_data": ProcessingData(1, "加工データ(型番)1", datetime.timedelta(minutes=2, seconds=34), WorkPieceShape.CIRCLE, 10.0, "加工者1", datetime.datetime.now()),
             "regist_process_count": 0,
             "process_time": datetime.timedelta(minutes=12, seconds=34),
             "good_count": 0,
             "data_file_path": "test/test.json",
             "bad_count": 0},
            {"process_data": ProcessingData(2, "加工データ(型番)2", datetime.timedelta(minutes=2, seconds=34), WorkPieceShape.SQUARE, 10.0, "加工者2", datetime.datetime.now()),
             "average_time": datetime.timedelta(minutes=2, seconds=34),
             "regist_process_count": 0,
             "process_time": datetime.timedelta(minutes=23, seconds=45),
             "good_count": 0,
             "data_file_path": "test/test2.json",
             "bad_count": 0},
            {"process_data": ProcessingData(3, "加工データ(型番)3", datetime.timedelta(minutes=5, seconds=43), WorkPieceShape.SQUARE, 10.0, "加工者3", datetime.datetime.now()),
             "average_time": datetime.timedelta(minutes=5, seconds=43),
             "regist_process_count": 0,
             "process_time": datetime.timedelta(minutes=23, seconds=45),
             "good_count": 0,
             "data_file_path": "test/test3.json",
             "bad_count": 0}
        ]
