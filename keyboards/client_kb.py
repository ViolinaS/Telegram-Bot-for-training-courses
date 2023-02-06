from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

but1 = KeyboardButton('Контакты')
but2 = KeyboardButton('Режим работы')
but3 = KeyboardButton('Тренировки')
but4 = KeyboardButton('Преподаватели')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(but1).add(but2).insert(but3).add(but4)