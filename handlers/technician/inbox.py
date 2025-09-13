# handlers/technician/inbox.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup

from datetime import datetime
import html

from filters.role_filter import RoleFilter
from database.queries import find_user_by_telegram_id
from database.technician_queries import (
    # Ulanish (connection_orders) oqimi
    fetch_technician_inbox,
    cancel_technician_request,
    accept_technician_work,
    start_technician_work,
    finish_technician_work,
    fetch_selected_materials_for_request,

    # Material oqimi (ikkala rejimda ham ishlatiladi)
    fetch_technician_materials,
    fetch_material_by_id,
    fetch_assigned_qty,
    upsert_material_request_and_decrease_stock,

    # Texnik xizmat (technician_orders) oqimi
    fetch_technician_inbox_tech,
    accept_technician_work_for_tech,
    start_technician_work_for_tech,
    save_technician_diagnosis,
    finish_technician_work_for_tech,
)

# ====== STATE-lar ======
class QtyStates(StatesGroup):
    waiting_qty = State()

class DiagStates(StatesGroup):
    waiting_text = State()

# ====== Router ======
router = Router()
router.message.filter(RoleFilter("technician"))
router.callback_query.filter(RoleFilter("technician"))

# tech_mode'ni yo'qotmasdan FSM datani tozalash
async def _preserve_mode_clear(state: FSMContext, keep_keys: list[str] | None = None):
    data = await state.get_data()
    mode = data.get("tech_mode")
    kept: dict = {}
    if keep_keys:
        for k in keep_keys:
            if k in data:
                kept[k] = data[k]
    await state.clear()
    payload = {"tech_mode": mode}
    payload.update(kept)
    await state.update_data(**payload)

# ====== Yordamchi funksiyalar ======
def fmt_dt(dt) -> str:
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except Exception:
            return html.escape(dt, quote=False)
    if isinstance(dt, datetime):
        return dt.strftime("%d.%m.%Y %H:%M")
    return "-"

def esc(v) -> str:
    return "-" if v is None else html.escape(str(v), quote=False)

def status_emoji(s: str) -> str:
    m = {
        "between_controller_technician": "🆕",
        "in_technician": "🧰",
        "in_technician_work": "🟢",
        "completed": "✅",
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

def action_keyboard(item_id: int, index: int, total: int, status: str, mode: str = "connection") -> InlineKeyboardMarkup:
    """
    mode:
      - "connection"  -> ulanish arizalari (ombor darhol)
      - "technician"  -> texnik xizmat arizalari (diagnostika -> keyin ombor)
    """
    rows = []

    # Navigatsiya
    if total > 1:
        nav = []
        if index > 0:
            nav.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"tech_inbox_prev_{index}"))
        if index < total - 1:
            nav.append(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"tech_inbox_next_{index}"))
        if nav:
            rows.append(nav)

    # Amallar
    if status == "between_controller_technician":
        rows.append([
            InlineKeyboardButton(text="🗑️ Bekor qilish", callback_data=f"tech_cancel_{item_id}"),
            InlineKeyboardButton(text="✅ Ishni qabul qilish", callback_data=f"tech_accept_{item_id}")
        ])
    elif status == "in_technician":
        rows.append([
            InlineKeyboardButton(text="▶️ Ishni boshlash", callback_data=f"tech_start_{item_id}")
        ])
    elif status == "in_technician_work" and mode == "technician":
        rows.append([
            InlineKeyboardButton(text="🩺 Diagnostika", callback_data=f"tech_diag_begin_{item_id}")
        ])

    return InlineKeyboardMarkup(inline_keyboard=rows)

def _dedup_by_id(items: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for it in items:
        i = it.get("id")
        if i in seen:
            continue
        seen.add(i)
        out.append(it)
    return out

def tech_category_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔌 Ulanish arizalari",       callback_data="tech_inbox_cat_connection")],
        [InlineKeyboardButton(text="🔧 Texnik xizmat arizalari", callback_data="tech_inbox_cat_tech")],
        [InlineKeyboardButton(text="📞 Operator arizalari",      callback_data="tech_inbox_cat_operator")],
    ])

