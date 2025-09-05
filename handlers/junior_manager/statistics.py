from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["📊 Statistika", "📊 Статистика"]))
async def statistics_handler(message: Message):
    await message.answer("📊 Statistika\n\nBu yerda junior manager statistikasi ko'rsatiladi.\n\n👤 Rol: Junior Manager")
