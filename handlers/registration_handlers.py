from aiogram import Router, F, flags
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from bot_states import User, Request
from filters import check_email

router = Router()


@router.message(F.text.lower() == 'регистрация')
@flags.chat_action(action=ChatAction.TYPING)
async def get_name(message: Message, state: FSMContext):
    await message.answer('Напишите как вас Фамилию и Имя?')
    await state.set_state(User.user_name)



@router.message(F.text, User.user_name)
@flags.chat_action(action=ChatAction.TYPING)
async def get_phone(message: Message, state: FSMContext):
    msg = message.text.split(' ')
    await state.update_data(user_name=msg[0])
    await state.update_data(user_last_name=msg[1])
    await message.answer('Напишите ваш рабочий номер телефона, как с вами можем связаться?')
    await state.set_state(User.user_phone)


@router.message(F.text, User.user_phone)
@flags.chat_action(action=ChatAction.TYPING)
async def check_phone(message: Message, state: FSMContext):
    number = message.text
    if not number[1:].isdigit() or len(number) > 13:
        await message.answer('Вы ввели неверный номер повторите попытку')
        await state.set_state(User.user_phone)
        return
    await message.answer('Напишите вашу рабочую почту')
    await state.set_state(User.user_email)


@router.message(F.text, User.user_email)
@flags.chat_action(action=ChatAction.TYPING)
async def email_chek(message: Message, state: FSMContext):
    msg = message.text.split()
    email = [i for i in msg if check_email(i)]
    if len(email) > 0:
        email = email[0]
        await state.update_data(user_email=email)
        data = await state.get_data()
        print(data)
    else:
        await message.reply("Пожалуйста, введите корректный email")
        await state.set_state(User.user_email)
        return
