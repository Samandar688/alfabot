# handlers/inventory.py
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from decimal import Decimal, InvalidOperation

from filters.role_filter import RoleFilter
from keyboards.warehouse_buttons import (
    get_warehouse_main_menu,
    get_inventory_actions_keyboard,
)
from states.warehouse_states import WarehouseStates, AddMaterialStates
from database.warehouse_queries import create_material

router = Router()
router.message.filter(RoleFilter("warehouse"))

def cancel_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
        resize_keyboard=True
    )

def fmt_sum(val: Decimal | int | float | None) -> str:
    if val is None:
        return "0"
    return f"{Decimal(val):,.0f}".replace(",", " ")

# Inventarizatsiya menyusiga kirish
@router.message(F.text.in_(["📦 Inventarizatsiya", "📦 Инвентаризация"]))
async def inventory_handler(message: Message, state: FSMContext):
    await state.set_state(WarehouseStates.inventory_menu)
    await message.answer("📦 Inventarizatsiya boshqaruvi", reply_markup=get_inventory_actions_keyboard("uz"))

# Orqaga (faqat inventarizatsiya holatida)
@router.message(StateFilter(WarehouseStates.inventory_menu), F.text.in_(["◀️ Orqaga", "🔙 Orqaga", "◀️ Назад", "Orqaga"]))
async def inventory_back(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("⬅️ Asosiy menyu", reply_markup=get_warehouse_main_menu("uz"))

# ============== ➕ Mahsulot qo'shish oqimi ==============

@router.message(StateFilter(WarehouseStates.inventory_menu), F.text.in_(["➕ Mahsulot qo'shish", "➕ Добавить товар"]))
async def inv_add_start(message: Message, state: FSMContext):
    await state.set_state(AddMaterialStates.name)
    await message.answer("🏷️ Mahsulot nomini kiriting:", reply_markup=cancel_kb())

@router.message(StateFilter(AddMaterialStates.name))
async def inv_add_name(message: Message, state: FSMContext):
    if message.text.strip().lower() in ("❌ bekor qilish", "bekor", "cancel"):
        await state.set_state(WarehouseStates.inventory_menu)
        return await message.answer("❌ Bekor qilindi.\n\n📦 Inventarizatsiya menyusi:", reply_markup=get_inventory_actions_keyboard("uz"))

    name = message.text.strip()
    if len(name) < 2:
        return await message.answer("❗ Nomi juda qisqa. Qaytadan kiriting:")

    await state.update_data(name=name)
    await state.set_state(AddMaterialStates.quantity)
    await message.answer("📦 Miqdorni kiriting (butun son):")

@router.message(StateFilter(AddMaterialStates.quantity))
async def inv_add_quantity(message: Message, state: FSMContext):
    txt = message.text.strip()
    if txt.lower() in ("❌ bekor qilish", "bekor", "cancel"):
        await state.set_state(WarehouseStates.inventory_menu)
        return await message.answer("❌ Bekor qilindi.\n\n📦 Inventarizatsiya menyusi:", reply_markup=get_inventory_actions_keyboard("uz"))

    if not txt.isdigit():
        return await message.answer("❗ Faqat butun son kiriting. Qayta kiriting:")

    qty = int(txt)
    if qty < 0:
        return await message.answer("❗ Miqdor manfiy bo‘lishi mumkin emas. Qayta kiriting:")

    await state.update_data(quantity=qty)
    await state.set_state(AddMaterialStates.price)
    await message.answer("💰 Narxni kiriting (so'm) — butun son yoki 100000.00 ko‘rinishida:")

@router.message(StateFilter(AddMaterialStates.price))
async def inv_add_price(message: Message, state: FSMContext):
    txt = message.text.strip()
    if txt.lower() in ("❌ bekor qilish", "bekor", "cancel"):
        await state.set_state(WarehouseStates.inventory_menu)
        return await message.answer("❌ Bekor qilindi.\n\n📦 Inventarizatsiya menyusi:", reply_markup=get_inventory_actions_keyboard("uz"))

    # vergul/bo‘shliqni tozalash
    norm = txt.replace(" ", "").replace(",", ".")
    try:
        price = Decimal(norm)
        if price < 0:
            return await message.answer("❗ Narx manfiy bo‘lishi mumkin emas. Qayta kiriting:")
    except InvalidOperation:
        return await message.answer("❗ Noto‘g‘ri format. Masalan: 500000 yoki 500000.00. Qayta kiriting:")

    await state.update_data(price=price)
    await state.set_state(AddMaterialStates.description)
    await message.answer("📝 Mahsulot tavsifi kiriting (ixtiyoriy, o‘tkazib yuborish uchun “-” yozing):")

@router.message(StateFilter(AddMaterialStates.description))
async def inv_add_description(message: Message, state: FSMContext):
    txt = message.text.strip()
    if txt.lower() in ("❌ bekor qilish", "bekor", "cancel"):
        await state.set_state(WarehouseStates.inventory_menu)
        return await message.answer("❌ Bekor qilindi.\n\n📦 Inventarizatsiya menyusi:", reply_markup=get_inventory_actions_keyboard("uz"))

    description = None if txt in ("-", "") else txt

    data = await state.get_data()
    name = data["name"]
    qty = data["quantity"]
    price = data["price"]

    try:
        created = await create_material(
            name=name,
            quantity=qty,
            price=price,
            description=description,
            serial_number=None  # hozircha kiritmaymiz
        )
    except Exception as e:
        # DB xatosi
        await state.set_state(WarehouseStates.inventory_menu)
        return await message.answer(f"❌ Xatolik: ma'lumot bazaga yozilmadi.\nDetails: {e}\n\n📦 Inventarizatsiya menyusi:", reply_markup=get_inventory_actions_keyboard("uz"))

    # Muvaffaqiyat
    await state.set_state(WarehouseStates.inventory_menu)
    await message.answer(
        "✅ Mahsulot muvaffaqiyatli qo‘shildi!\n"
        f"🏷️ Nom: <b>{created['name']}</b>\n"
        f"📦 Miqdor: <b>{created['quantity']}</b>\n"
        f"💰 Narx: <b>{fmt_sum(created['price'])} so'm</b>",
        parse_mode="HTML",
    )
    await message.answer("📦 Inventarizatsiya menyusi:", reply_markup=get_inventory_actions_keyboard("uz"))
