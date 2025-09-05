from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["👥 Xodimlar boshqaruvi", "👥 Управление сотрудниками"]))
async def staff_activity_handler(message: Message):
    await message.answer("👥 Xodimlar boshqaruvi\n\nBu yerda xodimlar faoliyati boshqariladi.\n\n👤 Rol: Call Center Supervisor")
