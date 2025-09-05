from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["🔍 Mijoz qidiruv", "🔍 Поиск клиентов"]))
async def client_search_handler(message: Message):
    await message.answer("🔍 Mijoz qidiruv\n\nBu yerda mijozlar qidiriladi.\n\n👤 Rol: Junior Manager")
