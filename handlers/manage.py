from aiogram import types, Dispatcher
from aiogram.types import chat
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from magic_filter import F
from create_bot import dp, bot, master_id
from school_database import sqlite_db
from keyboards import kb_manage

"""Администрирование Бота через FSM
Внесение изменений в базу через интерфейс Telegram
Владелец школы сможет сам управлять содержимым курсов/тренировок
и стоимостью в мобильном телефоне.
"""

ID_MASTER = master_id
ID_ADMIN = None


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


"""Бот проверяет является ли пользователь администратором школьной группы в Телеграм.
Проверка по ID_ADMIN (получаем ID текущего администратора чата в Телеграм)
В целях безопасности необходимо установить запрет на добавление Бота в другие группы!
Одновременно грузить информацию в Бота могут хозяин бота(ID_MASTER) и 
один администратор(ID_ADMIN), назначенный хозяином.
Доступ к загрузке информации гарантирован, только если администратор и хозяин бота
состоят в одной группе и оба являются администраторами группы.
Доступ также гарантирован для ID-MASTER при отсутствии других администраторов.
"""


@dp.message_handler(commands=['moderator'])
async def verify_admin(message: types.Message):
    global ID_ADMIN
    ID_ADMIN = message.from_user.id
    
    try:
        chat_admins = await bot.get_chat_administrators(chat_id=message.chat.id)
        await print(chat_admins)
    
    except:
        print('There are no admins in a private chat')
        chat_admins = []
        
              
    if ID_MASTER and ID_ADMIN in chat_admins or ID_MASTER in chat_admins:
        await bot.send_message(message.from_user.id, 'Готов к работе', reply_markup=kb_manage)
    else:
        await bot.send_message(message.from_user.id, 'Доступ запрещен')
    await message.delete()

    """Запуск FSM для внесения изменений в курсы/тренировки
    """

# Начало загрузки данных о курсе
# @dp.message_handler(commands=['Внести-Курс'], state=None)


async def add_course(message: types.Message):
    if message.from_user.id == ID_MASTER or ID_ADMIN:
        await FSMcourses.title.set()
        await message.reply('Загрузи название курса')


"""Функция отмены, выход из state, если администратор передумал вносить правки в бота
"""
# @dp.message_handler(state="*", commands=['отмена', 'stop'])
# @dp.message_handler(F.text.contains(['отмена', 'stop']).lower(), state="*")


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
    if message.from_user.id == ID_MASTER or ID_ADMIN:
        async with state.proxy() as data_course:
            data_course['title'] = message.text
        await FSMcourses.next()
        await message.reply('Загрузи фото')


# Бот ловит ответ и сохраняет в словарь фото курса
# @dp.message_handler(content_types=['photo'], state=FSMcourses.photo)
async def load_photo(message: types.Message, state=FSMContext):
    if message.from_user.id == ID_MASTER or ID_ADMIN:
        async with state.proxy() as data_course:
            data_course['photo'] = message.photo[0].file_id
        await FSMcourses.next()
        await message.reply('Загрузи описание курса')


# Бот ловит ответ и сохраняет в словарь описание курса
# @dp.message_handler(state=FSMcourses.description)
async def load_description(message: types.Message, state=FSMContext):
    if message.from_user.id == ID_MASTER or ID_ADMIN:
        async with state.proxy() as data_course:
            data_course['description'] = message.text
        await FSMcourses.next()
        await message.reply('Загрузи расписание')


# Бот ловит сообщение и сохраняет в словарь расписание занятий курса
# @dp.message_handler(state=FSMcourses.timetable)
async def load_timetable(message: types.Message, state=FSMContext):
    if message.from_user.id == ID_MASTER or ID_ADMIN:
        async with state.proxy() as data_course:
            data_course['timetable'] = message.text
        await FSMcourses.next()
        await message.reply('Загрузи продолжительность урока')


