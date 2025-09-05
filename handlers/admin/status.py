from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["🔧 Tizim holati", "🔧 Состояние системы"]))
async def status_handler(message: Message):
    await message.answer("🔧 Tizim holati\n\nBu yerda tizim holati ko'rsatiladi.\n\n👤 Rol: Admin")
