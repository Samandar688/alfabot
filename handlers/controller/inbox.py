from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from datetime import datetime
import html
from database.controller_inbox import (
    get_user_by_telegram_id,
    get_users_by_role,
    fetch_controller_inbox,
    assign_to_technician,
)
from filters.role_filter import RoleFilter


router = Router()

router.message.filter(RoleFilter("controller"))

def fmt_dt(dt: datetime) -> str:
    return dt.strftime("%d.%m.%Y %H:%M")

def esc(v) -> str:
    if v is None:
        return "-"
    return html.escape(str(v), quote=False)

def short_view_text(item: dict, idx: int | None = None, total: int | None = None) -> str:
    full_id = str(item["id"])
    parts = full_id.split("_")
    short_id = full_id if len(parts) < 2 else f"{parts[0]}-{parts[1]}"

    created = item["created_at"]
    created_dt = datetime.fromisoformat(created) if isinstance(created, str) else created
    tariff = esc(item.get('tariff', '-'))
    client_name = esc(item.get('client_name', '-'))
    client_phone = esc(item.get('client_phone', '-'))
    address = esc(item.get('address', '-'))
    short_id_safe = esc(short_id)

    base = (
        "🎛️ <b>Controller Inbox</b>\n"
        f"🆔 <b>ID:</b> {short_id_safe}\n"
        f"📊 <b>Tarif:</b> {tariff}\n"
        f"👤 <b>Mijoz:</b> {client_name}\n"
        f"📞 <b>Telefon:</b> {client_phone}\n"
        f"📍 <b>Manzil:</b> {address}\n"
        f"📅 <b>Yaratilgan:</b> {fmt_dt(created_dt)}"
    )

    # Ko‘rsatkich: “Ariza i / N”
    if idx is not None and total is not None and total > 0:
        base += f"\n\n🗂️ <i>Ariza {idx + 1} / {total}</i>"

    return base

def nav_keyboard(index: int, total: int, current_id: str) -> InlineKeyboardMarkup:
    rows = []
    if index > 0:
        rows.append([InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"ctrl_inbox_prev_{index}")])
    row2 = [InlineKeyboardButton(text="🔧 Texnikga yuborish", callback_data=f"ctrl_inbox_assign_{current_id}")]
    if index < total - 1:
        row2.append(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"ctrl_inbox_next_{index}"))
    rows.append(row2)
    return InlineKeyboardMarkup(inline_keyboard=rows)

def tech_list_keyboard(full_id: str, technicians: list) -> InlineKeyboardMarkup:
    rows = []
    for tech in technicians:
        rows.append([InlineKeyboardButton(text=f"🔧 {tech['full_name']}", callback_data=f"ctrl_inbox_pick_{full_id}_{tech['id']}")])
    rows.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"ctrl_inbox_back_{full_id}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

@router.message(F.text.in_(["📥 Inbox", "Inbox"]))
async def open_inbox(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user or user.get("role") != "controller":
        return

    items = await fetch_controller_inbox(limit=50, offset=0)
    if not items:
        await message.answer("📭 Inbox bo'sh")
        return

    await state.update_data(inbox=items, idx=0)
    text = short_view_text(items[0], idx=0, total=len(items))   # ⬅️ yangilandi
    kb = nav_keyboard(0, len(items), str(items[0]["id"]))
    await message.answer(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("ctrl_inbox_prev_"))
async def prev_item(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    items = data.get("inbox", [])
    idx = int(cb.data.replace("ctrl_inbox_prev_", "")) - 1
    if idx < 0 or idx >= len(items):
        return
    await state.update_data(idx=idx)
    text = short_view_text(items[idx], idx=idx, total=len(items))   # ⬅️ yangilandi
    kb = nav_keyboard(idx, len(items), str(items[idx]["id"]))
    await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("ctrl_inbox_next_"))
async def next_item(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    items = data.get("inbox", [])
    idx = int(cb.data.replace("ctrl_inbox_next_", "")) + 1
    if idx < 0 or idx >= len(items):
        return
    await state.update_data(idx=idx)
    text = short_view_text(items[idx], idx=idx, total=len(items))   # ⬅️ yangilandi
    kb = nav_keyboard(idx, len(items), str(items[idx]["id"]))
    await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("ctrl_inbox_assign_"))
async def assign_open(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    full_id = cb.data.replace("ctrl_inbox_assign_", "")
    technicians = await get_users_by_role("technician")
    if not technicians:
        await cb.message.edit_text("Texniklar topilmadi ❗")
        return
    text = f"🔧 <b>Texnik tanlang</b>\n🆔 {esc(full_id)}"
    kb = tech_list_keyboard(full_id, technicians)
    await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("ctrl_inbox_back_"))
async def assign_back(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    items = data.get("inbox", [])
    idx = data.get("idx", 0)
    if not items:
        await cb.message.edit_text("📭 Inbox bo'sh")
        return
    text = short_view_text(items[idx], idx=idx, total=len(items))   # ⬅️ yangilandi
    kb = nav_keyboard(idx, len(items), str(items[idx]["id"]))
    await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("ctrl_inbox_pick_"))
async def assign_pick(cb: CallbackQuery, state: FSMContext):
    try:
        raw = cb.data.replace("ctrl_inbox_pick_", "")
        full_id, tech_id_str = raw.rsplit("_", 1)   # oxirgi '_' bo‘yicha bo‘linadi
        tech_id = int(tech_id_str)
    except ValueError:
        await cb.answer("❌ Noto'g'ri callback format", show_alert=True)
        return

    user = await get_user_by_telegram_id(cb.from_user.id)
    if not user:
        await cb.answer("❌ Foydalanuvchi topilmadi", show_alert=True)
        return

    technicians = await get_users_by_role("technician")
    selected_tech = next((tech for tech in technicians if tech["id"] == tech_id), None)
    if not selected_tech:
        await cb.answer("❌ Texnik topilmadi", show_alert=True)
        return

    try:
        parts = full_id.split("_")
        request_id = int(parts[0]) if parts else int(full_id)
        
        await assign_to_technician(
            request_id=request_id,
            tech_id=tech_id,
            actor_id=user["id"]
        )
    except Exception as e:
        error_msg = str(e)
        await cb.answer(f"❌ Xatolik yuz berdi: {error_msg}", show_alert=True)
        return

    parts = full_id.split('_')
    short_id = full_id
    if len(parts) >= 2:
        short_id = f"{parts[0]}-{parts[1]}"

    confirmation_text = (
        f"✅ <b>Ariza muvaffaqiyatli yuborildi!</b>\n\n"
        f"🆔 <b>Ariza ID:</b> {esc(short_id)}\n"
        f"🔧 <b>Texnik:</b> {esc(selected_tech['full_name'])}\n"
        f"📅 <b>Yuborilgan vaqt:</b> {esc(fmt_dt(datetime.now()))}\n"
        f"🎛️ <b>Yuboruvchi:</b> {esc(user.get('full_name', 'Controller'))}"
    )
    await cb.message.edit_text(confirmation_text, parse_mode="HTML")

    # Remove the assigned item from the inbox
    data = await state.get_data()
    items = data.get("inbox", [])
    items = [it for it in items if str(it["id"]) != full_id]
    await state.update_data(inbox=items)
