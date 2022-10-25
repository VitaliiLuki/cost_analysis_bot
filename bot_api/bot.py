import os
import re
import time

import telegram
from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

load_dotenv()
ID_TOKEN = 205732562
BOT_TOKEN = '5508517134:AAElpf_IXLiNHsz7_OWXyLJ2uTqD-X8LW0I'
# Для хранения секретных ключей и токенов используется библиотека
# dotenv
# Перед запуском впишите свой chat_id 
# его можно узнать написав боту "userinfobot"
# для получения токена тетеграм-бота, напишите BotFather
# создайте своего бота и вы получите токен
TELEGRAM_CHAT_ID = os.getenv('ID_TOKEN')
TELEGRAM_BOT_TOKEN = os.getenv('BOT_TOKEN')
PATH_TO_FILE = os.path.exists('costs_data/')


bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

updater = Updater(token=TELEGRAM_BOT_TOKEN)

pattern = re.compile(r'\D+|\s+|\W+')


def costs_per_month(update, context):
    """Функция открывает созданный для пользователя файл, 
    собирает данные в словарь и находит сумму затрат за месяц."""
    file_parts = update.message.chat
    user_id = str(file_parts.id)
    file_name = f'{file_parts.first_name}{file_parts.last_name}{user_id[0:3]}'
    data_dict = {}
    try:
        open_data = open(f'costs_data/{file_name}')
        for line in open_data:
            data_dict[line.split(', ')[1]] = int(line.split(', ')[0])
        now = time.time()
        month_ago = time.time() - 60*60*24*30
        costs_per_month = 0
        for date, single_cost in data_dict.items():
            if month_ago <= float(date) <= now:
                costs_per_month += single_cost
            else:
                raise ValueError(f'Неподходящая дата {date}')
        message = (
            f'За последние 30 дней потрачено {costs_per_month} '
            'твоих денежных единиц :).'
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message
        )
    except Exception as error:
        message = f'При выполнении программы возникла ошибка: {error}'
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message
        )


def costs_per_week(update, context):
    """Функция открывает созданный для пользователя файл, 
    собирает данные в словарь и находит сумму затрат за неделю."""
    file_parts = update.message.chat
    user_id = str(file_parts.id)
    file_name = f'{file_parts.first_name}{file_parts.last_name}{user_id[0:3]}'
    data_dict = {}
    try:
        open_data = open(f'costs_data/{file_name}')
        for line in open_data:
            data_dict[line.split(', ')[1]] = int(line.split(', ')[0])
        now = time.time()
        week_ago = time.time() - 60*60*24*7
        costs_per_week = 0
        for date, single_cost in data_dict.items():
            if week_ago <= float(date) <= now:
                costs_per_week += single_cost
            else:
                raise ValueError(f'Неподходящая дата {date}')
        message = (
            f'За последние 7 дней потрачено {costs_per_week}'
            ' твоих денежных единиц :).')
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message
        )
    except Exception as error:
        message = f'При выполнении программы возникла ошибка: {error}'
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message
        )


def start(update, context):
    """Функция приветствия и создания кнопок для пользования ботом."""
    chat = update.effective_chat
    user_name = update.message.chat.first_name
    message = (
        f'Привет, {user_name} хочу помочь тебе разобраться в тратах. '
        'Введи сколько ты потратил(а) за сегодня и данные запишуться в базу. '
        'Нажав на кнопку "costs_per_month", узнаешь свои траты за месяц :)'
    )
    button = telegram.ReplyKeyboardMarkup(
        [
            ['/costs_per_month'],
            ['/costs_per_week']
        ],
        resize_keyboard=True
    )
    context.bot.send_message(
        chat_id=chat.id,
        text=message,
        reply_markup=button
    )


def write_data(update, context):
    """Создает и записывает полученные от пользователя данные в файл."""
    chat = update.effective_chat
    message = update.message.text
    file_parts = update.message.chat
    user_name = file_parts.first_name
    user_id = str(file_parts.id)
    file_name = f'{file_parts.first_name}{file_parts.last_name}{user_id[0:3]}'
    try:
        data = open(f'costs_data/{file_name}', 'a')
    except Exception as er:
        message = f'Ошибка создания/открытия файла: {er}'
    if not pattern.search(message):
        data.write(f'{message}, {time.time()}, \n')
        context.bot.send_message(
            chat_id=chat.id,
            text=f'{user_name},cумма {message} записана в базу'
        )
    else:
        context.bot.send_message(
            chat_id=chat.id,
            text=(
                'В базу записываются только цифры :) '
                f'"{message}" не подходит :)'
            )
        )


start_handler = CommandHandler('start', start)
write_handler = MessageHandler(Filters.text, write_data)
costs_per_month_handler = CommandHandler('costs_per_month', costs_per_month)
costs_per_week_handler = CommandHandler('costs_per_week', costs_per_week)


def main():
    if not PATH_TO_FILE:
        os.mkdir('costs_data/')
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(costs_per_month_handler)
    updater.dispatcher.add_handler(costs_per_week_handler)
    try:
        updater.dispatcher.add_handler(write_handler)
    except Exception as error:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=f'Произошла ошибка {error}'
        )


if __name__ == '__main__':
    main()
    updater.start_polling(poll_interval=1)
