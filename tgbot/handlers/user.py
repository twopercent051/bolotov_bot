from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from tgbot.misc.file_reader import file_reader
from tgbot.models.sql_connector import *
from tgbot.misc.msg_sender import sender_with_photo, sender_without_photo, next_step_timer
from tgbot.keyboards.inline import *
from tgbot.misc.states import FSMUser
from create_bot import bot

import time


async def user_greeting(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    user_info = await get_user_by_id_sql(user_id)
    if user_info is None or user_info[14] == 'enable':
        next_step_time = time.time() + 3600
        # next_step_time = time.time() + 10
        user_tuple = (user_id, 'how_it_work', next_step_time, 0, username)
        await create_user_sql(user_tuple)
        msg_list = file_reader(f'greeting.txt')
        await sender_with_photo(msg_list, 'greeting_photo.txt', user_id)


async def user_how_it_work(user_id):
    next_step_time = time.time() + 3600
    # next_step_time = time.time() + 10
    await user_status_toggle_sql(user_id, 'disable')
    await update_next_step_sql(user_id, 'are_you_ready', next_step_time)
    msg_list = file_reader(f'how_it_work.txt')
    await sender_with_photo(msg_list, 'how_it_work_photo.txt', user_id)


async def are_you_ready(user_id):
    text = 'Вы готовы начать?'
    kb = user_are_you_ready_kb()
    next_step_time = time.time() + 3600 * 24
    # next_step_time = time.time() + 10

    await update_next_step_sql(user_id, 'heating', next_step_time)
    await bot.send_message(user_id, text, reply_markup=kb)


async def user_heating_by_sched(user_id):
    next_step_time = time.time() + 3600 * 48
    # next_step_time = time.time() + 10

    await update_next_step_sql(user_id, 'heating', next_step_time)
    msg_list = file_reader(f'heating.txt')
    await sender_with_photo(msg_list, 'heating_photo.txt', user_id)
    text = 'Начать работать'
    kb = user_heating_kb()
    await bot.send_message(user_id, text, reply_markup=kb)


async def user_heating_by_kb(callback: CallbackQuery):
    next_step_time = time.time() + 3600 * 48
    # next_step_time = time.time() + 10

    user_id = callback.from_user.id
    await update_next_step_sql(user_id, 'heating', next_step_time)
    msg_list = file_reader(f'heating.txt')
    await sender_with_photo(msg_list, 'heating_photo.txt', user_id)
    text = 'Начать работать'
    kb = user_heating_kb()
    await bot.send_message(user_id, text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


async def payment(callback: CallbackQuery):
    text = 'Тут будет платёжка.'
    kb = user_payment_kb()
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


async def payment_finish(callback: CallbackQuery):
    next_step_time = time.time() + 3600
    # next_step_time = time.time() + 10

    paid_for_timestamp = time.time() + 3600 * 24 * 30
    user_id = callback.from_user.id
    await update_next_step_sql(user_id, 'what_i_need', next_step_time)
    await update_payment_sql(user_id, paid_for_timestamp)


async def user_what_i_need(user_id):
    next_step_time = time.time() + 3600
    # next_step_time = time.time() + 10

    await update_next_step_sql(user_id, 'intro_polling', next_step_time)
    msg_list = file_reader(f'what_i_need.txt')
    await sender_with_photo(msg_list, 'what_i_need_photo.txt', user_id)


async def user_intro_polling(user_id):
    text = [
        'Давайте немного познакомимся. Чтобы более объективно формировать программу, мне необходимо знать о вас',
        'некоторые данные'
    ]
    kb = user_ok_kb()
    await update_next_step_sql(user_id, '', 0)
    await bot.send_message(user_id, ' '.join(text), reply_markup=kb)


async def start_polling(callback: CallbackQuery):
    text = 'Год рождения (YYYY)'
    await FSMUser.year.set()
    await callback.message.answer(text)


async def user_get_year(message: Message, state: FSMContext):
    year = message.text
    if year.isdigit() and 1900 < int(year) < 2022:
        async with state.proxy() as data:
            data['year'] = year
        text = 'Рост (в сантиметрах)'
        await FSMUser.height.set()
    else:
        text = 'Не похоже на правду'
    await message.answer(text)


async def user_get_height(message: Message, state: FSMContext):
    height = message.text
    if height.isdigit() and 30 < int(height) < 250:
        async with state.proxy() as data:
            data['height'] = height
        text = 'Вес (в килограммах)'
        await FSMUser.weight.set()
    else:
        text = 'Не похоже на правду'
    await message.answer(text)


async def user_get_weight(message: Message, state: FSMContext):
    weight = message.text
    if weight.isdigit() and 30 < int(weight) < 250:
        async with state.proxy() as data:
            data['weight'] = weight
        text = 'Курите?'
        kb = user_smoking_kb()
        await FSMUser.smoking.set()
    else:
        text = 'Не похоже на правду'
        kb = None
    await message.answer(text, reply_markup=kb)


async def user_get_smoking(callback: CallbackQuery, state: FSMContext):
    smoking = callback.data
    async with state.proxy() as data:
        data['smoking'] = smoking
    text = 'Выпиваете?'
    kb = user_drinking_kb()
    await FSMUser.drinking.set()
    await callback.message.answer(text, reply_markup=kb)


async def user_get_drinking(callback: CallbackQuery, state: FSMContext):
    drinking = callback.data
    async with state.proxy() as data:
        data['drinking'] = drinking
    text = 'Ваш часовой пояс'
    kb = user_timezone_kb()
    await FSMUser.timezone.set()
    await callback.message.answer(text, reply_markup=kb)


async def user_get_timezone(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    timezone = int(callback.data.split(':')[1])
    async with state.proxy() as data:
        data['timezone'] = timezone
        data['user_id'] = user_id
    await FSMUser.home.set()
    await update_user_polling_sql(state)
    next_step_tm = next_step_timer(timezone, 1, 20)
    await update_next_step_sql(user_id, 'week:program:1', next_step_tm)


async def user_week_program(user_id, week_id):
    next_step_time = time.time() + 3600
    await update_next_step_sql(user_id, f'week:focus:{week_id}', next_step_time)
    msg_list = file_reader(f'week_{week_id}_program.txt')
    await sender_without_photo(msg_list, user_id)


async def user_week_focus(user_id, week_id):
    user_tz = await get_user_timezone_sql(user_id)
    next_step_time = next_step_timer(user_tz, 1, 12)
    await update_next_step_sql(user_id, f'workout:program:1:week:{week_id}', next_step_time)
    msg_list = file_reader(f'week_{week_id}_focus.txt')
    await sender_without_photo(msg_list, user_id)


async def user_workout_program(user_id, week_id, workout_id):
    user_tz = await get_user_timezone_sql(user_id)
    next_step_time = next_step_timer(user_tz, 0, 20)
    await update_next_step_sql(user_id, f'workout:reminder:{workout_id}:week:{week_id}', next_step_time)
    msg_list = file_reader(f'week_{week_id}_workout_{workout_id}_program.txt')
    await sender_without_photo(msg_list, user_id)


async def user_workout_reminder(user_id, week_id, workout_id):
    user_tz = await get_user_timezone_sql(user_id)
    next_step_time = next_step_timer(user_tz, 1, 20)
    await update_next_step_sql(user_id, f'workout:feedback_1:{workout_id}:week:{week_id}', next_step_time)
    msg_list = file_reader(f'week_{week_id}_workout_{workout_id}_reminder.txt')
    await sender_without_photo(msg_list, user_id)


async def user_workout_feedback_1(user_id, week_id, workout_id):
    text = 'Как прошла вчерашняя тренировка? Поделись обратной связью:'
    kb = user_workout_feedback_1_kb(week_id, workout_id)
    await update_next_step_sql(user_id, '', 0)
    await bot.send_message(user_id, text, reply_markup=kb)


async def user_workout_feedback_2(callback: CallbackQuery):
    user_id = callback.from_user.id
    feedback = callback.data.split(':')[1]
    week_id = callback.data.split(':')[2]
    workout_id = callback.data.split(':')[3]
    await create_feedback_1_sql(user_id, week_id, workout_id, feedback)
    if feedback == 'positive' or feedback == 'partly':
        text = 'Насколько сложной оказалась тренировка?'
        kb = user_workout_feedback_2_kb(week_id, workout_id)
        await callback.message.answer(text, reply_markup=kb)
    else:
        next_step_time = time.time() + 120
        await update_next_step_sql(user_id, f'workout:support:{workout_id}:week:{week_id}', next_step_time)


async def user_workout_feedback_finish(callback: CallbackQuery):
    user_id = callback.from_user.id
    feedback = callback.data.split(':')[1]
    week_id = callback.data.split(':')[2]
    workout_id = callback.data.split(':')[3]
    await create_feedback_2_sql(user_id, week_id, workout_id, feedback)
    next_step_time = time.time() + 120
    await update_next_step_sql(user_id, f'workout:support:{workout_id}:week:{week_id}', next_step_time)


async def user_workout_support(user_id, week_id, workout_id):
    user_tz = await get_user_timezone_sql(user_id)
    next_step_time = next_step_timer(user_tz, 1, 10)
    await update_next_step_sql(user_id, f'workout:habit:{workout_id}:week:{week_id}', next_step_time)
    feedback = await get_user_feedback_sql(user_id, week_id, workout_id)
    if feedback[0] == 'positive' or feedback[0] == 'partly':
        msg_list = file_reader(f'week_{week_id}_workout_{workout_id}_suppos.txt')
    else:
        msg_list = file_reader(f'week_{week_id}_workout_{workout_id}_supneg.txt')
    await sender_without_photo(msg_list, user_id)


async def user_workout_habit(user_id, week_id, workout_id):
    user_tz = await get_user_timezone_sql(user_id)
    if workout_id == 1 or workout_id == 2:
        next_step_time = next_step_timer(user_tz, 1, 12)
        await update_next_step_sql(user_id, f'workout:program:{workout_id + 1}:week:{week_id}', next_step_time)
    else:
        next_step_time = next_step_timer(user_tz, 0, 21)
        await update_next_step_sql(user_id, f'week:congratulation:{week_id}', next_step_time)
    msg_list = file_reader(f'week_{week_id}_workout_{workout_id}_habit.txt')
    await sender_without_photo(msg_list, user_id)


async def user_week_congratulation(user_id, week_id):
    user_tz = await get_user_timezone_sql(user_id)
    next_step_time = next_step_timer(user_tz, 1, 10)
    await update_next_step_sql(user_id, f'week:general_practices:{week_id}', next_step_time)
    msg_list = file_reader(f'week_{week_id}_congratulation.txt')
    await sender_without_photo(msg_list, user_id)


async def user_week_general_practices(user_id, week_id):
    user_tz = await get_user_timezone_sql(user_id)
    next_step_time = next_step_timer(user_tz, 0, 12)
    await update_next_step_sql(user_id, f'week:trichotomy_practices:{week_id}', next_step_time)
    msg_list = file_reader(f'week_{week_id}_general_practices.txt')
    await sender_without_photo(msg_list, user_id)


async def user_week_trichotomy_practices(user_id, week_id):
    user_tz = await get_user_timezone_sql(user_id)
    next_step_time = next_step_timer(user_tz, 0, 20)
    await update_next_step_sql(user_id, f'week:feedback:{week_id}', next_step_time)
    msg_list = file_reader(f'week_{week_id}_trichotomy_practices.txt')
    await sender_without_photo(msg_list, user_id)


async def user_week_feedback(user_id, week_id):
    text = [
        'Давайте немного выдохнем и попробуем проанализировать первую неделю, нужна небольшая обратная связь от вас.',
        '',
        'Как ваше самочувствие после первой недели тренировок?'
    ]
    kb = user_week_feedback_kb(week_id)
    await update_next_step_sql(user_id, '', 0)
    await bot.send_message(user_id, '\n'.join(text), reply_markup=kb)


async def user_week_feedback_finish(callback: CallbackQuery):
    user_id = callback.from_user.id
    feedback = callback.data.split(':')[1]
    week_id = int(callback.data.split(':')[2])
    await create_feedback_week_sql(user_id, week_id, feedback)
    weeks_num = await get_weeks_sql()
    print(weeks_num)
    if week_id == weeks_num[-1][0]:
        text = 'Вы успешно завершили курс'
        await update_next_step_sql(user_id, '', 0)
        await user_status_toggle_sql(user_id, 'disable')
        await callback.message.answer(text)
    else:
        user_tz = await get_user_timezone_sql(user_id)
        next_step_time = next_step_timer(user_tz, 1, 20)
        await update_next_step_sql(user_id, f'workout:program:1:week:{week_id + 1}', next_step_time)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_greeting, commands=["start"], state="*")
    dp.register_message_handler(user_get_year, content_types='text', state=FSMUser.year)
    dp.register_message_handler(user_get_height, content_types='text', state=FSMUser.height)
    dp.register_message_handler(user_get_weight, content_types='text', state=FSMUser.weight)

    dp.register_callback_query_handler(user_heating_by_kb, lambda x: x.data == 'no_ready', state='*')
    dp.register_callback_query_handler(payment, lambda x: x.data == 'yes_ready', state='*')
    dp.register_callback_query_handler(payment, lambda x: x.data == 'begin', state='*')
    dp.register_callback_query_handler(payment_finish, lambda x: x.data == 'paid', state='*')
    dp.register_callback_query_handler(start_polling, lambda x: x.data == 'ok', state='*')
    dp.register_callback_query_handler(user_get_smoking, state=FSMUser.smoking)
    dp.register_callback_query_handler(user_get_drinking, state=FSMUser.drinking)
    dp.register_callback_query_handler(user_get_timezone, lambda x: x.data.split(':')[0] == 'tz', state='*')
    dp.register_callback_query_handler(user_workout_feedback_2, lambda x: x.data.split(':')[0] == 'feedback_1',
                                       state='*')
    dp.register_callback_query_handler(user_workout_feedback_finish, lambda x: x.data.split(':')[0] == 'feedback_2',
                                       state='*')
    dp.register_callback_query_handler(user_week_feedback_finish, lambda x: x.data.split(':')[0] == 'feedback_week',
                                       state='*')
