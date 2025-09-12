import asyncpg
from typing import List, Dict, Any, Optional
from config import settings


async def get_user_by_telegram_id(telegram_id: int) -> Optional[Dict[str, Any]]:
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        row = await conn.fetchrow(
            """
            SELECT id, telegram_id, full_name, username, phone, role
            FROM users
            WHERE telegram_id = $1
            """,
            telegram_id,
        )
        return dict(row) if row else None
    finally:
        await conn.close()


async def fetch_smart_service_orders(limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Return list of smart service orders with joined user information.
    Orders are sorted by creation date (newest first).
    """
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        rows = await conn.fetch(
            """
            SELECT
                sso.id,
                sso.user_id,
                sso.category,
                sso.service_type,
                sso.address,
                sso.latitude,
                sso.longitude,
                sso.created_at,
                u.full_name,
                u.phone,
                u.telegram_id,
                u.username
            FROM smart_service_orders sso
            LEFT JOIN users u ON u.id = sso.user_id
            ORDER BY sso.created_at DESC, sso.id DESC
            LIMIT $1 OFFSET $2
            """,
            limit,
            offset,
        )
        result: List[Dict[str, Any]] = []
        for r in rows:
            item = dict(r)
            result.append(item)
        return result
    finally:
        await conn.close()