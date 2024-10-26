from aiogram import Router, F, flags
from aiogram.enums import ChatAction
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.formatting import Text, Bold
from keyboard import keyboard_answer
from aiogram.fsm.context import FSMContext
from bot_states import User
from handlers.examination import is_user_subscraibed
from config import CHANNEL_ID

router = Router()


@router.message(F.text, CommandStart())
@flags.chat_action(ChatAction.TYPING)
async def handle_start(message: Message, state: FSMContext):
    is_member = await is_user_subscraibed(CHANNEL_ID, message.from_user.id)
    if is_member:
        await state.set_state(User.user_id)
        await state.set_state(User.user_login)
        await state.set_state(User.chat_id)
        content = Text(
            "Hello, ",
            Bold(message.from_user.full_name)
        )
        await state.clear()

        await message.answer(
            **content.as_kwargs()
        )
        await state.update_data(user_id=message.from_user.id)
        await state.update_data(user_login=message.from_user.username)
        await state.update_data(chat_id=message.chat.id)
        await message.answer('Вы не зарегистрированы, вы готовы пройти регистрацию?', reply_markup=keyboard_answer())
        await state.set_state(User.user_name)
        await state.set_state(User.user_last_name)
    else:
        await message.answer('Изините но с вами я не буду работать')
        await message.answer('Всего доброго')


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
@flags.chat_action(ChatAction.TYPING)
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer('Всего доброго!😉')


@router.message(Command('help'))
async def handle_help(message: Message):
    pass
