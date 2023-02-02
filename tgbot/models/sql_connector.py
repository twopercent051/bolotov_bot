import pymysql
from create_bot import config


def connection_init():
    host = config.db.host
    user = config.db.user
    password = config.db.password
    db_name = config.db.database
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.SSCursor
    )
    return connection


def sql_start():
    connection = connection_init()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS weeks(
                           id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
                           week_num INT,
                           is_enabled VARCHAR(10));
                           """)
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS users(
                           id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
                           user_id VARCHAR(40),
                           next_step VARCHAR(40),
                           dtime_next_step INT,
                           paid_for INT,
                           year INT,
                           height INT,
                           weight INT,
                           smoking VARCHAR(100),
                           drinking VARCHAR(100),
                           timezone INT,
                           week_id INT,
                           workout_id INT,
                           username VARCHAR(40),
                           status VARCHAR(20));
                           """)
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS feedbacks(
                           id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
                           user_id VARCHAR(40),
                           week_id INT,
                           workout_id INT,
                           feedback_1 VARCHAR(40),
                           feedback_2 VARCHAR(40),
                           feedback_week VARCHAR(40));
                           """)
        print('MySQL started')
    finally:
        connection.close()


async def create_week_sql(week_id):
    connection = connection_init()
    query = 'INSERT INTO weeks (week_num, is_enabled) VALUES (%s, %s);'
    query_tuple = (week_id, 'True')
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, query_tuple)
    finally:
        connection.commit()
        connection.close()


async def get_weeks_sql():
    connection = connection_init()
    query = 'SELECT week_num FROM weeks;'
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
    finally:
        connection.commit()
        connection.close()
        return result


async def delete_week_sql(week_id):
    connection = connection_init()
    query = 'DELETE FROM weeks WHERE week_num = (%s);'
    query_tuple = (week_id,)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, query_tuple)
    finally:
        connection.commit()
        connection.close()


async def get_user_by_id_sql(user_id):
    connection = connection_init()
    query = 'SELECT * FROM users WHERE user_id = (%s);'
    query_tuple = (user_id,)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, query_tuple)
            result = cursor.fetchone()
    finally:
        connection.commit()
        connection.close()
        return result


async def create_user_sql(user_tuple):
    connection = connection_init()
    query = 'INSERT INTO users (user_id, next_step, dtime_next_step, paid_for, username) VALUES (%s, %s, %s, %s, %s);'
    query_tuple = user_tuple
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, query_tuple)
    finally:
        connection.commit()
        connection.close()


async def get_users_list_sql():
    connection = connection_init()
    query = 'SELECT * FROM users;'
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
    finally:
        connection.commit()
        connection.close()
        return result


async def user_status_toggle_sql(user_id, status):
    connection = connection_init()
    query = 'UPDATE users SET status = (%s) WHERE user_id = (%s);'
    query_tuple = (status, user_id)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, query_tuple)
    finally:
        connection.commit()
        connection.close()


async def update_next_step_sql(user_id, next_step, dtime_next_step):
    connection = connection_init()
    query = 'UPDATE users SET next_step = (%s), dtime_next_step = (%s) WHERE user_id = (%s);'
    query_tuple = (next_step, dtime_next_step, user_id)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, query_tuple)
    finally:
        connection.commit()
        connection.close()


async def update_payment_sql(user_id, paid_for):
    connection = connection_init()
    query = 'UPDATE users SET paid_for = (%s) WHERE user_id = (%s);'
    query_tuple = (paid_for, user_id)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, query_tuple)
    finally:
        connection.commit()
        connection.close()


async def update_user_polling_sql(state):
    connection = connection_init()
    async with state.proxy() as data:
        user_id = data.as_dict()['user_id']
        year = data.as_dict()['year']
        height = data.as_dict()['height']
        weight = data.as_dict()['weight']
        smoking = data.as_dict()['smoking']
        drinking = data.as_dict()['drinking']
        timezone = data.as_dict()['timezone']
    query = """UPDATE users 
            SET year = (%s), 
            height = (%s), 
            weight = (%s), 
            smoking = (%s), 
            drinking = (%s), 
            timezone = (%s)
            WHERE user_id = (%s);
            """
    query_tuple = (year, height, weight, smoking, drinking, timezone, user_id)
    print(query_tuple)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, query_tuple)
    finally:
        connection.commit()
        connection.close()


async def update_user_week_sql(user_id, week_id):
    connection = connection_init()
    query = 'UPDATE users SET week_id = (%s), workout_id = 1 WHERE user_id = (%s);'
    query_tuple = (week_id, user_id)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, query_tuple)
    finally:
        connection.commit()
        connection.close()


async def update_user_workout_sql(user_id, workout_id):
    connection = connection_init()
    query = 'UPDATE users SET workout_id = (%s) WHERE user_id = (%s);'
    query_tuple = (workout_id, user_id)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, query_tuple)
    finally:
        connection.commit()
        connection.close()


async def get_user_timezone_sql(user_id):
    connection = connection_init()
    query = 'SELECT id FROM users WHERE user_id = (%s);'
    query_tuple = (user_id,)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, query_tuple)
            result = cursor.fetchone()
    finally:
        connection.commit()
        connection.close()
        return result[0]


async def create_feedback_1_sql(user_id, week_id, workout_id, feedback):
    connection = connection_init()
    query = 'INSERT INTO feedbacks (user_id, week_id, workout_id, feedback_1) VALUES (%s, %s, %s, %s);'
    query_tuple = (user_id, week_id, workout_id, feedback)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, query_tuple)
    finally:
        connection.commit()
        connection.close()


async def create_feedback_2_sql(user_id, week_id, workout_id, feedback):
    connection = connection_init()
    query = 'UPDATE feedbacks SET feedback_2 = (%s) WHERE user_id = (%s) AND week_id = (%s) AND workout_id = (%s);'
    query_tuple = (feedback, user_id, week_id, workout_id)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, query_tuple)
    finally:
        connection.commit()
        connection.close()


async def get_user_feedback_sql(user_id, week_id, workout_id):
    connection = connection_init()
    query = 'SELECT feedback_1, feedback_2 FROM feedbacks WHERE user_id = (%s) AND week_id = (%s) AND workout_id = (' \
            '%s);'
    query_tuple = (user_id, week_id, workout_id)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, query_tuple)
            result = cursor.fetchone()
    finally:
        connection.commit()
        connection.close()
        return result


async def create_feedback_week_sql(user_id, week_id, feedback):
    connection = connection_init()
    query = 'UPDATE feedbacks SET feedback_week = (%s) WHERE user_id = (%s) AND week_id = (%s) AND workout_id = 3;'
    query_tuple = (feedback, user_id, week_id)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, query_tuple)
    finally:
        connection.commit()
        connection.close()
