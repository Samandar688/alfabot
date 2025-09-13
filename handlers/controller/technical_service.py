from aiogram import Router, F
from aiogram.types import Message
from filters.role_filter import RoleFilter

router = Router()

router.message.filter(RoleFilter("controller"))

@router.message(F.text.in_(["🔧 Texnik xizmat yaratish", "🔧 Создать техническую заявку"]))
async def technical_service_handler(message: Message):
    await message.answer("🔧 Texnik xizmat yaratish\n\nBu yerda texnik xizmat arizasi yaratiladi.\n\n👤 Rol: Controller")
