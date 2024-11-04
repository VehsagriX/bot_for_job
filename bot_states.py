from aiogram.filters.state import StatesGroup, State


class User(StatesGroup):
    chat_id = State()
    user_id = State()
    user_login = State()
    user_name = State()
    user_last_name = State()
    user_phone = State()
    user_email = State()


class Request(StatesGroup):
    request_type = State()
    company_name = State()
    request_title = State()
    request_description = State()
    request_id = State()
    request_creator = State()
    request_admin = State()
    
