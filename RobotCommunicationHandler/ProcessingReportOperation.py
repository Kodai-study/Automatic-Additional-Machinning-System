
import socket
import time

operation_start = "WRK 0,TAP_FIN"
move_end_machining = "SIG ATT_DRL_READY"
ejject_attatch = "EJCT 0,ATTACH"

# ソケット通信で受け取った文字列を引数と比較する関数


def compare_string(ur_socket: socket.socket, compare_string: str):
    while True:
        data = ur_socket.recv(1024)
        if data:
            print(data.decode())
            if data.decode() == compare_string:
                print(compare_string)
                break


def send_input_command(ur_socket: socket.socket):
    while True:
        data = input()
        if data == "bye":
            return
        ur_socket.sendall(data.encode())


def operation_sequence_start(ur_socket: socket.socket):
    ur_socket.sendall(operation_start.encode())
    compare_string(ur_socket, move_end_machining)
    ur_socket.sendall(move_end_machining.encode())
