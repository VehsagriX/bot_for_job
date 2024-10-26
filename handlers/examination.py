from aiogram.enums import ChatMemberStatus
from aiogram import types
from main import bot


async def is_user_subscraibed(chanel_url: str, user_id: int) -> bool:
    member = await bot.get_chat_member(chat_id=chanel_url, user_id=user_id)
    if member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        return False
    return True


async def get_message_in_group(channel_id: str, result: dict) -> None:
    from main import bot
    my_text = f""" Имя: {result.get('user_name')}\nФамилия: {result.get('user_last_name')}\nПочта: {result.get('user_email')}
              Номер: {result.get('user_phone')}
              """
    await bot.send_message(chat_id=channel_id, text=my_text)
