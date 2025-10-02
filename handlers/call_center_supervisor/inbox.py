# =============================
# FILE: handlers/call_center_supervisor/inbox.py
# Dual-mode Inbox (Operator orders / Technician orders)
# =============================
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Optional, Dict, Any, List

from filters.role_filter import RoleFilter
from database.language_queries import get_user_language

# ---- Existing operator-side queries (saff_orders) ----
from database.call_center_supervisor_inbox_queries import (
    ccs_count_active as op_count_active,
    ccs_cancel as op_cancel,
    ccs_fetch_by_offset as op_fetch_by_offset,
    ccs_send_to_control as op_send_to_control,
)

# ---- Technician-side queries ----
from database.call_center_supervisor_inbox_queries import (
    tech_count_active,
    tech_fetch_by_offset,
    list_operators_with_load,
    assign_to_operator_for_tech,
    get_user_by_telegram_id,   # telegram_id -> users.id rezolv qiladi
)

router = Router()
router.message.filter(RoleFilter("callcenter_supervisor"))
router.callback_query.filter(RoleFilter("callcenter_supervisor"))

# =========================================================
# Region helpers
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
# Localized text blocks
# =========================================================
TXT = {
    "uz": {
        "menu_title": "📥 <b>Inbox turini tanlang</b>",
        "menu_op": "👨‍💼 Operator arizalari",
        "menu_tech": "🛠️ Texnik arizalari",
        "inbox": "📥 <b>Call Center Supervisor Inbox</b>",
        "inbox_tech": "📥 <b>Supervisor: Texnik arizalar</b>",
        "empty": "📭 Inbox bo'sh.",
        "id": "🆔",
        "tel": "📞 <b>Tel:</b>",
        "client": "👤 <b>Mijoz:</b>",
        "region": "📍 <b>Region:</b>",
        "tariff": "💳 <b>Tarif:</b>",
        "address": "🏠 <b>Manzil:</b>",
        "issue": "📝 <b>Muammo:</b>",
        "back": "◀️ Orqaga",
        "next": "▶️ Oldinga",
        "send_control": "📤 Controlga jo'natish",
        "cancel": "❌ Bekor qilish",
        "send_operator": "📤 Operatorga jo'natish",
        "sent_control": "Controlga yuborildi",
        "cancelled": "Ariza bekor qilindi",
        "pick_operator": "Operatorni tanlang",
        "assign_ok": "Operatorga biriktirildi",
        "home": "🔙 Bosh sahifa",
        "no_ops_title": "⚠️ Hozircha operatorlar mavjud emas.",
        "choose_type": "📥 Qaysi turdagi arizalarni ko‘rasiz?",
        "choose_operator": "Operatorni tanlang:",
    },
    "ru": {
        "menu_title": "📥 <b>Выберите тип инбокса</b>",
        "menu_op": "👨‍💼 Заявки оператора",
        "menu_tech": "🛠️ Заявки техника",
        "inbox": "📥 <b>Входящие (Супервайзер Call Center)</b>",
        "inbox_tech": "📥 <b>Супервайзер: Заявки техника</b>",
        "empty": "📭 Инбокс пуст.",
        "id": "🆔",
        "tel": "📞 <b>Тел:</b>",
        "client": "👤 <b>Клиент:</b>",
        "region": "📍 <b>Регион:</b>",
        "tariff": "💳 <b>Тариф:</b>",
        "address": "🏠 <b>Адрес:</b>",
        "issue": "📝 <b>Проблема:</b>",
        "back": "◀️ Назад",
        "next": "▶️ Далее",
        "send_control": "📤 Отправить в Control",
        "cancel": "❌ Отменить",
        "send_operator": "📤 Отправить оператору",
        "sent_control": "Отправлено в Control",
        "cancelled": "Заявка отменена",
        "pick_operator": "Выберите оператора",
        "assign_ok": "Назначено оператору",
        "home": "🔙 Главное меню",
        "no_ops_title": "⚠️ Операторы пока отсутствуют.",
        "choose_type": "📥 Какие заявки посмотреть?",
        "choose_operator": "Выберите оператора:",
    },
}

