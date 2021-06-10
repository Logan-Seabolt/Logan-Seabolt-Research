import time

import PySimpleGUI as sg
import brainflow as bf
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
import keyboard as kb
import random as rd


class ExperimentProgram:

    index = 'f'
    middle = 'd'
    ring = 's'
    pinky = 'a'
    thumb = ' '
    test_length = 2
    board = 0

    def left_hand_map(self):
        self.index = 'f'
        self.middle = 'd'
        self.ring = 's'
        self.pinky = 'a'
        self.thumb = ' '

    def right_hand_map(self):
        self.index = 'j'
        self.middle = 'k'
        self.ring = 'l'
        self.pinky = ';'
        self.thumb = ' '

    def __init__(self):
        # Board type can be hard set to 1
        board_id = 1
        # Com port needs to be set on a by device basis
        params = BrainFlowInputParams()
        params.serial_port = "COM3"
        #self.board = BoardShim(board_id, params)
        self.board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)
        self.board.prepare_session()
        time.sleep(5)

    def set_test_length(self, new_test_length):
        self.test_length = new_test_length

    def run_battery(self, order):
        self.board.start_stream(4500)
        for finger in order:
            fing = finger[0]
            print("Please press: \"", fing, "\"")
            self.board.insert_marker(finger[1])
            while True:
                if kb.is_pressed(fing):
                    self.board.insert_marker(finger[1])
                    break
        data = self.board.get_board_data()
        self.board.stop_stream()
        return data

    def generate_battery(self):
        order = [(self.index, 1), (self.middle, 2), (self.ring, 3), (self.pinky, 4), (self.thumb, 5)]
        battery = []
        for i in range(self.test_length):
            test = rd.sample(order, len(order))
            battery.append(test)
        return battery


if __name__ == '__main__':
    exp = ExperimentProgram()
    battery = exp.generate_battery()
    print(battery)
    res = []
    print("When you are ready to begin press the space bar!")
    while True:
        if kb.is_pressed(" "):
            break
    time.sleep(0.5)
    for order in battery:
        res.append(exp.run_battery(order))
    for data in res:
        DataFilter.write_file(data, 'output.csv', 'a')



