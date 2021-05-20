import PySimpleGUI as sg
import brainflow as bf
import keyboard as kb
import random as rd

class ExperimentProgram:

    index = 'f'
    middle = 'd'
    ring = 's'
    pinky = 'a'
    thumb = ' '
    test_length = 10

    def leftHandMap(self):
        self.index = 'f'
        self.middle = 'd'
        self.ring = 's'
        self.pinky = 'a'
        self.thumb = ' '

    def rightHandMap(self):
        self.index = 'j'
        self.middle = 'k'
        self.ring = 'l'
        self.pinky = ';'
        self.thumb = ' '

    def set_test_length(self,new_test_length):
        self.test_length=new_test_length

    def run_battery(self, order):
        for finger in order:
            print("Please press: \"", finger,"\"")
            while True:
                if kb.is_pressed(finger):
                    print("Record Data")
                    break
        print("Battery Complete")

    def generate_battery(self):
        order = [self.index, self.middle, self.ring, self.pinky, self.thumb]
        battery = []
        for i in range(self.test_length):
            test = rd.sample(order, len(order))
            battery.append(test)
        return battery


if __name__ == '__main__':
    exp = ExperimentProgram()
    battery = exp.generate_battery()
    print(battery)
    for order in battery:
        exp.run_battery(order)



