from create_bot import bot
from tgbot.misc.file_reader import file_reader
import time, datetime
from datetime import datetime, timedelta


async def sender_with_photo(msg_list, photo_file, user_id):
    for msg_text in msg_list:
        if msg_text == '[$PHOTO$]':
            photo_id = file_reader(photo_file)[0]
            try:
                await bot.send_photo(user_id, photo=photo_id)
            except:
                pass
            continue
        time.sleep(2)
        if len(msg_text) > 0:
            try:
                await bot.send_message(user_id, msg_text)
            except:
                pass


async def sender_without_photo(msg_list, user_id):
    for msg_text in msg_list:
        if msg_text == '[$PHOTO$]':
            continue
        if len(msg_text) > 0:
            try:
                await bot.send_message(user_id, msg_text)
            except:
                pass
        time.sleep(2)


def next_step_timer(user_tz: int, days_offset: int, tm_hours: int):
    utc_offset = 3 + user_tz
    user_timestamp = datetime.utcnow().timestamp() + (3600 * utc_offset)
    user_date = datetime.fromtimestamp(user_timestamp)
    user_next_day = user_date + timedelta(days=days_offset)
    user_next_day_mod = user_next_day.replace(hour=tm_hours, minute=0).timestamp()
    utc_result = user_next_day_mod - (user_tz + 3) * 3600
    return int(utc_result)
