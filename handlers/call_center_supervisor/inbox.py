# handlers/call_center_supervisor/inbox.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Optional, Dict, Any
import asyncpg
from config import settings
from filters.role_filter import RoleFilter

# =========================================================
# Router (role: callcenter_supervisor)
# =========================================================
router = Router()
router.message.filter(RoleFilter("callcenter_supervisor"))
router.callback_query.filter(RoleFilter("callcenter_supervisor"))

# =========================================================
# DB helpers (single-file)
# =========================================================
async def _conn():
    return await asyncpg.connect(settings.DB_URL)

async def ccs_count_active() -> int:
    conn = await _conn()
    try:
        row = await conn.fetchrow("""
            SELECT COUNT(*) AS c
            FROM saff_orders
            WHERE status = 'in_call_center_supervisor'
              AND is_active = TRUE
        """)
        return int(row["c"])
    finally:
        await conn.close()

async def ccs_fetch_by_offset(offset: int) -> Optional[Dict[str, Any]]:
    """
    Joins:
      - users u by abonent_id to show full_name (instead of raw user_id)
      - tarif t by tarif_id to show tariff_name
    NOTE: no region_code / tariff_code columns are used here.
    """
    conn = await _conn()
    try:
        row = await conn.fetchrow("""
            SELECT
                so.id,
                so.user_id,                 -- kerak bo'lsa qoldiring
                so.phone,
                so.abonent_id,
                so.region,
                so.address,
                so.tarif_id,
                t.name AS tariff_name,
                so.description,
                so.created_at,

                u.full_name                 -- ✅ users.id orqali full_name

            FROM saff_orders AS so

            -- Tarif nomi
            LEFT JOIN public.tarif AS t
                   ON t.id = so.tarif_id

            -- ✅ users.id = CAST(so.abonent_id AS int)
            -- 1) bo'sh stringlardan qochish uchun NULLIF
            -- 2) agar ichida formatli matn bo'lsa, raqamlarnigina olib cast qilish uchun regexp_replace variantini ham ko'rsatdim (pastda)
            LEFT JOIN public.users AS u
                   ON u.id = NULLIF(so.abonent_id, '')::int

            WHERE so.status = 'in_call_center_supervisor'
              AND so.is_active = TRUE
            ORDER BY so.created_at ASC
            OFFSET $1
            LIMIT 1
        """, offset)
        return dict(row) if row else None
    finally:
        await conn.close()

async def ccs_send_to_control(order_id: int, supervisor_id: Optional[int] = None) -> None:
    conn = await _conn()
    try:
        await conn.execute("""
            UPDATE saff_orders
               SET status = 'in_controller',
                   updated_at = NOW()
             WHERE id = $1
        """, order_id)
        # TODO: optional audit log with supervisor_id
    finally:
        await conn.close()

async def ccs_cancel(order_id: int) -> None:
    conn = await _conn()
    try:
        await conn.execute("""
            UPDATE saff_orders
               SET is_active = FALSE,
                   updated_at = NOW()
             WHERE id = $1
        """, order_id)
    finally:
        await conn.close()

# =========================================================
# Region mapping (id -> human title)
# =========================================================
REGION_CODE_TO_ID = {
    "toshkent_city": 1, "toshkent_region": 2, "andijon": 3, "fergana": 4, "namangan": 5,
    "sirdaryo": 6, "jizzax": 7, "samarkand": 8, "bukhara": 9, "navoi": 10,
    "kashkadarya": 11, "surkhandarya": 12, "khorezm": 13, "karakalpakstan": 14,
}
REGION_TITLES = {
    "toshkent_city": "Toshkent shahri",
    "toshkent_region": "Toshkent viloyati",
    "andijon": "Andijon",
    "fergana": "Farg‘ona",
    "namangan": "Namangan",
    "sirdaryo": "Sirdaryo",
    "jizzax": "Jizzax",
    "samarkand": "Samarqand",
    "bukhara": "Buxoro",
    "navoi": "Navoiy",
    "kashkadarya": "Qashqadaryo",
    "surkhandarya": "Surxondaryo",
    "khorezm": "Xorazm",
    "karakalpakstan": "Qoraqalpog‘iston",
}
ID_TO_REGION_TITLE = {rid: REGION_TITLES[code] for code, rid in REGION_CODE_TO_ID.items()}

def region_title_from_id(rid: Optional[int]) -> str:
    if rid is None:
        return "-"
    try:
        return ID_TO_REGION_TITLE.get(int(rid), str(rid))
    except Exception:
        return str(rid)

