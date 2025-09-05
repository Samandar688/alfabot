from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from datetime import datetime
import html 
from database.manager_inbox import (
    get_user_by_telegram_id,
    get_users_by_role,
    fetch_manager_inbox,
    assign_to_junior_manager,
)
from filters.role_filter import RoleFilter


router = Router()

router.message.filter(RoleFilter("manager"))  # 🔒 faqat JM uchun

def fmt_dt(dt: datetime) -> str:
    return dt.strftime("%d.%m.%Y %H:%M")

def esc(v) -> str:

    if v is None:
        return "-"
    return html.escape(str(v), quote=False)

def short_view_text(item: dict) -> str:
    full_id = str(item["id"])
    parts = full_id.split("_")
    short_id = full_id
    if len(parts) >= 2:
        short_id = f"{parts[0]}-{parts[1]}"

    created = item["created_at"]
    created_dt = datetime.fromisoformat(created) if isinstance(created, str) else created

    # ⬇️ Escape ALL dynamic fields
    tariff = esc(item.get('tariff', '-'))
    client_name = esc(item.get('client_name', '-'))
    client_phone = esc(item.get('client_phone', '-'))
    address = esc(item.get('address', '-'))
    short_id_safe = esc(short_id)

    return (
        "🔌 <b>Manager Inbox</b>\n"
        f"🆔 <b>ID:</b> {short_id_safe}\n"
        f"📊 <b>Tarif:</b> {tariff}\n"
        f"👤 <b>Mijoz:</b> {client_name}\n"
        f"📞 <b>Telefon:</b> {client_phone}\n"
        f"📍 <b>Manzil:</b> {address}\n"
        f"📅 <b>Yaratilgan:</b> {fmt_dt(created_dt)}"
    )

def nav_keyboard(index: int, total: int, current_id: str) -> InlineKeyboardMarkup:
    rows = []
    if index > 0:
        rows.append([InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"mgr_inbox_prev_{index}")])
    row2 = [InlineKeyboardButton(text="📨 Kichik menejerga yuborish", callback_data=f"mgr_inbox_assign_{current_id}")]
    if index < total - 1:
        row2.append(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"mgr_inbox_next_{index}"))
    rows.append(row2)
    return InlineKeyboardMarkup(inline_keyboard=rows)

def jm_list_keyboard(full_id: str, juniors: list) -> InlineKeyboardMarkup:
    rows = []
    for jm in juniors:
        rows.append([InlineKeyboardButton(text=f"👤 {jm['full_name']}", callback_data=f"mgr_inbox_pick_{full_id}_{jm['id']}")])
    rows.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"mgr_inbox_back_{full_id}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

@router.message(F.text.in_(["📥 Inbox", "Inbox"]))
async def open_inbox(message: Message, state: FSMContext):
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user or user.get("role") not in ("manager", "controller"):
        return

    items = await fetch_manager_inbox(limit=50, offset=0)
    if not items:
        await message.answer("📭 Inbox bo'sh")
        return

    await state.update_data(inbox=items, idx=0)
    text = short_view_text(items[0])
    kb = nav_keyboard(0, len(items), str(items[0]["id"]))
    await message.answer(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("mgr_inbox_prev_"))
async def prev_item(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    items = data.get("inbox", [])
    idx = int(cb.data.replace("mgr_inbox_prev_", "")) - 1
    if idx < 0 or idx >= len(items):
        return
    await state.update_data(idx=idx)
    text = short_view_text(items[idx])
    kb = nav_keyboard(idx, len(items), str(items[idx]["id"]))
    await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("mgr_inbox_next_"))
async def next_item(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    items = data.get("inbox", [])
    idx = int(cb.data.replace("mgr_inbox_next_", "")) + 1
    if idx < 0 or idx >= len(items):
        return
    await state.update_data(idx=idx)
    text = short_view_text(items[idx])
    kb = nav_keyboard(idx, len(items), str(items[idx]["id"]))
    await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("mgr_inbox_assign_"))
