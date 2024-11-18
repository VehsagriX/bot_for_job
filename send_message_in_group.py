from aiogram.enums import ChatMemberStatus

from config import CHANNEL_ID_ADMIN, CHANNEL_ID_USER
from crud_user_file import get_user_name
from inline_keyboard import inline_request_kb


async def is_user_subscribed(user_id, channel_id: str = CHANNEL_ID_USER) -> bool:
    from main import bot
    member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
    if member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        return False
    return True


async def get_message_user_in_group(result: dict, channel_id: str = CHANNEL_ID_USER) -> None:
    from main import bot
    my_text = f"Имя: {result.get('user_name')}\nФамилия: {result.get('user_last_name')}\nПочта: {result.get('user_email')}\nНомер: {result.get('user_phone')}"
    await bot.send_message(chat_id=channel_id, text=my_text)


async def get_message_request_in_group(result: dict | str, user_id: int, channel_id: str = CHANNEL_ID_ADMIN) -> None:
    from main import bot
    name, last_name, company = get_user_name(user_id)
    print(result)
    my_text = f"""Тип заявки: {result.get('request_type')}\nID: {result.get('request_id')}\nКомпания: {company}
Создатель заявки: {name} {last_name}\nЗаголовок: {result.get('request_title')}\nОписание: {result.get('request_description')}
ID Создателя: {result.get('request_creator')}\nСвязаться с заявителем: @{result.get('login_creator')}\nИсполнитель: {result.get('request_admin')}
Статус: {result.get('request_status')}"""
    await bot.send_message(chat_id=channel_id, text=my_text, reply_markup=inline_request_kb())
