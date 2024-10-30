from aiogram.enums import ChatMemberStatus
from config import CHANNEL_ID


async def is_user_subscribed(user_id, channel_id: str = CHANNEL_ID) -> bool:
    from main import bot
    member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
    if member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        return False
    return True


async def get_message_user_in_group(result: dict, channel_id: str = CHANNEL_ID) -> None:
    from main import bot
    my_text = f""" Имя: {result.get('user_name')}\nФамилия: {result.get('user_last_name')}\nПочта: {result.get('user_email')}\nНомер: {result.get('user_phone')}
              """
    await bot.send_message(chat_id=channel_id, text=my_text)


async def get_message_request_in_group(result: dict, channel_id: str = CHANNEL_ID) -> None:
    from main import bot
    my_text = f"""ID: {result.get('request_id')}\nТип заявки: {result.get('request_type')}\nКомпания: {result.get('company_name')}
    \nЗаголовок: {result.get('request_title')}\nОписание: {result.get('request_description')}"""
    await bot.send_message(chat_id=channel_id, text=my_text)
