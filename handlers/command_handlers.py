from xml.dom.domreg import registered

from aiogram import Router, F, flags
from aiogram.enums import ChatAction
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.formatting import Text, Bold

from crud_user_file import is_registered, get_user_data
from reply_keyboard import keyboard_answer, kb_run_step, kb_get_started, edit_kb, keyboard_builder
from aiogram.fsm.context import FSMContext
from bot_states import User, Request
from send_message_in_group import is_user_subscribed

router = Router()



@router.message(F.text, CommandStart())
@flags.chat_action(ChatAction.TYPING)
async def handle_start_subscribed(message: Message, state: FSMContext):
    is_member = await is_user_subscribed(message.from_user.id)
    if is_member:
        if not is_registered(message.from_user.id):
            await state.set_state(User.user_id)
            await state.set_state(User.user_login)
            await state.set_state(User.chat_id)
            content = Text(
                "Hello",
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
        await cancel_message(message)


@router.message(F.text, Command('get_started'))
@router.message(F.text.lower() == "начать работу 💼")
@router.message(F.text.lower() == "начать работу")
async def handle_run(message: Message):
    await message.answer('Выберите то, что вам необходимо ⬇️', reply_markup=kb_run_step())


@router.message(F.text.lower() == 'создать заявку ✍️')
@router.message(F.text.lower() == 'создать заявку')
async def on_startup(message: Message, state: FSMContext):
    await message.answer('Запрос - приобретение что то нового\nИнцедент - исправление чего-либо',
                         reply_markup=keyboard_builder())
    await state.set_state(Request.request_type)

@router.message(F.text, Command("cancel"))
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
@router.message(F.text.lower() == "моя анкета")
async def view_profile(message: Message):
    name, last_name, phone, email = get_user_data(message.from_user.id)
    my_text = f'Имя: {name}\nФамилия: {last_name}\nТелефон: {phone}\nПочта: {email}'
    await message.answer(text=my_text, reply_markup=edit_kb())
    # Нужно Реализовать изменение данных


@router.message(Command('help'))
async def handle_help(message: Message):
    pass


@router.message(F.text, StateFilter(default_state))
async def cancel_message(message: Message):
    await message.answer('Изините но с вами я не буду работать')
    await message.answer('Всего доброго')
