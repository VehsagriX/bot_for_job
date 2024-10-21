from aiogram import Router, F, flags
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.enums import MessageEntityType, ChatAction
from aiogram.fsm.context import FSMContext
from bot_states import User, Request
from filters import check_email

router = Router()

# @router.message(F.text.lower() == 'запрос')
# @router.message(F.text.lower() == 'инцидент')
# @router.message(Request.request_type)
# @flags.chat_action(ChatAction.TYPING)
# async def handle_button(message: Message, state: FSMContext):
#     await state.update_data(request_type=message.text)
#
#     await message.answer('Напишите свою почту пожалуйста', reply_markup=ReplyKeyboardRemove())
#
#
#
# @router.message(F.text, Form.user_email)
# @flags.chat_action(ChatAction.TYPING)
# async def email_chek(message: Message, state: FSMContext):
#     msg = message.text.split()
#     email = [i for i in msg if check_email(i)]
#     if len(email) > 0:
#         email = email[0]
#         await state.update_data(user_email=email)
#     else:
#         await message.reply("Пожалуйста, введите корректный email")
#         await state.set_state(Form.user_email)
#         return
#
#     await message.answer('Опишите развернуто свою проблему, чтоб мы поняли в чем причина')
#
#     await state.set_state(Form.request_description)
#
#
# @router.message(F.text, F.text.len() > 50, Form.request_description)
# @flags.chat_action(ChatAction.TYPING)
# async def handler_description(message: Message, state: FSMContext):
#     await state.update_data(request_description=message.text)
#
#     await message.reply('Спасибо, я передам всю информацию специалистам')
#
#     data = await state.get_data()
#     msg = f'''Ваш id = {data.get('user_id')}.\nВас зовут {data.get('user_last_name')} {data.get('user_name')}.\n
#     Ваша почта {data.get('user_email')}.\nУ вас {data.get('request_name')}: {data.get('request_description')}'''
#     print(data)
#     await message.answer(msg)
