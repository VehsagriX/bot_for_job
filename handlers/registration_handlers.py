from aiogram import Router, F, flags

from aiogram.types import Message, CallbackQuery
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Bold

from config import all_company
from crud_user_file import add_user
from bot_states import User
from filters import check_email, check_num

from handlers.command_handlers import handle_run
from inline_keyboard import kb_company

router = Router()


@router.message(F.text.lower() == 'регистрация')
@flags.chat_action(action=ChatAction.TYPING)
async def get_name(message: Message, state: FSMContext) -> None:
    await message.answer('Напишите вашу Фамилию и Имя')
    await state.set_state(User.user_name)


@router.message(F.text, User.user_name)
@flags.chat_action(action=ChatAction.TYPING)
async def get_phone(message: Message, state: FSMContext) -> None:
    msg = message.text.split(' ')
    if len(msg) == 2:
        await state.update_data(user_last_name=msg[0])
        await state.update_data(user_name=msg[1])
        await message.answer('Напишите ваш рабочий номер телефона.')
        await state.set_state(User.user_phone)
    else:
        await message.answer('Введите правильно Имя Фамилию (Иван Иванов)')
        await state.set_state(User.user_name)


@router.message(F.text, User.user_phone)
@flags.chat_action(action=ChatAction.TYPING)
async def check_phone(message: Message, state: FSMContext) -> None:
    if not check_num(message.text):
        await message.answer('Вы ввели неверный номер. Повторите попытку')
        await state.set_state(User.user_phone)
        return
    await state.update_data(user_phone=message.text)
    await message.answer('Напишите вашу рабочую почту.')
    await state.set_state(User.user_email)


@router.message(F.text, User.user_email)
@flags.chat_action(action=ChatAction.TYPING)
async def email_check(message: Message, state: FSMContext, list_company=all_company) -> None:
    msg = message.text.split()
    email = [i for i in msg if check_email(i)]

    if len(email) > 0:
        email = email[0]
        await state.update_data(user_email=email)
        await message.answer('Какую компанию вы представляете?\nВыберите из списка:', reply_markup=kb_company())
        await state.set_state(User.company_name)
    else:
        await message.reply("Пожалуйста, введите корректный email")
        await state.set_state(User.user_email)
        return



@router.callback_query(F.data, User.company_name)
async def get_company(call: CallbackQuery, state: FSMContext):
    await state.update_data(company_name=call.data)
    await call.bot.send_message(chat_id=call.message.chat.id, text='Из какого вы отдела/департамента?')
    await state.set_state(User.department)


@router.message(F.text, User.company_name)
async def get_company_name(message: Message, state: FSMContext) -> None:
    await message.answer('Выберите пожалуйста из списка и нажмите на кнопку.  Другого я не пойму')
    await message.answer('Какую компанию вы представляете?\nВыберите из списка:', reply_markup=kb_company())
    await state.set_state(User.company_name)


@router.message(F.text, User.department)
async def get_departament(message: Message, state: FSMContext) -> None:
    await state.update_data(department=message.text)
    data = await state.get_data()
    await message.answer('Спасибо, регистрация прошла успешно')
    add_user(data)
    await state.clear()
    await handle_run(message)
