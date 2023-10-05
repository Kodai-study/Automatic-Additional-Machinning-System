import socket
import sys


def receive(port):
    # ソケットを作成し、指定されたポートで接続を待つ
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', port))
        s.listen()
        print(f"Listening on port {port}...")
        # 接続が確立されたら、データを受信して標準出力に出力する
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(data.decode())


if __name__ == '__main__':
    receive(5000)