# =========================================================
# Tariff name resolver (prefer JOIN result)
# =========================================================
def tariff_name_from_row(row: Dict[str, Any]) -> str:
    """
    Uses t.name (JOINed as tariff_name). If NULL/None, show '-'.
    """
    name = row.get("tariff_name")
    return name if name else "-"

# =========================================================
# UI (keyboards + card formatter)
# =========================================================
def _kb(idx: int, total: int, order_id: int) -> InlineKeyboardMarkup:
    prev_cb = f"ccs_prev:{idx}"
    next_cb = f"ccs_next:{idx}"
    send_cb = f"ccs_send:{order_id}:{idx}"
    cancel_cb = f"ccs_cancel:{order_id}:{idx}"

    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️ Orqaga", callback_data=prev_cb),
            InlineKeyboardButton(text="▶️ Oldinga", callback_data=next_cb),
        ],
        [InlineKeyboardButton(text="📤 Controlga jo'natish", callback_data=send_cb)],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data=cancel_cb)],
    ])

def _format_card(row: dict, idx: int, total: int) -> str:
    region_text = region_title_from_id(row.get("region"))
    tariff_text = row.get("tariff_name") or "-"
    full_name   = row.get("full_name") or "-"   # ✅ users dan keldi
    abonent_id  = row.get("abonent_id") or "-"
    phone_text  = row.get("phone") or "-"

    return (
        "📥 <b>Call Center Supervisor Inbox</b>\n"
        f"🆔 <b>#{row['id']}</b>\n<i>{idx+1}/{total}</i>\n"
        f"📞 <b>Tel:</b> {phone_text}\n"
        f"👤 <b>Mijoz:</b> {full_name} \n"
        f"📍 <b>Region:</b> {region_text}\n💳 <b>Tarif:</b> {tariff_text}\n"
        f"🏠 <b>Manzil:</b> {row.get('address') or '-'}\n"
        f"📝 <b>muommo:</b> {row.get('description') or '-'}\n"
    )
# =========================================================
# Show item (with bounds + refresh-after-action)
# =========================================================
async def _show_item(target, idx: int):
    total = await ccs_count_active()
    if total == 0:
        text = ("📭 Inbox bo'sh.\n")
        if isinstance(target, Message):
            return await target.answer(text, parse_mode="HTML")
        return await target.message.edit_text(text, parse_mode="HTML")

    # clamp index
    idx = max(0, min(idx, total - 1))

    row = await ccs_fetch_by_offset(idx)
    if not row:
        # try last index if offset slipped
        idx = max(0, total - 1)
        row = await ccs_fetch_by_offset(idx)

    kb = _kb(idx, total, row["id"])
    text = _format_card(row, idx, total)

    if isinstance(target, Message):
        return await target.answer(text, parse_mode="HTML", reply_markup=kb)
    else:
        return await target.message.edit_text(text, parse_mode="HTML", reply_markup=kb)

# =========================================================
# Handlers
# =========================================================
@router.message(F.text.in_(["📥 Inbox", "📥 Инбокс", "Inbox", "📥 Supervisor Inbox"]))
async def ccs_inbox(message: Message):
    await _show_item(message, idx=0)

@router.callback_query(F.data.startswith("ccs_prev:"))
async def ccs_prev(cb: CallbackQuery):
    cur = int(cb.data.split(":")[1])
    await _show_item(cb, idx=cur - 1)
    await cb.answer()

@router.callback_query(F.data.startswith("ccs_next:"))
async def ccs_next(cb: CallbackQuery):
    cur = int(cb.data.split(":")[1])
    await _show_item(cb, idx=cur + 1)
    await cb.answer()

@router.callback_query(F.data.startswith("ccs_send:"))
async def ccs_send(cb: CallbackQuery):
    _, order_id, cur = cb.data.split(":")
    order_id = int(order_id)
    cur = int(cur)

    await ccs_send_to_control(order_id, supervisor_id=cb.from_user.id)
    # item removed from current list; same index points to the next item
    await _show_item(cb, idx=cur)
    await cb.answer("Controlga yuborildi")

@router.callback_query(F.data.startswith("ccs_cancel:"))
async def ccs_cancel_cb(cb: CallbackQuery):
    _, order_id, cur = cb.data.split(":")
    order_id = int(order_id)
    cur = int(cur)

    await ccs_cancel(order_id)
    await _show_item(cb, idx=cur)
    await cb.answer("Ariza bekor qilindi")
