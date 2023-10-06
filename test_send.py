import socket
import time

stop_flag = False
"""
これをTrueにすると、send関数が終了する。
"""


def test_send(port, number=1):
    cnt = 0
    # ソケットを作成し、指定されたポートで接続を待つ
    # ロボット通信スレッドが接続しに来るので、待ち受ける
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', port))
        s.listen()
        conn, _ = s.accept()
        with conn:
            # 0.5秒間を開けて、相互に送信する
            if number % 2 == 0:
                time.sleep(0.5)
            while True:
                conn.sendall(f'sendNumber = {number} , cnt = {
                             cnt}'.encode('utf-8'))
                time.sleep(1)
                cnt += 1
                if stop_flag or cnt > 10:
                    break


if __name__ == '__main__':
    test_send(5000)
