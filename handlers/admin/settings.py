from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["⚙️ Sozlamalar", "⚙️ Настройки"]))
async def settings_handler(message: Message):
    await message.answer("⚙️ Tizim sozlamalari\n\nBu yerda tizim sozlamalari boshqariladi.\n\n👤 Rol: Admin")
