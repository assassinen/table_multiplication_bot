#/Library/Frameworks/Python.framework/Versions/3.5/bin/python3

import random
from settings import Settings


from configparser import ConfigParser

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from settings import Settings

# config = ConfigParser()
# config.read_file(open('config.ini'))
#
# # Create telegram poller with token from settings
# up = Updater(token=config['Telegram']['token'], workers=32)
# job_queue = up.job_queue


class Multiplier():

    def __init__(self, chat_id=None):
        # self.job_queue = job_queue
        self.chat_id = chat_id
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


    # def del_job(self, job):
    #     job.schedule_removal()
    #
    # def time_out(self, bot, job):
    #     # print(bot)
    #     msg = 'Вы слишком долго думаете.\n'
    #     job.schedule_removal()
    #     self.update_input_list()
    #     next_task = self.get_input_str()
    #     msg_task = 'Cколько будет {}?\n'.format(next_task)
    #
    #     bot.send_message(chat_id=self.chat_id,
    #                      text=msg + msg_task)


    def get_input_str(self):
        # self.job_queue.run_once(self.time_out, 10, name=self._input_str)
        # self.job_queue.run_repeating(self.time_out, 3)

        # print(self.job_queue.jobs())
        # self.del_job
        # print(self._input_str)
        # print(self.job_queue.get_jobs_by_name(self._input_str))
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




# ===============
msg_hello = '''
Привет {user_name}! 
Я - {bot_name}.
Я помогу тебе выучить таблицу умножения. \n 
Я умею выполнять следующие комманды: \n'''
msg_task = 'Cколько будет {}?\n'
msg_grade = 'Оценка - {}\n\n'
msg_true_response = 'Верно\n'
msg_false_response = 'Не верно\n'
msg_input_no_int = 'Ответ не является числом.\n'
msg_continuation = 'Для продолжение используйте слейдующие комманды: \n'
msg_reset = 'Предыдущие результаты онулированы.\n'
msg_command_list = '''
/study - начать обучение
/reset - прервать обучение
/setting - настройка
/statistic - статистика обучения
'''

def get_next_message(multiplier):
    if sum(multiplier.rez) < multiplier._number_steps:
        return msg_task
    else:
        grade = multiplier.grade()
        multiplier.reset()
        return msg_grade.format(grade) + msg_continuation + msg_command_list


def test():
    multiplier = Multiplier(chat_id=379201876)

    # msg = ''
    multiplier.set_input_str()
    next_task = multiplier.get_input_str()
    msg = msg_task.format(next_task)

    while True:
        replay = input(msg)

        if replay.isdigit():
            if multiplier.response(replay):
                msg = msg_true_response + get_next_message(multiplier)
            else:
                msg = msg_false_response + get_next_message(multiplier)

            multiplier.set_input_str()
            next_task = multiplier.get_input_str()
            msg = msg.format(next_task)

        if replay == 'exit':
            break



if __name__ == '__main__':
    test()

