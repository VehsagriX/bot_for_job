from datetime import datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery
from config import CHANNEL_ID_ADMIN
from crud_request_file import change_value_request
from inline_keyboard import inline_request_chat_admin, inline_request_kb

router = Router()


@router.callback_query(F.data == "accepted", )
async def callback_accept(call: CallbackQuery):
    text = call.message.text.split('\n')

    text = [x.split(':') for x in text]

    request_id = text[1][1].strip()


    text[-2][1] = '@' + call.from_user.username
    edit_key = 'request_admin'
    edit_value = call.from_user.username
    change_value_request(request_id, edit_key, edit_value)
    text[-1][1] = 'В работе'
    key_status = 'request_status'
    status_value = text[-1][1]

    change_value_request(request_id, key_status, status_value)
    today = datetime.now()
    change_value_request(request_id, 'date_accepted', today.strftime("%d.%m.%Y"))
    change_value_request(request_id, 'time_accepted', today.strftime("%H:%M"))


    id_user = [x for x in text if 'ID Создателя' in x][0][1].strip()
    text = [':'.join(x) for x in text]
    result = '\n'.join(text)

    await call.message.edit_text(result)
    await call.bot.send_message(chat_id=call.from_user.id, text=result, reply_markup=inline_request_chat_admin())
    await call.bot.send_message(chat_id=id_user, text=result)


@router.callback_query(F.data == 'stupid')
async def callback_failed(call: CallbackQuery):
    text = call.message.text.split('\n')
    text = [x.split(':') for x in text]
    print(text)
    request_id = text[1][1].strip()
    text[-2][1] = 'В ожидании'
    edit_key = 'request_admin'
    edit_value = text[-2][1]

    change_value_request(request_id, edit_key, edit_value)
    text[-1][1] = 'Новый'
    key_status = 'request_status'
    status_value = text[-1][1]

    change_value_request(request_id, key_status, status_value)
    change_value_request(request_id, 'date_accepted', None)
    change_value_request(request_id, 'time_accepted', None)

    text = [':'.join(x) for x in text]
    result = '\n'.join(text)
    # print(result)
    # await call.message.edit_text(text=result)
    await call.bot.send_message(chat_id=CHANNEL_ID_ADMIN, text=result, reply_markup=inline_request_kb())

@router.callback_query(F.data == 'finished')
async def callback_finished(call: CallbackQuery):
    text = call.message.text.split('\n')
    text = [x.split(':') for x in text]

    user_id = text[6][1].strip()

    text[-1][1] = "Выполнено"

    request_id = text[1][1].strip()

    status_key = 'request_status'
    status_value = text[-1][1]

    change_value_request(request_id, status_key, status_value)
    today = datetime.now()
    change_value_request(request_id, 'date_finished', today.strftime("%d.%m.%Y"))
    change_value_request(request_id, 'time_finished', today.strftime("%H:%M"))
    result = [':'.join(x) for x in text]
    result = '\n'.join(result)

    await call.bot.send_message(chat_id=user_id, text=result + '‼️‼️‼️')
    await call.message.edit_text(result + '‼️‼️‼️')
    await call.bot.send_message(chat_id=CHANNEL_TEST_ADMIN, text=result + '‼️‼️‼️')
