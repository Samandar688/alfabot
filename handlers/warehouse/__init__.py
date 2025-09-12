from aiogram import Router

from . import (
    export,
    inbox,
    inventory,
    orders,
    language,
    statistics,
)

router = Router()

router.include_routers(
    export.router,
    inbox.router,
    inventory.router,
    orders.router,
    language.router,
    statistics.router,
)
