from aiogram.fsm.state import State, StatesGroup

class WarehouseStates(StatesGroup):
    inventory_menu = State()

class AddMaterialStates(StatesGroup):
    name = State()
    quantity = State()
    price = State()
    description = State()

class UpdateMaterialStates(StatesGroup):
    search = State()
    select = State()
    name = State()
    description = State()

class TechnicianMaterialStates(StatesGroup):
    select_technician = State()
    select_material = State()
    enter_quantity = State()

class StatsStates(StatesGroup):
    waiting_range = State()