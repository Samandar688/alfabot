# handlers/manager/staff_activity.py
# Faqat INLINE tugmalar bilan ishlaydi. Reply keyboard yuborilmaydi.
# Kartochka: "Xodimlar faoliyati" — statistikalar va bo‘limlar.

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from filters.role_filter import RoleFilter
from database.queries import find_user_by_telegram_id
from database.manager_staff_activity import (
    get_active_connection_tasks_count,
    get_junior_manager_count,
)


router = Router()
router.message.filter(RoleFilter("manager"))
router.callback_query.filter(RoleFilter("manager"))

# ---------- UI helperlar ----------

def _menu_keyboard() -> InlineKeyboardMarkup:
    """
    Asosiy inline menyu (rasmdagi kabi):
      📊 Samaradorlik | 📈 Ish yuki | 👤 Xodimlar kesimi
      🧑‍💼 Kichik menejerlar ishlari | ♻️ Yangilash | 🔙 Orqaga
    """
    rows = [
        [InlineKeyboardButton(text="📊 Samaradorlik", callback_data="staff:eff")],
        [InlineKeyboardButton(text="📈 Ish yuki", callback_data="staff:load")],
        [InlineKeyboardButton(text="👤 Xodimlar kesimi", callback_data="staff:cut")],
        [InlineKeyboardButton(text="🧑‍💼 Kichik menejerlar ishlari", callback_data="staff:jm")],
        [InlineKeyboardButton(text="♻️ Yangilash", callback_data="staff:refresh")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="staff:back")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)

def _back_keyboard() -> InlineKeyboardMarkup:
    """Bo‘lim matnlari ostida faqat “Orqaga” tugmasi."""
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Orqaga", callback_data="staff:back")]]
    )

def _card_text(active_tasks: int, jm_count: int) -> str:
    """
    Kartochkadagi matn. Eslatma: sonlar DB’dan olinadi.
    - Aktiv vazifalar: connection_orders (is_active = TRUE, status <> 'completed')
    - Umumiy xodimlar: users (role = 'junior_manager')
    """
    return (
        "👥 Xodimlar faoliyati\n\n"
        f"🧾 Aktiv vazifalar: {active_tasks}\n"
        f"🧑‍💼 Umumiy xodimlar: {jm_count}\n\n"
        "Quyidagi bo‘limlardan birini tanlang:"
    )

# ---------- Asosiy handler ----------

@router.message(F.text.in_(["👥 Xodimlar faoliyati", "👥 Активность сотрудников"]))
async def staff_activity_entry(message: Message, state: FSMContext):
    """
    Reply keyboarddan kelgan matnni qabul qiladi,
    lekin ichkarida faqat INLINE bilan ishlaymiz.
    """
    # (Ixtiyoriy) foydalanuvchi tilini aniqlab olishingiz mumkin
    _ = await find_user_by_telegram_id(message.from_user.id)

    active_tasks = await get_active_connection_tasks_count()
    jm_count = await get_junior_manager_count()

    await message.answer(
        _card_text(active_tasks, jm_count),
        reply_markup=_menu_keyboard()
    )

# ---------- Callbacklar (bo‘lim izohlari va yangilash) ----------

@router.callback_query(F.data == "staff:eff")
async def staff_efficiency(call: CallbackQuery, state: FSMContext):
    """
    📊 Samaradorlik — KPI va sifat ko‘rsatkichlari sahifasi.
    Keyinchalik grafik/statistik funksiyalar shu yerdan chaqiriladi.
    """
    await call.answer()
    await _safe_edit(
        call,
        "📊 Samaradorlik\n\n"
        "• O‘rtacha bajarish vaqti\n"
        "• O‘z vaqtida/kechikkan ishlar ulushi\n"
        "• Eng samarali xodimlar TOP-5\n"
        "• Muammolar toifasi bo‘yicha kesim",
        _back_keyboard()
    )

@router.callback_query(F.data == "staff:load")
async def staff_workload(call: CallbackQuery, state: FSMContext):
    """
    📈 Ish yuki — xodim boshiga aktiv vazifalar, navbatlar, pik soatlar.
    """
    await call.answer()
    await _safe_edit(
        call,
        "📈 Ish yuki\n\n"
        "• Xodim boshiga aktiv vazifalar soni\n"
        "• Yangi kelayotgan ishlar oqimi (soat/kun)\n"
        "• Ustuvor navbatlar va taqsimot\n"
        "• Pik vaqtlar va teng taqsimlanmaslik",
        _back_keyboard()
    )

@router.callback_query(F.data == "staff:cut")
async def staff_cut(call: CallbackQuery, state: FSMContext):
    """
    👤 Xodimlar kesimi — lavozim, hudud, smena va tajriba bo‘yicha statistik ko‘rinish.
    """
    await call.answer()
    await _safe_edit(
        call,
        "👤 Xodimlar kesimi\n\n"
        "• Lavozimlar bo‘yicha son/ulush\n"
        "• Hudud/smena bo‘yicha taqsimot\n"
        "• Tajriba darajasi va faol/ta’til holatlari",
        _back_keyboard()
    )

@router.callback_query(F.data == "staff:jm")
async def staff_jm(call: CallbackQuery, state: FSMContext):
    """
    🧑‍💼 Kichik menejerlar ishlari — junior_manager’lar faoliyati.
    """
    await call.answer()
    await _safe_edit(
        call,
        "🧑‍💼 Kichik menejerlar ishlari\n\n"
        "• Biriktirilgan aktiv ishlar\n"
        "• Yakunlash tezligi va kechikishlar\n"
        "• Qayta ishlashlar va mijoz fikrlari\n"
        "• O‘qitish/ko‘mak ehtiyojlari",
        _back_keyboard()
    )

@router.callback_query(F.data == "staff:refresh")
async def staff_refresh(call: CallbackQuery, state: FSMContext):
    """
    ♻️ Yangilash — sonlarni DB’dan qayta olib, kartochkani EDIT qiladi.
    """
    await call.answer("Yangilanmoqda…")
    active_tasks = await get_active_connection_tasks_count()
    jm_count = await get_junior_manager_count()
    await _safe_edit(call, _card_text(active_tasks, jm_count), _menu_keyboard())

@router.callback_query(F.data == "staff:back")
async def staff_back(call: CallbackQuery, state: FSMContext):
    """
    🔙 Orqaga — asosiy kartochkaga qaytish (INLINE bilan).
    """
    await call.answer()
    active_tasks = await get_active_connection_tasks_count()
    jm_count = await get_junior_manager_count()
    await _safe_edit(call, _card_text(active_tasks, jm_count), _menu_keyboard())

# ---------- Kichik utility ----------

async def _safe_edit(call: CallbackQuery, text: str, kb: InlineKeyboardMarkup):
    """
    Xabarni tahrirlash. Agar tahrirlab bo‘lmasa (masalan, eski matn bilan bir xil),
    yangi xabar sifatida yuboradi.
    """
    try:
        await call.message.edit_text(text, reply_markup=kb)
    except TelegramBadRequest:
        await call.message.answer(text, reply_markup=kb)
