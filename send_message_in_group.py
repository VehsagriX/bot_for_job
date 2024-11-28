import os
from datetime import datetime, date

import pandas as pd
from aiogram.types.input_file import FSInputFile
from aiogram.enums import ChatMemberStatus

from config import CHANNEL_ID_ADMIN, CHANNEL_ID_USER, CHANNEL_TEST_USER, CHANNEL_TEST_ADMIN
from crud_user_file import get_user_name
from inline_keyboard import inline_request_kb

async def is_admin(user_id, channel_admin: str = CHANNEL_ID_ADMIN):
    from main import bot
    user_channel_status = await bot.get_chat_member(chat_id=channel_admin, user_id=user_id)

    if user_channel_status.status == ChatMemberStatus.LEFT:
        return False
    return True




async def is_user_subscribed(user_id, channel_user_id: str = CHANNEL_ID_USER, channel_admin_id: str = CHANNEL_ID_ADMIN) -> bool:
    from main import bot
    member_user = await bot.get_chat_member(chat_id=channel_user_id, user_id=user_id)
    member_admin = await bot.get_chat_member(chat_id=channel_admin_id, user_id=user_id)

    if member_user.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR] or member_admin.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        return True
    return False


async def get_message_user_in_group(result: dict, channel_id: str = CHANNEL_ID_USER) -> None:
    from main import bot
    my_text = f"Имя: {result.get('user_name')}\nФамилия: {result.get('user_last_name')}\nПочта: {result.get('user_email')}\nНомер: {result.get('user_phone')}"
    await bot.send_message(chat_id=channel_id, text=my_text)


async def get_message_request_in_group(result: dict | str, user_id: int, channel_id: str = CHANNEL_ID_ADMIN) -> None:
    from main import bot
    name, last_name, company = get_user_name(user_id)

    my_text = f"""Тип заявки: {result.get('request_type')}\nID: {result.get('request_id')}\nКомпания: {company}
Создатель заявки: {name} {last_name}\nЗаголовок: {result.get('request_title')}\nОписание: {result.get('request_description')}
ID Создателя: {result.get('request_creator')}\nСвязаться с заявителем: @{result.get('login_creator')}\nИсполнитель: {result.get('request_admin')}
Статус: {result.get('request_status')}"""
    await bot.send_message(chat_id=channel_id, text=my_text, reply_markup=inline_request_kb())





def create_otchet():
    df_users = pd.read_excel('user_file.xlsx')
    df_requests = pd.read_excel('request_file.xlsx')

    user_names = df_requests.merge(df_users[['user_login', 'user_last_name', 'user_name', 'company_name']],
                                   how='left', left_on='request_admin',
                                   right_on='user_login').drop(['request_admin', 'user_login'], axis=1)

    user_names = user_names.merge(df_users[['user_login', 'user_last_name', 'user_name']],
                                  how='left', left_on='login_creator',
                                  right_on='user_login').drop(['login_creator', 'request_creator', 'user_login'],
                                                              axis=1)

    user_names['admin'] = user_names['user_last_name_x'] + ' ' + user_names['user_name_x']
    user_names['applicant'] = user_names['user_last_name_y'] + ' ' + user_names['user_name_y']

    user_names.drop(['user_last_name_x', 'user_name_x', 'user_last_name_y', 'user_name_y'], axis=1, inplace=True)

    user_names.columns = ['Тип запроса', 'Идентификатор запроса', 'Заголовок запроса', 'Описание запроса',
                          'Статус запроса', 'Дата создания', 'Время создания', 'Дата принятия', 'Время принятия','Дата завершения', 'Время завершения',
                          'Название компании', 'Исполнитель', 'Заявитель']
    today = datetime.today()
    name_file = f'otchet_{today.day}.{today.month}.{today.year}.xlsx'
    user_names.to_excel(name_file)
    return name_file

async def send_file_admin(user_id):
    from main import bot
    name_file = create_otchet()
    document = FSInputFile(name_file)
    await bot.send_document(chat_id=user_id, document=document)
    os.remove(name_file)



