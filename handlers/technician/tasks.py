from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["📋 Vazifalarim", "📋 Мои задачи"]))
async def tasks_handler(message: Message):
    await message.answer("📋 Vazifalarim\n\nBu yerda sizning vazifalaringiz ko'rsatiladi.\n\n👤 Rol: Texnik")