async def _safe_edit(message, text: str, kb: InlineKeyboardMarkup):
    try:
        if message.text == text:
            try:
                await message.edit_reply_markup(reply_markup=kb)
                return
            except TelegramBadRequest as e:
                if "message is not modified" in str(e):
                    return
                raise
        await message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            return
        raise

def _fmt_price_uzs(val) -> str:
    try:
        s = f"{int(val):,}"
        return s.replace(",", " ")
    except Exception:
        return str(val)

def materials_keyboard(materials: list[dict], applications_id: int) -> InlineKeyboardMarkup:
    rows = []
    if materials:
        for mat in materials:
            title = f"📦 {mat.get('name')} — {_fmt_price_uzs(mat.get('price'))} so'm ({mat.get('stock_quantity','0')} dona)"
            rows.append([InlineKeyboardButton(
                text=title[:64],
                callback_data=f"tech_mat_select_{mat.get('material_id')}_{applications_id}"
            )])
    rows.append([InlineKeyboardButton(text="➕ Boshqa mahsulot", callback_data=f"tech_mat_custom_{applications_id}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def _guard_connection_mode(data: dict) -> bool:
    return data.get("tech_mode", "connection") == "connection"

# ====== Inbox ochish: avval kategoriya ======
@router.message(F.text.in_(["📥 Inbox", "Inbox"]))
async def tech_open_inbox(message: Message, state: FSMContext):
    user = await find_user_by_telegram_id(message.from_user.id)
    if not user or user.get("role") != "technician":
        return
    await state.update_data(tech_mode=None, tech_inbox=[], tech_idx=0)
    await message.answer("📂 Qaysi bo‘limni ko‘ramiz?", reply_markup=tech_category_keyboard())

# ====== Kategoriya handlerlari ======
@router.callback_query(F.data == "tech_inbox_cat_connection")
async def tech_cat_connection(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    user = await find_user_by_telegram_id(cb.from_user.id)
    if not user or user.get("role") != "technician":
        return await cb.answer("❌ Ruxsat yo‘q", show_alert=True)

    items = _dedup_by_id(await fetch_technician_inbox(technician_id=user["id"], limit=50, offset=0))
    await state.update_data(tech_mode="connection", tech_inbox=items, tech_idx=0)

    if not items:
        return await cb.message.edit_text("📭 Ulanish arizalari bo‘sh")

    item = items[0]; total = len(items)
    text = short_view_text(item, 0, total)
    kb = action_keyboard(item.get("id"), 0, total, item.get("status", ""), mode="connection")
    await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data == "tech_inbox_cat_tech")
async def tech_cat_tech(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    user = await find_user_by_telegram_id(cb.from_user.id)
    if not user or user.get("role") != "technician":
        return await cb.answer("❌ Ruxsat yo‘q", show_alert=True)

    items = _dedup_by_id(await fetch_technician_inbox_tech(technician_id=user["id"], limit=50, offset=0))
    await state.update_data(tech_mode="technician", tech_inbox=items, tech_idx=0)

    if not items:
        return await cb.message.edit_text("📭 Texnik xizmat arizalari bo‘sh")

    item = items[0]; total = len(items)
    text = short_view_text(item, 0, total)
    kb = action_keyboard(item.get("id"), 0, total, item.get("status", ""), mode="technician")
    await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data == "tech_inbox_cat_operator")
async def tech_cat_operator(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await cb.message.edit_text(
        "📞 Operator arizalari bo‘limi keyingi bosqichda ulanadi.",
        reply_markup=tech_category_keyboard()
    )

# ====== Navigatsiya (prev/next) ======
@router.callback_query(F.data.startswith("tech_inbox_prev_"))
async def tech_prev(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    mode = data.get("tech_mode", "connection")
    items = _dedup_by_id(data.get("tech_inbox", []))
    if not items:
        return
    total = len(items)
    idx = int(cb.data.replace("tech_inbox_prev_", "")) - 1
    if idx < 0 or idx >= total:
        return
    await state.update_data(tech_inbox=items, tech_idx=idx)
    item = items[idx]
    text = short_view_text(item, idx, total)
    kb = action_keyboard(item.get("id"), idx, total, item.get("status", ""), mode=mode)
    await _safe_edit(cb.message, text, kb)

@router.callback_query(F.data.startswith("tech_inbox_next_"))
async def tech_next(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    mode = data.get("tech_mode", "connection")
    items = _dedup_by_id(data.get("tech_inbox", []))
    if not items:
        return
    total = len(items)
    idx = int(cb.data.replace("tech_inbox_next_", "")) + 1
    if idx < 0 or idx >= total:
        return
    await state.update_data(tech_inbox=items, tech_idx=idx)
    item = items[idx]
    text = short_view_text(item, idx, total)
    kb = action_keyboard(item.get("id"), idx, total, item.get("status", ""), mode=mode)
    await _safe_edit(cb.message, text, kb)

# ====== Qabul qilish / Bekor qilish / Boshlash ======
@router.callback_query(F.data.startswith("tech_accept_"))
async def tech_accept(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    mode = data.get("tech_mode", "connection")

    user = await find_user_by_telegram_id(cb.from_user.id)
    if not user or user.get("role") != "technician":
        return await cb.answer("❌ Ruxsat yo‘q", show_alert=True)

    req_id = int(cb.data.replace("tech_accept_", ""))
    try:
        if mode == "technician":
            ok = await accept_technician_work_for_tech(applications_id=req_id, technician_id=user["id"])
        else:
            ok = await accept_technician_work(applications_id=req_id, technician_id=user["id"])
        if not ok:
            return await cb.answer("⚠️ Holat mos emas yoki ariza topilmadi.", show_alert=True)
    except Exception as e:
        return await cb.answer(f"❌ Xatolik: {e}", show_alert=True)

    # Karta ichida tugma yangilanadi
    st = await state.get_data()
    items = _dedup_by_id(st.get("tech_inbox", []))
    idx = int(st.get("tech_idx", 0))
    for it in items:
        if it.get("id") == req_id:
            it["status"] = "in_technician"
            break
    await state.update_data(tech_inbox=items)

    total = len(items)
    item = items[idx] if 0 <= idx < total else items[0]
    text = short_view_text(item, idx, total)
    kb = action_keyboard(item.get("id"), idx, total, item.get("status", ""), mode=mode)
    await _safe_edit(cb.message, text, kb)
    await cb.answer()  # xabar yubormaymiz

@router.callback_query(F.data.startswith("tech_cancel_"))
async def tech_cancel(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    mode = data.get("tech_mode", "connection")
    if not _guard_connection_mode(data):
        return await cb.answer("Bu bo‘limda hozircha amal yo‘q.", show_alert=True)

    user = await find_user_by_telegram_id(cb.from_user.id)
    if not user or user.get("role") != "technician":
        return await cb.answer("❌ Ruxsat yo‘q", show_alert=True)

    req_id = int(cb.data.replace("tech_cancel_", ""))

    try:
        await cancel_technician_request(applications_id=req_id, technician_id=user["id"])
    except Exception as e:
        return await cb.answer(f"❌ Xatolik: {e}", show_alert=True)

    st = await state.get_data()
    items = _dedup_by_id(st.get("tech_inbox", []))
    idx = int(st.get("tech_idx", 0))

    items = [it for it in items if it.get("id") != req_id]

    if not items:
        await state.update_data(tech_inbox=[], tech_idx=0)
        await cb.answer("🗑️ Ariza bekor qilindi")
        return await _safe_edit(cb.message, "📭 Inbox bo‘sh", InlineKeyboardMarkup(inline_keyboard=[]))

    if idx >= len(items):
        idx = len(items) - 1

    await state.update_data(tech_inbox=items, tech_idx=idx)
    total = len(items)
    item = items[idx]
    await cb.answer("🗑️ Ariza bekor qilindi")
    text = short_view_text(item, idx, total)
    kb = action_keyboard(item.get("id"), idx, total, item.get("status", ""), mode=mode)
    await _safe_edit(cb.message, text, kb)

@router.callback_query(F.data.startswith("tech_start_"))
async def tech_start(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    mode = data.get("tech_mode", "connection")

    user = await find_user_by_telegram_id(cb.from_user.id)
    if not user or user.get("role") != "technician":
        return await cb.answer("❌ Ruxsat yo‘q", show_alert=True)

    req_id = int(cb.data.replace("tech_start_", ""))

    try:
        if mode == "technician":
            ok = await start_technician_work_for_tech(applications_id=req_id, technician_id=user["id"])
        else:
            ok = await start_technician_work(applications_id=req_id, technician_id=user["id"])
        if not ok:
            return await cb.answer("⚠️ Holat mos emas (faqat 'in_technician').", show_alert=True)
    except Exception as e:
        return await cb.answer(f"❌ Xatolik: {e}", show_alert=True)

    # Lokal status -> in_technician_work
    st = await state.get_data()
    items = _dedup_by_id(st.get("tech_inbox", []))
    idx = int(st.get("tech_idx", 0))
    for it in items:
        if it.get("id") == req_id:
            it["status"] = "in_technician_work"
            break
    await state.update_data(tech_inbox=items)

    total = len(items)
    item = items[idx] if 0 <= idx < total else items[0]
    text = short_view_text(item, idx, total)
    kb = action_keyboard(item.get("id"), idx, total, item.get("status", ""), mode=mode)
    await _safe_edit(cb.message, text, kb)

    if mode == "technician":
        # 👉 Texnik xizmat: DIAGNOSTIKA (ombor keyin!)
        diag_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🩺 Diagnostika boshlash", callback_data=f"tech_diag_begin_{req_id}")]
        ])
        await cb.message.answer(
            "🟢 Ish boshlandi.\n\n🩺 Endi diagnostika qo‘yishingiz kerak.",
            reply_markup=diag_kb
        )
        await cb.answer("✅ Ish boshlandi")
        return  # omborni bu yerda chiqarmaymiz!

    # 👉 Ulanish rejimi: darhol ombor
    mats = await fetch_technician_materials(user_id=user["id"])
    header_text = (
        "📦 <b>Ombor jihozlari</b>\n"
        f"🆔 <b>Ariza ID:</b> {req_id}\n"
        "Kerakli jihozlarni tanlang yoki boshqa mahsulot kiriting:"
    )
    await cb.message.answer(header_text, reply_markup=materials_keyboard(mats, applications_id=req_id), parse_mode="HTML")

# ====== DIAGNOSTIKA ======
@router.callback_query(F.data.startswith("tech_diag_begin_"))
async def tech_diag_begin(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    try:
        req_id = int(cb.data.replace("tech_diag_begin_", ""))
    except Exception:
        return
    await state.update_data(diag_req_id=req_id)
    await cb.message.answer(
        "🩺 <b>Diagnostika matnini kiriting</b>\n\n"
        "Masalan: <i>Modem moslamasi ishdan chiqqan</i>.",
        parse_mode="HTML"
    )
    await state.set_state(DiagStates.waiting_text)

@router.message(StateFilter(DiagStates.waiting_text))
async def tech_diag_text(msg: Message, state: FSMContext):
    user = await find_user_by_telegram_id(msg.from_user.id)
    if not user or user.get("role") != "technician":
        return await msg.answer("❌ Ruxsat yo‘q")

    data = await state.get_data()
    req_id = int(data.get("diag_req_id", 0))
    if req_id <= 0:
        await _preserve_mode_clear(state)
        return await msg.answer("❗️ Ariza aniqlanmadi.")

    text = (msg.text or "").strip()
    if not text:
        return await msg.answer("❗️ Bo‘sh matn yuborilmadi. Diagnostikani qayta kiriting.")

    try:
        await save_technician_diagnosis(applications_id=req_id, technician_id=user["id"], text=text)
    except Exception as e:
        await _preserve_mode_clear(state)
        return await msg.answer(f"❌ Diagnostika yozishda xato: {e}")

    # FSM'ni tozalaymiz, lekin tech_mode saqlansin
    await _preserve_mode_clear(state)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Ha",  callback_data=f"tech_diag_go_store_{req_id}")],
        [InlineKeyboardButton(text="❌ Yo‘q", callback_data=f"tech_diag_cancel_{req_id}")],
    ])
    await msg.answer(
        "✅ <b>Diagnostika qo‘yildi!</b>\n\n"
        f"🆔 <b>Ariza ID:</b> {esc(req_id)}\n"
        f"🧰 <b>Diagnostika:</b>\n<code>{html.escape(text, quote=False)}</code>\n\n"
        "🧑‍🏭 <b>Ombor bilan ishlaysizmi?</b>\n"
        "<i>Agar kerakli jihozlar omborda bo‘lsa, ularni olish kerak.</i>",
        reply_markup=kb,
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("tech_diag_go_store_"))
async def tech_diag_go_store(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    try:
        req_id = int(cb.data.replace("tech_diag_go_store_", ""))
    except Exception:
        return

    user = await find_user_by_telegram_id(cb.from_user.id)
    if not user or user.get("role") != "technician":
        return await cb.answer("❌ Ruxsat yo‘q", show_alert=True)

    mats = await fetch_technician_materials(user_id=user["id"])
    header_text = (
        "📦 <b>Ombor jihozlari</b>\n"
        f"🆔 <b>Ariza ID:</b> {req_id}\n"
        "Kerakli jihozlarni tanlang yoki boshqa mahsulot kiriting:"
    )
    await cb.message.answer(header_text, reply_markup=materials_keyboard(mats, applications_id=req_id), parse_mode="HTML")

@router.callback_query(F.data.startswith("tech_diag_cancel_"))
async def tech_diag_cancel(cb: CallbackQuery, state: FSMContext):
    await cb.answer("Bekor qilindi")
    await cb.message.answer("ℹ️ Omborga murojaat qilinmadi. Davom etishingiz mumkin.")

# ====== Materiallar oqimi ======
@router.callback_query(F.data.startswith("tech_mat_select_"))
async def tech_mat_select(cb: CallbackQuery, state: FSMContext):
    try:
        payload = cb.data[len("tech_mat_select_"):]
        material_id, req_id = map(int, payload.split("_", 1))
    except Exception:
        return await cb.answer("❌ Xato format", show_alert=True)

    user = await find_user_by_telegram_id(cb.from_user.id)
    if not user or user.get("role") != "technician":
        return await cb.answer("❌ Ruxsat yo‘q", show_alert=True)

    mat = await fetch_material_by_id(material_id)
    if not mat:
        return await cb.answer("❌ Material topilmadi", show_alert=True)

    assigned_left = await fetch_assigned_qty(user["id"], material_id)

    text = (
        "📦 <b>Miqdorni kiriting</b>\n\n"
        f"🆔 <b>Ariza ID:</b> {req_id}\n"
        f"📦 <b>Tanlangan mahsulot:</b> {esc(mat['name'])}\n"
        f"💰 <b>Narx:</b> {_fmt_price_uzs(mat['price'])} so'm\n"
        f"📊 <b>Sizga biriktirilgan qoldiq:</b> {assigned_left} dona\n\n"
        "📝 Iltimos, olinadigan miqdorni kiriting:\n"
        "• Faqat raqam (masalan: 2)\n\n"
        f"<i>Maksimal: {assigned_left} dona</i>"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"tech_qty_cancel_{req_id}")]
    ])

    await state.update_data(
        qty_ctx={
            "applications_id": req_id,
            "material_id": material_id,
            "material_name": mat["name"],
            "price": mat["price"],
            "max_qty": int(assigned_left),
        }
    )

    await cb.message.answer(text, reply_markup=kb, parse_mode="HTML")
    await state.set_state(QtyStates.waiting_qty)
    await cb.answer()

@router.callback_query(F.data.startswith("tech_qty_cancel_"))
async def tech_qty_cancel(cb: CallbackQuery, state: FSMContext):
    try:
        req_id = int(cb.data.replace("tech_qty_cancel_", ""))
    except Exception:
        return await cb.answer()

    user = await find_user_by_telegram_id(cb.from_user.id)
    if not user or user.get("role") != "technician":
        return await cb.answer("❌ Ruxsat yo‘q", show_alert=True)

    mats = await fetch_technician_materials(user_id=user["id"])
    header_text = (
        "📦 <b>Ombor jihozlari</b>\n"
        f"🆔 <b>Ariza ID:</b> {req_id}\n\n"
        "Kerakli jihozlarni tanlang yoki boshqa mahsulot kiriting:"
    )
    await cb.message.answer(header_text, reply_markup=materials_keyboard(mats, applications_id=req_id), parse_mode="HTML")
    await _preserve_mode_clear(state)   # <-- tech_mode saqlansin
    await cb.answer("Bekor qilindi")

@router.message(StateFilter(QtyStates.waiting_qty))
async def tech_qty_entered(msg: Message, state: FSMContext):
    user = await find_user_by_telegram_id(msg.from_user.id)
    if not user or user.get("role") != "technician":
        return await msg.answer("❌ Ruxsat yo‘q")

    data = await state.get_data()
    ctx = data.get("qty_ctx") or {}
    req_id = int(ctx.get("applications_id", 0))
    material_id = int(ctx.get("material_id", 0))
    max_qty = int(ctx.get("max_qty", 0))

    try:
        qty = int((msg.text or "").strip())
        if qty <= 0:
            return await msg.answer("❗️ Iltimos, 0 dan katta butun son kiriting.")
    except Exception:
        return await msg.answer("❗️ Faqat butun son kiriting (masalan: 2).")

    if qty > max_qty:
        return await msg.answer(f"❗️ Sizga biriktirilgan miqdor: {max_qty} dona. {max_qty} dan oshiq kiritib bo‘lmaydi.")

    try:
        await upsert_material_request_and_decrease_stock(
            user_id=user["id"],
            applications_id=req_id,
            material_id=material_id,
            add_qty=qty
        )
    except ValueError as ve:
        return await msg.answer(f"❌ {ve}")
    except Exception as e:
        return await msg.answer(f"❌ Xatolik: {e}")

    selected = await fetch_selected_materials_for_request(user["id"], req_id)
    lines = [
        "✅ <b>Tanlov saqlandi</b>\n",
        f"🆔 <b>Ariza ID:</b> {req_id}",
        "📦 <b>Tanlangan mahsulotlar:</b>"
    ]
    for it in selected:
        qty_txt = f"{it.get('description')} dona" if it.get('description') is not None else "-"
        lines.append(f"• {esc(it['name'])} — {qty_txt} (💰 {_fmt_price_uzs(it['price'])} so'm)")

    text = "\n".join(lines)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Yana material tanlash", callback_data=f"tech_add_more_{req_id}")],
        [InlineKeyboardButton(text="📋 Yakuniy ko‘rinish", callback_data=f"tech_review_{req_id}")]
    ])
    await msg.answer(text, reply_markup=kb, parse_mode="HTML")
    await _preserve_mode_clear(state)   # <-- tech_mode saqlansin

@router.callback_query(F.data.startswith("tech_back_to_materials_"))
async def tech_back_to_materials(cb: CallbackQuery, state: FSMContext):
    try:
        req_id = int(cb.data.replace("tech_back_to_materials_", ""))
    except Exception:
        return await cb.answer()

    user = await find_user_by_telegram_id(cb.from_user.id)
    if not user or user.get("role") != "technician":
        return await cb.answer("❌ Ruxsat yo‘q", show_alert=True)

    mats = await fetch_technician_materials(user_id=user["id"])
    header_text = (
        "📦 <b>Ombor jihozlari</b>\n"
        f"🆔 <b>Ariza ID:</b> {req_id}\n\n"
        "Kerakli jihozlarni tanlang yoki boshqa mahsulot kiriting:"
    )
    await cb.message.answer(header_text, reply_markup=materials_keyboard(mats, applications_id=req_id), parse_mode="HTML")
    await cb.answer()

@router.callback_query(F.data.startswith("tech_finish_"))
async def tech_finish(cb: CallbackQuery, state: FSMContext):
    try:
        req_id = int(cb.data.replace("tech_finish_", ""))
    except Exception:
        return await cb.answer()

    user = await find_user_by_telegram_id(cb.from_user.id)
    if not user or user.get("role") != "technician":
        return await cb.answer("❌ Ruxsat yo‘q", show_alert=True)

    st = await state.get_data()
    mode = st.get("tech_mode", "connection")

    selected = await fetch_selected_materials_for_request(user["id"], req_id)
    if not selected:
        return await cb.answer("⚠️ Avval hech bo‘lmasa bitta material tanlang.", show_alert=True)

    try:
        if mode == "technician":
            ok = await finish_technician_work_for_tech(applications_id=req_id, technician_id=user["id"])
        else:
            ok = await finish_technician_work(applications_id=req_id, technician_id=user["id"])
        if not ok:
            return await cb.answer("⚠️ Holat mos emas (faqat 'in_technician_work').", show_alert=True)
    except Exception as e:
        return await cb.answer(f"❌ Yakunlashda xatolik: {e}", show_alert=True)

    lines = [
        "✅ <b>Ish yakunlandi</b>\n",
        f"🆔 <b>Ariza ID:</b> {req_id}",
        "📦 <b>Ishlatilgan mahsulotlar:</b>"
    ]
    for it in selected:
        qty_txt = f"{it.get('description')} dona" if it.get('description') is not None else "-"
        lines.append(f"• {esc(it['name'])} — {qty_txt}")
    await cb.message.answer("\n".join(lines), parse_mode="HTML")
    await cb.answer("Yakunlandi ✅")

@router.callback_query(F.data.startswith("tech_add_more_"))
async def tech_add_more(cb: CallbackQuery, state: FSMContext):
    req_id = int(cb.data.replace("tech_add_more_", ""))
    user = await find_user_by_telegram_id(cb.from_user.id)
    if not user or user.get("role") != "technician":
        return await cb.answer("❌ Ruxsat yo‘q", show_alert=True)

    mats = await fetch_technician_materials(user_id=user["id"])
    header_text = (
        "📦 <b>Ombor jihozlari</b>\n"
        f"🆔 <b>Ariza ID:</b> {req_id}\n\n"
        "Kerakli jihozlarni tanlang yoki boshqa mahsulot kiriting:"
    )
    await cb.message.answer(header_text, reply_markup=materials_keyboard(mats, applications_id=req_id), parse_mode="HTML")
    await cb.answer()

@router.callback_query(F.data.startswith("tech_review_"))
async def tech_review(cb: CallbackQuery, state: FSMContext):
    req_id = int(cb.data.replace("tech_review_", ""))
    user = await find_user_by_telegram_id(cb.from_user.id)
    if not user or user.get("role") != "technician":
        return await cb.answer("❌ Ruxsat yo‘q", show_alert=True)

    selected = await fetch_selected_materials_for_request(user["id"], req_id)
    if not selected:
        return await cb.answer("⚠️ Hali material tanlamadingiz.", show_alert=True)

    lines = [
        "📋 <b>Yakuniy ko‘rinish</b>\n",
        f"🆔 <b>Ariza ID:</b> {req_id}",
        "📦 <b>Ishlatiladigan mahsulotlar:</b>"
    ]
    for it in selected:
        qty_txt = f"{it.get('description')} dona" if it.get('description') is not None else "-"
        lines.append(f"• {esc(it['name'])} — {qty_txt} (💰 {_fmt_price_uzs(it['price'])} so'm)")

    text = "\n".join(lines)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Ishni yakunlash", callback_data=f"tech_finish_{req_id}")],
        [InlineKeyboardButton(text="⬅️ Orqaga qaytish", callback_data=f"tech_back_to_materials_{req_id}")]
    ])
    await cb.message.answer(text, reply_markup=kb, parse_mode="HTML")
    await cb.answer()
