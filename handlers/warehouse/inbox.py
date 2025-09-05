from aiogram import Router, F
from aiogram.types import Message
from filters.role_filter import RoleFilter
router = Router()
router.message.filter(RoleFilter("warehouse"))
@router.message(F.text == "📥 Inbox")
async def inbox_handler(message: Message):
    await message.answer("📥 Inbox\n\nBu yerda kiruvchi xabarlar ko'rsatiladi.\n\n👤 Rol: Ombor")
