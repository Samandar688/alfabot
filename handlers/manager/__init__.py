from aiogram import Router

from . import (
    applications,
    connection_order,
    export,
    filters,
    inbox,
    language,
    realtime_monitoring,
    staff_activity,
    status_management,
    technician_order,
)

router = Router()

router.include_routers(
    applications.router,
    connection_order.router,
    export.router,
    filters.router,
    inbox.router,
    language.router,
    realtime_monitoring.router,
    staff_activity.router,
    status_management.router,
    technician_order.router,
)
