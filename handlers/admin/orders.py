from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["📝 Zayavkalar", "📝 Заявки"]))
async def orders_handler(message: Message):
    await message.answer("📝 Zayavkalar boshqaruvi\n\nBu yerda barcha zayavkalar ro'yxati ko'rsatiladi.\n\n👤 Rol: Admin")
