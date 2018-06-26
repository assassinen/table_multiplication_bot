# -*- coding:utf-8 -*-

import re
from sys import path

from configparser import ConfigParser

# from telegram import ParseMode, Emoji
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
from multiplier import Multiplier


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
    multiplier_dict[update.message.chat_id] = Multiplier()
    msg = msg_hello + msg_command_list

    # Send the message
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg.format(
                         user_name=update.message.from_user.first_name,
                         bot_name=bot.name))

def study(bot, update):
    if update.message.chat_id not in multiplier_dict:
        multiplier_dict[update.message.chat_id] = Multiplier()
    msg = multiplier_dict[update.message.chat_id].get_next_message()
    # msg = multiplier.get_next_message()
    # Send the message
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg.format(
                         user_name=update.message.from_user.first_name,
                         bot_name=bot.name))

def reset(bot, update):
    multiplier_dict[update.message.chat_id].reset()

    msg = msg_reset + msg_continuation + msg_command_list

    # Send the message
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg.format(
                         user_name=update.message.from_user.first_name,
                         bot_name=bot.name))

def setting(bot, update):
    msg = 'Извините, данная комманда пока не доступна'

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
def process(bot, update):
    chat_id = update.message.chat_id
    replay = update.message.text
    multiplier = get_multiplier_on_chat_id(chat_id)
    next_task = ''

    # print(chat_id, replay, multiplier)

    if multiplier is None or not multiplier._is_run:
        msg = msg_continuation + msg_command_list
    elif replay.isdigit():
        if multiplier.response(replay):
            msg = 'Верно\nСколько будет {}? '
        else:
            msg = 'Не верно\nСколько будет {}? '
        multiplier.set_input_str()
        next_task = multiplier.get_input_str()

    else:
        msg = 'Ответ не является числом.\nСколько будет {}? '
        multiplier.set_input_str()
        next_task = multiplier.get_input_str()

    # Send the message
    bot.send_message(chat_id=update.message.chat_id,
                     text=msg.format(next_task))


def get_multiplier_on_chat_id(chat_id=None):
    if chat_id in multiplier_dict:
        return multiplier_dict[chat_id]


def main():
    # Add handlers to dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("study", study))
    dispatcher.add_handler(CommandHandler("reset", reset))
    dispatcher.add_handler(CommandHandler("setting", setting))
    dispatcher.add_handler(CommandHandler("statistic", statistic))
    dispatcher.add_handler(MessageHandler(Filters.text, process))

    # Start the program
    up.start_polling()
    up.idle()

if __name__ == '__main__':
    main()