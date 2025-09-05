from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["🔍 Mijoz qidirish", "🔍 Поиск клиента"]))
async def client_search_handler(message: Message):
    await message.answer("🔍 Mijoz qidirish\n\nBu yerda mijozlar qidiriladi.\n\n👤 Rol: Call Center")
