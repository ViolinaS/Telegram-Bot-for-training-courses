import sqlite3 as sq
from create_bot import bot
from aiogram import types


def bot_tables_sql():
    global base_sql
    global cur
    base_sql = sq.connect('bot_sql.db')
    cur = base_sql.cursor()

    if base_sql == True:
        print('Database connected')
    cur.execute("""CREATE TABLE IF NOT EXISTS courses(
        title Text PRIMARY KEY, 
        photo Text, 
        description Text,                         
        timetable Text, 
        duration_of_lesson Text, 
        price_of_lesson Text)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS teachers(
        name Text PRIMARY KEY, 
        photo Text,
        description Text, 
        courses Text)""")

    base_sql.commit()


async def sql_add_commands_courses(state):
    async with state.proxy() as data_course:
        cur.execute('INSERT INTO courses VALUES (?, ?, ?, ?, ?, ?)',
                    tuple(data_course.values()))

    base_sql.commit()


async def sql_add_commands_teachers(state):
    async with state.proxy() as data_teacher:
        cur.execute('INSERT INTO teachers VALUES (?, ?, ?, ?)',
                    tuple(data_teacher.values()))

    base_sql.commit()


async def sql_read_from_courses(message: types.Message):
    for info_c in cur.execute('SELECT * FROM courses').fetchall():
        await bot.send_photo(message.from_user.id, info_c[1],\
            f'{info_c[0]}\nОписание: {info_c[2]}\n'\
                f'Расписание: {info_c[3]}\nПродолжительность тренировки: {info_c[4]}\nСтоимость тренировки: {info_c[5]} рублей')


async def sql_read_from_teachers(message: types.Message):
    for info_t in cur.execute('SELECT * FROM teachers').fetchall():
        await bot.send_photo(message.from_user.id, info_t[1], \
            f'{info_t[0]}\nОписание: {info_t[2]}\nТренировки: {info_t[3]}')


async def choose_delete_courses():
    return cur.execute('SELECT * FROM courses').fetchall()


async def delete_course(data):
    cur.execute('DELETE FROM courses WHERE title == ?', (data,))
    base_sql.commit()


async def choose_delete_teachers():
    return cur.execute('SELECT * FROM teachers').fetchall()


async def delete_teacher(data):
    cur.execute('DELETE FROM teachers WHERE name == ?', (data, ))
    base_sql.commit()