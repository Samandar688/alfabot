from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["📋 Mening arizalarim", "📋 Мои заявки"]))
async def orders_handler(message: Message):
    await message.answer("📋 Mening arizalarim\n\nBu yerda sizning arizalaringiz ro'yxati ko'rsatiladi.\n\n👤 Rol: Mijoz")
