#/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import random
from settings import Settings

class Multiplier():

    def __init__(self, chat_id=None):
        self.settings(chat_id)
        self._input_list = {None}
        self._input_str = None
        self.x = None
        self.y = None
        self._is_run = False
        self.rez = [0, 0, 0]

    def settings(self, chat_id=None):
        settings = Settings()
        chat_id_settings = settings.get_settings(chat_id)
        self._start = chat_id_settings['start']
        self._stop = chat_id_settings['stop']
        self._number_steps = chat_id_settings['number_steps']
        self._timeout = chat_id_settings['timeout']
        # print(self._start)

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
        if int(replay) == self.x * self.y:
            self.update_input_list()
            self.rez[0] = self.rez[0] + 1
            msg = True
        else:
            self.update_input_list()
            self.rez[1] = self.rez[1] + 1
            msg = False
        return msg

    def reset(self):
        self._input_list = {None}
        self._input_str = None
        self.x = None
        self.y = None
        self._is_run = False
        self.rez = [0, 0, 0]

    def grade(self):
        msg = str(int(5 * self.rez[0] / (len(self._input_list) - 1)))
        return msg



def test():
    # settings = Settings()
    # set = settings.get_settings()
    # print(set)
    multiplier = Multiplier(chat_id=379201876, kwargs=set)
    # print()

    msg = ''
    while True:
        replay = input(msg)
        if replay == 'exit':
            break
        msg = multiplier.get_next_message(replay)



if __name__ == '__main__':
    test()

