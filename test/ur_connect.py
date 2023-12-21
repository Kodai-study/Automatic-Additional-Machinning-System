import socket
from threading import Thread        

socket_ur = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)

host = "192.168.16.101"
port = 8765

socket_ur.bind((host, port))
socket_ur.listen()
print(f"""UR との接続を待機中... IPアドレス:{
    host} ポート番号: {port}, """)
socket_ur, _ = socket_ur.accept()

def read_socket():
    while True:
        data = socket_ur.recv(1024)
        if not data:
            return
        print("UR receiv " + data.decode())

Thread(target=read_socket).start()

while True:
    cmd = input()
    if cmd == "bye":
        exit()
    cmd += "\r\n"
    socket_ur.sendall(cmd.encode('utf-8'))

