from email.policy import default

from aiogram.filters.state import StatesGroup, State


class User(StatesGroup):
    chat_id = State()
    user_id = State()
    user_login = State()
    user_name = State()
    user_last_name = State()
    user_phone = State()
    user_email = State()
    company_name = State()
    department = State()


class Request(StatesGroup):
    request_type = State()
    request_title = State()
    request_admin = State()
    request_description = State()
    request_id = State()
    request_creator = State()
    login_creator = State()
    request_status = State()
    date_create = State()
    time_create = State()
    date_accepted = State()
    time_accepted = State()
    date_finished = State()
    time_finished = State()

class EditState(StatesGroup):
    edit_state = State()
    edit_column = State()
    edit_value_phone = State()
    edit_value_email = State()
    edit_company = State()
    edit_departament = State()


class Voucher(StatesGroup):
    id_user = State()
    user_fullname = State()
    description = State()
    hour = State()

class AdminState(StatesGroup):
    admin_login = State()
    work_status = State()
