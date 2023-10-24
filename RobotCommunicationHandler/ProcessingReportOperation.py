
import socket
import time

cmd_operation_start = "WRK 0,TAP_FIN\n"
cmd_move_end_machining = "SIG ATT_DRL_READY"
cmd_eject_attatch = "EJCT 0,ATTACH\n"
cmd_eject_detach = "EJCT 0,DETACH\n"
"""
WRK 0,TAP_FIN
EJCT 0,ATTACH
EJCT 0,DETACH
EJCT 0,ATTACH
EJCT 0,DETACH
WRK 0,TAP_FIN
"""
# ソケット通信で受け取った文字列を引数と比較する関数


def wait_until_match_command(ur_socket: socket.socket, compare_string: str):
    while True:
        data = ur_socket.recv(1024)
        if data:
            print(data.decode())
            if data.decode() == compare_string:
                print(compare_string)
                break


def send_input_command(ur_socket: socket.socket):
    print("connected! please input command")
    while True:
        data = input()
        data = data + "\n"
        if data == "bye":
            return
        elif data == "start\n":
            operation_sequence_start(ur_socket)
        ur_socket.sendall(data.encode())


def operation_sequence_start(ur_socket: socket.socket):
    ur_socket.sendall(cmd_operation_start.encode())
    wait_until_match_command(ur_socket, cmd_move_end_machining)
    ur_socket.sendall(cmd_eject_attatch.encode())
    time.sleep(10)
    ur_socket.sendall(cmd_eject_detach.encode())
    wait_until_match_command(ur_socket, cmd_move_end_machining)
    ur_socket.sendall(cmd_eject_attatch.encode())
    time.sleep(10)
    ur_socket.sendall(cmd_eject_detach.encode())
