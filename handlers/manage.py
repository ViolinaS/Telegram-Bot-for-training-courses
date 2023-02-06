from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from magic_filter import F
from create_bot import dp, bot, master_id
from school_database import sqlite_db
from keyboards import kb_manage

"""Администрирование Бота через FSM
Внесение изменений в базу через интерфейс Telegram
Владелец школы сможет сам управлять содержимым курсов/тренировок
и стоимостью в мобильном телефоне.
"""

ID_MASTER = int(master_id)


class FSMcourses(StatesGroup):
    title = State()
    photo = State()
    description = State()
    timetable = State()
    duration_of_lesson = State()
    price_of_lesson = State()


class FSMteacher(StatesGroup):
    name = State()
    photo = State()
    description = State()
    courses = State()



"""Бот проверяет является ли пользователь хозяином бота.
Проверка ID_MASTER по ID на совпадение
В целях безопасности необходимо установить запрет на добавление Бота в другие группы!
Активация клавиатуры администратора по команде /moderate
"""


#@dp.message_handler(commands=['moderate'])
async def verify_owner(message: types.Message):
    id_check = message.from_user.id
    if id_check == ID_MASTER:
        await bot.send_message(message.from_user.id, 'Готов к работе, пожалуйста выбери команды на клавиатуре', reply_markup=kb_manage)
        
    else:
        await bot.send_message(message.from_user.id, 'Доступ запрещен')
    await message.delete()



"""Запуск FSM для внесения изменений в курсы/тренировки
"""

# Начало загрузки данных о курсе
# @dp.message_handler(Text(equals='Загрузить Курс', ignore_case=True), state=None)
async def add_course(message: types.Message):
    if message.from_user.id == ID_MASTER:
        await FSMcourses.title.set()
        await message.reply('Загрузи название курса')


"""Функция отмены, выход из state, если администратор передумал вносить правки в бота
"""
#@dp.message_handler(Text(equals='Отмена Загрузки'), state="*")
#@dp.message_handler(F.text.contains(['отмена', 'stop']).lower(), state="*")
async def cancel_state(message: types.Message, state=FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.reply('Изменения не внесены')


# Бот ловит ответ и пишет в словарь название курса
# @dp.message_handler(state=FSMcourses.title)
async def load_title(message: types.Message, state=FSMContext):
    if message.from_user.id == ID_MASTER:
        async with state.proxy() as data_course:
            data_course['title'] = message.text
        await FSMcourses.next()
        await message.reply('Загрузи фото')


# Бот ловит ответ и сохраняет в словарь фото курса
# @dp.message_handler(content_types=['photo'], state=FSMcourses.photo)
async def load_photo(message: types.Message, state=FSMContext):
    if message.from_user.id == ID_MASTER:
        async with state.proxy() as data_course:
            data_course['photo'] = message.photo[0].file_id
        await FSMcourses.next()
        await message.reply('Загрузи описание курса')


# Бот ловит ответ и сохраняет в словарь описание курса
# @dp.message_handler(state=FSMcourses.description)
async def load_description(message: types.Message, state=FSMContext):
    if message.from_user.id == ID_MASTER:
        async with state.proxy() as data_course:
            data_course['description'] = message.text
        await FSMcourses.next()
        await message.reply('Загрузи расписание')


# Бот ловит сообщение и сохраняет в словарь расписание занятий курса
# @dp.message_handler(state=FSMcourses.timetable)
async def load_timetable(message: types.Message, state=FSMContext):
    if message.from_user.id == ID_MASTER:
        async with state.proxy() as data_course:
            data_course['timetable'] = message.text
        await FSMcourses.next()
        await message.reply('Загрузи продолжительность урока')


# Бот ловит сообщение и сохраняет в словарь время продолжительности одного урока
# @dp.message_handler(state=FSMcourses.duration_of_lesson)
async def load_duration(message: types.Message, state=FSMContext):
    if message.from_user.id == ID_MASTER:
        async with state.proxy() as data_course:
            data_course['duration_of_lesson'] = message.text
        await FSMcourses.next()
        await message.reply('Загрузи стоимость одного урока')


# Бот ловит сообщение и сохраняет в словарь стоимость урока
# @dp.message_handler(state=FSMcourses.price_of_lesson)
async def load_price(message: types.Message, state=FSMContext):
    if message.from_user.id == ID_MASTER:
        async with state.proxy() as data_course:
            data_course['price_of_lesson'] = float(message.text)

        await sqlite_db.sql_add_commands_courses(state)
        await state.finish()
        await message.reply('Загрузка информации об курсе/тренировке окончена')


"""Запуск FSM для внесения информации об учителях
"""
# Начало загрузки данных от учителе
#@dp.message_handler(Text(equals='Загрузить Учителя', ignore_case=True), state=None)

async def add_teacher(message: types.Message):
    if message.from_user.id == ID_MASTER:
        await FSMteacher.name.set()
        await message.reply('Загрузи ФИО учителя')


# Бот ловит ответ и пишет в словарь имя учителя
# @dp.message_handler(state=FSMteacher.name)
async def load_name(message: types.Message, state=FSMContext):
    if message.from_user.id == ID_MASTER:
        async with state.proxy() as data_teacher:
            data_teacher['name'] = message.text
        await FSMteacher.next()
        await message.reply('Загрузи фото')


# Бот ловит ответ и сохраняет в словарь фото учителя
# @dp.message_handler(content_types=['photo'], state=FSMteacher.photo)

async def load_teacher_photo(message: types.Message, state=FSMContext):
    if message.from_user.id == ID_MASTER:
        async with state.proxy() as data_teacher:
            data_teacher['photo'] = message.photo[0].file_id
        await FSMteacher.next()
        await message.reply('Загрузи информацию об учителе')


# Бот ловит ответ и сохраняет в словарь описание навыков учителя
# @dp.message_handler(state=FSMteacher.description)

async def load_teacher_description(message: types.Message, state=FSMContext):
    if message.from_user.id == ID_MASTER:
        async with state.proxy() as data_teacher:
            data_teacher['description'] = message.text
        await FSMteacher.next()
        await message.reply('Загрузи курсы/тренировки для учителя')

# Бот ловит ответ и сохраняет в словарь информацию о курсах, которые ведет учитель
# @dp.message_handler(state=FSMteacher.courses)


async def load_teacher_courses(message: types.Message, state=FSMContext):
    if message.from_user.id == ID_MASTER:
        async with state.proxy() as data_teacher:
            data_teacher['courses'] = message.text

        await sqlite_db.sql_add_commands_teachers(state)
        await state.finish()
        await message.reply('Загрузка информации об учителе окончена')


"""Инлайн кнопки для удаления из базы сведений о тренировках/курсах и учителях
"""

#@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def inform_delete_callback(callback_query: types.CallbackQuery):
    await sqlite_db.delete_course(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'запись {callback_query.data.replace("del ", "")} удалена')
    

#@dp.message_handler(Text(equals='Удалить Курс', ignore_case=True))
async def delete_info(message: types.Message):
    if message.from_user.id == ID_MASTER:
        info = await sqlite_db.choose_delete_courses()
        for info_c in info:
            await bot.send_photo(message.from_user.id, info_c[1], f'{info_c[0]}\nОписание: {info_c[2]}')
            await bot.send_message(message.from_user.id, text='Удалить?', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'delete {info_c[0]}', callback_data=f'del {info_c[0]}')))


