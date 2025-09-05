from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["Bot qo'llanmasi", "Инструкция по использованию бота"]))
async def bot_guide_handler(message: Message):
    await message.answer("📖 Bot qo'llanmasi\n\nBu yerda botdan foydalanish bo'yicha yo'riqnoma ko'rsatiladi.\n\n👤 Rol: Mijoz")
