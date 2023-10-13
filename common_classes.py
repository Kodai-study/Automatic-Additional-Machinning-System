# coding: utf-8

from enum import Enum
from dataclasses import dataclass
from common_data_type import *
from queue import Queue
from typing import Union, List, Tuple


class GUIDesigner:
    """
    GUIのデザインを行うクラス
    GUIの画面を作成し、ユーザからの入力を受け付けて、それをキューに入れて統合ソフトに送ったり、
    統合ソフトから受け取ったデータをGUIに表示したりする
    """

    def __init__(self):
        pass

    def start_gui(self, send_queue: Queue, receive_queue: Queue):
        """
        GUIを起動し、ループを開始する。

        Args:
            send_queue (Queue): 統合ソフトに送るデータを入れるキュー\n
            receive_queue (Queue): 統合ソフトから受け取ったデータを入れるキュー
        """
        pass


class RobotCommunicationHandler:
    """
    ロボットとの通信を管理するクラス
    常にロボットとのソケット接続を確立しておき、
    送信要求や受信に関する処理を行う
    """

    def __init__(self):
        self.send_queue = None
        self.receive_queue = None

    def communication_loop(self, send_queue: Queue, receive_queue: Queue):
        """
        受信する、統合スレッドからの送信要求の待ち受けのループを開始する

        Args:
            send_queue (Queue): 統合スレッドに送るデータを入れるキュー\n
            receive_queue (Queue): 統合スレッドから受け取ったデータを入れるキュー
        """
        self.send_queue = send_queue
        self.receive_queue = receive_queue


class DBAccessHandler:
    """
    データベースへのアクセスを管理するクラス
    """

    def __init__(self):
        pass

    def fetch_data_from_database(self, sql_query: str) -> List[dict]:
        """
        データベースからデータを取得する

        Args:
            sql_query (str): SQLクエリの文字列。そのままSQL文として実行される

        Returns:
            dict: 帰ってくるデータを辞書型で返す。データのキーと値はテーブルのカラム名と値に対応する
            読み込みが失敗した場合は空の辞書を返す
        """
        pass

    def write_data_to_database(self, sql_query: str) -> Tuple[bool, str]:
        """
        データベースにデータを書き込む

        Args:
            sql_query (str): SQLクエリの文字列。そのままSQL文として実行される

        Returns:
            Tuple[bool, str]: 書き込みが成功したかどうかの真偽値と、エラーがあった場合はエラーの内容を返す
        """
        pass


class ImageInspectionController:

    def __init__(self):
        pass

    def perform_image_inspection(self, inspection_type: InspectionType, inspection_data: Union[PreProcessingInspectionData, ToolInspectionData, List[HoleCheckInfo]]):
        """
        画像検査を行って、結果を返す関数。

        Args:
            inspection_type (InspectionType): 画像検査の種類の列挙型\n
            inspection_data (Union[PreProcessingInspectionData, WorkPieceShape, List[HoleCheckInfo]]): 検査に必要なデータ。検査の種類によってデータの型が異なる
        """
        pass





