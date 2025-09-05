from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import List, Dict, Any
from datetime import datetime

from filters.role_filter import RoleFilter
from database.jm_inbox_queries import (
    db_get_user_by_telegram_id,
    db_get_jm_inbox_items,
    db_move_order_to_controller,
)
from keyboards.junior_manager_buttons import get_junior_manager_main_menu

router = Router()
router.message.filter(RoleFilter("junior_manager"))
router.callback_query.filter(RoleFilter("junior_manager"))

@router.message(F.text == "📥 Inbox")
async def handle_inbox(msg: Message, state: FSMContext):
    user = await db_get_user_by_telegram_id(msg.from_user.id)
    if not user:
        return await msg.answer("❌ Foydalanuvchi topilmadi.")
    if user.get("is_blocked"):
        return await msg.answer("🚫 Profil bloklangan.")

    lang = user.get("language", "uz")
    items = await db_get_jm_inbox_items(recipient_id=user["id"], limit=50)

    if not items:
        return await msg.answer("📭 Inbox bo‘sh.", reply_markup=get_junior_manager_main_menu(lang))

    await state.update_data(items=items, idx=0, lang=lang)
    await _render_card(target=msg, items=items, idx=0, lang=lang)

def _fmt_dt(dt) -> str:
    if isinstance(dt, datetime):
        return dt.strftime("%d.%m.%Y %H:%M")
    return (str(dt)[:16]) if dt else "—"

async def _render_card(target: Message | CallbackQuery, items: List[Dict[str, Any]], idx: int, lang: str):
    total = len(items)
    it = items[idx]

    conn_id        = it.get("connection_id")          # = order_id
    order_created  = _fmt_dt(it.get("order_created_at"))
    client_name    = it.get("client_full_name") or "—"
    client_phone   = it.get("client_phone") or "—"
    region         = it.get("order_region") or "—"
    address        = it.get("order_address") or "—"

    if lang == "uz":
        text = (
            "🛠 <b>Ulanish arizasi — To‘liq ma'lumot</b>\n\n"
            f"🆔 <b>Ariza ID:</b> {conn_id or '—'}\n"
            f"📅 <b>Sana:</b> {order_created}\n"
            f"👤 <b>Mijoz:</b> {client_name}\n"
            f"📞 <b>Telefon:</b> {client_phone}\n"
            f"🏙 <b>Hudud:</b> {region}\n"
            f"📍 <b>Manzil:</b> {address}\n\n"
            f"📄 <i>Ariza #{idx+1} / {total}</i>"
        )
    else:
        text = (
            "🛠 <b>Заявка на подключение — Полные данные</b>\n\n"
            f"🆔 <b>ID:</b> {conn_id or '—'}\n"
            f"📅 <b>Дата:</b> {order_created}\n"
            f"👤 <b>Клиент:</b> {client_name}\n"
            f"📞 <b>Телефон:</b> {client_phone}\n"
            f"🏙 <b>Регион:</b> {region}\n"
            f"📍 <b>Адрес:</b> {address}\n\n"
            f"📄 <i>Заявка #{idx+1} / {total}</i>"
        )

    kb = _kb(idx, total, conn_id=conn_id, lang=lang)

    if isinstance(target, Message):
        await target.answer(text, reply_markup=kb, parse_mode="HTML")
    else:
        await target.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

def _kb(idx: int, total: int, conn_id: int | None, lang: str) -> InlineKeyboardMarkup:
    rows: List[List[InlineKeyboardButton]] = []

    if total > 1:
        nav: List[InlineKeyboardButton] = []
        if idx > 0:
            nav.append(InlineKeyboardButton(text=("⬅️ Oldingi" if lang=="uz" else "⬅️ Предыдущий"),
                                            callback_data="jm_conn_prev"))
        if idx < total - 1:
            nav.append(InlineKeyboardButton(text=("Keyingi ➡️" if lang=="uz" else "Следующий ➡️"),
                                            callback_data="jm_conn_next"))
        if nav: rows.append(nav)

    rows.append([
        InlineKeyboardButton(text=("📞 Mijoz bilan bog'lanish" if lang=="uz" else "📞 Связаться с клиентом"),
                             callback_data=f"jm_contact_client:{conn_id}"),
        InlineKeyboardButton(text=("📤 Controller'ga yuborish" if lang=="uz" else "📤 Отправить контроллеру"),
                             callback_data=f"jm_send_to_controller:{conn_id}"),
    ])

    return InlineKeyboardMarkup(inline_keyboard=rows)

@router.callback_query(F.data == "jm_conn_prev")
async def jm_conn_prev(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    items = data.get("items", [])
    lang  = data.get("lang", "uz")
    idx   = max(0, (data.get("idx") or 0) - 1)
    await state.update_data(idx=idx)
    await _render_card(target=cb, items=items, idx=idx, lang=lang)

@router.callback_query(F.data == "jm_conn_next")
async def jm_conn_next(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    items = data.get("items", [])
    lang  = data.get("lang", "uz")
    idx   = data.get("idx") or 0
    if idx < len(items) - 1:
        idx += 1
    await state.update_data(idx=idx)
    await _render_card(target=cb, items=items, idx=idx, lang=lang)

# 📤 Controller'ga yuborish
@router.callback_query(F.data.startswith("jm_send_to_controller:"))
async def jm_send_to_controller(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    order_id = int(cb.data.split(":")[1])  # = connection_id (order_id)

    ok = await db_move_order_to_controller(order_id)
    if not ok:
        return await cb.answer("❌ Yuborishning iloji yo‘q (status mos emas).", show_alert=True)

    # Ro'yxatdan olib tashlaymiz va sahifani yangilaymiz
    data  = await state.get_data()
    items = data.get("items", [])
    lang  = data.get("lang", "uz")
    idx   = data.get("idx", 0)

    items = [x for x in items if x.get("connection_id") != order_id]

    if not items:
        await state.clear()
        return await cb.message.edit_text("✅ Controller’ga yuborildi.\n\n📭 Inbox bo‘sh.")

    if idx >= len(items):
        idx = len(items) - 1

    await state.update_data(items=items, idx=idx)
    await cb.message.answer("✅ Controller’ga yuborildi.")
    await _render_card(target=cb, items=items, idx=idx, lang=lang)
