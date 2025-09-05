from aiogram import Router

from . import (
    start_handler,
    admin,
    client,
    manager,
    junior_manager,
    controller,
    technician,
    warehouse,
    call_center,
    call_center_supervisor,
)

# Asosiy router
router = Router()

# Barcha handlerlarni birlashtirish
router.include_routers(
    start_handler.router,
    admin.router,
    client.router,
    manager.router,
    junior_manager.router,
    controller.router,
    technician.router,
    warehouse.router,
    call_center.router,
    call_center_supervisor.router,
)
