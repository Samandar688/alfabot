from aiogram.fsm.state import State, StatesGroup

class WarehouseStates(StatesGroup):
    inventory_menu = State()

class AddMaterialStates(StatesGroup):
    name = State()
    quantity = State()
    price = State()
    description = State()