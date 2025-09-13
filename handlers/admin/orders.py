from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from datetime import datetime
import html
from database.admin_orders_queries import (
    get_user_by_telegram_id,
    get_connection_orders,
    get_technician_orders,
    get_saff_orders
)
from filters.role_filter import RoleFilter
from keyboards.admin_buttons import get_applications_main_menu, get_admin_main_menu

router = Router()

router.message.filter(RoleFilter("admin")) 

def fmt_dt(dt: datetime) -> str:
    return dt.strftime("%d.%m.%Y %H:%M")

def esc(v) -> str:
    if v is None:
        return "-"
    return html.escape(str(v), quote=False)

# Status nomlarini mapping
CONNECTION_STATUS_NAMES = {
    "new": "🆕 Yangi",
    "in_manager": "👨‍💼 Menejerda",
    "in_junior_manager": "👨‍💼 Junior menejerda",
    "in_controller": "🎛️ Controllerda",
    "in_technician": "🔧 Texnikda",
    "in_diagnostics": "🔍 Diagnostikada",
    "in_repairs": "🛠️ Ta'mirda",
    "in_warehouse": "📦 Omborда",
    "in_technician_work": "⚙️ Texnik ishda",
    "completed": "✅ Tugallangan"
}

TECHNICIAN_STATUS_NAMES = {
    "new": "🆕 Yangi",
    "in_controller": "🎛️ Controllerda",
    "in_technician": "🔧 Texnikda",
    "in_diagnostics": "🔍 Diagnostikada",
    "in_repairs": "🛠️ Ta'mirda",
    "in_warehouse": "📦 Omborда",
    "in_technician_work": "⚙️ Texnik ishda",
    "completed": "✅ Tugallangan"
}

def connection_order_text(item: dict) -> str:
    order_id = item['id']
    created = item["created_at"]
    created_dt = datetime.fromisoformat(created) if isinstance(created, str) else created
    
    # Escape ALL dynamic fields
    full_name = esc(item.get('full_name', '-'))
    phone = esc(item.get('phone', '-'))
    username = esc(item.get('username', ''))
    address = esc(item.get('address', '-'))
    region = esc(item.get('region', '-'))
    tarif_name = esc(item.get('tarif_name', '-'))
    status = CONNECTION_STATUS_NAMES.get(item.get('status', 'new'), item.get('status', 'new'))
    notes = esc(item.get('notes', '-'))
    jm_notes = esc(item.get('jm_notes', '-'))
    rating = item.get('rating', 0) or 0
    
    username_text = f"\n👤 Username: @{username}" if username else ""
    location_text = ""
    if item.get('latitude') and item.get('longitude'):
        lat = item['latitude']
        lon = item['longitude']
        location_text = f"\n📍 GPS: https://maps.google.com/?q={lat},{lon}"
    
    rating_text = "⭐" * rating if rating > 0 else "Baholanmagan"
    
    return (
        "🔌 <b>ULANISH ZAYAVKASI</b>\n\n"
        f"📋 <b>Buyurtma:</b> #{esc(order_id)}\n"
        f"🏷️ <b>Status:</b> {status}\n"
        f"👤 <b>Mijoz:</b> {full_name}\n"
        f"📞 <b>Telefon:</b> {phone}{username_text}\n"
        f"🌍 <b>Hudud:</b> {region}\n"
        f"📍 <b>Manzil:</b> {address}{location_text}\n"
        f"📦 <b>Tarif:</b> {tarif_name}\n"
        f"⭐ <b>Baho:</b> {rating_text}\n"
        f"📝 <b>Izohlar:</b> {notes}\n"
        f"📝 <b>JM Izohlar:</b> {jm_notes}\n"
        f"📅 <b>Sana:</b> {fmt_dt(created_dt)}"
    )

