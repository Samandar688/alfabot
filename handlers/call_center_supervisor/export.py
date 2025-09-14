from aiogram import Router, F
from aiogram.types import Message
from filters.role_filter import RoleFilter

router = Router()
router.message.filter(RoleFilter("callcenter_supervisor"))


@router.message(F.text.in_(["📤 Export", "📤 Экспорт"]))
async def export_handler(message: Message):
    await message.answer("📤 Export\n\nBu yerda ma'lumotlar eksport qilinadi.\n\n👤 Rol: Call Center Supervisor")
