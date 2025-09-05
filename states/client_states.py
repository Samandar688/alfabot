from aiogram.fsm.state import State, StatesGroup

class ConnectionOrderStates(StatesGroup):
    """Connection order states for client"""
    selecting_region = State()
    selecting_connection_type = State()
    selecting_tariff = State()
    entering_address = State()
    asking_for_geo = State()
    waiting_for_geo = State()
    confirming_connection = State()

class ServiceOrderStates(StatesGroup):
    """Service order states for client"""
    selecting_region = State()
    selecting_abonent_type = State()
    waiting_for_contact = State()
    entering_description = State()
    entering_reason = State()
    entering_address = State()
    asking_for_media = State()
    waiting_for_media = State()
    asking_for_location = State()
    waiting_for_location = State()