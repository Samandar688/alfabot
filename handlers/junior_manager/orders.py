from aiogram import Router, F
from aiogram.types import Message
from filters.role_filter import RoleFilter

router = Router()
router.message.filter(RoleFilter("junior_manager"))
router.callback_query.filter(RoleFilter("junior_manager"))

@router.message(F.text.in_(["📋 Arizalarni ko'rish", "📋 Просмотр заявок"]))
async def orders_handler(message: Message):
    await message.answer("📋 Arizalarni ko'rish\n\nBu yerda barcha arizalar ro'yxati ko'rsatiladi.\n\n👤 Rol: Junior Manager")
