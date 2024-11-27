from aiogram import Router, F, flags
from aiogram.enums import ChatAction
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.formatting import Text, Bold
from pydantic.v1 import NoneStr

from config import users_for_voucher, super_admin
from crud_request_file import show_all_requests
from crud_user_file import is_registered, get_user_data
from get_vaucher import get_voucher
from reply_keyboard import keyboard_answer, kb_get_started, edit_kb, keyboard_builder, edit_key_kb, \
    kb_run_step_user, kb_run_step_admin, kb_admin, kb_super_admin

from bot_states import User, Request, EditState, AdminState
from send_message_in_group import is_user_subscribed, is_admin

router = Router()


@router.message(F.text, CommandStart())
@flags.chat_action(ChatAction.TYPING)
async def handle_start_subscribed(message: Message, state: FSMContext) -> None:
    """
    Функция комадны /start. Проверяет на подписку пользователя в группах, проверяет зарегистрирован ли пользователь,
    отправляет в разные направления state
    :param message: Message которым мы отправляем и получаем сообщение
    :param state: FSM контроль пошагового действия(Выбор в какой стейт идти)
    :return: None
    """
    is_member = await is_user_subscribed(message.from_user.id)

    if is_member:
        if not is_registered(message.from_user.id):
            await state.set_state(User.user_id)
            await state.set_state(User.user_login)
            await state.set_state(User.chat_id)
            content = Text(
                "Приветствую ",
                Bold(message.from_user.full_name)
            )
            await state.clear()

            await message.answer(
                **content.as_kwargs()
            )
            await state.update_data(user_id=message.from_user.id)
            await state.update_data(user_login=message.from_user.username)
            await state.update_data(chat_id=message.chat.id)
            await message.answer('Вы не зарегистрированы. Готовы пройти регистрацию?',
                                 reply_markup=keyboard_answer())
            await state.set_state(User.user_name)
            await state.set_state(User.user_last_name)
        else:
            await message.answer(
                'Добрый день, я помощник Группы Поддержки Пользователей Департамента Информационных Технологий ЗАО «КОИНОТИ НАВ». Выберите, что вы хотели бы сделать ⬇️',
                reply_markup=kb_get_started())

    else:
        await cancel_message(message)


@router.message(F.text, Command('get_started'))
@router.message(F.text.lower() == "начать работу 💼")
@router.message(F.text.lower() == "начать работу")
async def handle_run(message: Message) -> None:
    """
    Начало работы после команды /start, функция предназначена дать выбор пользователю начать работу или отменить действия
    После проверка это обычный user или admin
    :param message: Message которым мы отправляем и получаем сообщение
    :return: None
    """
    admin = await is_admin(message.from_user.id)
    if not admin:
        await message.answer('Выберите то, что вам необходимо ⬇️', reply_markup=kb_run_step_user())
    else:
        await message.answer('Выберите то, что вам необходимо ⬇️', reply_markup=kb_run_step_admin())


@router.message(F.text.lower() == 'создать заявку ✍️')
@router.message(F.text.lower() == 'создать заявку')
async def on_startup(message: Message, state: FSMContext) -> None:
    """
    Фунция начала шага для Создания заявки и переход в начало Request-state
    :param message: Message которым мы отправляем и получаем сообщение
    :param state: FSM контроль пошагового действия
    :return:
    """
    await message.answer(
        'Запрос - приобретение ИТ оборудования и ПО, либо выполнение новых определённых ИТ работ.\nИнцидент - исправление проблем в ИТ оборудовании или ПО.',
        reply_markup=keyboard_builder())
    await state.set_state(Request.request_type)


@router.message(F.text.lower() == 'назад ◀️', Request.request_type)
@router.message(F.text.lower() == 'назад ◀️', StateFilter(default_state))
async def get_back(message: Message, state: FSMContext):
    """
    Фу-ция для шага перехода в главное меню бота, очищает state
    :param message: Message которым мы отправляем и получаем сообщение
    :param state: FSM контроль пошагового действия
    :return:
    """
    await state.clear()
    await handle_run(message)


@router.message(F.text.lower() == '⚙️ админ панель', StateFilter(None))
@router.message(F.text == '⚙️ Админ панель', default_state)
async def admin_works(message: Message, state: FSMContext):
    await state.set_state(AdminState.admin_login)
    if message.from_user.id in super_admin:
        await message.answer('Выберите, что вас интересует', reply_markup=kb_super_admin())
    else:
        await message.answer('Выберите, что вас интересует', reply_markup=kb_admin())



