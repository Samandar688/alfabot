from aiogram import Router, F
from aiogram.types import Message
from filters.role_filter import RoleFilter

router = Router()

@router.message(RoleFilter("controller"), F.text.in_(["🕐 Real vaqtda kuzatish", "🕐 Мониторинг в реальном времени"]))
async def realtime_monitoring_handler(message: Message):
    await message.answer("🕐 Real vaqtda kuzatish\n\nBu yerda real vaqtda monitoring ko'rsatiladi.\n\n👤 Rol: Controller")
