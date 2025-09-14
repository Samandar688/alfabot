# handlers/junior_manager/stats.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from datetime import timezone, timedelta

from filters.role_filter import RoleFilter
from database.junior_manager_statistika_queries import get_jm_stats_for_telegram

router = Router()
# Agar sizda RoleFilter nomi boshqacha bo‘lsa (masalan, "manager"),
# shu joyni moslab qo‘ying:
router.message.filter(RoleFilter("junior_manager"))
router.callback_query.filter(RoleFilter("junior_manager"))

def _tz():
    try:
        return ZoneInfo("Asia/Tashkent")
    except Exception:
        return timezone(timedelta(hours=5))

def _fmt_block(title: str, row: dict) -> str:
    return (
        f"• Qabul qilingan: <b>{row['received']}</b>\n"
        f"• Controllerga yuborilgan: <b>{row['sent_to_controller']}</b>\n"
        f"• Yuborganlaridan <code>completed</code>: <b>{row['completed_from_sent']}</b>\n"
    )

def _fmt_stats(stats: dict) -> str:
    # stats = {"today": {...}, "7d": {...}, "10d": {...}, "30d": {...}}
    lines = [
        "📊 <b>Junior Manager — Statistika</b>\n",
        "📅 <b>Bugun</b>",
        _fmt_block("Bugun", stats["today"]),
        "🗓 <b>So‘nggi 7 kun</b>",
        _fmt_block("7d", stats["7d"]),
        "🗓 <b>So‘nggi 10 kun</b>",
        _fmt_block("10d", stats["10d"]),
        "🗓 <b>So‘nggi 30 kun</b>",
        _fmt_block("30d", stats["30d"]),
    ]
    return "\n".join(lines)

# --- Text tugma (masalan: "📊 Statistika") ---
@router.message(F.text.in_(["📊 Statistika", "Statistika"]))
async def jm_stats_msg(msg: Message, state: FSMContext):
    tg_id = msg.from_user.id
    stats = await get_jm_stats_for_telegram(tg_id, tz=_tz())
    if stats is None:
        await msg.answer("Foydalanuvchi profili topilmadi (users jadvali bilan moslik yo‘q).")
        return
    await msg.answer(_fmt_stats(stats))

# --- Callback tugma (agar sizda inline keyboardda bo‘lsa) ---
@router.callback_query(F.data == "jm_stats")
async def jm_stats_cb(cb: CallbackQuery, state: FSMContext):
    tg_id = cb.from_user.id
    stats = await get_jm_stats_for_telegram(tg_id, tz=_tz())
    if stats is None:
        await cb.message.edit_text("Foydalanuvchi profili topilmadi (users jadvali bilan moslik yo‘q).")
        return
    await cb.message.edit_text(_fmt_stats(stats))
