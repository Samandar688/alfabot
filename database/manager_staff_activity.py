# database/staff_activity_queries.py
import asyncpg
from config import settings

async def get_active_connection_tasks_count() -> int:
    """
    Aktiv vazifalar soni:
      connection_orders jadvalidan is_active = TRUE
      va status 'completed' EMAS (ENUM: connection_order_status)
    """
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        return await conn.fetchval(
            """
            SELECT COUNT(*)
              FROM connection_orders
             WHERE is_active = TRUE
               AND status <> 'completed'::connection_order_status
            """
        )
    finally:
        await conn.close()


async def get_junior_manager_count() -> int:
    """
    Umumiy xodimlar soni:
      users jadvalidan role = 'junior_manager'
    """
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        return await conn.fetchval(
            """
            SELECT COUNT(*)
              FROM users
             WHERE role = 'junior_manager'
            """
        )
    finally:
        await conn.close()