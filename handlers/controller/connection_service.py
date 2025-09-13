from aiogram import Router, F
from aiogram.types import Message
from filters.role_filter import RoleFilter


router = Router()

router.message.filter(RoleFilter("controller"))

@router.message(F.text.in_(["🔌 Ulanish arizasi yaratish", "🔌 Создать заявку на подключение"]))
async def connection_service_handler(message: Message):
    await message.answer("🔌 Ulanish arizasi yaratish\n\nBu yerda yangi ulanish arizasi yaratiladi.\n\n👤 Rol: Controller")
