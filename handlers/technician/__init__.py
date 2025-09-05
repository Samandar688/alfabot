from aiogram import Router

from . import (
    inbox,
    reports,
    tasks,
)

router = Router()

router.include_routers(
    inbox.router,
    reports.router,
    tasks.router,
)
