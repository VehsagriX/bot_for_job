from aiogram import Router, F, flags
from aiogram.types import Message
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from bot_states import Request
from examination import get_message_request_in_group
from keyboard import keyboard_builder
from aiogram.filters import StateFilter
from add_to_file import get_user_name

router = Router()


@router.message(F.text.lower() == 'создать заявку ✍️')
@router.message(F.text.lower() == 'создать заявку')
@router.message(StateFilter(None))
async def on_startup(message: Message, state: FSMContext):
    await message.answer('Запрос - приобретение что то нового\nИнцедент - исправление чего-либо',
                         reply_markup=keyboard_builder())
    await state.set_state(Request.request_type)


@router.message(F.text.lower() == 'запрос')
@router.message(F.text.lower() == 'инцидент')
@router.message(Request.request_type)
@flags.chat_action(ChatAction.TYPING)
async def handle_button(message: Message, state: FSMContext):
    await state.update_data(request_type=message.text)
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
    await state.update_data(request_description=message.text)
    await message.reply('Спасибо, я передам всю информацию специалистам')
    await state.update_data()
    data = await state.get_data()
    await get_message_request_in_group(data)
