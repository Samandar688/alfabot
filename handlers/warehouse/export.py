from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["📤 Export", "📤 Экспорт"]))
async def export_handler(message: Message):
    await message.answer("📤 Export\n\nBu yerda ombor ma'lumotlari eksport qilinadi.\n\n👤 Rol: Ombor")
