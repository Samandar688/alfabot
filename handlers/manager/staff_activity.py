from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["👥 Xodimlar faoliyati", "👥 Активность сотрудников"]))
async def staff_activity_handler(message: Message):
    await message.answer("👥 Xodimlar faoliyati\n\nBu yerda xodimlar faoliyati ko'rsatiladi.\n\n👤 Rol: Menejer")
