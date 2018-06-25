#/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import random


class Multiplier:

    def __init__(self, start = 4, stop = 4, number_steps = 5, timeout = 10):
        self._start = start
        self._stop = stop
        self._number_steps = number_steps
        self._timeout = timeout
        self._input_list = {None}
        self._input_str = None
        self.x = None
        self.y = None
        self._is_run = False
        self.rez = [0, 0, 0]

    def gen_input_str(self):
        x = random.randint(self._start, self._stop)
        y = random.randint(1, 10)
        self._input_str = str(x) + " * " + str(y)
        self.x = x
        self.y = y

    def set_input_str(self):
        self.gen_input_str()
        while self._input_str in self._input_list:
            self.gen_input_str()

    def get_input_str(self):
        return self._input_str

    def update_input_list(self):
        self._input_list.add(self._input_str)
        self.set_input_str()

    def response(self, replay = None):
        if replay.isdigit():
            replay = int(replay)
            msg = self.resolution(replay)
        else:
            self.set_input_str()
            msg = "Ответ не является числом."
        return msg

    def resolution(self, replay = None):
        if replay == self.x * self.y:
            self.update_input_list()
            self.rez[0] = self.rez[0] + 1
            msg = 'Верно.'
        else:
            self.update_input_list()
            self.rez[1] = self.rez[1] + 1
            msg = 'Не верно.'
        return msg

    def reset(self):
        self._input_list = {None}
        self._input_str = None
        self.x = None
        self.y = None
        self._is_run = False
        self.rez = [0, 0, 0]

    def grade(self):
        msg = "Оценка - " + str(int(5 * self.rez[0] / (len(self._input_list) - 1))) + '\n'
        return msg

    def get_next_message(self, replay = None):
        if self._is_run:
            msg = self.response(replay) + '\n'
            if len(self._input_list) > self._number_steps:
                msg = msg + self.grade()
                self.reset()
            else:
                msg = msg + 'Сколько будет {}? '.format(self.get_input_str())
        else:
            self._is_run = True
            self.set_input_str()
            msg = 'Сколько будет {}? '.format(self.get_input_str())
        return msg + '\n'


def test():
    multiplier = Multiplier()
    msg = ''
    while True:
        replay = input(msg)
        if replay == 'exit':
            break
        msg = multiplier.get_next_message(replay)



if __name__ == '__main__':
    test()

