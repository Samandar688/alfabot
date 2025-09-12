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
    fetch_technician_inbox,
    cancel_technician_request,
    accept_technician_work,
    start_technician_work,
    fetch_technician_materials,
    finish_technician_work,
    fetch_selected_materials_for_request,
    fetch_material_by_id,
    fetch_assigned_qty,
    upsert_material_request_and_decrease_stock,
)

class QtyStates(StatesGroup):
    waiting_qty = State()

router = Router()
router.message.filter(RoleFilter("technician"))
router.callback_query.filter(RoleFilter("technician"))

# ---------- yordamchilar ----------
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
        "completed": "✅",   # <— add this
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

def action_keyboard(item_id: int, index: int, total: int, status: str) -> InlineKeyboardMarkup:
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
    # Maxsus tugmalar
    rows.append([InlineKeyboardButton(text="➕ Boshqa mahsulot", callback_data=f"tech_mat_custom_{applications_id}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

# ---------- Inbox ochish ----------
@router.message(F.text.in_(["📥 Inbox", "Inbox"]))
async def tech_open_inbox(message: Message, state: FSMContext):
    user = await find_user_by_telegram_id(message.from_user.id)
    if not user or user.get("role") != "technician":
        return

    tech_id = user["id"]
    items = await fetch_technician_inbox(technician_id=tech_id, limit=50, offset=0)
    items = _dedup_by_id(items)

    if not items:
        await message.answer("📭 Inbox bo‘sh")
        return

    total = len(items)
    await state.update_data(tech_inbox=items, tech_idx=0)

    item = items[0]
    text = short_view_text(item, 0, total)
    kb = action_keyboard(item.get("id"), 0, total, item.get("status", ""))
    await message.answer(text, reply_markup=kb, parse_mode="HTML")

# ---------- Oldingi / Keyingi ----------
@router.callback_query(F.data.startswith("tech_inbox_prev_"))
async def tech_prev(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    items = _dedup_by_id(data.get("tech_inbox", []))
    if not items:
        return
    total = len(items)
    idx_now = int(cb.data.replace("tech_inbox_prev_", ""))
    idx = idx_now - 1
    if idx < 0 or idx >= total:
        return

    await state.update_data(tech_inbox=items, tech_idx=idx)
    item = items[idx]
    text = short_view_text(item, idx, total)
    kb = action_keyboard(item.get("id"), idx, total, item.get("status", ""))
    await _safe_edit(cb.message, text, kb)

@router.callback_query(F.data.startswith("tech_inbox_next_"))
async def tech_next(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    items = _dedup_by_id(data.get("tech_inbox", []))
    if not items:
        return
    total = len(items)
    idx_now = int(cb.data.replace("tech_inbox_next_", ""))
    idx = idx_now + 1
    if idx < 0 or idx >= total:
        return

    await state.update_data(tech_inbox=items, tech_idx=idx)
    item = items[idx]
    text = short_view_text(item, idx, total)
    kb = action_keyboard(item.get("id"), idx, total, item.get("status", ""))
    await _safe_edit(cb.message, text, kb)

# ---------- Ishni qabul qilish ----------
@router.callback_query(F.data.startswith("tech_accept_"))
async def tech_accept(cb: CallbackQuery, state: FSMContext):
    user = await find_user_by_telegram_id(cb.from_user.id)
    if not user or user.get("role") != "technician":
        return await cb.answer("❌ Ruxsat yo‘q", show_alert=True)

    req_id = int(cb.data.replace("tech_accept_", ""))

    # 1) DB
    try:
        ok = await accept_technician_work(applications_id=req_id, technician_id=user["id"])
        if not ok:
            return await cb.answer("⚠️ Holat mos emas yoki ariza topilmadi.", show_alert=True)
    except Exception as e:
        return await cb.answer(f"❌ Xatolik: {e}", show_alert=True)

    # 2) Lokal yangilash
    data = await state.get_data()
    items = _dedup_by_id(data.get("tech_inbox", []))
    idx = int(data.get("tech_idx", 0))

    current = None
    if 0 <= idx < len(items) and items[idx].get("id") == req_id:
        items[idx]["status"] = "in_technician"
        current = items[idx]
    else:
        for it in items:
            if it.get("id") == req_id:
                it["status"] = "in_technician"
                current = it
                break

    await state.update_data(tech_inbox=items)

    total = len(items)
    if idx >= total:
        idx = total - 1
    item = items[idx] if current is None else current
    text = short_view_text(item, idx, total)
    kb = action_keyboard(item.get("id"), idx, total, item.get("status", ""))

    await _safe_edit(cb.message, text, kb)
    await cb.answer("✅ Ish qabul qilindi")

# ---------- Bekor qilish ----------
@router.callback_query(F.data.startswith("tech_cancel_"))
async def tech_cancel(cb: CallbackQuery, state: FSMContext):
    user = await find_user_by_telegram_id(cb.from_user.id)
    if not user or user.get("role") != "technician":
        return await cb.answer("❌ Ruxsat yo‘q", show_alert=True)

    req_id = int(cb.data.replace("tech_cancel_", ""))

    try:
        await cancel_technician_request(applications_id=req_id, technician_id=user["id"])
    except Exception as e:
        return await cb.answer(f"❌ Xatolik: {e}", show_alert=True)

    data = await state.get_data()
    items = _dedup_by_id(data.get("tech_inbox", []))
    idx = int(data.get("tech_idx", 0))

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
    kb = action_keyboard(item.get("id"), idx, total, item.get("status", ""))
    await _safe_edit(cb.message, text, kb)

# ---------- Ishni boshlash ----------
@router.callback_query(F.data.startswith("tech_start_"))
async def tech_start(cb: CallbackQuery, state: FSMContext):
    user = await find_user_by_telegram_id(cb.from_user.id)
    if not user or user.get("role") != "technician":
        return await cb.answer("❌ Ruxsat yo‘q", show_alert=True)

    req_id = int(cb.data.replace("tech_start_", ""))

    try:
        ok = await start_technician_work(applications_id=req_id, technician_id=user["id"])
        if not ok:
            return await cb.answer("⚠️ Holat mos emas (faqat 'in_technician').", show_alert=True)
    except Exception as e:
        return await cb.answer(f"❌ Xatolik: {e}", show_alert=True)

    await cb.answer("✅ Ish boshlandi")

    # STATE tiklash
    data = await state.get_data()
    items = _dedup_by_id(data.get("tech_inbox", []))
    idx = int(data.get("tech_idx", 0))

    if not items:
        try:
            items = await fetch_technician_inbox(technician_id=user["id"], limit=50, offset=0)
            items = _dedup_by_id(items)
            idx = 0
        except Exception:
            items = []
            idx = 0

    current = None
    for it in items:
        if it.get("id") == req_id:
            it["status"] = "in_technician_work"
            current = it
            break

    total = len(items)
    if total > 0:
        if idx < 0 or idx >= total:
            idx = 0
        await state.update_data(tech_inbox=items, tech_idx=idx)

        item_to_show = current or items[idx]
        text = short_view_text(item_to_show, idx, total)
        kb = action_keyboard(item_to_show.get("id"), idx, total, item_to_show.get("status", ""))
        try:
            await _safe_edit(cb.message, text, kb)
        except Exception:
            await cb.message.answer(text, reply_markup=kb, parse_mode="HTML")
    else:
        await state.update_data(tech_inbox=[], tech_idx=0)
        await cb.message.answer("ℹ️ Inbox ro‘yxati yangilandi yoki bo‘sh. Davom etamiz.", parse_mode="HTML")

    # Materiallar menyusi
    mats = await fetch_technician_materials(user_id=user["id"])
    header_text = "📦 <b>Ombor jihozlari</b>\n" \
                  f"🆔 <b>Ariza ID:</b> {req_id}\n" \
                  "Kerakli jihozlarni tanlang yoki boshqa mahsulot kiriting:"
    if not mats:
        await cb.message.answer(
            header_text + "\n\nℹ️ Hozircha sizga biriktirilgan jihozlar topilmadi.",
            reply_markup=materials_keyboard([], applications_id=req_id),
            parse_mode="HTML"
        )
    else:
        info_lines = ["\n<b>Sizga biriktirilgan materiallar:</b>"]
        for i, m in enumerate(mats, 1):
            info_lines.append(
                f"{i}) {esc(m['name'])} — {_fmt_price_uzs(m['price'])} so'm"
                f" | S/N: {esc(m.get('serial_number') or '-')} | Biriktirilgan: {m['stock_quantity']} dona"
            )
        await cb.message.answer("\n".join([header_text, *info_lines]), parse_mode="HTML",
                                reply_markup=materials_keyboard(mats, applications_id=req_id))

# ---------- Material tanlash ----------
@router.callback_query(F.data.startswith("tech_mat_select_"))
async def tech_mat_select(cb: CallbackQuery, state: FSMContext):
    # format: tech_mat_select_{material_id}_{applications_id}
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

# ---------- Miqdorni kiritish ----------
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
    await state.clear()
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

    # Raqam tekshiruvi
    try:
        qty = int(msg.text.strip())
        if qty <= 0:
            return await msg.answer("❗️ Iltimos, 0 dan katta butun son kiriting.")
    except Exception:
        return await msg.answer("❗️ Faqat butun son kiriting (masalan: 2).")

    if qty > max_qty:
        return await msg.answer(f"❗️ Sizga biriktirilgan miqdor: {max_qty} dona. {max_qty} dan oshiq kiritib bo‘lmaydi.")

    # UPSERT + texnik qoldiqdan ayirish (tranzaksiya)
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

    # Xulosa
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
    await state.clear()

# ---------- Review / Back / Finish ----------
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

    selected = await fetch_selected_materials_for_request(user["id"], req_id)
    if not selected:
        return await cb.answer("⚠️ Avval hech bo‘lmasa bitta material tanlang.", show_alert=True)

    try:
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
    text = "\n".join(lines)

    await cb.message.answer(text, parse_mode="HTML")
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
