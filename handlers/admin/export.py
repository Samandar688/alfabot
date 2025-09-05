from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["📤 Export", "📤 Экспорт"]))
async def export_handler(message: Message):
    await message.answer("📤 Ma'lumotlarni eksport qilish\n\nBu yerda ma'lumotlar eksport qilinadi.\n\n👤 Rol: Admin")
