from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["📊 Statistikalar", "📊 Статистика"]))
async def statistics_handler(message: Message):
    await message.answer("📊 Statistikalar\n\nBu yerda ombor statistikasi ko'rsatiladi.\n\n👤 Rol: Ombor")
