from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder



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


def kb_run_step_user() -> types.ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.button(text='Создать заявку ✍️'),
    kb_builder.button(text='Моя анкета 📝'),
    kb_builder.button(text='Мои заявки в работе ⏳'),
    kb_builder.button(text='Доступ к Гостевому WIFI🛜')
    kb_builder.button(text='Отмена 🔚')

    kb_builder.adjust(2, 1, 1, 1)
    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def kb_run_step_admin() -> types.ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()

    kb_builder.button(text='Создать заявку ✍️'),
    kb_builder.button(text='Моя анкета 📝'),
    kb_builder.button(text='Мои заявки в работе ⏳'),
    kb_builder.button(text='Доступ к Гостевому WIFI🛜')
    kb_builder.button(text="⚙️ Админ панель")
    kb_builder.button(text='Отмена 🔚')
    kb_builder.adjust(2, 1, 1, 2)

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)



def kb_admin() -> types.ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    kb_builder.button(text='Мои заявки в исполнении 🧑‍💻')
    kb_builder.button(text='Мои решенные заявки ✅')
    kb_builder.button(text='Назад ️◀️')
    kb_builder.adjust(1,2)

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def kb_super_admin() -> types.ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    kb_builder.button(text='Мои заявки в исполнении 🧑‍💻')
    kb_builder.button(text='Мои решенные заявки ✅')
    kb_builder.button(text='Отчет 📊')
    kb_builder.button(text='Назад ️◀️')
    kb_builder.adjust(1,1,2)

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def keyboard_builder() -> types.ReplyKeyboardMarkup:
    kb = [
        [
            types.KeyboardButton(text="Запрос"),
            types.KeyboardButton(text="Инцидент"),
            types.KeyboardButton(text='Назад ◀️'),
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
            types.KeyboardButton(text='Назад ◀️'),
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

        ],
        [
            types.KeyboardButton(text='Компания'),
            types.KeyboardButton(text='Департамент / Отдел'),
        ],
        [
            types.KeyboardButton(text='Назад ◀️'),
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите что вам нужно"
    )
    return keyboard

