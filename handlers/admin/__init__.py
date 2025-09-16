from aiogram import Router

from . import (
    export,
    language,
    orders,
    statistics,
    status,
    users,
)

router = Router()

router.include_routers(
    export.router,
    language.router,
    orders.router,
    statistics.router,
    status.router,
    users.router,
)
