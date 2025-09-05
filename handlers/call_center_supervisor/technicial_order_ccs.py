from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.in_(["🔧 Texnik xizmat yaratish", "🔧 Создать техническую заявку"]))
async def technicial_order_ccs_handler(message: Message):
    await message.answer("🔧 Texnik xizmat yaratish\n\nBu yerda texnik xizmat arizasi yaratiladi.\n\n👤 Rol: Call Center Supervisor")
