import os

def file_reader(file_name):
    file_path = f'{os.getcwd()}/templates/{file_name}'
    with open(file_path, 'r') as file:
        file_text = file.read()
        file_list = file_text.split('###$%$###')[2:]
        msg_list = []
        for msg in file_list:
            if len(msg.strip()) > 4096:
                msg = f'Слишком длинное сообщение. Допустимая длина 4096 символов. Отправлено {len(msg.strip())}'
            msg_list.append(msg.strip())
    return msg_list


def photo_append(file_name, photo_id):
    file_path = f'{os.getcwd()}/templates/{file_name}_photo.txt'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f'###$%$######$%$###{photo_id}')


def week_files(week_id, is_create):
    main_names = [
        f'week_{week_id}_program.txt',
        f'week_{week_id}_focus.txt',
        f'week_{week_id}_congratulation.txt',
        f'week_{week_id}_general_practices.txt',
        f'week_{week_id}_trichotomy_practices.txt',
        f'week_{week_id}_feedback.txt',
    ]
    for i in range(3):
        trains_files = [
            f'week_{week_id}_workout_{i + 1}_program.txt',
            f'week_{week_id}_workout_{i + 1}_reminder.txt',
            f'week_{week_id}_workout_{i + 1}_suppos.txt',
            f'week_{week_id}_workout_{i + 1}_supneg.txt',
            f'week_{week_id}_workout_{i + 1}_habit.txt',
        ]
        if is_create:
            for file in trains_files:
                os.system(f'cp {os.getcwd()}/templates/template.txt {os.getcwd()}/templates/{file}')
        else:
            for file in trains_files:
                os.remove(f'{os.getcwd()}/templates/{file}')
    if is_create:
        for file in main_names:
            os.system(f'cp {os.getcwd()}/templates/template.txt {os.getcwd()}/templates/{file}')
    else:
        for file in main_names:
            os.remove(f'{os.getcwd()}/templates/{file}')

