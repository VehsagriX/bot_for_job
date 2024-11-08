from datetime import datetime
from gc import callbacks

from aiogram import Router, F, flags
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext


from bot_states import Request
from examination import get_message_request_in_group
from handlers.command_handlers import handle_start_subscribed, handle_run
from keyboard import keyboard_builder, inline_request_chat_kb

from add_to_file import get_user_name

router = Router()





@router.message(Request.request_type)
@router.message(F.text.lower() == 'запрос')
@router.message(F.text.lower() == 'инцидент')
@flags.chat_action(ChatAction.TYPING)
async def handle_button(message: Message, state: FSMContext):
    await state.update_data(request_type=message.text)
    my_data = datetime.now()
    result = f'{my_data.day}{my_data.month}{my_data.year}{my_data.hour}{my_data.minute}'
    await state.update_data(request_id=f'{result}{message.from_user.id}')
    await state.update_data(request_creator=message.from_user.id)
    await message.answer('Какую компанию вы представляете')
    await state.set_state(Request.company_name)


@router.message(F.text, Request.company_name)
@flags.chat_action(ChatAction.TYPING)
async def handler_company(message: Message, state: FSMContext):
    await state.update_data(company_name=message.text)
    await message.answer('Можете написать кратко о вашей проблеме прим(Заправка картриджа, Установка windows...)')
    await state.set_state(Request.request_title)


@router.message(F.text, Request.request_title)
@flags.chat_action(ChatAction.TYPING)
async def handler_title(message: Message, state: FSMContext):
    await state.update_data(request_title=message.text)
    await message.answer("Теперь опишите полностью о своей проблеме, если не можете описать или есть фото, видео,"
                         "прикрепите к сообщению")
    await state.set_state(Request.request_description)


@router.message(F.text, Request.request_description)
@flags.chat_action(ChatAction.TYPING)
async def handler_description(message: Message, state: FSMContext):
    if len(message.text) < 20:
        await message.answer('Этого недостаточно, попробуйте описать более развернуто')
        await state.set_state(Request.request_description)
    else:
        await state.update_data(request_description=message.text)
        await state.set_state(Request.request_admin)
        await message.reply('Спасибо, я передам всю информацию специалистам')
        data = await state.get_data()
        user_id = message.from_user.id
        await get_message_request_in_group(data, user_id)
        # Пооопробоовть этоо изменение, еслии не поолучитсся, тто рабоотать с переменной data


#
@router.callback_query(F.data == "accepted",)
async def callback_accept(call: CallbackQuery, state: FSMContext):
    await state.update_data(request_admin=call.from_user.id)
    print(call)
#     data = await state.get_data()
#     print(data)
#     name, last_name = get_user_name(data.get('request_creator'))
#     text = f"""ID: {data.get('request_id')}\nТип заявки: {data.get('request_type')}\nКомпания: {data.get('company_name')}
# Создатель заявки: {name} {last_name}\nЗаголовок: {data.get('request_title')}\nОписание: {data.get('request_description')}
# ID Создателя: {data.get('request_creator')}"""
#     await call.bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=inline_request_chat_kb())


@router.message(F.text, Request())
async def error_message(message: Message):
    await message.answer('Я не понимаю, выберите то что вам нужно')
    await handle_run(message)
