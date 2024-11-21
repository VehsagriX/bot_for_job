from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import all_company


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


def kb_company(list_company=all_company) -> InlineKeyboardMarkup:
    # list_company = ['ГО', 'Evolet']
    builder = InlineKeyboardBuilder()
    for value in list_company:
        builder.button(text=f'{value}', callback_data=f'{value}')
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Выберите что вам нужно")