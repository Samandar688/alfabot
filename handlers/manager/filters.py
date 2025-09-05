from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["📊 Monitoring", "📊 Мониторинг"]))
async def filters_handler(message: Message):
    await message.answer("📊 Monitoring\n\nBu yerda monitoring va filtrlash ko'rsatiladi.\n\n👤 Rol: Menejer")
