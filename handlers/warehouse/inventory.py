from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["📦 Inventarizatsiya", "📦 Инвентаризация"]))
async def inventory_handler(message: Message):
    await message.answer("📦 Inventarizatsiya\n\nBu yerda inventarizatsiya boshqariladi.\n\n👤 Rol: Ombor")
