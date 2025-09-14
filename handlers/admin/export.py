from aiogram import Router, F
from aiogram.types import Message
from filters.role_filter import RoleFilter

router = Router()
router.message.filter(RoleFilter(role="admin"))

@router.message(F.text.in_(["📤 Export", "📤 Экспорт"]))
async def export_handler(message: Message):
    await message.answer("📤 Ma'lumotlarni eksport qilish\n\nBu yerda ma'lumotlar eksport qilinadi.\n\n👤 Rol: Admin")
