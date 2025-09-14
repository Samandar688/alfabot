# handlers/manager/applications.py
# Maqsad: "📋 Arizalarni ko'rish" bo'limi faqat INLINE tugmalar bilan ishlasin.
# Bu handler faqat menejer (manager) roli uchun filtrlangan.

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
import html  # matnlarni HTML formatida xavfsiz chiqarish uchun

from filters.role_filter import RoleFilter

# E’TIBOR: Query’lar bitta faylda — siz xohlagancha shu importlarni qoldirdim.
from database.manager_application import (
    get_total_orders_count,
    get_new_orders_today_count,
    get_in_progress_count,
    get_completed_today_count,
    get_cancelled_count,
)
from database.manager_application import (
    list_new_orders,
    list_in_progress_orders,
    list_completed_today_orders,
    list_cancelled_orders,
)

from filters.role_filter import RoleFilter

router = Router()
<<<<<<< HEAD
router.message.filter(RoleFilter("manager"))
router.callback_query.filter(RoleFilter("manager"))

# ---------------- UI helperlar ----------------

def _apps_menu_kb() -> InlineKeyboardMarkup:
    """
    Asosiy inline menyu (kartochka ostida).
    """
    rows = [
        [InlineKeyboardButton(text="🆕 Yangi buyurtmalar", callback_data="apps:new")],
        [InlineKeyboardButton(text="⏳ Jarayondagilar", callback_data="apps:progress")],
        [InlineKeyboardButton(text="✅ Bugun bajarilgan", callback_data="apps:done_today")],
        [InlineKeyboardButton(text="❌ Bekor qilinganlar", callback_data="apps:cancelled")],
        [InlineKeyboardButton(text="♻️ Yangilash", callback_data="apps:refresh")],
        [InlineKeyboardButton(text="📑 Hisobot", callback_data="apps:report")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)

def _back_kb() -> InlineKeyboardMarkup:
    """
    Bo'lim sahifalarida ko'rsatiladigan "Orqaga" tugmasi.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Orqaga", callback_data="apps:back")]]
    )

def _card_text(total: int, new_today: int, in_progress: int, done_today: int, cancelled: int) -> str:
    """
    Asosiy kartochka matni (statistika).
    """
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

def _fmt_dt(dt) -> str:
    """
    Sana/vaqtni chiroyli ko'rinishda chiqarish.
    """
    try:
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return str(dt) if dt else "-"

def _esc(x: str | None) -> str:
    """
    HTML chiqishda xatoga yo'l qo'ymaslik uchun escapelash.
    """
    return html.escape(x or "-")

def _fmt_list(prefix: str, items: list[dict]) -> str:
    """
    Ro'yxat matnini yig'ish. Juda uzun bo'lib ketmasligi uchun qisqa format.
    """
    if not items:
        return f"{prefix}\n\n— Hech narsa topilmadi."
    lines = [prefix, ""]
    for r in items:
        lines.append(
            f"#{r.get('id')} • {_esc(r.get('client_name'))} ({_esc(r.get('client_phone'))})\n"
            f"📍 {_esc(r.get('address'))}\n"
            f"🛈 {_esc(str(r.get('status')))} • ⏱ {_fmt_dt(r.get('created_at'))}"
        )
        lines.append("— — —")
    # oxirgi ajratgichni olib tashlaymiz
    return "\n".join(lines[:-1])

async def _load_stats():
    """
    Statistika sonlarini bir joyda yig'ib qaytarish.
    """
    total = await get_total_orders_count()
    new_today = await get_new_orders_today_count()
    in_progress = await get_in_progress_count()
    done_today = await get_completed_today_count()
    cancelled = await get_cancelled_count()
    return total, new_today, in_progress, done_today, cancelled

async def _safe_edit(call: CallbackQuery, text: str, kb: InlineKeyboardMarkup):
    """
    Xabarni tahrirlash. Agar tahrirlab bo'lmasa (masalan, matn bir xil),
    yangi xabar sifatida yuboradi.
    """
    try:
        await call.message.edit_text(text, reply_markup=kb)
    except TelegramBadRequest:
        await call.message.answer(text, reply_markup=kb)

# ---------------- Kirish (reply tugmadan) ----------------
=======
router.message.filter(RoleFilter("Admin"))
router.callback_query.filter(RoleFilter("Admin"))
>>>>>>> 327c05a31618b997091abaefeaaf85d47fc33151

@router.message(F.text.in_(["📋 Arizalarni ko'rish", "📋 Все заявки"]))
async def applications_handler(message: Message, state: FSMContext):
    """
    Reply keyboarddan "📋 Arizalarni ko'rish" bosilganda — asosiy kartochkani chiqaradi.
    Keyingi barcha navigatsiya faqat INLINE tugmalar bilan bo'ladi.
    """
    total, new_today, in_progress, done_today, cancelled = await _load_stats()
    await message.answer(
        _card_text(total, new_today, in_progress, done_today, cancelled),
        reply_markup=_apps_menu_kb()
    )

# ---------------- Ro'yxatlar va bo'limlar ----------------

@router.callback_query(F.data == "apps:new")
async def apps_new(call: CallbackQuery, state: FSMContext):
    """
    🆕 Yangi buyurtmalar ro'yxati:
      • is_active = TRUE
      • status = 'in_manager'
    """
    await call.answer()
    items = await list_new_orders(limit=20)
    await _safe_edit(call, _fmt_list("🆕 <b>Yangi buyurtmalar</b>", items), _back_kb())

@router.callback_query(F.data == "apps:progress")
async def apps_progress(call: CallbackQuery, state: FSMContext):
    """
    ⏳ Jarayondagilar ro'yxati:
      • is_active = TRUE
      • status <> 'completed'
    """
    await call.answer()
    items = await list_in_progress_orders(limit=20)
    await _safe_edit(call, _fmt_list("⏳ <b>Jarayondagilar</b>", items), _back_kb())

@router.callback_query(F.data == "apps:done_today")
async def apps_done_today(call: CallbackQuery, state: FSMContext):
    """
    ✅ Bugun bajarilgan ro'yxati:
      • status = 'completed'
      • DATE(updated_at) = CURRENT_DATE
    (Eslatma: ro'yxatda updated_at bo'yicha filtr ishlatiladi — sizning talabingizga ko'ra.)
    """
    await call.answer()
    items = await list_completed_today_orders(limit=20)
    await _safe_edit(call, _fmt_list("✅ <b>Bugun bajarilgan</b>", items), _back_kb())

@router.callback_query(F.data == "apps:cancelled")
async def apps_cancelled(call: CallbackQuery, state: FSMContext):
    """
    ❌ Bekor qilinganlar ro'yxati:
      • is_active = FALSE
    """
    await call.answer()
    items = await list_cancelled_orders(limit=20)
    await _safe_edit(call, _fmt_list("❌ <b>Bekor qilinganlar</b>", items), _back_kb())

# ---------------- Hozircha placeholderlar ----------------

@router.callback_query(F.data == "apps:refresh")
async def apps_refresh(call: CallbackQuery, state: FSMContext):
    """
    ♻️ Kartochka statistikalarini qayta yuklash.
    """
    await call.answer("Yangilanmoqda…")
    total, new_today, in_progress, done_today, cancelled = await _load_stats()
    await _safe_edit(
        call,
        _card_text(total, new_today, in_progress, done_today, cancelled),
        _apps_menu_kb()
    )

@router.callback_query(F.data == "apps:report")
async def apps_report(call: CallbackQuery, state: FSMContext):
    """
    📑 Hisobot — hozircha oddiy xabar (keyin CSV/Excel/grafik qo'shamiz).
    """
    await call.answer()
    await _safe_edit(call, "📑 <b>Hisobot</b>\n\nBu bo‘lim keyinroq to‘ldiriladi.", _back_kb())

@router.callback_query(F.data == "apps:back")
async def apps_back(call: CallbackQuery, state: FSMContext):
    """
    🔙 Asosiy kartochkaga qaytish.
    """
    await call.answer()
    total, new_today, in_progress, done_today, cancelled = await _load_stats()
    await _safe_edit(
        call,
        _card_text(total, new_today, in_progress, done_today, cancelled),
        _apps_menu_kb()
    )
