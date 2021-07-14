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
    response_time = 0

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

    def calc_response_time(self):
        self.response_time = self.response_time/(self.test_length*5)

    def __init__(self):
        # Board type can be hard set to 1
        board_id = 1
        # Com port needs to be set on a by device basis
        params = BrainFlowInputParams()
        params.serial_port = "COM3"
        #self.board = BoardShim(board_id, params)
        self.board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)
        self.board.prepare_session()
        time.sleep(2)

    def set_test_length(self, new_test_length):
        self.test_length = new_test_length

    def run_battery(self, order):
        self.board.start_stream(4500)
        for finger in order:
            fing = finger[0]
            start = time.time()
            print("Please press: \"", fing, "\"")
            self.board.insert_marker(finger[1])
            while True:
                if kb.is_pressed(fing):
                    self.board.insert_marker(finger[1])
                    break
            self.response_time += time.time()-start
            time.sleep(0.5)
        data = self.board.get_board_data()
        self.board.stop_stream()
        return data

    def run_battery_practice(self, order):
        for finger in order:
            fing = finger[0]
            print("Please press: \"", fing, "\"")
            while True:
                if kb.is_pressed(fing):
                    break
            time.sleep(0.5)

    def run_battery_imagined(self, order):
        self.board.start_stream(4500)
        for finger in order:
            fing = finger[0]
            print("Please imagine pressing: \"", fing, "\"")
            self.board.insert_marker(finger[1])
            start = time.time()
            while time.time() - start < self.response_time:
                if kb.is_pressed(self.index) or kb.is_pressed(self.middle) or kb.is_pressed(self.ring) or kb.is_pressed(
                        self.pinky) or kb.is_pressed(self.thumb):
                    print("You pressed a key, test is invalid")
                    self.board.insert_marker(-1)
                    break
            self.board.insert_marker(finger[1])
            time.sleep(0.5)
        data = self.board.get_board_data()
        self.board.stop_stream()
        return data

    def run_battery_imagined_practice(self, order):
        for finger in order:
            fing = finger[0]
            print("Please imagine pressing: \"", fing, "\"")
            start = time.time()
            while time.time()-start < self.response_time:
                if kb.is_pressed(self.index) or kb.is_pressed(self.middle) or kb.is_pressed(self.ring) or kb.is_pressed(self.pinky) or kb.is_pressed(self.thumb):
                    print("You pressed a key, test is invalid")
                    break
            time.sleep(0.5)

    def generate_battery(self, tlength=test_length):
        order = [(self.index, 1), (self.middle, 2), (self.ring, 3), (self.pinky, 4), (self.thumb, 5)]
        battery = []
        for i in range(tlength):
            test = rd.sample(order, len(order))
            battery.append(test)
        return battery


if __name__ == '__main__':
    debug = False
    exp = ExperimentProgram()
    res = []
    userID = input("Enter user ID number: ")
    exp.test_length = int(input("Enter number of experiments (15,30): "))
    break_duration = float(input("Enter duration of break in minutes (1-5): "))
    handedness = input("Are you left or right handed? l/r? ")
    if handedness.lower()[0] == 'l':
        exp.left_hand_map()
    else:
        exp.right_hand_map()
    battery = exp.generate_battery()
    test_battery = exp.generate_battery(3)
    if debug:
        print(battery)
    while True:
        if input("Would you like to practice the experiment movements? y/n: ").lower()[0] == "y":
            for bat in test_battery:
                exp.run_battery_practice(bat)
        else:
            break
    print("When you are ready to begin press the space bar!")
    while True:
        if kb.is_pressed(" "):
            break
    time.sleep(0.5)
    count = 1
    for order in battery:
        if count % 5 == 0:
            print('Beginning a short user break, the break will last until you press the space bar')
            while True:
                if kb.is_pressed(" "):
                    print("Resuming Experiment")
                    break
            time.sleep(0.5)
        res.append(exp.run_battery(order))
        count += 1
    for data in res:
        DataFilter.write_file(data, userID+'_real_movement_output.csv', 'a')
    print("\n\nPreparing for imagined finger movement test")
    exp.calc_response_time()
    if debug:
        print("Average response time", exp.response_time, "seconds")
    time.sleep(60*break_duration)
    while True:
        if input("Would you like to practice the imagined movements? y/n: ").lower()[0] == "y":
            for bat in test_battery:
                exp.run_battery_imagined_practice(bat)
        else:
            break
    print("When you are ready to begin press the space bar!")
    while True:
        if kb.is_pressed(" "):
            break
    time.sleep(0.5)
    res.clear()
    battery = exp.generate_battery()
    count = 1
    for order in battery:
        if count%5 == 0:
            print('Beginning a short user break, the break will last until you press the space bar')
            while True:
                if kb.is_pressed(" "):
                    print("Resuming Experiment")
                    break
            time.sleep(0.5)
        res.append(exp.run_battery_imagined(order))
        count += 1
    for data in res:
        DataFilter.write_file(data, userID+'_imagined_movement_output.csv', 'a')