@router.message(F.text, Command("cancel"))
@router.message(F.text.lower() == "отмена 🔚")
@router.message(F.text.lower() == 'отмена')
@flags.chat_action(ChatAction.TYPING)
async def cmd_cancel(message: Message, state: FSMContext):
    """
    Отмена работы и выход из бота, очищаем state полностью.
    :param message: Message которым мы отправляем и получаем сообщение
    :param state: FSM контроль пошагового действия
    :return: None
    """
    await state.clear()

    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer('Всего доброго!😉')


@router.message(Command('/myprofile'))
@router.message(F.text.lower() == "моя анкета 📝")
@router.message(F.text.lower() == "моя анкета")
async def view_profile(message: Message) -> None:
    """
    Фун-ция для получения данных пользователя, отправляет данные пользователю, для проверки и информации
    :param message: Message которым мы отправляем и получаем сообщение
    :return:
    """
    name, last_name, phone, email, company, departament = get_user_data(message.from_user.id)
    my_text = f'Имя: {name}\nФамилия: {last_name}\nТелефон: {phone}\nПочта: {email}\nКомпания: {company}\nДепартамент/Отдел: {departament}'
    await message.answer(text=my_text, reply_markup=edit_kb())


@router.message(F.text == 'Изменить данные')
@router.message(F.text == 'изменить данные')
async def change_profile(message: Message, state: FSMContext) -> None:
    await message.answer('Выберите какие данные будете изменять⬇️', reply_markup=edit_key_kb())
    await state.set_state(EditState.edit_state)


@router.message(F.text == 'Мои заявки в работе ⏳')
@router.message(F.text.lower() == 'мои заявки в работе ⏳')
async def show_all_request(message: Message) -> None:
    """
    Фун-ция получения всех заявок пользователя по id-пользователю, если нет заявок будет отправлять соответствующее сообщение
    :param message: Message которым мы отправляем и получаем сообщение
    :return: None
    """
    user_id = message.from_user.id
    result = show_all_requests(user_id)
    if len(result) > 0:
        for text in result:
            await message.answer(text)
    else:
        await message.answer('У вас нет активных заявок')


@router.message(F.text == 'Доступ к Гостевому WIFI🛜', StateFilter(default_state))
@router.message(F.text.lower() == 'доступ к гостевому wifi🛜', StateFilter(default_state))
async def send_voucher(message: Message):
    """

    :param message:
    :return:
    """
    if str(message.from_user.id) in users_for_voucher:
        result = get_voucher(message.from_user.id, message.from_user.username)
        await message.answer(f'{result}')
    else:
        await message.answer('Прошу прощения, у вас нет доступа. Пожалуйста обратитесь в тех. поддержку 446607070')
        await handle_run(message)


@router.message(F.text == 'Назад ◀️')
@router.message(F.text.lower() == 'назад ◀️')
async def get_back(message: Message, state: FSMContext) -> None:
    await state.clear()
    await handle_run(message)


@router.message(Command('help'))
async def handle_help(message: Message) -> None:
    """

    :param message:
    :return:
    """
    text = """Этот бот разработан с целью улучшения качества коммуникации и взаимодействия с группой поддержки пользователей (ГПП) ДИТ ЗАО «КОИНОТИ НАВ». Мы стремимся предоставить максимально оперативную и эффективную помощь по всем вопросам, связанным с вопросами ИТ направления. Ваше обращение через этот канал позволит нам быстрее и эффективнее реагировать на ваши запросы, обеспечивая высокий уровень поддержки и удовлетворённости.
Возможности бота: 
✅ создание заявки на ИТ поддержку;
✅ создание заявки на ИТ работы;
✅ создание заявки на закуп ИТ оборудования;
✅ просмотр статуса заявки;
✅ связаться с исполнителем заявки;
✅ выдать ваучер на подключение к гостевому WI FI;
✅ изменить данные регистрации пользователя (телефон, почта);
/start - Для начала работы с ботом необходимо запустить команду - /start, или дать команду боту путем отправки сообщения /start;
/cancel – Отменяет и выходит из работы с ботом, для последующего взаимодействия нужно запустить бот заново;
"""
    await message.answer(text)


@router.message(F.text, StateFilter(default_state))
async def cancel_message(message: Message) -> None:
    """

    :param message:
    :return:
    """
    await message.answer("""Прошу прощения, по причине того, что вы отсутствуете в списке зарегистрированных пользователей, я не могу вам помочь. До свидания.""")
