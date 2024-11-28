from datetime import datetime

from aiogram import Router, F, flags

from aiogram.types import Message
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext

from bot_states import Request
from crud_request_file import add_request
from send_message_in_group import get_message_request_in_group
from handlers.command_handlers import handle_run

router = Router()


@router.message(Request.request_type)
@router.message(F.text.lower() == 'запрос')
@router.message(F.text.lower() == 'инцидент')
@flags.chat_action(ChatAction.TYPING)
async def handle_button(message: Message, state: FSMContext) -> None:
    """
    Фун-ция получает значение нажатой кнопк, присваивает в request_type значение заявки, отправляет сообщение для получения значения
    в request_title
    :param message: Message которым мы отправляем и получаем сообщение
    :param state: FSM контроль пошагового действия
    :return: None
    """
    await state.update_data(request_type=message.text)
    my_data = datetime.now()
    result = f'{my_data.day}{my_data.month}{my_data.year}{my_data.hour}{my_data.minute}'

    await state.update_data(request_id=f'{result}{message.from_user.id}')
    await state.update_data(request_creator=message.from_user.id)
    await state.update_data(login_creator=message.from_user.username)
    if message.text.lower() == 'инцидент':
        await message.answer('Напишите коротко о вашей проблеме. Пример: Заправка картриджа, Установка windows или другого ПО, перенос данных и т.п.')
        await state.set_state(Request.request_title)
    elif message.text.lower() == 'запрос':
        await message.answer('Напишите коротко о вашем запросе. Пример: закуп ноутбука, новое подключение к сети интернет, либо к локальной сети, закуп принтера и т.п.')
        await state.set_state(Request.request_title)
    else:
        await message.answer('Я вас не понимаю, повторите попытку')
        await state.set_state(Request.request_type)
        return


@router.message(F.text.lower() == 'назад ◀️', Request())
async def get_back(message: Message, state: FSMContext) -> None:
    """
    Фун-ция для неверных данных в Request-state
    :param message: Message получение и отправка сообщения
    :param state: FSM контроль пошагового действия
    :return:
    """
    await state.clear()
    await message.answer('Попробуйте заново.')

    await handle_run(message)


@router.message(F.text, Request.request_title)
@flags.chat_action(ChatAction.TYPING)
async def handler_title(message: Message, state: FSMContext) -> None:
    """
    Функция для получения значения в request_title, отправляет сообщение для получения значения request_description
    :param message: Message получение и отправка сообщения
    :param state: FSM контроль пошагового действия
    :return: None
    """
    await state.update_data(request_title=message.text)
    await message.answer("""Пожалуйста, опишите вашу проблему как можно подробнее. 
Если у вас есть визуальные материалы (фотографии или видео), которые помогут лучше понять ситуацию, вы сможете 
отправить их исполнителю личным сообщением, после принятия вашей заявки в работу.""")
    await state.set_state(Request.request_description)




@router.message(F.text, Request.request_description)
@flags.chat_action(ChatAction.TYPING)
async def handler_description(message: Message, state: FSMContext) -> None:
    """
    Фунция проверяет введенные данные на достаточное кол-во длинны, получает данные в data: dict, обнуляет Request-state,
    отправляет данные в функцию add_request(data) для записи в БД
    :param message: Message получение и отправка сообщения
    :param state: FSM контроль пошагового действия
    :return:
    """
    if len(message.text) < 20:
        await message.answer('Этого недостаточно, попробуйте описать более подробно.')
        await state.set_state(Request.request_description)
    else:
        await state.set_state(Request.request_admin)
        await state.update_data(request_description=message.text)
        await state.update_data(request_admin='В ожидании')
        await state.update_data(request_status='Новый')
        await state.update_data(date_create=datetime.now().strftime('%d.%m.%Y'))
        await state.update_data(time_create=datetime.now().strftime('%H:%M'))
        await message.reply('Спасибо, ваша информация передана в ГПП.')
        await handle_run(message)
        data = await state.get_data()
        await state.clear()
        add_request(data)
        user_id = message.from_user.id
        await get_message_request_in_group(data, user_id)



@router.message(F.text, Request())
async def error_message(message: Message):
    """
    Ошибочный ввод данных в любом шаге Request-state
    :param message: Message получение и отправка сообщения
    :return:
    """
    await message.answer('Я не понимаю, выберите то, что нужно ⬇️')
    await handle_run(message)