def technician_order_text(item: dict) -> str:
    order_id = item['id']
    created = item["created_at"]
    created_dt = datetime.fromisoformat(created) if isinstance(created, str) else created
    
    # Escape ALL dynamic fields
    full_name = esc(item.get('full_name', '-'))
    phone = esc(item.get('phone', '-'))
    username = esc(item.get('username', ''))
    address = esc(item.get('address', '-'))
    region = esc(item.get('region', '-'))
    abonent_id = esc(item.get('abonent_id', '-'))
    description = esc(item.get('description', '-'))
    status = TECHNICIAN_STATUS_NAMES.get(item.get('status', 'new'), item.get('status', 'new'))
    notes = esc(item.get('notes', '-'))
    rating = item.get('rating', 0) or 0
    
    username_text = f"\n👤 Username: @{username}" if username else ""
    location_text = ""
    if item.get('latitude') and item.get('longitude'):
        lat = item['latitude']
        lon = item['longitude']
        location_text = f"\n📍 GPS: https://maps.google.com/?q={lat},{lon}"
    
    rating_text = "⭐" * rating if rating > 0 else "Baholanmagan"
    
    return (
        "🔧 <b>TEXNIK ZAYAVKA</b>\n\n"
        f"📋 <b>Buyurtma:</b> #{esc(order_id)}\n"
        f"🏷️ <b>Status:</b> {status}\n"
        f"👤 <b>Mijoz:</b> {full_name}\n"
        f"📞 <b>Telefon:</b> {phone}{username_text}\n"
        f"🆔 <b>Abonent ID:</b> {abonent_id}\n"
        f"🌍 <b>Hudud:</b> {region}\n"
        f"📍 <b>Manzil:</b> {address}{location_text}\n"
        f"📝 <b>Tavsif:</b> {description}\n"
        f"⭐ <b>Baho:</b> {rating_text}\n"
        f"📝 <b>Izohlar:</b> {notes}\n"
        f"📅 <b>Sana:</b> {fmt_dt(created_dt)}"
    )

def saff_order_text(item: dict) -> str:
    order_id = item['id']
    created = item["created_at"]
    created_dt = datetime.fromisoformat(created) if isinstance(created, str) else created
    
    # Escape ALL dynamic fields
    full_name = esc(item.get('full_name', '-'))
    phone = esc(item.get('phone', '-'))
    username = esc(item.get('username', ''))
    address = esc(item.get('address', '-'))
    region = esc(item.get('region', '-'))
    abonent_id = esc(item.get('abonent_id', '-'))
    description = esc(item.get('description', '-'))
    status = CONNECTION_STATUS_NAMES.get(item.get('status', 'new'), item.get('status', 'new'))
    tarif_name = esc(item.get('tarif_name', '-'))
    type_of_zayavka = esc(item.get('type_of_zayavka', '-'))
    
    username_text = f"\n👤 Username: @{username}" if username else ""
    
    return (
        "👥 <b>XODIM ZAYAVKASI</b>\n\n"
        f"📋 <b>Buyurtma:</b> #{esc(order_id)}\n"
        f"🏷️ <b>Status:</b> {status}\n"
        f"🔧 <b>Tur:</b> {type_of_zayavka}\n"
        f"👤 <b>Mijoz:</b> {full_name}\n"
        f"📞 <b>Telefon:</b> {phone}{username_text}\n"
        f"🆔 <b>Abonent ID:</b> {abonent_id}\n"
        f"🌍 <b>Hudud:</b> {region}\n"
        f"📍 <b>Manzil:</b> {address}\n"
        f"📦 <b>Tarif:</b> {tarif_name}\n"
        f"📝 <b>Tavsif:</b> {description}\n"
        f"📅 <b>Sana:</b> {fmt_dt(created_dt)}"
    )

