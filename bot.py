# -*- coding:utf-8 -*-

import re
from sys import path

from configparser import ConfigParser

# from telegram import ParseMode, Emoji
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
from multiplier import Multiplier
from settings import Settings

settings = Settings()
config = ConfigParser()
config.read_file(open('config.ini'))

# Create telegram poller with token from settings
up = Updater(token=config['Telegram']['token'], workers=32)
dispatcher = up.dispatcher

multiplier_dict = {}

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

# Welcome message
def start(bot, update):
    chat_id = update.message.chat_id
    multiplier_dict[chat_id] = Multiplier(chat_id=chat_id)
    msg = msg_hello + msg_command_list

    # Send the message
    bot.send_message(chat_id=chat_id,
                     text=msg.format(
                         user_name=update.message.from_user.first_name,
                         bot_name=bot.name))

def study(bot, update):
    chat_id = update.message.chat_id
    multiplier = get_multiplier_on_chat_id(chat_id=chat_id)

    if multiplier is None:
        multiplier = Multiplier(chat_id=chat_id)
        multiplier_dict[chat_id] = multiplier

    if multiplier._is_run == True:
        multiplier.reset()
        msg = msg_reset + msg_continuation + msg_command_list
    else:
        multiplier._is_run = True
        multiplier.set_input_str()
        msg = msg_task.format(multiplier.get_input_str())

    # Send the message
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg)

def reset(bot, update):
    chat_id = update.message.chat_id
    multiplier = get_multiplier_on_chat_id(chat_id)

    if multiplier is None or not multiplier._is_run:
        msg = msg_continuation + msg_command_list
    else:
        multiplier.reset()
        msg = msg_reset + msg_continuation + msg_command_list

    # Send the message
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg.format(
                         user_name=update.message.from_user.first_name,
                         bot_name=bot.name))

def setting(bot, update):
    chat_id = update.message.chat_id
    replay = update.message.text.split(' ')[1:]
    if settings.set_settings(chat_id, *replay):
        multiplier_dict[chat_id] = Multiplier(chat_id=chat_id)
        msg = 'Настройки применены.\n'
    else:
        msg = 'Что-то пошло не так.\n'

    msg = msg + msg_continuation + msg_command_list

    # Send the message
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg.format(
                         user_name=update.message.from_user.first_name,
                         bot_name=bot.name))

def statistic(bot, update):
    msg = 'Извините, данная комманда пока не доступна, {chat_id}'

    # Send the message
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg.format(
                         user_name=update.message.from_user.first_name,
                         bot_name=bot.name,
                         bot_id = bot.id,
                         chat_id=update.message.chat_id))

@run_async
def process(bot, update, job_queue):

    print(update.message.chat_id)
    # bot.send_message(chat_id=update.message.chat_id,
    #                  text='Setting a timer for 1 minute!')

    # job_queue.run_once(callback_alarm, 10, context=update.message.chat_id)
    # print(job_queue.jobs())

    chat_id = update.message.chat_id
    replay = update.message.text
    multiplier = get_multiplier_on_chat_id(chat_id)
    next_task = ''

    if multiplier is None or not multiplier._is_run:
        msg = msg_continuation + msg_command_list
    else:
        if replay.isdigit():
            if multiplier.response(replay):
                msg = msg_true_response + get_next_message(multiplier)
            else:
                msg = msg_false_response + get_next_message(multiplier)
        else:
            msg = msg_input_no_int + msg_task

        multiplier.set_input_str()
        next_task = multiplier.get_input_str()

    # Send the message
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg.format(next_task))


def get_next_message(multiplier):
    if sum(multiplier.rez) < multiplier._number_steps:
        return msg_task
    else:
        grade = multiplier.grade()
        multiplier.reset()
        return msg_grade.format(grade) + msg_continuation + msg_command_list


def get_multiplier_on_chat_id(chat_id=None):
    if chat_id in multiplier_dict:
        return multiplier_dict[chat_id]

def get_multiplier(chat_id=None):
    if not is_multiplier:
        set_multiplier(chat_id)
    return multiplier_dict[chat_id]

def is_multiplier(chat_id):
    if chat_id in multiplier_dict:
        return True

def set_multiplier(chat_id):
    if is_multiplier:
        multiplier_dict[chat_id] = Multiplier(chat_id=chat_id)



def callback_alarm(bot, job):
    bot.send_message(chat_id=job.context, text='BEEP')

# def callback_timer(bot, update, job_queue):
#     print(update.message.chat_id)
#     bot.send_message(chat_id=update.message.chat_id,
#                      text='Setting a timer for 1 minute!')

    # job_queue.run_once(callback_alarm, 10, context=update.message.chat_id)


def main():
    # Add handlers to dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("study", study))
    dispatcher.add_handler(CommandHandler("reset", reset))
    dispatcher.add_handler(CommandHandler("setting", setting))
    dispatcher.add_handler(CommandHandler("statistic", statistic))
    dispatcher.add_handler(MessageHandler(Filters.text, process))

    # dispatcher.add_handler(CommandHandler("timer", callback_timer))
    # dispatcher.add_handler(CommandHandler("timer", callback_timer, pass_job_queue=True))



    # Start the program
    up.start_polling()
    up.idle()

if __name__ == '__main__':
    main()