async def assign_open(cb: CallbackQuery, state: FSMContext):
    print("mgr_inbox_assign_ callback ishladi:", cb.data)
    await cb.answer()
    full_id = cb.data.replace("mgr_inbox_assign_", "")
    juniors = await get_users_by_role("junior_manager")
    if not juniors:
        await cb.message.edit_text("Kichik menejerlar topilmadi ❗")
        return
    text = f"👨‍💼 <b>Kichik menejer tanlang</b>\n🆔 {esc(full_id)}"  # ⬅️ escape
    kb = jm_list_keyboard(full_id, juniors)
    await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("mgr_inbox_back_"))
async def assign_back(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    items = data.get("inbox", [])
    idx = data.get("idx", 0)
    if not items:
        await cb.message.edit_text("📭 Inbox bo'sh")
        return
    text = short_view_text(items[idx])
    kb = nav_keyboard(idx, len(items), str(items[idx]["id"]))
    await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("mgr_inbox_pick_"))
async def assign_pick(cb: CallbackQuery, state: FSMContext):
    print("mgr_inbox_pick_ callback:", cb.data)
    # Split the callback data by underscores
    parts = cb.data.split("_")
    print("Parts:", parts)
    
    # The format is: mgr_inbox_pick_[request_id]_[jm_id]
    # So we need at least 4 parts: ['mgr', 'inbox', 'pick', request_id, jm_id]
    if len(parts) < 5:
        await cb.answer("❌ Noto'g'ri format", show_alert=True)
        return
    
    # The request_id is the 4th part (index 3)
    full_id = parts[3]
    # The jm_id is the 5th part (index 4) and onwards (in case there are more parts)
    jm_id = "_".join(parts[4:])
    
    try:
        jm_id = int(jm_id)
    except ValueError:
        await cb.answer("❌ Noto'g'ri kichik menejer ID raqami", show_alert=True)
        return

    user = await get_user_by_telegram_id(cb.from_user.id)
    if not user:
        await cb.answer("❌ Foydalanuvchi topilmadi", show_alert=True)
        return

    juniors = await get_users_by_role("junior_manager")
    selected_jm = next((jm for jm in juniors if jm["id"] == jm_id), None)
    if not selected_jm:
        await cb.answer("❌ Kichik menejer topilmadi", show_alert=True)
        return

    try:
        # Convert full_id to int (it might be in format like "2_9")
        # Xavfsiz usulda request_id ni ajratib olish
        parts = full_id.split("_")
        request_id = int(parts[0]) if parts else int(full_id)
        
        await assign_to_junior_manager(
            request_id=request_id,
            jm_id=jm_id,
            actor_id=user["id"]
        )
    except Exception as e:
        error_msg = str(e)
        print(f"Error in assign_to_junior_manager: {error_msg}")
        await cb.answer(f"❌ Xatolik yuz berdi: {error_msg}", show_alert=True)
        return

    # Xavfsiz usulda short_id yaratish
    parts = full_id.split('_')
    short_id = full_id
    if len(parts) >= 2:
        short_id = f"{parts[0]}-{parts[1]}"

    confirmation_text = (
        f"✅ <b>Ariza muvaffaqiyatli yuborildi!</b>\n\n"
        f"🆔 <b>Ariza ID:</b> {esc(short_id)}\n"
        f"👤 <b>Kichik menejer:</b> {esc(selected_jm['full_name'])}\n"
        f"📅 <b>Yuborilgan vaqt:</b> {esc(fmt_dt(datetime.now()))}\n"
        f"👨‍💼 <b>Yuboruvchi:</b> {esc(user.get('full_name', 'Manager'))}"
    )
    await cb.message.edit_text(confirmation_text, parse_mode="HTML")

    # Remove the assigned item from the inbox
    data = await state.get_data()
    items = data.get("inbox", [])
    items = [it for it in items if str(it["id"]) != full_id]
    await state.update_data(inbox=items)
