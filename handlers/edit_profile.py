from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot_states import EditState
from filters import check_email

router = Router()



@router.message(StateFilter(EditState.edit_key))
@router.message(F.text == 'Почта 📧')
@router.message(F.text.lower() == 'почта 📧')
async def answer_edit_value(message: Message, state: FSMContext):
    await state.update_data(edit_key='user_email')
    await message.answer('Введите данные для замены')
    await state.set_state(EditState.edit_value)


@router.message(StateFilter(EditState.edit_key))
@router.message(F.text == 'Номер 📱')
@router.message(F.text.lower() == 'номер 📱')
async def answer_edit_value(message: Message, state: FSMContext):
    await state.update_data(edit_key='user_email')
    await message.answer('Введите данные для замены')
    await state.set_state(EditState.edit_value)



@router.message(StateFilter(EditState.edit_key))
@router.message(F.text)
async def cancel_edit_key(message: Message, state: FSMContext):
    await message.answer('Ввели неверные данные, повторите попытку')
    await state.set_state(EditState.edit_key)


@router.message(StateFilter(EditState.edit_value))
@router.message(F.text)
async def get_edit_value(message: Message, state: FSMContext):
    if len(message.text.split()) > 1:
        await message.answer('Вы ввели неверные данные попробуйте снова')
        await state.set_state(EditState.edit_value)
        return
    await state.update_data(edit_value=message.text)
    data = await state.get_data()
    print(data)