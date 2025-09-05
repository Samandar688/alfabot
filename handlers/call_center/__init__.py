from aiogram import Router

from . import (
    client_search,
    connection_order_cc,
    inbox,
    language,
    orders,
    statistics,
    technician_order_cc,
)

router = Router()

router.include_routers(
    client_search.router,
    connection_order_cc.router,
    inbox.router,
    language.router,
    orders.router,
    statistics.router,
    technician_order_cc.router,
)
