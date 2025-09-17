import asyncpg
from typing import List, Dict, Any
from config import settings

SELECT_BASE = """
    SELECT
        co.id,
        co.address,
        co.region,
        co.status,
        co.created_at,
        co.updated_at,
        u.full_name AS client_name,
        u.phone      AS client_phone,
        t.name       AS tariff
    FROM connection_orders co
    LEFT JOIN users  u ON u.id = co.user_id
    LEFT JOIN tarif  t ON t.id = co.tarif_id
"""

async def list_new_orders(limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """🆕 YANGI (BUGUN YARATILGAN): DATE(co.created_at)=CURRENT_DATE"""
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        rows = await conn.fetch(
            f"""
            WITH filtered AS (
                {SELECT_BASE}
                WHERE DATE(co.created_at) = CURRENT_DATE
            )
            SELECT *,
                   COUNT(*) OVER() AS total_count
              FROM filtered
             ORDER BY created_at DESC, id DESC
             LIMIT $1 OFFSET $2;
            """,
            limit, offset
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()


async def list_in_progress_orders(limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """⏳ JARAYONDAGILAR: is_active=TRUE AND status<>'completed'"""
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        rows = await conn.fetch(
            f"""
            WITH filtered AS (
                {SELECT_BASE}
                WHERE co.is_active = TRUE
                  AND co.status <> 'completed'::connection_order_status
            )
            SELECT *,
                   COUNT(*) OVER() AS total_count
              FROM filtered
             ORDER BY created_at DESC, id DESC
             LIMIT $1 OFFSET $2;
            """,
            limit, offset
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()


async def list_completed_today_orders(limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """✅ BUGUN BAJARILGAN: status='completed' AND DATE(co.updated_at)=CURRENT_DATE"""
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        rows = await conn.fetch(
            f"""
            WITH filtered AS (
                {SELECT_BASE}
                WHERE co.status = 'completed'::connection_order_status
                  AND DATE(co.updated_at) = CURRENT_DATE
            )
            SELECT *,
                   COUNT(*) OVER() AS total_count
              FROM filtered
             ORDER BY updated_at DESC, id DESC
             LIMIT $1 OFFSET $2;
            """,
            limit, offset
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()


async def list_cancelled_orders(limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """❌ BEKOR QILINGANLAR: is_active=FALSE"""
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        rows = await conn.fetch(
            f"""
            WITH filtered AS (
                {SELECT_BASE}
                WHERE co.is_active = FALSE
            )
            SELECT *,
                   COUNT(*) OVER() AS total_count
              FROM filtered
             ORDER BY updated_at DESC NULLS LAST, id DESC
             LIMIT $1 OFFSET $2;
            """,
            limit, offset
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()

async def get_total_orders_count() -> int:
    """JAMI: Barcha arizalar soni (filtrsiz)."""
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        return await conn.fetchval("SELECT COUNT(*) FROM connection_orders;")
    finally:
        await conn.close()


async def get_new_orders_today_count() -> int:
    """YANGI (BUGUN): DATE(created_at) = CURRENT_DATE."""
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        return await conn.fetchval(
            """
            SELECT COUNT(*)
              FROM connection_orders
             WHERE DATE(created_at) = CURRENT_DATE;
            """
        )
    finally:
        await conn.close()


async def get_in_progress_count() -> int:
    """JARAYONDA: is_active = TRUE AND status <> 'completed'."""
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        return await conn.fetchval(
            """
            SELECT COUNT(*)
              FROM connection_orders
             WHERE is_active = TRUE
               AND status <> 'completed'::connection_order_status;
            """
        )
    finally:
        await conn.close()


async def get_completed_today_count() -> int:
    """BUGUN BAJARILGAN: status='completed' AND DATE(updated_at)=CURRENT_DATE."""
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        return await conn.fetchval(
            """
            SELECT COUNT(*)
              FROM connection_orders
             WHERE status = 'completed'::connection_order_status
               AND DATE(updated_at) = CURRENT_DATE;
            """
        )
    finally:
        await conn.close()


async def get_cancelled_count() -> int:
    """BEKOR QILINGANLAR: is_active = FALSE."""
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        return await conn.fetchval(
            "SELECT COUNT(*) FROM connection_orders WHERE is_active = FALSE;"
        )
    finally:
        await conn.close()