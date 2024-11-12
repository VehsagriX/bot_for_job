from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def kb_get_started() -> types.ReplyKeyboardMarkup:
    kb = [
        [
            types.KeyboardButton(text='Начать работу 💼'),
            types.KeyboardButton(text='Отмена 🔚'),
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


def kb_run_step() -> types.ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.button(text='Создать заявку ✍️'),
    kb_builder.button(text='Моя анкета 📝'),
    kb_builder.button(text='Мои заявки в работе ⏳'),
    kb_builder.button(text='Отмена 🔚')
    kb_builder.adjust(2)

    return kb_builder.as_markup(resize_keyboard=True)


def keyboard_builder() -> types.ReplyKeyboardMarkup:
    kb = [
        [
            types.KeyboardButton(text="Запрос"),
            types.KeyboardButton(text="Инцидент"),
            types.KeyboardButton(text='Отмена'),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите что вам нужно"
    )

    return keyboard


def keyboard_answer() -> types.ReplyKeyboardMarkup:
    kb = [
        [
            types.KeyboardButton(text='Регистрация'),
            types.KeyboardButton(text='Отмена'),
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите что вам нужно"
    )
    return keyboard


def edit_kb() -> types.ReplyKeyboardMarkup:
    kb = [
        [
            types.KeyboardButton(text='Изменить данные'),
            types.KeyboardButton(text='Назад'),
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите что вам нужно"
    )
    return keyboard


def edit_key_kb() -> types.ReplyKeyboardMarkup:
    kb = [
        [
            types.KeyboardButton(text='Почта 📧'),
            types.KeyboardButton(text='Номер 📱'),
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите что вам нужно"
    )
    return keyboard



