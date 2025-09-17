from aiogram import Router, F
from aiogram.types import Message
from filters.role_filter import RoleFilter
router = Router()

router.message.filter(RoleFilter("controller"))
router.callback_query.filter(RoleFilter("controller"))

@router.message(F.text.in_(["👥 Xodimlar faoliyati", "👥 Активность сотрудников"]))
async def technicians_handler(message: Message):
    await message.answer("👥 Xodimlar faoliyati\n\nBu yerda xodimlar faoliyati ko'rsatiladi.\n\n👤 Rol: Controller")
