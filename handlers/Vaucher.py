from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot_states import Voucher
from get_vaucher import get_voucher
from handlers.command_handlers import send_voucher, handle_run
from inline_keyboard import voucher_kb
from config import VOUCHERS_PATH_4_HOUER, VOUCHERS_PATH_8_HOUER

router = Router()



@router.message(F.text, Voucher.description)
async def get_description(message: Message, state: FSMContext):
    text = message.text
    if len(text) < 15:
        await message.answer('Прошу напишите больше информации.')
        await send_voucher(message, state)
    else:
        await state.update_data(description=message.text)
        await state.set_state(Voucher.hour)
        await message.answer('Выберите из списка скольки часовой ваучер вам необходим:', reply_markup=voucher_kb())



@router.callback_query(F.data, Voucher.hour)
async def call_voucher(call: CallbackQuery, state: FSMContext):
    if call.data == '4':
        await state.update_data(hour=call.data)
        data = await state.get_data()

        result = get_voucher(data.get('id_user'), data.get('user_fullname'), data.get('description'), VOUCHERS_PATH_4_HOUER)
        await state.clear()
        await call.message.answer(result)
        await handle_run(call.message)
    elif call.data == '8':
        await state.update_data(hour=call.data)
        data = await state.get_data()
        result = get_voucher(data.get('id_user'), data.get('user_fullname'), data.get('description'), VOUCHERS_PATH_8_HOUER)
        await state.clear()
        await call.message.answer(result)
        await handle_run(call.message)


@router.message(F.text, Voucher.hour)
async def wrong_step(message: Message, state: FSMContext):
    await message.answer('Я не понимаю вас...')
    await state.set_state(Voucher.description)
    return