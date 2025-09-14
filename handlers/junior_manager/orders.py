# handlers/junior_manager/orders.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import json

from filters.role_filter import RoleFilter
from database.junior_manager_orders_queries import (
    list_new_for_jm,
    list_inprogress_for_jm,
    list_completed_for_jm,
)

router = Router()
router.message.filter(RoleFilter("junior_manager"))
router.callback_query.filter(RoleFilter("junior_manager"))

# --- Labels ---
LBL_MENU = "📋 Arizalarni ko‘rish"
LBL_NEW = "🆕 Yangi buyurtmalar"
LBL_WIP = "⏳ Jarayondagilar"
LBL_DONE = "✅ Tugatilganlari"
LBL_BACK = "🔙 Orqaga"
LBL_PREV = "⬅️ Oldingi"
LBL_NEXT = "➡️ Keyingi"

# Agar sizdagi text tugma "Arizalarni ko'rish" bo‘lsa – shuni moslang:
ENTRY_TEXTS = [LBL_MENU, "📋 Arizalarni ko'rish", "Arizalarni ko‘rish"]

def _tz():
    try:
        return ZoneInfo("Asia/Tashkent")
    except Exception:
        return timezone(timedelta(hours=5))

def _ago(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    delta = datetime.now(timezone.utc) - dt
    s = int(delta.total_seconds())
    d, r = divmod(s, 86400)
    h, r = divmod(r, 3600)
    m, _ = divmod(r, 60)
    if d: return f"{d} kun oldin"
    if h: return f"{h} soat oldin"
    if m: return f"{m} daqiqa oldin"
    return "hozirgina"

def _kb_root() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=LBL_NEW, callback_data="jm_list:new")
    kb.button(text=LBL_WIP, callback_data="jm_list:wip")
    kb.button(text=LBL_DONE, callback_data="jm_list:done")
    kb.adjust(1)
    return kb.as_markup()

def _kb_pager(idx: int, total: int, kind: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=LBL_PREV, callback_data=f"jm_nav:{kind}:prev")
    kb.button(text=f"{idx+1}/{total}", callback_data="noop")
    kb.button(text=LBL_NEXT, callback_data=f"jm_nav:{kind}:next")
    kb.row()
    kb.button(text=LBL_BACK, callback_data="jm_back")
    return kb.as_markup()

def _safe_kb_fp(kb) -> str:
    if kb is None: return "NONE"
    try:
        data = kb.model_dump(by_alias=True, exclude_none=True)
        return json.dumps(data, sort_keys=True, ensure_ascii=False)
    except Exception:
        return str(kb)

async def _safe_edit(cb: CallbackQuery, text: str, kb: InlineKeyboardMarkup | None):
    msg = cb.message
    cur_text = msg.html_text or msg.text or ""
    if cur_text == text and _safe_kb_fp(msg.reply_markup) == _safe_kb_fp(kb):
        await cb.answer("Yangilanish yo‘q ✅", show_alert=False)
        return
    try:
        await msg.edit_text(text, reply_markup=kb)
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            await cb.answer("Yangilanish yo‘q ✅", show_alert=False)
        else:
            raise

def _fmt_card(item: dict, kind: str) -> str:
    """
    item: {
      id, created_at, status_text, address, user_name, flow_status?
    }
    """
    rid = item.get("id")
    fio = item.get("user_name") or "—"
    addr = item.get("address") or "—"
    created_at = item.get("created_at")
    when = _ago(created_at) if created_at else "—"

    # Status ko‘rsatish
    if kind == "wip":
        status_line = item.get("flow_status") or item.get("status_text") or "—"
    elif kind == "done":
        status_line = "completed"
    else:
        status_line = item.get("status_text") or "—"

    title = {
        "new": "🆕 <b>Yangi buyurtma</b>",
        "wip": "⏳ <b>Jarayonda</b>",
        "done": "✅ <b>Tugatilgan</b>",
    }[kind]

    return (
        f"{title}\n"
        f"<b>#{rid:03d}</b>\n"
        f"👤 {fio}\n"
        f"📦 connection\n"
        f"📊 <code>{status_line}</code>\n"
        f"📍 {addr}\n"
        f"⏱ {when}"
    )

# --- Entry ---
@router.message(F.text.in_(ENTRY_TEXTS))
async def jm_orders_menu(msg: Message):
    await msg.answer("📋 <b>Arizalarni ko‘rish</b>\nQuyidan bo‘limni tanlang:", reply_markup=_kb_root())

# --- Open list ---
@router.callback_query(F.data.startswith("jm_list:"))
async def jm_open_list(cb: CallbackQuery, state: FSMContext):
    kind = cb.data.split(":")[1]  # new | wip | done
    tg_id = cb.from_user.id
    if kind == "new":
        items = await list_new_for_jm(tg_id)
    elif kind == "wip":
        items = await list_inprogress_for_jm(tg_id)
    else:
        items = await list_completed_for_jm(tg_id)

    if not items:
        await _safe_edit(cb, "Hech narsa topilmadi.", _kb_root())
        return

    await state.update_data(jm_items=items, jm_idx=0, jm_kind=kind)
    text = _fmt_card(items[0], kind)
    await _safe_edit(cb, text, _kb_pager(0, len(items), kind))

# --- Navigation ---
@router.callback_query(F.data.startswith("jm_nav:"))
async def jm_nav(cb: CallbackQuery, state: FSMContext):
    _, kind, direction = cb.data.split(":")
    data = await state.get_data()
    items = data.get("jm_items") or []
    if not items:
        await cb.answer("Bo‘sh.", show_alert=False); return
    idx = int(data.get("jm_idx", 0))
    if direction == "prev":
        idx = (idx - 1) % len(items)
    else:
        idx = (idx + 1) % len(items)
    await state.update_data(jm_idx=idx, jm_kind=kind)
    await _safe_edit(cb, _fmt_card(items[idx], kind), _kb_pager(idx, len(items), kind))

@router.callback_query(F.data == "jm_back")
async def jm_back(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await _safe_edit(cb, "📋 <b>Arizalarni ko‘rish</b>\nQuyidan bo‘limni tanlang:", _kb_root())

@router.callback_query(F.data == "noop")
async def noop(cb: CallbackQuery):
    await cb.answer()
