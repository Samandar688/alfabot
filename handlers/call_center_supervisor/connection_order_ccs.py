from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["🔌 Ulanish arizasi yaratish", "🔌 Создать заявку на подключение"]))
async def connection_order_ccs_handler(message: Message):
    await message.answer("🔌 Ulanish arizasi yaratish\n\nBu yerda yangi ulanish arizasi yaratiladi.\n\n👤 Rol: Call Center Supervisor")
