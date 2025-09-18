from aiogram import Router, F
from aiogram.types import Message
from filters.role_filter import RoleFilter
router = Router()
router.message.filter(RoleFilter("callcenter_operator"))
router.callback_query.filter(RoleFilter("callcenter_operator"))

@router.message(F.text.in_(["📊 Statistikalar", "📊 Статистика"]))
async def statistics_handler(message: Message):
    await message.answer("📊 Statistikalar\n\nBu yerda call center statistikasi ko'rsatiladi.\n\n👤 Rol: Call Center")
