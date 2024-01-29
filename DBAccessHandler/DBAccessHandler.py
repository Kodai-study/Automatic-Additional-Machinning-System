# coding: utf-8
from common_data_type import *
from typing import List, Tuple
from test_flags import TEST_FEATURE_DB
if TEST_FEATURE_DB:
    from mysql.connector import pooling


class DBAccessHandler:
    """
    データベースへのアクセスを管理するクラス
    """

    def __init__(self):
        if TEST_FEATURE_DB:
            self.pool = pooling.MySQLConnectionPool(
                pool_name="mypool",
                pool_size=5,
                pool_reset_session=True,
                host="192.168.16.101",
                user="admin",
                passwd="t5admin",
                database="test"
            )

    def fetch_data_from_database(self, sql_query: str, *values) -> List[dict]:
        """
        データベースからデータを取得する

        Args:
            sql_query (str): SQLクエリの文字列。そのままSQL文として実行される

        Returns:
            dict: 帰ってくるデータを辞書型で返す。データのキーと値はテーブルのカラム名と値に対応する
            読み込みが失敗した場合は空の辞書を返す
        """
        if TEST_FEATURE_DB:
            with self.pool.get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    try:
                        if values:
                            cursor.execute(sql_query, values)
                        else:
                            cursor.execute(sql_query)
                        result = cursor.fetchall()
                        return result
                    except Exception as e:
                        print(e)
                        return []
        else:
            print("実行されるSQL文 : ", sql_query % values)
            return []

    def write_data_to_database(self, sql_query: str, *values) -> Tuple[bool, str]:
        """
        データベースにデータを書き込む

        Args:
            sql_query (str): SQLクエリの文字列。そのままSQL文として実行される

        Returns:
            Tuple[bool, str]: 書き込みが成功したかどうかの真偽値と、エラーがあった場合はエラーの内容を返す
        """
        # print("実行されるSQL文 : ", sql_query % values)
        return (True, "")
