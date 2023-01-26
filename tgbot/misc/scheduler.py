
from tgbot.handlers.user import *

from create_bot import config, scheduler, dp


async def user_scheduler():
    user_list = await get_users_list_sql()
    now = time.time()
    for user in user_list:
        if user[3] < now:
            user_next_step = user[2]
            if user_next_step == 'how_it_work':
                await user_how_it_work(user[1])
            if user_next_step == 'are_you_ready':
                await are_you_ready(user[1])
            if user_next_step == 'heating':
                await user_heating_by_sched(user[1])
            if user_next_step == 'what_i_need':
                await user_what_i_need(user[1])
            if user_next_step == 'intro_polling':
                await user_intro_polling(user[1])
            if user_next_step.split(':')[0] == 'week':
                week_id = int(user_next_step.split(':')[2])
                if user_next_step.split(':')[1] == 'program':
                    await user_week_program(user[1], week_id)
                if user_next_step.split(':')[1] == 'focus':
                    await user_week_focus(user[1], week_id)
                if user_next_step.split(':')[1] == 'congratulation':
                    await user_week_congratulation(user[1], week_id)
                if user_next_step.split(':')[1] == 'general_practices':
                    await user_week_general_practices(user[1], week_id)
                if user_next_step.split(':')[1] == 'trichotomy_practices':
                    await user_week_trichotomy_practices(user[1], week_id)
                if user_next_step.split(':')[1] == 'feedback':
                    await user_week_feedback(user[1], week_id)
            if user_next_step.split(':')[0] == 'workout':
                week_id = int(user_next_step.split(':')[4])
                workout_id = int(user_next_step.split(':')[2])
                if user_next_step.split(':')[1] == 'program':
                    await user_workout_program(user[1], week_id, workout_id)
                if user_next_step.split(':')[1] == 'reminder':
                    await user_workout_reminder(user[1], week_id, workout_id)
                if user_next_step.split(':')[1] == 'feedback_1':
                    await user_workout_feedback_1(user[1], week_id, workout_id)
                if user_next_step.split(':')[1] == 'support':
                    await user_workout_support(user[1], week_id, workout_id)
                if user_next_step.split(':')[1] == 'habit':
                    await user_workout_habit(user[1], week_id, workout_id)


def scheduler_jobs():
    scheduler.add_job(user_scheduler, "interval", seconds=10)
