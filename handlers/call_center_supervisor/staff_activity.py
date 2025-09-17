from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from filters.role_filter import RoleFilter
from database.queries import find_user_by_telegram_id
from database.call_supervisor_static_queries import (
    get_active_connection_tasks_count,
    get_callcenter_operator_count,
    get_operator_orders_stat,
    get_canceled_connection_tasks_count,
)

router = Router()
router.message.filter(RoleFilter("callcenter_supervisor"))
router.callback_query.filter(RoleFilter("callcenter_supervisor"))

# ---------- UI helperlar ----------

def _menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Asosiy inline menyu."""
    rows = [
        [InlineKeyboardButton(
            text="👤 Xodimlar kesimi" if lang == "uz" else "👤 Срез по сотрудникам",
            callback_data="staff:cut"
        )],
        [InlineKeyboardButton(
            text="♻️ Yangilash" if lang == "uz" else "♻️ Обновить",
            callback_data="staff:refresh"
        )],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)

def _back_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Orqaga tugmasi."""
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
            text="🔙 Orqaga" if lang == "uz" else "🔙 Назад",
            callback_data="staff:back"
        )]]
    )

def _card_text(active_tasks: int, co_count: int, canceled_tasks: int, lang: str) -> str:
    """Kartochkadagi matn."""
    if lang == "uz":
        return (
            "👥 Xodimlar faoliyati\n\n"
            f"🧾 Aktiv arizalar: {active_tasks}\n"
            f"🧑‍💼 Umumiy xodimlar: {co_count}\n"
            f"❌ Bekor qilingan arizalar: {canceled_tasks}\n\n"
            "Quyidagi bo‘limlardan birini tanlang:"
        )
    else:
        return (
            "👥 Активность сотрудников\n\n"
            f"🧾 Активные заявки: {active_tasks}\n"
            f"🧑‍💼 Всего сотрудников: {co_count}\n"
            f"❌ Отмененные заявки: {canceled_tasks}\n\n"
            "Выберите один из разделов ниже:"
        )

# ---------- Asosiy handler ----------

@router.message(F.text.in_(["👥 Xodimlar faoliyati", "👥 Активность сотрудников"]))
async def staff_activity_entry(message: Message, state: FSMContext):
    """Reply keyboarddan kelgan matnni qabul qiladi."""
    user = await find_user_by_telegram_id(message.from_user.id)
    lang = getattr(user, "lang", "uz")  # default = uz

    active_tasks = await get_active_connection_tasks_count()
    co_count = await get_callcenter_operator_count()
    canceled_tasks = await get_canceled_connection_tasks_count()

    await message.answer(
        _card_text(active_tasks, co_count, canceled_tasks, lang),
        reply_markup=_menu_keyboard(lang)
    )

# ---------- Callbacklar ----------

@router.callback_query(F.data == "staff:cut")
async def staff_cut(call: CallbackQuery, state: FSMContext):
    user = await find_user_by_telegram_id(call.from_user.id)
    lang = getattr(user, "lang", "uz")

    try:
        operator_stats = await get_operator_orders_stat()

        if not operator_stats:
            text = (
                "📊 Hozircha hech bir operator ariza yaratmagan."
                if lang == "uz"
                else "📊 Пока что ни один оператор не создал заявку."
            )
        else:
            text = (
                "📊 Hodimlar kesimi:\n\n"
                if lang == "uz" else
                "📊 Срез по сотрудникам:\n\n"
            )
            for i, op in enumerate(operator_stats, 1):
                if lang == "uz":
                    text += (
                        f"{i}. {op['full_name']}\n"
                        f"   ├ Connection: {op['connection_count']} ta\n"
                        f"   └ Technician: {op['technician_count']} ta\n\n"
                    )
                else:
                    text += (
                        f"{i}. {op['full_name']}\n"
                        f"   ├ Подключение: {op['connection_count']} заявок\n"
                        f"   └ Техник: {op['technician_count']} заявок\n\n"
                    )

        await call.message.edit_text(text, reply_markup=_back_keyboard(lang))
        await call.answer()

    except Exception:
        await call.answer(
            "Xatolik yuz berdi" if lang == "uz" else "Произошла ошибка",
            show_alert=True
        )

@router.callback_query(F.data == "staff:jm")
async def staff_jm(call: CallbackQuery, state: FSMContext):
    user = await find_user_by_telegram_id(call.from_user.id)
    lang = getattr(user, "lang", "uz")

    await call.answer()
    await _safe_edit(
        call,
        (
            "🧑‍💼 callcenter_operator ishlari\n\n"
            "• Biriktirilgan aktiv ishlar\n"
            "• Yakunlash tezligi va kechikishlar\n"
            "• Qayta ishlashlar va mijoz fikrlari\n"
            "• O‘qitish/ko‘mak ehtiyojlari"
            if lang == "uz" else
            "🧑‍💼 Работа операторов\n\n"
            "• Закрепленные активные задачи\n"
            "• Скорость выполнения и задержки\n"
            "• Повторные заявки и отзывы клиентов\n"
            "• Необходимость обучения/поддержки"
        ),
        _back_keyboard(lang)
    )

@router.callback_query(F.data == "staff:refresh")
async def staff_refresh(call: CallbackQuery, state: FSMContext):
    user = await find_user_by_telegram_id(call.from_user.id)
    lang = getattr(user, "lang", "uz")

    await call.answer("Yangilanmoqda…" if lang == "uz" else "Обновляется…")

    active_tasks = await get_active_connection_tasks_count()
    co_count = await get_callcenter_operator_count()
    canceled_tasks = await get_canceled_connection_tasks_count()

    await _safe_edit(
        call,
        _card_text(active_tasks, co_count, canceled_tasks, lang),
        _menu_keyboard(lang)
    )

@router.callback_query(F.data == "staff:back")
async def staff_back(call: CallbackQuery, state: FSMContext):
    user = await find_user_by_telegram_id(call.from_user.id)
    lang = getattr(user, "lang", "uz")

    await call.answer()

    active_tasks = await get_active_connection_tasks_count()
    co_count = await get_callcenter_operator_count()
    canceled_tasks = await get_canceled_connection_tasks_count()

    await _safe_edit(
        call,
        _card_text(active_tasks, co_count, canceled_tasks, lang),
        _menu_keyboard(lang)
    )

# ---------- Utility ----------

async def _safe_edit(call: CallbackQuery, text: str, kb: InlineKeyboardMarkup):
    """Xabarni xavfsiz tahrirlash."""
    try:
        await call.message.edit_text(text, reply_markup=kb)
    except TelegramBadRequest:
        await call.message.answer(text, reply_markup=kb)
