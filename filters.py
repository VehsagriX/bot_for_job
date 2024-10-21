import re

from aiogram.filters import BaseFilter
from aiogram.types import Message

def check_email(email):
    EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    email_candidates = re.findall(EMAIL_REGEX, email)
    if email_candidates:
        return True
    else:
        return False

class EmailCheck(BaseFilter):
    key = 'is_email'
    pattern = re.compile('')

    async def __call__(self, message: Message) -> bool:
        return self.pattern.match(message.text)