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
    print(text)
    print(request_id)
    text[-2][1] = str(call.from_user.id)
    edit_key = 'request_admin'
    edit_value = call.from_user.id
    change_value_request(request_id, edit_key, edit_value)
    text[-1][1] = 'В работе'
    key_status = 'request_status'
    status_value = text[-1][1]
    change_value_request(request_id, key_status, status_value)
    # нужно изменить данные в файле по ключу TODO
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
    request_id = text[1][1].strip()
    text[-2][1] = 'Никто'
    edit_key = 'request_admin'
    edit_value = text[-2][1]
    change_value_request(request_id, edit_key, edit_value)
    text[-1][1] = 'Новый'
    key_status = 'request_status'
    status_value = text[-1][1]
    change_value_request(request_id, key_status, status_value)

    # нужно изменить данные в файле по ключу TODO
    text = [':'.join(x) for x in text]
    result = '\n'.join(text)
    await call.bot.send_message(chat_id=CHANNEL_ID_ADMIN, text=result, reply_markup=inline_request_kb())


@router.callback_query(F.data == 'finished')
async def callback_finished(call: CallbackQuery):
    text = call.message.text.split('\n')
    text = [x.split(':') for x in text]
    text[-1][1] = "Выполнено‼️‼️‼️"
    id_user = [x for x in text if 'ID Создателя' in x][0][1].strip()
    request_id = text[0][1]
    status_key = 'request_status'
    status_value = text[-1][1]
    change_value_request(request_id, status_key, status_value)
    result = [':'.join(x) for x in text]
    result = '\n'.join(result)
    await call.bot.send_message(chat_id=id_user, text=result)
