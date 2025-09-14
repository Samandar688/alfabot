from aiogram import Router, F
from aiogram.types import Message
from filters.role_filter import RoleFilter

router = Router()
router.message.filter(RoleFilter("Admin"))
router.callback_query.filter(RoleFilter("Admin"))

@router.message(F.text.in_(["📊 Statistika", "📊 Статистика"]))
async def statistics_handler(message: Message):
    await message.answer("📊 Statistika bo'limi\n\nBu yerda umumiy statistika ko'rsatiladi.\n\n👤 Rol: Admin")
