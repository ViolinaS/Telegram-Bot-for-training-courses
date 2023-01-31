from aiogram import types, Dispatcher
from create_bot import dp, bot


"""Хендлеры для взаимодействия с клиентом
"""


#@dp.message_handler(commands=['start', 'help'])
async def start_bot(message: types.Message):
    bot_home = 't.me/botname'
    try:
        await bot.send_message(message.from_user.id, 'Привет')
        await message.delete()
    except:
        await message.reply(f'Пожалуйста напишите боту в ЛС: {bot_home}')


#@dp.message_handler(commands=['Контакты'])
async def get_contacts(message: types.Message):
    await bot.send_message(message.from_user.id, 'Адрес школы и телефоны')


#@dp.message_handler(commands=['Режим работы'])
async def get_work_hours(message: types.Message):
    await bot.send_message(message.from_user.id, 'Режим работы вашей школы')


#@dp.message_handler(commands=['Учебные группы'])
async def get_training_courses(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберите учебную группу на клавиатуре')


#@dp.message_handler(commands=['Преподаватели'])
async def get_trainers_info(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вывод информации на экран о преподавателях')


#@dp.message_handler() # Фильтрация спама и мата в чате
async def clean_chat(message: types.Message):
    if message.text not in ['start', 'help', 'Преподаватели', 'Учебные группы', 'Режим работы', 'Контакты']:
        await message.delete()
        await bot.send_message(message.from_user.id, 'Бот Вас не понял, пожалуйста воспользуйтесь командами на клавиатуре')

def handlers_register(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands=['start', 'help'])
    dp.register_message_handler(get_contacts, commands=['Контакты'])
    dp.register_message_handler(get_work_hours, commands=['Режим работы'])
    dp.register_message_handler(get_training_courses, commands=['Учебные группы'])
    dp.register_message_handler(get_trainers_info, commands=['Преподаватели'])
    dp.register_message_handler(clean_chat)