TEST_UR_CONNECTION_LOCAL = True
"""
URとの接続をローカル別スレッドでテストする場合はTrue
"""

TEST_CFD_CONNECTION_LOCAL = True
"""
CFDとの接続をローカル別スレッドでテストする場合はTrue
"""

TEST_FEATURE_GUI = True
"""
GUIの機能をONにする場合はTrue
リモートデスクトップ以外の接続で動かす場合はFalseにしないと動かない
"""

TEST_FEATURE_IMAGE_PROCESSING = False
"""
画像検査の機能をONにする場合はTrue
Telicamのインストールがされていない環境で動かす場合はFalseにしないと動かない
"""

TEST_FEATURE_DB = False
"""
データベースへの書き込み・読み込みの機能をONにする場合はTrue
linux以外の環境で動かす場合はFalseにしないと動かない
"""

TEST_FEATURE_CONNECTION = True
"""
ロボットやテスト用のソケット通信を行う機能をONにする場合はTrue
Windowsで接続を試す場合はTEST_UR_CONNECTION_LOCAL や TEST_CFD_CONNECTION_LOCALをTrueにして動かしてテストできる
接続の機能を使わない場合はFalseにしておいた方が良い
"""
