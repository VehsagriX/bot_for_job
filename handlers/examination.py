from aiogram.enums import ChatMemberStatus
from main import bot


async def is_user_subscraibed(chanel_url: str, user_id: int) -> bool:
    member = await bot.get_chat_member(chat_id=chanel_url, user_id=user_id)
    if member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        return False
    return True





