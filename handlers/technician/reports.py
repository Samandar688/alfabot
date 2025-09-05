from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["📊 Hisobotlarim", "📊 Мои отчеты"]))
async def reports_handler(message: Message):
    await message.answer("📊 Hisobotlarim\n\nBu yerda sizning hisobotlaringiz ko'rsatiladi.\n\n👤 Rol: Texnik")
