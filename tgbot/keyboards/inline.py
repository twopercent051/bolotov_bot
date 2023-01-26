from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

home_button = InlineKeyboardButton(text='🏠 В главное меню', callback_data='home')


def home_kb():
    keyboard = InlineKeyboardMarkup(row_width=1).add(home_button)
    return keyboard


def admin_mainmenu_kb():
    text_button = InlineKeyboardButton(text='🗓 Редактировать тексты', callback_data='texts')
    keyboard = InlineKeyboardMarkup(row_width=1).add(text_button)
    return keyboard


def admin_edit_text_kb():
    introduction_button = InlineKeyboardButton(text='Вступление', callback_data='introduction')
    weeks_button = InlineKeyboardButton(text='Недели', callback_data='weeks')
    rings_button = InlineKeyboardButton(text='Кольца (не работает)', callback_data='rings')
    keyboard = InlineKeyboardMarkup(row_width=1).add(introduction_button, weeks_button, rings_button, home_button)
    return keyboard


def admin_intro_kb():
    greeting_button = InlineKeyboardButton(text='Приветствие', callback_data='intro:greeting')
    how_it_work_button = InlineKeyboardButton(text='Как это работает', callback_data='intro:how_it_work')
    heating_button = InlineKeyboardButton(text='Прогрев', callback_data='intro:heating')
    what_i_need_button = InlineKeyboardButton(text='Что понадобится', callback_data='intro:what_i_need')
    keyboard = InlineKeyboardMarkup(row_width=1).add(greeting_button, how_it_work_button, heating_button,
                                                     what_i_need_button, home_button)
    return keyboard


def admin_weeks_kb(weeks):
    new_week_button = InlineKeyboardButton(text='📂 Создать неделю', callback_data='new_week')
    keyboard = InlineKeyboardMarkup(row_width=1).add(new_week_button)
    for week in weeks:
        week_button = InlineKeyboardButton(text=f'Неделя номер {week[0]}', callback_data=f'week_num:{week[0]}')
        keyboard.add(week_button)
    keyboard.add(home_button)
    return keyboard


def admin_weeks_text_kb(week_id):
    program_button = InlineKeyboardButton(text='Программа на неделю', callback_data=f'week:program:{week_id}')
    focus_button = InlineKeyboardButton(text='Фокус', callback_data=f'week:focus:{week_id}')
    tr_1_button = InlineKeyboardButton(text='Тренировка 1', callback_data=f'week_tr:1:{week_id}')
    tr_2_button = InlineKeyboardButton(text='Тренировка 2', callback_data=f'week_tr:2:{week_id}')
    tr_3_button = InlineKeyboardButton(text='Тренировка 3', callback_data=f'week_tr:3:{week_id}')
    congratulation_button = InlineKeyboardButton(text='Поздравление с неделей',
                                                 callback_data=f'week:congratulation:{week_id}')
    general_practices_button = InlineKeyboardButton(text='Ст. практики общ',
                                                    callback_data=f'week:general_practices:{week_id}')
    trichotomy_practices_button = InlineKeyboardButton(text='Ст. практики трих',
                                                       callback_data=f'week:trichotomy_practices:{week_id}')
    delete_button = InlineKeyboardButton(text='❌ Удалить неделю', callback_data=f'week_delete:{week_id}')
    keyboard = InlineKeyboardMarkup(row_width=1).add(program_button, focus_button, tr_1_button, tr_2_button,
                                                     tr_3_button, congratulation_button, general_practices_button,
                                                     trichotomy_practices_button, delete_button, home_button)
    return keyboard


def admin_workout_text_kb():
    program_button = InlineKeyboardButton(text='Программа тренировки', callback_data='tr_program')
    reminder_button = InlineKeyboardButton(text='Напоминалка', callback_data='tr_reminder')
    sup_pos_button = InlineKeyboardButton(text='Поддержка поз', callback_data='tr_suppos')
    sup_neg_button = InlineKeyboardButton(text='Поддержка нег', callback_data='tr_supneg')
    habit_button = InlineKeyboardButton(text='Полезный пост', callback_data='tr_habit')
    keyboard = InlineKeyboardMarkup(row_width=1).add(program_button, reminder_button, sup_pos_button, sup_neg_button,
                                                     habit_button, home_button)
    return keyboard


def user_are_you_ready_kb():
    yes_button = InlineKeyboardButton(text='✅ Да', callback_data='yes_ready')
    no_button = InlineKeyboardButton(text='❌ Нет', callback_data='no_ready')
    keyboard = InlineKeyboardMarkup(row_width=1).add(yes_button, no_button)
    return keyboard


def user_heating_kb():
    begin_button = InlineKeyboardButton(text='Начать работать', callback_data='begin')
    keyboard = InlineKeyboardMarkup(row_width=1).add(begin_button)
    return keyboard


