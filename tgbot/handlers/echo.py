from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode
# import pyzbar
# from create_bot import bot
# import os
# from PIL import Image
#
# import cv2


async def get_id(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = f'chat_id: {hcode(chat_id)} || user_id: {hcode(user_id)}'

    await message.answer(text)


# async def qr_reader(message: types.Message):
#     id_img = message.photo[-1].file_id
#     await bot.download_file_by_id(id_img, f'{os.getcwd()}/test_image.png')
#     filename = f'{os.getcwd()}/test_image.png'
#     image = cv2.imread(filename)
#     detector = cv2.QRCodeDetector()
#     data, vertices_array, _ = detector.detectAndDecode(image)
#     print(data)
#



def register_echo(dp: Dispatcher):
    dp.register_message_handler(get_id, commands='get_id')
    # dp.register_message_handler(qr_reader, commands='start')
    # dp.register_message_handler(qr_reader, content_types='photo')