# =========================================================
# Keyboards
# =========================================================
def kb_mode(lang: str) -> InlineKeyboardMarkup:
    t = TXT[lang]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["menu_op"], callback_data="ccs_mode:op")],
        [InlineKeyboardButton(text=t["menu_tech"], callback_data="ccs_mode:tech")],
    ])

def kb_operator(idx: int, total: int, order_id: int, lang: str) -> InlineKeyboardMarkup:
    t = TXT[lang]
    prev_cb = f"ccs_prev:{idx}"
    next_cb = f"ccs_next:{idx}"
    send_cb = f"ccs_send:{order_id}:{idx}"
    cancel_cb = f"ccs_cancel:{order_id}:{idx}"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["back"], callback_data=prev_cb),
         InlineKeyboardButton(text=t["next"], callback_data=next_cb)],
        [InlineKeyboardButton(text=t["send_control"], callback_data=send_cb)],
        [InlineKeyboardButton(text=t["cancel"], callback_data=cancel_cb)],
        [InlineKeyboardButton(text=t["home"], callback_data="ccs_back_home")],
    ])

def kb_tech(idx: int, total: int, order_id: int, lang: str) -> InlineKeyboardMarkup:
    t = TXT[lang]
    prev_cb = f"ccs_t_prev:{idx}"
    next_cb = f"ccs_t_next:{idx}"
    send_cb = f"ccs_t_send:{order_id}:{idx}"  # open operator picker
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["back"], callback_data=prev_cb),
         InlineKeyboardButton(text=t["next"], callback_data=next_cb)],
        [InlineKeyboardButton(text=t["send_operator"], callback_data=send_cb)],
        [InlineKeyboardButton(text=t["home"], callback_data="ccs_back_home")],
    ])

def kb_operator_picker(order_id: int, idx: int, operators: List[dict], lang: str) -> InlineKeyboardMarkup:
    t = TXT[lang]
    rows = []
    for op in operators:
        title = f"{op['full_name']} ({op['active_count']})"
        rows.append([InlineKeyboardButton(text=title, callback_data=f"ccs_t_assign:{order_id}:{op['id']}:{idx}")])
    rows.append([InlineKeyboardButton(text=t["home"], callback_data="ccs_back_home")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

# =========================================================
# Card formatters
# =========================================================
def format_operator_card(row: dict, idx: int, total: int, lang: str) -> str:
    t = TXT[lang]
    region_text = region_title_from_id(row.get("region"))
    full_name   = row.get("full_name") or "-"
    phone_text  = row.get("phone") or "-"
    description = row.get("description")
    tariff      = row.get("tariff_name")

    description_text = f"{t['issue']} {description}\n" if description else ""
    tariff_text = f"{t['tariff']} {tariff}\n" if tariff else ""

    return (
        f"{t['inbox']}\n"
        f"{t['id']} <b>#{row['id']}</b>\n<i>{idx+1}/{total}</i>\n"
        f"{t['tel']} {phone_text}\n"
        f"{t['client']} {full_name}\n"
        f"{t['region']} {region_text}\n"
        f"{tariff_text}"
        f"{t['address']} {row.get('address') or '-'}\n"
        f"{description_text}"
    )

def format_tech_card(row: dict, idx: int, total: int, lang: str) -> str:
    t = TXT[lang]
    region_text = region_title_from_id(row.get("region"))
    full_name   = row.get("client_name") or "-"
    phone_text  = row.get("client_phone") or "-"
    description = row.get("description")

    description_text = f"{t['issue']} {description}\n" if description else ""

    return (
        f"{t['inbox_tech']}\n"
        f"{t['id']} <b>#{row['id']}</b>\n<i>{idx+1}/{total}</i>\n"
        f"{t['tel']} {phone_text}\n"
        f"{t['client']} {full_name}\n"
        f"{t['region']} {region_text}\n"
        f"{t['address']} {row.get('address') or '-'}\n"
        f"{description_text}"
    )

# =========================================================
# Showers
# =========================================================
async def show_menu(target, user_id: int):
    lang = await get_user_language(user_id) or "uz"
    t = TXT[lang]
    if isinstance(target, Message):
        return await target.answer(t["menu_title"], parse_mode="HTML", reply_markup=kb_mode(lang))
    return await target.message.edit_text(t["menu_title"], parse_mode="HTML", reply_markup=kb_mode(lang))

async def show_operator_item(target, idx: int, user_id: int):
    lang = await get_user_language(user_id) or "uz"
    t = TXT[lang]
    total = await op_count_active()
    if total == 0:
        text = t["empty"]
        if isinstance(target, Message):
            return await target.answer(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text=t["home"], callback_data="ccs_back_home")]]
            ))
        return await target.message.edit_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=t["home"], callback_data="ccs_back_home")]]
        ))

    idx = max(0, min(idx, total - 1))
    row = await op_fetch_by_offset(idx)
    if not row:
        idx = max(0, total - 1)
        row = await op_fetch_by_offset(idx)

    kb = kb_operator(idx, total, row["id"], lang)
    text = format_operator_card(row, idx, total, lang)

    if isinstance(target, Message):
        return await target.answer(text, parse_mode="HTML", reply_markup=kb)
    else:
        return await target.message.edit_text(text, parse_mode="HTML", reply_markup=kb)

