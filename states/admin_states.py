from aiogram.fsm.state import StatesGroup, State

class UserRoleChange(StatesGroup):
    waiting_for_search_method = State()
    waiting_for_telegram_id = State()
    waiting_for_phone = State()
    waiting_for_new_role = State()
