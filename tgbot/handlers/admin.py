from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
import os
import time

from tgbot.keyboards.inline import *
from tgbot.misc.states import FSMAdmin
from tgbot.misc.file_reader import file_reader, photo_append, week_files
from tgbot.models.sql_connector import *
from create_bot import bot, config

admin_group = config.misc.admin_group

async def admin_start(message: Message):
    text = 'Привет, хозяин!'
    kb = admin_mainmenu_kb()
    await message.answer(text, reply_markup=kb)


async def admin_start_clb(callback: CallbackQuery):
    text = 'Привет, хозяин!'
    kb = admin_mainmenu_kb()
    await FSMAdmin.home.set()
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)

async def edit_texts(callback: CallbackQuery):
    text = 'Выберите раздел для редактирования'
    kb = admin_edit_text_kb()
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)

async def edit_introduction(callback: CallbackQuery):
    text = 'Выберите раздел'
    kb = admin_intro_kb()
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)

async def template_main(callback: CallbackQuery, state: FSMContext):
    chapter = callback.data.split(':')[1]
    text = [
        'Так сейчас выглядит текст. Для редактирования воспользуйтесь шаблоном. Отправьте новый шаблон',
        'или загрузите фото'
    ]
    async with state.proxy() as data:
        data['title'] = chapter
    doc_path = f'{os.getcwd()}/templates/{chapter}.txt'
    kb = home_kb()
    msg_list = file_reader(f'{chapter}.txt')
    for msg_text in msg_list:
        if msg_text == '[$PHOTO$]':
            photo_id = file_reader(f'{chapter}_photo.txt')[0]
            try:
                await bot.send_photo(admin_group, photo=photo_id)
            except:
                pass
            continue
        if len(msg_text) > 0:
            await callback.message.answer(msg_text)
    await bot.send_document(chat_id=admin_group, document=open(doc_path, 'rb'), caption=' '.join(text), reply_markup=kb)
    await bot.answer_callback_query(callback.id)



async def template_photo(message: Message, state: FSMContext):
    async with state.proxy() as data:
        title = data.as_dict()['title']
    text = 'Фото обновлено'
    kb = home_kb()
    photo_id = message.photo[-1].file_id
    photo_append(title, photo_id)
    await message.answer(text, reply_markup=kb)


async def template_doc(message: Message, state: FSMContext):
    async with state.proxy() as data:
        title = data.as_dict()['title']
    text = 'Шаблон обновлён'
    kb = home_kb()
    file_id = message['document']['file_id']
    await bot.download_file_by_id(file_id, f'{os.getcwd()}/templates/{title}.txt')
    await message.answer(text, reply_markup=kb)


async def weeks_main(callback: CallbackQuery):
    text = 'Выберите неделю'
    weeks = await get_weeks_sql()
    kb = admin_weeks_kb(weeks)
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


async def create_week(callback: CallbackQuery):
    weeks = await get_weeks_sql()
    await create_week_sql(len(weeks) + 1)
    weeks = await get_weeks_sql()
    kb = admin_weeks_kb(weeks)
    week_files(week_id=len(weeks), is_create=True)
    time.sleep(2)
    await bot.edit_message_reply_markup(admin_group, callback.message.message_id, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


async def week_menu(callback: CallbackQuery):
    week_id = callback.data.split(':')[1]
    text = 'Выберите действие'
    kb = admin_weeks_text_kb(week_id)
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


async def delete_week(callback: CallbackQuery):
    week_id = callback.data.split(':')[1]
    try:
        week_files(week_id=week_id, is_create=False)
    except:
        pass
    await delete_week_sql(week_id)
    await weeks_main(callback)


async def template_week(callback: CallbackQuery, state: FSMContext):
    week_id = callback.data.split(':')[2]
    chapter = callback.data.split(':')[1]
    async with state.proxy() as data:
        data['title'] = f'week_{week_id}_{chapter}'
    text = [
        'Так сейчас выглядит текст. Для редактирования воспользуйтесь шаблоном. Отправьте новый шаблон',
        'или загрузите фото'
    ]
    doc_path = f'{os.getcwd()}/templates/week_{week_id}_{chapter}.txt'
    kb = home_kb()
    msg_list = file_reader(f'week_{week_id}_{chapter}.txt')
    for msg_text in msg_list:
        if len(msg_text) > 0:
            await callback.message.answer(msg_text)
    await bot.send_document(chat_id=admin_group, document=open(doc_path, 'rb'), caption=' '.join(text), reply_markup=kb)
    await bot.answer_callback_query(callback.id)


async def workout_menu(callback: CallbackQuery, state: FSMContext):
    week_id = callback.data.split(':')[2]
    workout_id = callback.data.split(':')[1]
    text = f'Вы в меню недели {week_id} тренировки {workout_id}. Выберите действие'
    kb = admin_workout_text_kb()
    async with state.proxy() as data:
        data['title'] = f'week_{week_id}_workout_{workout_id}'
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


async def template_workout(callback: CallbackQuery, state: FSMContext):
    chapter = callback.data.split('_')[1]
    async with state.proxy() as data:
        title = data.as_dict()['title']
    title = '_'.join(title.split('_')[:4])
    async with state.proxy() as data:
        data['title'] = f'{title}_{chapter}'
    text = [
        'Так сейчас выглядит текст. Для редактирования воспользуйтесь шаблоном. Отправьте новый шаблон',
        'или загрузите фото'
    ]
    doc_path = f'{os.getcwd()}/templates/{title}_{chapter}.txt'
    kb = home_kb()
    msg_list = file_reader(f'{title}_{chapter}.txt')
    for msg_text in msg_list:
        if len(msg_text) > 0:
            await callback.message.answer(msg_text)
    await bot.send_document(chat_id=admin_group, document=open(doc_path, 'rb'), caption=' '.join(text), reply_markup=kb)
    await bot.answer_callback_query(callback.id)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", chat_id=admin_group)
    dp.register_message_handler(template_photo, content_types=['photo'], state='*', chat_id=admin_group)
    dp.register_message_handler(template_doc, content_types=['document'], state='*', chat_id=admin_group)

    dp.register_callback_query_handler(admin_start_clb, lambda x: x.data == 'home', state='*', chat_id=admin_group)
    dp.register_callback_query_handler(edit_texts, lambda x: x.data == 'texts', state='*', chat_id=admin_group)
    dp.register_callback_query_handler(edit_introduction, lambda x: x.data == 'introduction', state='*',
                                       chat_id=admin_group)
    dp.register_callback_query_handler(template_main, lambda x: x.data.split(':')[0] == 'intro', state='*',
                                       chat_id=admin_group)
    dp.register_callback_query_handler(weeks_main, lambda x: x.data == 'weeks', state='*', chat_id=admin_group)
    dp.register_callback_query_handler(week_menu, lambda x: x.data.split(':')[0] == 'week_num', state='*',
                                       chat_id=admin_group)
    dp.register_callback_query_handler(create_week, lambda x: x.data == 'new_week', state='*', chat_id=admin_group)
    dp.register_callback_query_handler(delete_week, lambda x: x.data.split(':')[0] == 'week_delete', state='*',
                                       chat_id=admin_group)
    dp.register_callback_query_handler(template_week, lambda x: x.data.split(':')[0] == 'week', state='*',
                                       chat_id=admin_group)
    dp.register_callback_query_handler(workout_menu, lambda x: x.data.split(':')[0] == 'week_tr', state='*',
                                       chat_id=admin_group)
    dp.register_callback_query_handler(template_workout, lambda x: x.data.split('_')[0] == 'tr', state='*',
                                       chat_id=admin_group)