# Бот ловит сообщение и сохраняет в словарь время продолжительности одного урока
# @dp.message_handler(state=FSMcourses.duration_of_lesson)
async def load_duration(message: types.Message, state=FSMContext):
    if message.from_user.id == ID_MASTER or ID_ADMIN:
        async with state.proxy() as data_course:
            data_course['duration_of_lesson'] = message.text
        await FSMcourses.next()
        await message.reply('Загрузи стоимость одного урока')


# Бот ловит сообщение и сохраняет в словарь стоимость урока
# @dp.message_handler(state=FSMcourses.price_of_lesson)
async def load_price(message: types.Message, state=FSMContext):
    if message.from_user.id == ID_MASTER or ID_ADMIN:
        async with state.proxy() as data_course:
            data_course['price_of_lesson'] = float(message.text)

        await sqlite_db.sql_add_command_courses(state)
        await state.finish()
        await message.reply('Загрузка информации об курсе/тренировке окончена')


    """Запуск FSM для внесения информации об учителях
    """
# Начало загрузки данных от учителе
# @dp.message_handler(commands=['Внести-Учителя'], state=None)

async def add_teacher(message: types.Message):
    if message.from_user.id == ID_MASTER or ID_ADMIN:
        await FSMteacher.name.set()
        await message.reply('Загрузи ФИО учителя')


# Бот ловит ответ и пишет в словарь имя учителя
# @dp.message_handler(state=FSMteacher.name)
async def load_name(message: types.Message, state=FSMContext):
    if message.from_user.id == ID_MASTER or ID_ADMIN:
        async with state.proxy() as data_teacher:
            data_teacher['name'] = message.text
        await FSMteacher.next()
        await message.reply('Загрузи фото')


# Бот ловит ответ и сохраняет в словарь фото учителя
# @dp.message_handler(content_types=['photo'], state=FSMteacher.photo)

async def load_teacher_photo(message: types.Message, state=FSMContext):
    if message.from_user.id == ID_MASTER or ID_ADMIN:
        async with state.proxy() as data_teacher:
            data_teacher['photo'] = message.photo[0].file_id
        await FSMteacher.next()
        await message.reply('Загрузи информацию об учителе')


# Бот ловит ответ и сохраняет в словарь описание навыков учителя
# @dp.message_handler(state=FSMteacher.description)

async def load_teacher_description(message: types.Message, state=FSMContext):
    if message.from_user.id == ID_MASTER or ID_ADMIN:
        async with state.proxy() as data_teacher:
            data_teacher['description'] = message.text
        await FSMteacher.next()
        await message.reply('Загрузи курсы/тренировки для учителя')

# Бот ловит ответ и сохраняет в словарь информацию о курсах, которые ведет учитель
# @dp.message_handler(state=FSMteacher.courses)


async def load_teacher_courses(message: types.Message, state=FSMContext):
    if message.from_user.id == ID_MASTER or ID_ADMIN:
        async with state.proxy() as data_teacher:
            data_teacher['courses'] = message.text

        await sqlite_db.sql_add_command_teachers(state)
        await state.finish()
        await message.reply('Загрузка информации об учителе окончена')


"""Регистрируем хендлеры
"""


def register_handlers_manage(dp: Dispatcher):
    # FSM для курсов
    dp.register_message_handler(verify_admin, commands=['moderator'])
    dp.register_message_handler(
        add_course, commands=['Внести-Курс'], state=None)
    dp.register_message_handler(
        cancel_state, state="*", commands=['отмена', 'stop'])
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
    dp.register_message_handler(add_teacher, commands=[
                                'Внести-Учителя'], state=None)
    dp.register_message_handler(load_name, state=FSMteacher.name)
    dp.register_message_handler(load_teacher_photo, content_types=['photo'], state=FSMteacher.photo)
    dp.register_message_handler(
        load_teacher_description, state=FSMteacher.description)
    dp.register_message_handler(load_teacher_courses, state=FSMteacher.courses)
