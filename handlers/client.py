from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot, bot_address
from keyboards import kb_client
from school_database import sqlite_db

"""Хендлеры для взаимодействия с клиентом
"""


#@dp.message_handler(commands=['start', 'help'])
async def start_bot(message: types.Message):
    bot_home = bot_address  # можно указать адрес бота в телеграм строкой 't.me/bot'
    try:
        await bot.send_message(message.from_user.id, 
                               f'Привет, Это бот "Центра йоги и здоровья, Практики нашего центра подходят людям любого уровня подготовки,\
            Пожалуйста воспользуйтесь клавиатурой, чтобы узнать больше о нашем центре', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply(f'Пожалуйста напишите боту в ЛС: {bot_home}')


#@dp.message_handler(Text(equals='Контакты', ignore_case=True))
async def get_contacts(message: types.Message):
    address = "Yoga's Street, 00/00"
    phones = '+000 000-00-00'
    await bot.send_message(message.from_user.id, f'Адрес школы: {address} \nКонтактные номера: {phones}')


#@dp.message_handler(Text(equals='Режим работы', ignore_case=True))
async def get_work_hours(message: types.Message):
    w_days = 'пн-вс'
    w_hours = '06.30–22.30'
    await bot.send_message(message.from_user.id, f'Время работы: {w_days} {w_hours}')


#@dp.message_handler(Text(equals='Тренировки', ignore_case=True))
async def get_training_courses(message: types.Message):
    await sqlite_db.sql_read_from_courses(message)


#@dp.message_handler(Text(equals='Преподаватели', ignore_case=True))
async def get_trainers_info(message: types.Message):
    await sqlite_db.sql_read_from_teachers(message)


def handlers_register(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=['start', 'help'])
    dp.register_message_handler(get_contacts, Text(equals='Контакты', ignore_case=True))
    dp.register_message_handler(get_work_hours, Text(equals='Режим работы', ignore_case=True))
    dp.register_message_handler(get_training_courses, Text(equals='Тренировки', ignore_case=True))
    dp.register_message_handler(get_trainers_info, Text(equals='Преподаватели', ignore_case=True))
    