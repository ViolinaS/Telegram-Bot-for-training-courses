from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

download_course_but = KeyboardButton('/загрузить_курс ')
download_teacher_but = KeyboardButton('/загрузить_учителя')
canceal_but = KeyboardButton('отмена')
delete_but = KeyboardButton('/удалить')


kb_manage = ReplyKeyboardMarkup(resize_keyboard=True)
kb_manage.add(download_course_but).add(download_teacher_but).insert(canceal_but).add(delete_but)