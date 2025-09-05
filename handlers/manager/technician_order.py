from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["🔧 Texnik xizmat yaratish", "🔧 Создать заявку на тех. обслуживание"]))
async def technician_order_handler(message: Message):
    await message.answer("🔧 Texnik xizmat yaratish\n\nBu yerda texnik xizmat arizasi yaratiladi.\n\n👤 Rol: Menejer")