def nav_keyboard(index: int, total: int, order_type: str) -> InlineKeyboardMarkup:
    rows = []
    nav_row = []
    
    if index > 0:
        nav_row.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"{order_type}_prev_{index}"))
    
    if index < total - 1:
        nav_row.append(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"{order_type}_next_{index}"))
    
    if nav_row:
        rows.append(nav_row)
    
    # Orqaga qaytish tugmasi
    rows.append([InlineKeyboardButton(text="◀️ Orqaga", callback_data="orders_back_to_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=rows)

# Asosiy zayavkalar menyusi
@router.message(F.text.in_(["📝 Zayavkalar", "📝 Заявки"]))
async def open_orders_menu(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user or user.get("role") != "admin":
        return
    
    await message.answer(
        "📝 <b>Zayavkalar bo'limi</b>\n\n"
        "Quyidagi tugmalardan birini tanlang:",
        parse_mode='HTML',
        reply_markup=get_applications_main_menu()
    )

# Ulanish zayavkalari
@router.message(F.text.in_(["🔌 Ulanish zayavkalari", "🔌 Заявки на подключение"]))
async def open_connection_orders(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user or user.get("role") != "admin":
        return
    
    items = await get_connection_orders(limit=50, offset=0)
    if not items:
        await message.answer(
            "🔌 <b>Ulanish Zayavkalari</b>\n\n"
            "Hozircha zayavkalar yo'q.",
            parse_mode='HTML',
            reply_markup=get_applications_main_menu()
        )
        return
    
    await state.update_data(connection_orders=items, idx=0)
    text = connection_order_text(items[0])
    kb = nav_keyboard(0, len(items), "connection")
    await message.answer(text, reply_markup=kb, parse_mode="HTML")

# Texnik zayavkalar
@router.message(F.text.in_(["🔧 Texnik zayavkalar", "🔧 Технические заявки"]))
async def open_technician_orders(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user or user.get("role") != "admin":
        return
    
    items = await get_technician_orders(limit=50, offset=0)
    if not items:
        await message.answer(
            "🔧 <b>Texnik Zayavkalar</b>\n\n"
            "Hozircha zayavkalar yo'q.",
            parse_mode='HTML',
            reply_markup=get_applications_main_menu()
        )
        return
    
    await state.update_data(technician_orders=items, idx=0)
    text = technician_order_text(items[0])
    kb = nav_keyboard(0, len(items), "technician")
    await message.answer(text, reply_markup=kb, parse_mode="HTML")

# Xodim zayavkalari
@router.message(F.text.in_(["👥 Xodim zayavkalari", "👥 Заявки сотрудников"]))
async def open_saff_orders(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user or user.get("role") != "admin":
        return
    
    items = await get_saff_orders(limit=50, offset=0)
    if not items:
        await message.answer(
            "👥 <b>Xodim Zayavkalari</b>\n\n"
            "Hozircha zayavkalar yo'q.",
            parse_mode='HTML',
            reply_markup=get_applications_main_menu()
        )
        return
    
    await state.update_data(saff_orders=items, idx=0)
    text = saff_order_text(items[0])
    kb = nav_keyboard(0, len(items), "saff")
    await message.answer(text, reply_markup=kb, parse_mode="HTML")

# Navigation callbacks
@router.callback_query(F.data.startswith("connection_prev_"))
async def prev_connection_order(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    items = data.get("connection_orders", [])
    idx = int(cb.data.replace("connection_prev_", "")) - 1
    if idx < 0 or idx >= len(items):
        return
    await state.update_data(idx=idx)
    text = connection_order_text(items[idx])
    kb = nav_keyboard(idx, len(items), "connection")
    await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("connection_next_"))
async def next_connection_order(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    items = data.get("connection_orders", [])
    idx = int(cb.data.replace("connection_next_", "")) + 1
    if idx < 0 or idx >= len(items):
        return
    await state.update_data(idx=idx)
    text = connection_order_text(items[idx])
    kb = nav_keyboard(idx, len(items), "connection")
    await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("technician_prev_"))
async def prev_technician_order(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    items = data.get("technician_orders", [])
    idx = int(cb.data.replace("technician_prev_", "")) - 1
    if idx < 0 or idx >= len(items):
        return
    await state.update_data(idx=idx)
    text = technician_order_text(items[idx])
    kb = nav_keyboard(idx, len(items), "technician")
    await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("technician_next_"))
async def next_technician_order(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    items = data.get("technician_orders", [])
    idx = int(cb.data.replace("technician_next_", "")) + 1
    if idx < 0 or idx >= len(items):
        return
    await state.update_data(idx=idx)
    text = technician_order_text(items[idx])
    kb = nav_keyboard(idx, len(items), "technician")
    await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("saff_prev_"))
async def prev_saff_order(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    items = data.get("saff_orders", [])
    idx = int(cb.data.replace("saff_prev_", "")) - 1
    if idx < 0 or idx >= len(items):
        return
    await state.update_data(idx=idx)
    text = saff_order_text(items[idx])
    kb = nav_keyboard(idx, len(items), "saff")
    await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("saff_next_"))
async def next_saff_order(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    items = data.get("saff_orders", [])
    idx = int(cb.data.replace("saff_next_", "")) + 1
    if idx < 0 or idx >= len(items):
        return
    await state.update_data(idx=idx)
    text = saff_order_text(items[idx])
    kb = nav_keyboard(idx, len(items), "saff")
    await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

# Orqaga qaytish
@router.callback_query(F.data == "orders_back_to_menu")
async def back_to_orders_menu(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await cb.message.edit_text(
        "📝 <b>Zayavkalar bo'limi</b>\n\n"
        "Quyidagi tugmalardan birini tanlang:",
        parse_mode='HTML',
        reply_markup=get_applications_main_menu()
    )

# Orqaga (asosiy menyuga)
@router.message(F.text.in_(["◀️ Orqaga", "◀️ Назад"]))
async def back_to_main_menu(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user or user.get("role") != "admin":
        return
    
    await message.answer(
        "🏠 <b>Admin Panel</b>\n\n"
        "Asosiy menyuga qaytdingiz.",
        parse_mode='HTML',
        reply_markup=get_admin_main_menu()
    )