from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

download_course_but = KeyboardButton('Загрузить Курс')
download_teacher_but = KeyboardButton('Загрузить Учителя')
canceal_but = KeyboardButton('Отмена Загрузки')
delete_but_course = KeyboardButton('Удалить Курс')
delete_but_teacher = KeyboardButton('Удалить Учителя')


kb_manage = ReplyKeyboardMarkup(resize_keyboard=True)
kb_manage.add(canceal_but).add(download_course_but).insert(delete_but_course).add(download_teacher_but).insert(delete_but_teacher)