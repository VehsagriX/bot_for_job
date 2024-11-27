from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from pyexpat.errors import messages

from bot_states import AdminState
from crud_request_file import show_all_requests
from handlers.command_handlers import handle_run, admin_works

router = Router()


@router.message(AdminState.admin_login, F.text == 'Мои заявки в исполнении 🧑‍💻')
async def get_request_status_worked(message: Message, state: FSMContext):
    await state.update_data(admin_login=message.from_user.username)
    await state.update_data(work_status='В работе')
    data = await state.get_data()
    user_login = data['admin_login']
    search_status = data['work_status']
    result = show_all_requests(user_login, search_status)
    if len(result) > 0:
        for text in result:
            await message.answer(text)
    else:
        await message.answer('У вас нет активных заявок')
    await state.clear()
    await handle_run(message)


@router.message(AdminState.admin_login, F.text == 'Мои решенные заявки ✅')
async def get_request_status_completed(message: Message, state: FSMContext):
    await state.update_data(admin_login=message.from_user.username)
    await state.update_data(work_status='Выполнено')
    data = await state.get_data()
    user_login = data['admin_login']
    search_status = data['work_status']
    result = show_all_requests(user_login, search_status)
    if len(result) > 0:
        for text in result:
            await message.answer(text)
    else:
        await message.answer('У вас нет выполненных заявок')
    await state.clear()
    await handle_run(message)



@router.message(F.text == 'Отчет 📊', AdminState.admin_login)
async def get_report(message: Message, state: FSMContext):
    pass

@router.message(F.text == 'Назад ️◀️', AdminState.admin_login)
async def back_admin(message: Message, state: FSMContext):
    await state.clear()
    await handle_run(message)




@router.message(AdminState.admin_login, F.text)
async def wrong_step(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Я вас не понимаю')
    await admin_works(message, state)