#@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def inform_delete_callback_teachers(callback_query: types.CallbackQuery):
    await sqlite_db.delete_teacher(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'запись {callback_query.data.replace("del ", "")} удалена')
    

#@dp.message_handler(Text(equals='Удалить Учителя', ignore_case=True))
async def delete_teacher_info(message: types.Message):
    if message.from_user.id == ID_MASTER:
        info = await sqlite_db.choose_delete_teachers()
        for info_t in info:
            await bot.send_photo(message.from_user.id, info_t[1], f'{info_t[0]}\nОписание: {info_t[2]}')
            await bot.send_message(message.from_user.id, text='Удалить учителя?', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'delete {info_t[0]}', callback_data=f'del {info_t[0]}')))



"""Регистрируем хендлеры
"""


def handlers_register_manage(dp: Dispatcher):
    # FSM для курсов
    dp.register_message_handler(verify_owner, commands=['moderate'])
    dp.register_message_handler(
        add_course, Text(equals='Загрузить Курс', ignore_case=True), state=None)
    dp.register_message_handler(
        cancel_state, Text(equals='Отмена Загрузки'), state="*")
    dp.register_message_handler(cancel_state, F.text.contains(
        ['отмена', 'stop']).lower(), state="*")
    dp.register_message_handler(load_title, state=FSMcourses.title)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMcourses.photo)
    dp.register_message_handler(load_description, state=FSMcourses.description)
    dp.register_message_handler(load_timetable, state=FSMcourses.timetable)
    dp.register_message_handler(
        load_duration, state=FSMcourses.duration_of_lesson)
    dp.register_message_handler(load_price, state=FSMcourses.price_of_lesson)
    

    # FSM для учителей
    dp.register_message_handler(add_teacher, Text(equals='Загрузить Учителя', ignore_case=True), state=None)
    dp.register_message_handler(load_name, state=FSMteacher.name)
    dp.register_message_handler(load_teacher_photo, content_types=['photo'], state=FSMteacher.photo)
    dp.register_message_handler(
        load_teacher_description, state=FSMteacher.description)
    dp.register_message_handler(load_teacher_courses, state=FSMteacher.courses)
    
    # Удаление данных
    dp.register_callback_query_handler(inform_delete_callback, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(delete_info, Text(equals='Удалить Курс', ignore_case=True))
    dp.callback_query_handler(inform_delete_callback_teachers, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(delete_teacher_info, Text(equals='Удалить Учителя', ignore_case=True))
