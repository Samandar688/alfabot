from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from datetime import datetime
import html
from database.smart_service_queries import (
    get_user_by_telegram_id,
    fetch_smart_service_orders,
    
)
from filters.role_filter import RoleFilter
from keyboards.manager_buttons import get_manager_main_menu

router = Router()

router.message.filter(RoleFilter("manager")) 

def fmt_dt(dt: datetime) -> str:
    return dt.strftime("%d.%m.%Y %H:%M")

def esc(v) -> str:
    if v is None:
        return "-"
    return html.escape(str(v), quote=False)

# Kategoriya nomlarini mapping - global o'zgaruvchi
CATEGORY_NAMES = {
    "aqlli_avtomatlashtirilgan_xizmatlar": "🏠 Aqlli uy va avtomatlashtirilgan xizmatlar",
    "xavfsizlik_kuzatuv_tizimlari": "🔒 Xavfsizlik va kuzatuv tizimlari",
    "internet_tarmoq_xizmatlari": "🌐 Internet va tarmoq xizmatlari",
    "energiya_yashil_texnologiyalar": "⚡ Energiya va yashil texnologiyalar",
    "multimediya_aloqa_tizimlari": "📺 Multimediya va aloqa tizimlari",
    "maxsus_qoshimcha_xizmatlar": "🔧 Maxsus va qo'shimcha xizmatlar"
}

def short_view_text(item: dict) -> str:
    
    order_id = item['id']
    category_name = CATEGORY_NAMES.get(item['category'], item['category'].replace('_', ' ').title())
    service_name = item['service_type'].replace('_', ' ').title()
    
    created = item["created_at"]
    created_dt = datetime.fromisoformat(created) if isinstance(created, str) else created
    
    # Escape ALL dynamic fields
    full_name = esc(item.get('full_name', '-'))
    phone = esc(item.get('phone', '-'))
    username = esc(item.get('username', ''))
    address = esc(item.get('address', '-'))
    category_safe = esc(category_name)
    service_safe = esc(service_name)
    
    username_text = f"\n👤 Username: @{username}" if username else ""
    location_text = ""
    if item.get('latitude') and item.get('longitude'):
        lat = item['latitude']
        lon = item['longitude']
        location_text = f"\n📍 GPS: https://maps.google.com/?q={lat},{lon}"
    
    
    return (
        "🎯 <b>SMART SERVICE ARIZALARI</b>\n\n"
        f"📋 <b>Buyurtma:</b> #{esc(order_id)}\n"
        f"🏷️ <b>Kategoriya:</b> {category_safe}\n"
        f"🔧 <b>Xizmat:</b> {service_safe}\n"
        f"👤 <b>Mijoz:</b> {full_name}\n"
        f"📞 <b>Telefon:</b> {phone}{username_text}\n"
        f"📍 <b>Manzil:</b> {address}{location_text}\n"
        f"📅 <b>Sana:</b> {fmt_dt(created_dt)}"
    )

def nav_keyboard(index: int, total: int, current_id: str) -> InlineKeyboardMarkup:
    rows = []
    nav_row = []
    
    if index > 0:
        nav_row.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"smart_prev_{index}"))
    
    if index < total - 1:
        nav_row.append(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"smart_next_{index}"))
    
    if nav_row:
        rows.append(nav_row)
    
    return InlineKeyboardMarkup(inline_keyboard=rows)

@router.message(F.text.in_(["🛜 SmartService arizalari", "🛜 SmartService заявки"]))
async def open_smart_service_orders(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user or user.get("role") != "manager":
        return
    
    items = await fetch_smart_service_orders(limit=50, offset=0)
    if not items:
        await message.answer(
            "🛜 <b>SmartService Arizalari</b>\n\n"
            "Hozircha arizalar yo'q.",
            parse_mode='HTML',
            reply_markup=get_manager_main_menu()
        )
        return
    
    await state.update_data(smart_orders=items, idx=0)
    text = short_view_text(items[0])
    kb = nav_keyboard(0, len(items), str(items[0]["id"]))
    await message.answer(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("smart_prev_"))
async def prev_smart_order(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    items = data.get("smart_orders", [])
    idx = int(cb.data.replace("smart_prev_", "")) - 1
    if idx < 0 or idx >= len(items):
        return
    await state.update_data(idx=idx)
    text = short_view_text(items[idx])
    kb = nav_keyboard(idx, len(items), str(items[idx]["id"]))
    await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("smart_next_"))
async def next_smart_order(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    items = data.get("smart_orders", [])
    idx = int(cb.data.replace("smart_next_", "")) + 1
    if idx < 0 or idx >= len(items):
        return
    await state.update_data(idx=idx)
    text = short_view_text(items[idx])
    kb = nav_keyboard(idx, len(items), str(items[idx]["id"]))
    await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")



@router.callback_query(F.data.startswith("smart_back_"))
async def back_to_smart_list(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    items = data.get("smart_orders", [])
    idx = data.get("idx", 0)
    if not items:
        await cb.message.edit_text("📭 Arizalar yo'q")
        return
    text = short_view_text(items[idx])
    kb = nav_keyboard(idx, len(items), str(items[idx]["id"]))
    await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")