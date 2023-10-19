import socket


def test_receive(port):
    # ソケットを作成し、指定されたポートで接続を待つ
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', port))
        s.listen()
        print(f"Listening on port {port}...")
        # 接続が確立されたら、データを受信して標準出力に出力する
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            conn.settimeout(5)  # 10秒間受信がなかったら、処理を終了する
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print("receiv_task", data.decode())
                except socket.timeout:
                    print("Timeout: No data received for 10 seconds.")
                    break


if __name__ == '__main__':
    test_receive(5000)