async def show_tech_item(target, idx: int, user_id: int):
    lang = await get_user_language(user_id) or "uz"
    t = TXT[lang]
    total = await tech_count_active()
    if total == 0:
        text = t["empty"]
        if isinstance(target, Message):
            return await target.answer(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text=t["home"], callback_data="ccs_back_home")]]
            ))
        return await target.message.edit_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=t["home"], callback_data="ccs_back_home")]]
        ))

    idx = max(0, min(idx, total - 1))
    row = await tech_fetch_by_offset(idx)
    if not row:
        idx = max(0, total - 1)
        row = await tech_fetch_by_offset(idx)

    kb = kb_tech(idx, total, row["id"], lang)
    text = format_tech_card(row, idx, total, lang)

    if isinstance(target, Message):
        return await target.answer(text, parse_mode="HTML", reply_markup=kb)
    else:
        return await target.message.edit_text(text, parse_mode="HTML", reply_markup=kb)

# =========================================================
# Handlers — Home
# =========================================================
@router.message(F.text.in_(["📥 Inbox", "📥 Входящие"]))
async def ccs_inbox(message: Message):
    await show_menu(message, user_id=message.from_user.id)

@router.callback_query(F.data == "ccs_back_home")
async def ccs_back_home(cb: CallbackQuery):
    await show_menu(cb, user_id=cb.from_user.id)
    await cb.answer()

@router.callback_query(F.data.startswith("ccs_mode:"))
async def ccs_mode(cb: CallbackQuery):
    mode = cb.data.split(":")[1]
    if mode == "op":
        await show_operator_item(cb, idx=0, user_id=cb.from_user.id)
    else:
        await show_tech_item(cb, idx=0, user_id=cb.from_user.id)
    await cb.answer()

# =========================================================
# Handlers — Operator flow (saff_orders)
# =========================================================
@router.callback_query(F.data.startswith("ccs_prev:"))
async def ccs_prev(cb: CallbackQuery):
    cur = int(cb.data.split(":")[1])
    await show_operator_item(cb, idx=cur - 1, user_id=cb.from_user.id)
    await cb.answer()

@router.callback_query(F.data.startswith("ccs_next:"))
async def ccs_next(cb: CallbackQuery):
    cur = int(cb.data.split(":")[1])
    await show_operator_item(cb, idx=cur + 1, user_id=cb.from_user.id)
    await cb.answer()

