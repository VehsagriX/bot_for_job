from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def inline_request_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Принять', callback_data='accepted')
    return builder.as_markup()

def inline_request_chat_admin() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Завершить работу', callback_data='finished')
    builder.button(text='Не справился', callback_data='stupid')
    builder.adjust(2)
    return builder.as_markup()


