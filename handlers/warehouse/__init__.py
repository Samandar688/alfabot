from aiogram import Router

from . import (
    export,
    inbox,
    inventory,
    orders,
    role_integration,
    statistics,
)

router = Router()

router.include_routers(
    export.router,
    inbox.router,
    inventory.router,
    orders.router,
    role_integration.router,
    statistics.router,
)
