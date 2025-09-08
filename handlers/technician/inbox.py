# handlers/technician/inbox.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import datetime
import html

from filters.role_filter import RoleFilter
from database.queries import find_user_by_telegram_id
from database.technician_queries import fetch_technician_inbox
# TODO: implement this in your DB layer:
# from database.technician_queries import accept_technician_work

router = Router()
router.message.filter(RoleFilter("technician"))
router.callback_query.filter(RoleFilter("technician"))  # <— callbacks ham texnik uchun

# ---------- yordamchi ----------
def fmt_dt(dt) -> str:
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except Exception:
            return html.escape(dt, quote=False)
    return dt.strftime("%d.%m.%Y %H:%M")

def esc(v) -> str:
    return "-" if v is None else html.escape(str(v), quote=False)

def status_emoji(s: str) -> str:
    m = {
        "in_technician": "🆕",
        "tech_in_progress": "🟢",
        "returned_to_technician": "↩️",
        "waiting_warehouse": "⏳",
        "closed_by_technician": "✅",
        "closed_by_warehouse": "🔒",
    }
    return m.get(s, "📌")

def short_view_text(item: dict, idx: int, total: int) -> str:
    return (
        "👨‍🔧 <b>Texnik — Inbox</b>\n"
        f"🆔 <b>ID:</b> {esc(item.get('id'))}\n"
        f"{status_emoji(item.get('status',''))} <b>Status:</b> {esc(item.get('status'))}\n"
        f"👤 <b>Mijoz:</b> {esc(item.get('client_name'))}\n"
        f"📞 <b>Telefon:</b> {esc(item.get('client_phone'))}\n"
        f"📍 <b>Manzil:</b> {esc(item.get('address'))}\n"
        f"📊 <b>Tarif:</b> {esc(item.get('tariff'))}\n"
        f"📅 <b>Yaratilgan:</b> {fmt_dt(item.get('created_at'))}\n\n"
        f"🗂️ <i>Ariza {idx + 1} / {total}</i>"
    )

def action_keyboard(item_id: int, index: int, total: int) -> InlineKeyboardMarkup:
    rows = []
    # 1) Navigatsiya (faqat 2+ bo'lsa)
    if total > 1:
        nav = []
        if index > 0:
            nav.append(InlineKeyboardButton(text="⬅️ Oldingi",
                                            callback_data=f"tech_inbox_prev_{index}"))
        if index < total - 1:
            nav.append(InlineKeyboardButton(text="Keyingi ➡️",
                                            callback_data=f"tech_inbox_next_{index}"))
        if nav:
            rows.append(nav)
    # 2) Ishni qabul qilish
    rows.append([
        InlineKeyboardButton(text="✅ Ishni qabul qilish",
                             callback_data=f"tech_accept_{item_id}")
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)

# ---------- open inbox ----------
@router.message(F.text.in_(["📥 Inbox", "Inbox"]))
async def tech_open_inbox(message: Message, state: FSMContext):
    user = await find_user_by_telegram_id(message.from_user.id)
    if not user or user.get("role") != "technician":
        return

    tech_id = user["id"]
    items = await fetch_technician_inbox(technician_id=tech_id, limit=50, offset=0)

    if not items:
        await message.answer("📭 Inbox bo‘sh")
        return

    total = len(items)
    await state.update_data(tech_inbox=items, tech_idx=0)

    text = short_view_text(items[0], 0, total)
    kb = action_keyboard(items[0].get("id"), 0, total)
    await message.answer(text, reply_markup=kb, parse_mode="HTML")

# ---------- prev ----------
@router.callback_query(F.data.startswith("tech_inbox_prev_"))
async def tech_prev(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    items = data.get("tech_inbox", [])
    if not items:
        return
    total = len(items)
    idx = int(cb.data.replace("tech_inbox_prev_", "")) - 1
    if idx < 0 or idx >= total:
        return

    await state.update_data(tech_idx=idx)
    item = items[idx]
    text = short_view_text(item, idx, total)
    kb = action_keyboard(item.get("id"), idx, total)
    await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

# ---------- next ----------
@router.callback_query(F.data.startswith("tech_inbox_next_"))
async def tech_next(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    items = data.get("tech_inbox", [])
    if not items:
        return
    total = len(items)
    idx = int(cb.data.replace("tech_inbox_next_", "")) + 1
    if idx < 0 or idx >= total:
        return

    await state.update_data(tech_idx=idx)
    item = items[idx]
    text = short_view_text(item, idx, total)
    kb = action_keyboard(item.get("id"), idx, total)
    await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

# ---------- accept work ----------
@router.callback_query(F.data.startswith("tech_accept_"))
async def tech_accept(cb: CallbackQuery, state: FSMContext):
    user = await find_user_by_telegram_id(cb.from_user.id)
    if not user or user.get("role") != "technician":
        return await cb.answer("❌ Ruxsat yo‘q", show_alert=True)

    req_id = int(cb.data.replace("tech_accept_", ""))

    try:
        # --- DB ga yozish (o'zingizda implement qiling):
        # await accept_technician_work(request_id=req_id, technician_id=user["id"])
        # Masalan: status = 'tech_in_progress', accepted_at = NOW() ...
        pass
    except Exception as e:
        return await cb.answer(f"❌ Xatolik: {e}", show_alert=True)

    # Lokal state’dagi elementni yangilab qo’yamiz (UI tez yangilansin)
    data = await state.get_data()
    items = data.get("tech_inbox", [])
    idx = data.get("tech_idx", 0)
    for it in items:
        if it.get("id") == req_id:
            it["status"] = "tech_in_progress"  # vizual yangilanish
            break
    await state.update_data(tech_inbox=items)

    total = len(items)
    item = items[idx] if items else None
    if not item:
        return await cb.message.edit_text("📭 Inbox bo‘sh", parse_mode="HTML")

    await cb.answer("✅ Ish qabul qilindi")
    text = short_view_text(item, idx, total)
    kb = action_keyboard(item.get("id"), idx, total)
    await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
