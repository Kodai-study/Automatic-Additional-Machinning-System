import socket
import sys
import socket
import sys
import time
import RobotCommunication

stop_flag = False


def send(port, number=1):
    cnt = 0
    # ソケットを作成し、指定されたポートで接続を待つ
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', port))
        s.listen()
        conn, _ = s.accept()
        with conn:
            if number % 2 == 0:
                time.sleep(0.5)
            while True:
                conn.sendall(f'sendNumber = {number} , cnt = {cnt}'.encode('utf-8'))
                time.sleep(1)
                cnt += 1
                if stop_flag or cnt > 10:
                    break


if __name__ == '__main__':
    send(5000)
