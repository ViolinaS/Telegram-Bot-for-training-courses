from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, Dispatcher

"""Администрирование Бота через FSM
   Внесение изменений в базу через интерфейс Telegram
   Владелец школы (условный заказчик программы) сможет 
   сам управлять содержимым курсов/тренировок и стоимостью в  
   мобильном телефоне.
"""


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


# Начало загрузки данных о курсе
@dp.message_handler(commands=['Внести-Курс'], state=None)
async def add_course(message: types.Message):
    await FSMcourses.title.set()
    await message.reply('Загрузи название курса')


# Бот ловит ответ и пишет в словарь название курса
@dp.message_handler(state=FSMcourses.title)
async def load_title(message: types.Message, state=FSMContext):
    async with state.proxy() as data_course:
        data_course['title'] = message.text
    await FSMcourses.next()
    await message.reply('Загрузи фото')


# Бот ловит ответ и сохраняет в словарь фото курса
@dp.message_handler(content_types=['photo'], state=FSMcourses.photo)
async def load_photo(message: types.Message, state=FSMContext):
    async with state.proxy() as data_course:
        data_course['photo'] = message.photo[0].file_id
    await FSMcourses.next()
    await message.reply('Загрузи описание курса')


# Бот ловит ответ и сохраняет в словарь описание курса
@dp.message_handler(state=FSMcourses.description)
async def load_description(message: types.Message, state=FSMContext):
    async with state.proxy() as data_course:
        data_course['description'] = message.text
    await FSMcourses.next()
    await message.reply('Загрузи расписание')


# Бот ловит сообщение и сохраняет в словарь расписание занятий курса
@dp.message_handler(state=FSMcourses.timetable)
async def load_timetable(message: types.Message, state=FSMContext):
    async with state.proxy() as data_course:
        data_course['timetable'] = message.text
    await FSMcourses.next()
    await message.reply('Загрузи продолжительность урока')
        

# Бот ловит сообщение и сохраняет в словарь время продолжительности одного урока
dp.message_handler(state=FSMcourses.duration_of_lesson)
async def load_duration(message: types.Message, state=FSMContext):
    async with state.proxy() as data_course:
        data_course['duration_of_lesson'] = message.text
    await FSMcourses.next()
    await message.reply('Загрузи стоимость одного урока')

# Бот ловит сообщение и сохраняет в словарь стоимость урока
dp.message_handler(state=FSMcourses.price_of_lesson)
async def load_price(message: types.Message, state=FSMContext):
    async with state.proxy() as data_course:
        data_course['price_of_lesson'] = float(message.text)
    
    async with state.proxy() as data_course:
        await message.reply(str(data_course))
    await state.finish()

# Регестрируем хендлеры 
def register_handlers_manage(dp: Dispatcher):
    dp.register_message_handler(add_course, commands=['Внести-Курс'], state=None)
    dp.register_message_handler(load_title, state=FSMcourses.title)
    dp.register_message_handler(load_photo, state=FSMcourses.photo)
    dp.register_message_handler(load_description, state=FSMcourses.description)
    dp.register_message_handler(load_timetable, state=FSMcourses.timetable)
    dp.register_message_handler(load_duration, state=FSMcourses.duration_of_lesson)
    dp.register_message_handler(load_price, state=FSMcourses.price_of_lesson)          