@router.callback_query(F.data.startswith("ccs_send:"))
async def ccs_send(cb: CallbackQuery):
    _, order_id, cur = cb.data.split(":")
    order_id = int(order_id)
    cur = int(cur)

    # Eslatma: op_send_to_control supervisor_id ni ishlatmaydi (connections'ga clientni yozadi)
    await op_send_to_control(order_id, supervisor_id=cb.from_user.id)
    await show_operator_item(cb, idx=cur, user_id=cb.from_user.id)

    lang = await get_user_language(cb.from_user.id) or "uz"
    await cb.answer(TXT[lang]["sent_control"])

@router.callback_query(F.data.startswith("ccs_cancel:"))
async def ccs_cancel_cb(cb: CallbackQuery):
    _, order_id, cur = cb.data.split(":")
    order_id = int(order_id)
    cur = int(cur)

    await op_cancel(order_id)
    await show_operator_item(cb, idx=cur, user_id=cb.from_user.id)

    lang = await get_user_language(cb.from_user.id) or "uz"
    await cb.answer(TXT[lang]["cancelled"])

# =========================================================
# Handlers — Technician flow (technician_orders)
# =========================================================
@router.callback_query(F.data.startswith("ccs_t_prev:"))
async def ccs_t_prev(cb: CallbackQuery):
    cur = int(cb.data.split(":")[1])
    await show_tech_item(cb, idx=cur - 1, user_id=cb.from_user.id)
    await cb.answer()

@router.callback_query(F.data.startswith("ccs_t_next:"))
async def ccs_t_next(cb: CallbackQuery):
    cur = int(cb.data.split(":")[1])
    await show_tech_item(cb, idx=cur + 1, user_id=cb.from_user.id)
    await cb.answer()

@router.callback_query(F.data.startswith("ccs_t_send:"))
async def ccs_t_send(cb: CallbackQuery):
    """
    Texnik ariza kartasida 'Operatorga jo'natish' bosilganda — operatorlar ro'yxatini chiqaramiz.
    """
    _, order_id, cur = cb.data.split(":")
    order_id = int(order_id)
    cur = int(cur)

    lang = await get_user_language(cb.from_user.id) or "uz"
    t = TXT[lang]

    ops = await list_operators_with_load()
    if not ops:
        # Operatorlar yo‘q — fallback matn (home tugmasi bilan)
        await cb.message.edit_text(t["no_ops_title"], reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=t["home"], callback_data="ccs_back_home")]]
        ))
        await cb.answer(t["no_ops_title"], show_alert=True)
        return

    kb = kb_operator_picker(order_id, cur, ops, lang)
    await cb.message.edit_text(t["choose_operator"], reply_markup=kb)
    await cb.answer()

@router.callback_query(F.data.startswith("ccs_t_assign:"))
async def ccs_t_assign(cb: CallbackQuery):
    """
    Operator tanlanganda — arizani operatorga biriktiramiz (connections + status update).
    sender_id/recipient_id FK'lari uchun ichki users.id'lardan foydalanamiz.
    """
    _, order_id, operator_id, cur = cb.data.split(":")
    order_id = int(order_id)
    operator_id = int(operator_id)   # ro‘yxatdan kelgan users.id (ok)
    cur = int(cur)

    # Supervisor (telegram_id -> users.id) rezolv
    supervisor = await get_user_by_telegram_id(cb.from_user.id)
    if not supervisor:
        await cb.answer("Supervisor users jadvalida topilmadi", show_alert=True)
        return
    supervisor_db_id = supervisor["id"]

    # Arizani operatorga biriktirish (status -> in_call_center_operator, connections log)
    await assign_to_operator_for_tech(
        order_id,
        tech_id=operator_id,        # operator users.id
        actor_id=supervisor_db_id   # supervisor users.id (FK mos)
    )

    # Hozirgi indeksda qolgan holda kartani yangilaymiz
    await show_tech_item(cb, idx=cur, user_id=cb.from_user.id)

    lang = await get_user_language(cb.from_user.id) or "uz"
    await cb.answer(TXT[lang]["assign_ok"])
