from aiogram import Router

from . import (
    bot_guide,
    connection_order,
    contact,
    language,
    orders,
    profile,
    service_order,
)

router = Router()

router.include_routers(
    bot_guide.router,
    connection_order.router,
    contact.router,
    language.router,
    orders.router,
    profile.router,
    service_order.router,
)