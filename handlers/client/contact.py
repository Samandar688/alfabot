from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["📞 Operator bilan bog'lanish", "📞 Связаться с оператором"]))
async def contact_handler(message: Message):
    await message.answer("📞 Operator bilan bog'lanish\n\nBu yerda operator bilan bog'lanish mumkin.\n\n👤 Rol: Mijoz")
