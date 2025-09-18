# handlers/manager/applications.py

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
import html
from aiogram.exceptions import TelegramBadRequest

from filters.role_filter import RoleFilter

from database.manager_application import (
    get_total_orders_count,
    get_in_progress_count,
    get_completed_today_count,
    get_cancelled_count,
    get_new_orders_today_count,
    list_new_orders,
    list_in_progress_orders,
    list_completed_today_orders,
    list_cancelled_orders
)


router = Router()
router.message.filter(RoleFilter("manager"))
router.callback_query.filter(RoleFilter("manager"))

# --------- UI helpers ---------

def _apps_menu_kb() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text="🆕 Yangi buyurtmalar", callback_data="apps:new")],
        [InlineKeyboardButton(text="⏳ Jarayondagilar",     callback_data="apps:progress")],
        [InlineKeyboardButton(text="✅ Bugun bajarilgan",   callback_data="apps:done_today")],
        [InlineKeyboardButton(text="🚫 Bekor qilinganlar",  callback_data="apps:cancelled")],  # ⬅️ oldingi ❌ ni 🚫 ga almashtirdik
        [InlineKeyboardButton(text="♻️ Yangilash",         callback_data="apps:refresh")],
        [InlineKeyboardButton(text="❌ Yopish",             callback_data="apps:close")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)

def _back_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Orqaga", callback_data="apps:back")]]
    )

def _list_nav_kb(index: int, total_loaded: int) -> InlineKeyboardMarkup:
    rows = []
    row = []
    if index > 0:
        row.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data="apps:nav:prev"))
    if index < total_loaded - 1:
        row.append(InlineKeyboardButton(text="Keyingi ➡️", callback_data="apps:nav:next"))
    if row:
        rows.append(row)
    rows.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="apps:back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

@router.callback_query(F.data == "apps:close")
async def apps_close(call: CallbackQuery, state: FSMContext):
    await call.answer("Yopildi")
    # State ichidagi ro'yxat kontekstini tozalab qo'yamiz (ixtiyoriy)
    await state.update_data(apps_cat=None, apps_items=None, apps_idx=None, apps_total=None)
    try:
        await call.message.delete()  # 🔥 xabarni to‘liq o‘chiradi
    except TelegramBadRequest:
        # Fallback: hech bo'lmasa tugmalarni olib tashlaymiz
        try:
            await call.message.edit_reply_markup(reply_markup=None)
        except TelegramBadRequest:
            pass

def _esc(x: str | None) -> str:
    return html.escape(x or "-")

def _fmt_dt(dt) -> str:
    try:
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return str(dt) if dt else "-"

def _card_text(total: int, new_today: int, in_progress: int, done_today: int, cancelled: int) -> str:
    return (
        "🗂 <b>Buyurtmalar nazorati</b>\n\n"
        "📊 <b>Statistika:</b>\n"
        f"• Jami: <b>{total}</b>\n"
        f"• Yangi: <b>{new_today}</b>\n"
        f"• Jarayonda: <b>{in_progress}</b>\n"
        f"• Bugun bajarilgan: <b>{done_today}</b>\n"
        f"• Bekor qilinganlar: <b>{cancelled}</b>\n\n"
        "Quyidagini tanlang:"
    )

def _item_card(item: dict, index: int, total: int) -> str:
    """
    Bitta arizani karta ko‘rinishida chiqarish + matn ichida indikator: 📄 n/N
    """
    full_id = str(item.get("id", "-"))
    client_name  = _esc(item.get("client_name"))
    client_phone = _esc(item.get("client_phone"))
    address      = _esc(item.get("address"))
    tariff       = _esc(item.get("tariff"))
    status       = _esc(str(item.get("status")))
    created_at   = _fmt_dt(item.get("created_at"))
    updated_at   = _fmt_dt(item.get("updated_at"))

    return (
        "🗂 <b>Buyurtma</b>\n\n"
        f"🆔 <b>ID:</b> {_esc(full_id)}\n"
        f"📊 <b>Tarif:</b> {tariff}\n"
        f"👤 <b>Mijoz:</b> {client_name}\n"
        f"📞 <b>Telefon:</b> {client_phone}\n"
        f"📍 <b>Manzil:</b> {address}\n"
        f"🛈 <b>Status:</b> {status}\n"
        f"🗓 <b>Yaratilgan:</b> {created_at}\n"
        f"🗓 <b>Yangilangan:</b> {updated_at}\n"
        f"📄 <b>Ariza:</b> {index + 1}/{total}"
    )

async def _load_stats():
    total      = await get_total_orders_count()
    new_today  = await get_new_orders_today_count()
    in_prog    = await get_in_progress_count()
    done_today = await get_completed_today_count()
    cancelled  = await get_cancelled_count()
    return total, new_today, in_prog, done_today, cancelled

async def _safe_edit(call: CallbackQuery, text: str, kb: InlineKeyboardMarkup):
    """
    Xabarni o'sha joyida yangilash. Agar matn aynan bir xil bo'lsa, shunchaki javob berilmaydi.
    (Yangi xabar yubormaymiz — ketma-ket tushishining oldini oladi.)
    """
    try:
        await call.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except TelegramBadRequest as e:
        # 'message is not modified' bo'lsa — e'tibor bermaymiz
        if "not modified" in str(e).lower():
            await call.answer("Yangilandi ✅", show_alert=False)
        else:
            # Oxirgi chora sifatida faqat klaviaturani yangilashga harakat
            try:
                await call.message.edit_reply_markup(reply_markup=kb)
            except TelegramBadRequest:
                pass

# --------- Kirish (reply tugmadan) ---------

