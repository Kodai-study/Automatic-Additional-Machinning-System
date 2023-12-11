# coding: utf-8

from mysql.connector import pooling
from common_data_type import *
from typing import List, Tuple


class DBAccessHandler:
    """
    データベースへのアクセスを管理するクラス
    """

    def __init__(self):
        pass

    def fetch_data_from_database(self, sql_query: str, *values) -> List[dict]:
        """
        データベースからデータを取得する

        Args:
            sql_query (str): SQLクエリの文字列。そのままSQL文として実行される

        Returns:
            dict: 帰ってくるデータを辞書型で返す。データのキーと値はテーブルのカラム名と値に対応する
            読み込みが失敗した場合は空の辞書を返す
        """
        pass

    def write_data_to_database(self, sql_query: str, *values) -> Tuple[bool, str]:
        """
        データベースにデータを書き込む

        Args:
            sql_query (str): SQLクエリの文字列。そのままSQL文として実行される

        Returns:
            Tuple[bool, str]: 書き込みが成功したかどうかの真偽値と、エラーがあった場合はエラーの内容を返す
        """
        print("実行されるSQL文 : ", sql_query)
