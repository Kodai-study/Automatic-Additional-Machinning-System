
import socket
import time

cmd_operation_start = "WRK 0,TAP_FIN\n"
cmd_move_end_machining = "SIG 0,ATT_DRL_READY"
cmd_move_imp_machining = "SIG 0,ATT_IMP_READY"
cmd_eject_detach_ready = "SIG DET"
cmd_eject_attatch = "EJCT 0,ATTACH\n"
cmd_eject_detach = "EJCT 0,DETACH\n"

_cmd_stream = \
    """\
WRK 0,TAP_FIN
Main_Received: SIG 0,ATT_DRL_READY
EJCT 0,ATTACH
Main_Received: SIG DET
EJCT 0,DETACH
Main_Received: SIG 0,ATT_IMP_READY
EJCT 0,ATTACH
Main_Received: SIG DET
EJCT 0,DETACH
"""


def wait_until_match_command(ur_socket: socket.socket, compare_string: str):
    """ソケット通信で受け取った文字列を引数と比較する関数
        比較する文字列と一致するまでループを回す"""
    while True:
        data = ur_socket.recv(1024)
        if not data:
            continue
        data = data.decode()
        print(data)
        if data == compare_string:
            print("Main_Received: ", compare_string)
            break


def send_input_command(ur_socket: socket.socket):
    print("connected! please input command")
    while True:
        data = input()
        if data == "bye":
            return
        elif data == "start":
            operation_sequence_start(ur_socket)
        else:
            data = data + "\n"
            ur_socket.sendall(data.encode())


def operation_sequence_start(ur_socket: socket.socket):
    ur_socket.sendall(cmd_operation_start.encode())
    print("command_send: ", cmd_operation_start)  # 加工が終了したことを通知

    # wait_until_match_command(
    #     ur_socket, cmd_move_end_machining)  # 加工部のワークがある部分に移動

    ur_socket.sendall(cmd_eject_attatch.encode())
    print("command_send: ", cmd_eject_attatch)  # 吸着が完了→加工部から検査部へ移動

    # wait_until_match_command(ur_socket, cmd_eject_detach_ready)

    ur_socket.sendall(cmd_eject_detach.encode())  # 吸着を解除
    print("command_send: ", cmd_eject_detach)

    # wait_until_match_command(
    #     ur_socket, cmd_move_imp_machining)  # 搬入部へ移動したことを通知

    ur_socket.sendall(cmd_eject_attatch.encode())  # 吸着が完了したことを通知
    print("command_send: ", cmd_eject_attatch)

    # wait_until_match_command(ur_socket, cmd_eject_detach_ready)

    ur_socket.sendall(cmd_eject_detach.encode())  # 吸着を解除
    print("command_send: ", cmd_eject_detach)
