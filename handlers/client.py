from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot, bot_address, client_commands
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


#@dp.message_handler(commands=['Контакты'])
async def get_contacts(message: types.Message):
    address = "Yoga's Street, 00/00"
    phones = '+000 000-00-00'
    await bot.send_message(message.from_user.id, f'Адрес школы: {address} \nКонтактные номера: {phones}')


#@dp.message_handler(commands=['Режим работы'])
async def get_work_hours(message: types.Message):
    w_days = 'пн-вс'
    w_hours = '06.30–22.30'
    await bot.send_message(message.from_user.id, f'Время работы: {w_days} {w_hours}')


#@dp.message_handler(commands=['Тренировки'])
async def get_training_courses(message: types.Message):
    await sqlite_db.sql_read_from_courses(message)


#@dp.message_handler(commands=['Преподаватели'])
async def get_trainers_info(message: types.Message):
    await sqlite_db.sql_read_from_courses(message)


#@dp.message_handler() # Фильтрация спама и мата в чате клиентской части
# async def clean_chat(message: types.Message):
#     if message.text not in client_commands:
#         await message.delete()
#         await bot.send_message(message.from_user.id, 'Бот Вас не понял, пожалуйста воспользуйтесь командами на клавиатуре')

def handlers_register(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=['start', 'help'])
    dp.register_message_handler(get_contacts, commands=['Контакты'])
    dp.register_message_handler(get_work_hours, commands=['Режим_работы'])
    dp.register_message_handler(get_training_courses, commands=['Тренировки'])
    dp.register_message_handler(get_trainers_info, commands=['Преподаватели'])
    #dp.register_message_handler(clean_chat)