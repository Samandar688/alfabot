from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["🔄 Status o'zgartirish", "🔄 Изменить статус"]))
async def status_management_handler(message: Message):
    await message.answer("🔄 Status o'zgartirish\n\nBu yerda arizalar statusi o'zgartiriladi.\n\n👤 Rol: Menejer")
