from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["🌐 Tilni o'zgartirish", "🌐 Изменить язык"]))
async def role_integration_handler(message: Message):
    await message.answer("🌐 Tilni o'zgartirish\n\nBu yerda til o'zgartiriladi.\n\n👤 Rol: Ombor")
