from enum import Enum


class Processes(Enum):
    start = 0,
    attach_work_delivery = 1,
    move_to_process = 2,
    start_process = 3,
    end_process = 4,
    attach_work_move_inspection = 5,
    move_inspection = 6,
    end_inspection = 7,
    carry_out = 8


def get_process_number(instruction, dev_num, detail):
    if instruction == "FIN_FST_POSITION":
        return Processes.start

    if instruction == "SIG":
        if dev_num == 0 and detail == "ATT_IMP_READY":
            return Processes.attach_work_delivery
        elif dev_num == 0 and detail == "ATT_DRL_READY":
            return Processes.attach_work_move_inspection

    if instruction == "SNS":
        if dev_num == 3 and detail == "ON":
            return Processes.move_to_process
        elif dev_num == 4 and detail == "ON":
            return Processes.move_inspection

    return None
