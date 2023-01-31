from aiogram import types, Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('Token'))
dp = Dispatcher(bot)


"""Хендлеры для взаимодействия с клиентом
"""


@dp.message_handler(commands=['start', 'help'])
async def start_bot(message: types.Message):
    bot_home = 't.me/botname'
    try:
        await bot.send_message(message.from_user.id, 'Привет')
        await bot.delete_message()
    except:
        await message.reply(f'Пожалуйста напишите боту в ЛС: {bot_home}')


@dp.message_handler(commands=['Контакты'])
async def get_contacts(message: types.Message):
    await bot.send_message(message.from_user.id, 'Адрес школы и телефоны')


@dp.message_handler(commands=['Режим работы'])
async def get_work_hours(message: types.Message):
    await bot.send_message(message.from_user.id, 'Режим работы вашей школы')


@dp.message_handler(commands=['Учебные группы'])
async def get_training_courses(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберите учебную группу на клавиатуре')


@dp.message_handler(commands=['Преподаватели'])
async def get_trainers_info(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вывод информации на экран о преподавателях')


executor.start_polling(dp, skip_updates=True)