def user_payment_kb():
    pay_button = InlineKeyboardButton(text='Я оплатил', callback_data='paid')
    keyboard = InlineKeyboardMarkup(row_width=1).add(pay_button)
    return keyboard


def user_ok_kb():
    ok_button = InlineKeyboardButton(text='OK', callback_data='ok')
    keyboard = InlineKeyboardMarkup(row_width=1).add(ok_button)
    return keyboard


def user_smoking_kb():
    always_button = InlineKeyboardButton(text='Как паровоз', callback_data='always')
    sometimes_button = InlineKeyboardButton(text='Иногда за компанию', callback_data='sometimes')
    never_button = InlineKeyboardButton(text='Не курю', callback_data='never')
    keyboard = InlineKeyboardMarkup(row_width=1).add(always_button, sometimes_button, never_button)
    return keyboard


def user_drinking_kb():
    some_per_week_button = InlineKeyboardButton(text='Несколько дней в неделю', callback_data='some_per_week')
    one_per_week_button = InlineKeyboardButton(text='Раз в неделю', callback_data='one_per_week')
    one_per_month_button = InlineKeyboardButton(text='Раз в месяц', callback_data='one_per_month')
    less_one_per_month_button = InlineKeyboardButton(text='Реже одного раза в месяц',
                                                     callback_data='less_one_per_month')
    never_button = InlineKeyboardButton(text='Не пью алкоголь совсем', callback_data='never')
    keyboard = InlineKeyboardMarkup(row_width=1).add(some_per_week_button, one_per_week_button, one_per_month_button,
                                                     less_one_per_month_button, never_button)
    return keyboard


def user_timezone_kb():
    msk_button = InlineKeyboardButton(text='Московское время', callback_data='tz:0')
    a_button = InlineKeyboardButton(text='-1', callback_data='tz:-1')
    b_button = InlineKeyboardButton(text='+1', callback_data='tz:1')
    c_button = InlineKeyboardButton(text='+2', callback_data='tz:2')
    d_button = InlineKeyboardButton(text='+3', callback_data='tz:3')
    e_button = InlineKeyboardButton(text='+4', callback_data='tz:4')
    f_button = InlineKeyboardButton(text='+5', callback_data='tz:5')
    g_button = InlineKeyboardButton(text='+6', callback_data='tz:6')
    h_button = InlineKeyboardButton(text='+7', callback_data='tz:7')
    i_button = InlineKeyboardButton(text='+8', callback_data='tz:8')
    j_button = InlineKeyboardButton(text='+9', callback_data='tz:9')
    keyboard = InlineKeyboardMarkup(row_width=1).add(msk_button).row(a_button, b_button, c_button, d_button, e_button). \
        row(f_button, g_button, h_button, i_button, j_button)
    return keyboard


def user_workout_feedback_1_kb(week_id, workout_id):
    positive_button = InlineKeyboardButton(text='Сделал всё',
                                           callback_data=f'feedback_1:positive:{week_id}:{workout_id}')
    partly_button = InlineKeyboardButton(text='Выполнил тренировку частично',
                                              callback_data=f'feedback_1:partly:{week_id}:{workout_id}')
    negative_button = InlineKeyboardButton(text='Не сделал тренировку вообще',
                                          callback_data=f'feedback_1:negative:{week_id}:{workout_id}')
    keyboard = InlineKeyboardMarkup(row_width=1).add(positive_button, partly_button, negative_button)
    return keyboard


def user_workout_feedback_2_kb(week_id, workout_id):
    easy_button = InlineKeyboardButton(text='Очень легкая, я практически её не почувствовал',
                                       callback_data=f'feedback_2:easy:{week_id}:{workout_id}')
    medium_button = InlineKeyboardButton(text='Пришлось поработать',
                                         callback_data=f'feedback_2:medium:{week_id}:{workout_id}')
    hard_button = InlineKeyboardButton(text='Было очень тяжело, я плохо себя чувствовал(а)',
                                       callback_data=f'feedback_2:hard:{week_id}:{workout_id}')
    keyboard = InlineKeyboardMarkup(row_width=1).add(easy_button, medium_button, hard_button)
    return keyboard


def user_week_feedback_kb(week_id):
    no_changes_button = InlineKeyboardButton(text='Ничего не изменилось',
                                             callback_data=f'feedback_week:no_changes:{week_id}')
    something_button = InlineKeyboardButton(text='Кажется, что-то начинает происходить',
                                            callback_data=f'feedback_week:something:{week_id}')
    all_right_button = InlineKeyboardButton(text='Я воодушевлен, чувствую, что делаю всё правильно',
                                            callback_data=f'feedback_week:all_right:{week_id}')
    worse_button = InlineKeyboardButton(text='Стало только хуже', callback_data=f'feedback_week:worse:{week_id}')
    keyboard = InlineKeyboardMarkup(row_width=1).add(no_changes_button, something_button, all_right_button,
                                                     worse_button)
    return keyboard
