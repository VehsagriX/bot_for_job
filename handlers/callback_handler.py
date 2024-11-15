from aiogram import Router, F
from aiogram.types import CallbackQuery
from config import CHANNEL_ID_ADMIN
from inline_keyboard import inline_request_chat_admin, inline_request_kb

router = Router()


@router.callback_query(F.data == "accepted", )
async def callback_accept(call: CallbackQuery):
    print(call.message.text)
    text = call.message.text.split('\n')
    text = [x.split(' ') for x in text]
    text[-2][1] = str(call.from_user.id)
    edit_key = text[-2][0]
    edit_value = text[-2][1]
    # нужно изменить данные в файле по ключу TODO
    text = [' '.join(x) for x in text]
    result = '\n'.join(text)
    await call.message.edit_text(result)
    await call.bot.send_message(chat_id=call.from_user.id, text=result, reply_markup=inline_request_chat_admin())


@router.callback_query(F.data == 'stupid')
async def callback_failed(call: CallbackQuery):
    text = call.message.text.split('\n')
    text = [x.split(' ') for x in text]
    text[-2][1] = 'Никто'
    edit_value = text[-2][1]
    edit_key = text[-2][0]

    # нужно изменить данные в файле по ключу TODO
    text = [' '.join(x) for x in text]
    result = '\n'.join(text)
    await call.bot.send_message(chat_id=CHANNEL_ID_ADMIN, text=result, reply_markup=inline_request_kb())


@router.callback_query(F.data == 'finished')
async def callback_finished(call: CallbackQuery):
    result = call.message.text.split('\n')

    text = [x.split(' ') for x in result if 'ID' in x].pop()
    print(text)
    result = '\n'.join(result) + '\nВыполнено‼️‼️‼️'
    await call.bot.send_message(chat_id=text[-1], text=result)
