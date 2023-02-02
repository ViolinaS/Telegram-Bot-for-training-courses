import sqlite3 as sq

def courses_base_sql():
    global base_courses, cur
    base_courses = sq.connect('courses_db')
    cur = base_courses.cursor()
    if base_courses:
        print('Database courses connected')
    base_courses.execute('CREATE TABLE IF NOT EXISTS курсы(title Text PRIMARY KEY, photo Text, description Text,\
                         timetable Text, duration_of_lesson Text, price_of_lesson Integer)')
    base_courses.commit()
    
def teacher_base_sql():
    global base_teacher, cursor
    base_teacher = sq.connect('teachers_db')
    cursor = base_teacher.cursor()
    if base_teacher:
        print('Database teachers connected')
    base_teacher.execute('CREATE TABLE IF NOT EXISTS учителя(name Text PRIMARY KEY, photo Text,\
                         description Text, courses Text)')
    base_teacher.commit()
    

async def sql_add_command_courses(state):
    async with state.proxy() as data_course:
        cur.execute('INSERT INTO курсы VALUES (?, ?, ?, ?, ?, ?)', tuple(data_course.values()))
        base_courses.commit()
        

async def sql_add_command_teachers(state):
    async with state.proxy() as data_teacher:
        cursor.execute('INSERT INTO учителя VALUES (?, ?, ?, ?)', tuple(data_teacher.values()))
        base_teacher.commit()

