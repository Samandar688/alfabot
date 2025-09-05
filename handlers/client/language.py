from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["🌐 Til o'zgartirish", "🌐 Изменить язык"]))
async def language_handler(message: Message):
    await message.answer("🌐 Til o'zgartirish\n\nBu yerda til o'zgartiriladi.\n\n👤 Rol: Mijoz")