@router.message(F.text.in_(["📋 Arizalarni ko'rish", "📋 Все заявки"]))
async def applications_handler(message: Message, state: FSMContext):
    total, new_today, in_prog, done_today, cancelled = await _load_stats()
    await message.answer(
        _card_text(total, new_today, in_prog, done_today, cancelled),
        reply_markup=_apps_menu_kb(),
        parse_mode="HTML"
    )

# --------- Kategoriya bo'yicha ro'yxatni ko'rsatish ---------

CAT_NEW        = "new"
CAT_PROGRESS   = "progress"
CAT_DONE_TODAY = "done_today"
CAT_CANCELLED  = "cancelled"

async def _load_items_by_cat(cat: str) -> list[dict]:
    if cat == CAT_NEW:
        return await list_new_orders(limit=50)
    if cat == CAT_PROGRESS:
        return await list_in_progress_orders(limit=50)
    if cat == CAT_DONE_TODAY:
        return await list_completed_today_orders(limit=50)
    if cat == CAT_CANCELLED:
        return await list_cancelled_orders(limit=50)
    return []

async def _open_category(call: CallbackQuery, state: FSMContext, cat: str, title: str):
    await call.answer()
    items = await _load_items_by_cat(cat)
    if not items:
        await _safe_edit(call, f"{title}\n\n— Hech narsa topilmadi.", _back_kb())
        return

    idx = 0
    total_loaded = len(items)
    await state.update_data(apps_cat=cat, apps_items=items, apps_idx=idx, apps_total=total_loaded)

    text = f"{title}\n\n" + _item_card(items[idx], idx, total_loaded)
    kb = _list_nav_kb(idx, total_loaded)
    await _safe_edit(call, text, kb)

@router.callback_query(F.data == "apps:new")
async def apps_new(call: CallbackQuery, state: FSMContext):
    await _open_category(call, state, CAT_NEW, "🆕 <b>Yangi buyurtmalar</b>")

@router.callback_query(F.data == "apps:progress")
async def apps_progress(call: CallbackQuery, state: FSMContext):
    await _open_category(call, state, CAT_PROGRESS, "⏳ <b>Jarayondagilar</b>")

@router.callback_query(F.data == "apps:done_today")
async def apps_done_today(call: CallbackQuery, state: FSMContext):
    await _open_category(call, state, CAT_DONE_TODAY, "✅ <b>Bugun bajarilgan</b>")

@router.callback_query(F.data == "apps:cancelled")
async def apps_cancelled(call: CallbackQuery, state: FSMContext):
    await _open_category(call, state, CAT_CANCELLED, "❌ <b>Bekor qilinganlar</b>")

# --------- Oldingi / Keyingi ---------

@router.callback_query(F.data == "apps:nav:prev")
async def apps_nav_prev(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    items = data.get("apps_items", [])
    idx   = max(0, int(data.get("apps_idx", 0)) - 1)
    total_loaded = len(items)
    if not items:
        await _safe_edit(call, "— Hech narsa topilmadi.", _back_kb()); return
    await state.update_data(apps_idx=idx)
    text = _item_card(items[idx], idx, total_loaded)
    # yuqori titulni saqlash uchun kategoriya nomi qo'shib beramiz
    cat = data.get("apps_cat", "")
    title = {
        CAT_NEW: "🆕 <b>Yangi buyurtmalar</b>",
        CAT_PROGRESS: "⏳ <b>Jarayondagilar</b>",
        CAT_DONE_TODAY: "✅ <b>Bugun bajarilgan</b>",
        CAT_CANCELLED: "❌ <b>Bekor qilinganlar</b>",
    }.get(cat, "🗂 <b>Buyurtmalar</b>")
    kb = _list_nav_kb(idx, total_loaded)
    await _safe_edit(call, f"{title}\n\n{text}", kb)

@router.callback_query(F.data == "apps:nav:next")
async def apps_nav_next(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    items = data.get("apps_items", [])
    idx   = min(len(items)-1, int(data.get("apps_idx", 0)) + 1)
    total_loaded = len(items)
    if not items:
        await _safe_edit(call, "— Hech narsa topilmadi.", _back_kb()); return
    await state.update_data(apps_idx=idx)
    text = _item_card(items[idx], idx, total_loaded)
    cat = data.get("apps_cat", "")
    title = {
        CAT_NEW: "🆕 <b>Yangi buyurtmalar</b>",
        CAT_PROGRESS: "⏳ <b>Jarayondagilar</b>",
        CAT_DONE_TODAY: "✅ <b>Bugun bajarilgan</b>",
        CAT_CANCELLED: "❌ <b>Bekor qilinganlar</b>",
    }.get(cat, "🗂 <b>Buyurtmalar</b>")
    kb = _list_nav_kb(idx, total_loaded)
    await _safe_edit(call, f"{title}\n\n{text}", kb)

# --------- Yangilash / Orqaga ---------

@router.callback_query(F.data == "apps:refresh")
async def apps_refresh(call: CallbackQuery, state: FSMContext):
    """
    ♻️ Kartochkani o'sha joyida yangilaydi (yangi xabar yubormaydi).
    """
    await call.answer("Yangilanmoqda…")
    total, new_today, in_prog, done_today, cancelled = await _load_stats()
    await _safe_edit(
        call,
        _card_text(total, new_today, in_prog, done_today, cancelled),
        _apps_menu_kb()
    )

@router.callback_query(F.data == "apps:back")
async def apps_back(call: CallbackQuery, state: FSMContext):
    await call.answer()
    # state tozalash shart emas, lekin xohlasangiz:
    # await state.clear()
    total, new_today, in_prog, done_today, cancelled = await _load_stats()
    await _safe_edit(
        call,
        _card_text(total, new_today, in_prog, done_today, cancelled),
        _apps_menu_kb()
    )
