from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

download_course_but = KeyboardButton('/загрузить_курс ')
download_teacher_but = KeyboardButton('/загрузить_учителя')
canceal_but = KeyboardButton('/отмена_загрузки')
delete_but_course = KeyboardButton('/удалить_курс')
delete_but_teacher = KeyboardButton('/удалить_учителя')


kb_manage = ReplyKeyboardMarkup(resize_keyboard=True)
kb_manage.add(download_course_but).add(download_teacher_but).insert(delete_but_course).add(delete_but_teacher).insert(canceal_but)