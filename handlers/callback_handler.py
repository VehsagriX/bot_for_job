from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, ReplyKeyboardRemove

from inline_keyboard import inline_request_chat_admin

router = Router()




@router.callback_query(F.data == "accepted",)
async def callback_accept(call: CallbackQuery):
    print(call.message.text)
    text = call.message.text.split('\n')
    text = [x.split(' ') for x in text]
    text[-1][1] = str(call.from_user.id)
    text = [' '.join(x) for x in text]
    result = '\n'.join(text)
    await call.message.edit_text(result)
    await call.bot.send_message(chat_id=call.from_user.id, text=result, reply_markup=inline_request_chat_admin())