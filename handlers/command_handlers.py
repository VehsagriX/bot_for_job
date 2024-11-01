from aiogram import Router, F, flags
from aiogram.enums import ChatAction
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.formatting import Text, Bold

from add_to_file import is_registered
from keyboard import keyboard_answer, kb_run_step, kb_get_started
from aiogram.fsm.context import FSMContext
from bot_states import User
from examination import is_user_subscribed
from config import CHANNEL_ID

router = Router()


@router.message(F.text, CommandStart())
@flags.chat_action(ChatAction.TYPING)
async def handle_start(message: Message, state: FSMContext):
    is_member = await is_user_subscribed(message.from_user.id)
    if is_member:
        if not is_registered(message.from_user.id):
            await state.set_state(User.user_id)
            await state.set_state(User.user_login)
            await state.set_state(User.chat_id)
            content = Text(
                "Hello, Motheer",
                Bold(message.from_user.full_name)
            )
            await state.clear()

            await message.answer(
                **content.as_kwargs()
            )
            await state.update_data(user_id=message.from_user.id)
            await state.update_data(user_login=message.from_user.username)
            await state.update_data(chat_id=message.chat.id)
            await message.answer('Вы не зарегистрированы, вы готовы пройти регистрацию?',
                                 reply_markup=keyboard_answer())
            await state.set_state(User.user_name)
            await state.set_state(User.user_last_name)
        else:
            await message.answer('Добрый день, я помощник технической поддержки компании KOINOTI NAV. '
                                 'Выберите что вы хотели сделать', reply_markup=kb_get_started())

    else:
        await message.answer('Изините но с вами я не буду работать')
        await message.answer('Всего доброго')


@router.message(Command(commands=['/get_stared']))
@router.message(F.text.lower() == "начать работу 💼")
@router.message(F.text.lower() == "начать работу")
async def handle_run(message: Message):
    await message.answer('Выберите то, что вам необходимо ⬇️', reply_markup=kb_run_step())


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена 🔚")
@router.message(F.text.lower() == 'отмена')
@flags.chat_action(ChatAction.TYPING)
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer('Всего доброго!😉')


@router.message(Command('/myprofile'))
@router.message(F.text.lower() == "моя анкета 📝")
async def edit_profile(message: Message):
    pass


@router.message(Command('help'))
async def handle_help(message: Message):
    pass
