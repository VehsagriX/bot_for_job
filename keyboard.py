from aiogram import types


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