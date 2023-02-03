from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

download_but = KeyboardButton('/Загрузить ')
delete_but = KeyboardButton('/Удалить')

kb_manage = ReplyKeyboardMarkup(resize_keyboard=True)
kb_manage.add(download_but).add(delete_but)