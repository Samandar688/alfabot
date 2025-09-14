from aiogram import Router, F
from aiogram.types import Message
from filters.role_filter import RoleFilter

router = Router()

@router.message(RoleFilter("manager"), F.text.in_(["📊 Monitoring", "📊 Мониторинг"]))
async def filters_handler(message: Message):
    await message.answer("📊 Monitoring\n\nBu yerda monitoring va filtrlash ko'rsatiladi.\n\n👤 Rol: Menejer")
