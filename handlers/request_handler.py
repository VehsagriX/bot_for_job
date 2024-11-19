from datetime import datetime


from aiogram import Router, F, flags
from aiogram.types import Message
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Bold

from bot_states import Request
from crud_request_file import add_request
from send_message_in_group import get_message_request_in_group
from handlers.command_handlers import handle_run



router = Router()





@router.message(Request.request_type)
@router.message(F.text.lower() == 'запрос')
@router.message(F.text.lower() == 'инцидент')
@flags.chat_action(ChatAction.TYPING)
async def handle_button(message: Message, state: FSMContext)-> None:
    await state.update_data(request_type=message.text)
    my_data = datetime.now()
    result = f'{my_data.day}{my_data.month}{my_data.year}{my_data.hour}{my_data.minute}'
    await state.update_data(request_id=f'<b>{result}{message.from_user.id}</b>')
    await state.update_data(request_creator=message.from_user.id)
    await state.update_data(login_creator=message.from_user.username)
    await message.answer('Можете написать кратко о вашей проблеме прим(Заправка картриджа, Установка windows...)')
    await state.set_state(Request.request_title)


@router.message(F.text, Request.request_title)
@flags.chat_action(ChatAction.TYPING)
async def handler_title(message: Message, state: FSMContext)-> None:
    await state.update_data(request_title=message.text)
    await message.answer("Теперь опишите полностью о своей проблеме, если не можете описать или есть фото, видео,"
                         "прикрепите к сообщению")
    await state.set_state(Request.request_description)


@router.message(F.text, Request.request_description)
@flags.chat_action(ChatAction.TYPING)
async def handler_description(message: Message, state: FSMContext)-> None:
    if len(message.text) < 20:
        await message.answer('Этого недостаточно, попробуйте описать более развернуто')
        await state.set_state(Request.request_description)
    else:
        await state.set_state(Request.request_admin)
        await state.update_data(request_description=message.text)
        await state.update_data(request_admin='В ожидании')
        await state.update_data(request_status='Новый')
        await message.reply('Спасибо, я передам всю информацию специалистам')
        await handle_run(message)
        data = await state.get_data()

        add_request(data)
        user_id = message.from_user.id
        await get_message_request_in_group(data, user_id)





@router.message(F.text, Request())
async def error_message(message: Message):
    await message.answer('Я не понимаю, выберите то что вам нужно ')
    await handle_run(message)
