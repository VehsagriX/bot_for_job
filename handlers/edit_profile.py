from aiogram import Router, F

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot_states import EditState
from crud_user_file import edit_profile_for_value
from filters import check_email, check_num
from handlers.command_handlers import change_profile, handle_run

router = Router()


@router.message(F.text, EditState.edit_state)
async def answer_edit_value(message: Message, state: FSMContext):
    text = message.text.lower()
    if text == 'почта 📧' or 'почта' in text:
        await state.set_state(EditState.edit_value_email)
        await message.answer('Пожалуйста введите почту')
        await state.update_data(edit_state=True)
        await state.update_data(edit_email='user_email')

    elif text == 'номер 📱' or 'номер' in text:
        await state.set_state(EditState.edit_value_phone)
        await message.answer('Пожалуйста введите номер')
        await state.update_data(edit_state=True)
        await state.update_data(edit_phone='user_phone')





@router.message(F.text, EditState.edit_value_email)
async def get_edit_value(message: Message, state: FSMContext):
    if len(message.text.split()) == 1 and check_email(message.text):
        await state.update_data(edit_value_email=message.text)
        data = await state.get_data()
        user_id = message.from_user.id
        key_email = data.get('edit_email')
        value_email = data.get('edit_value_email')

        result = edit_profile_for_value(user_id, key_email, value_email)
        await message.answer(result)
        # тут изменение данных и вывод
        await state.clear()
        await handle_run(message)
    else:
        await message.answer('Вы ввели неверные данные попробуйте снова')
        await state.set_state(EditState.edit_value_email)
        return



@router.message(F.text, EditState.edit_value_phone)
async def get_edit_value(message: Message, state: FSMContext):
    if len(message.text.split()) == 1 and check_num(message.text):
        await state.update_data(edit_value_phone=message.text)
        data = await state.get_data()

        user_id = message.from_user.id
        key_phone = data.get('edit_phone')
        value_phone = int(data.get('edit_value_phone'))

        result = edit_profile_for_value(user_id, key_phone, value_phone)
        # тут изменение данных и вывод
        await message.answer(result)
        await state.clear()

        await handle_run(message)
    else:
        await message.answer('Вы ввели неверные данные попробуйте снова')
        await state.set_state(EditState.edit_value_phone)
        return


@router.message(EditState.edit_state)
@router.message(F.text)
async def answer_edit_wrong_value(message: Message, state: FSMContext):
    await message.answer('Вы ошиблись, повторите пожалуйста, можете воспользоваться кнопками ⬇️')
    await state.clear()
    await change_profile(message, state)
