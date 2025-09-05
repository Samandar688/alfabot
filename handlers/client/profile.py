from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["👤 Kabinet", "👤 Кабинет"]))
async def profile_handler(message: Message):
    await message.answer("Sizning profilingiz\n\n👤 Rol: Mijoz")