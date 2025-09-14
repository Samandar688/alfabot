# database/applications_queries.py
# Maqsad: "📋 Arizalarni ko'rish" bo'limidagi STATISTIK ko'rsatkichlar uchun COUNT so'rovlari.
# Uslub: asyncpg -> to'g'ridan-to'g'ri connect(settings.DB_URL) / close()

import asyncpg
from config import settings


async def get_total_orders_count() -> int:
    """
    JAMI:
      connection_orders dagi BARCHA arizalar soni (is_active/shart yo'q).
    """
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        return await conn.fetchval("SELECT COUNT(*) FROM connection_orders;")
    finally:
        await conn.close()


async def get_new_orders_today_count() -> int:
    """
    YANGI:
      is_active = TRUE
      status <> 'completed'
      DATE(created_at) = CURRENT_DATE   # (talabingizga ko'ra created_at)
    """
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        return await conn.fetchval(
            """
            SELECT COUNT(*)
              FROM connection_orders
             WHERE is_active = TRUE
               AND status <> 'completed'::connection_order_status
               AND DATE(created_at) = CURRENT_DATE;
            """
        )
    finally:
        await conn.close()


async def get_in_progress_count() -> int:
    """
    JARAYONDA:
      is_active = TRUE
      status <> 'completed'
    """
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
    """
    BUGUN BAJARILGAN:
      is_active = TRUE
      status = 'completed'
      DATE(created_at) = CURRENT_DATE   # (statistika uchun created_at asosida)
    """
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        return await conn.fetchval(
            """
            SELECT COUNT(*)
              FROM connection_orders
             WHERE is_active = TRUE
               AND status = 'completed'::connection_order_status
               AND DATE(created_at) = CURRENT_DATE;
            """
        )
    finally:
        await conn.close()


async def get_cancelled_count() -> int:
    """
    BEKOR QILINGANLAR:
      is_active = FALSE
    """
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        return await conn.fetchval(
            "SELECT COUNT(*) FROM connection_orders WHERE is_active = FALSE;"
        )
    finally:
        await conn.close()


# database/applications_list_queries.py
# Maqsad: inline tugmalar bo'yicha RO'YXAT chiqarish (pagination bilan).
# Uslub: asyncpg -> to'g'ridan-to'g'ri connect(settings.DB_URL) / close()

import asyncpg
from typing import List, Dict, Any
from config import settings


# Ro'yxatlarda ishlatiladigan asosiy SELECT qismini bir joyga to'pladik:
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


async def list_new_orders(limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
    """
    🆕 YANGI BUYURTMALAR:
      is_active = TRUE
      status = 'in_manager'
    """
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        rows = await conn.fetch(
            SELECT_BASE + """
            WHERE co.is_active = TRUE
              AND co.status = 'in_manager'::connection_order_status
            ORDER BY co.created_at DESC, co.id DESC
            LIMIT $1 OFFSET $2;
            """,
            limit, offset
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()


async def list_in_progress_orders(limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
    """
    ⏳ JARAYONDAGILAR:
      is_active = TRUE
      status <> 'completed'
    """
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        rows = await conn.fetch(
            SELECT_BASE + """
            WHERE co.is_active = TRUE
              AND co.status <> 'completed'::connection_order_status
            ORDER BY co.created_at DESC, co.id DESC
            LIMIT $1 OFFSET $2;
            """,
            limit, offset
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()


async def list_completed_today_orders(limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
    """
    ✅ BUGUN BAJARILGAN:
      status = 'completed'
      DATE(updated_at) = CURRENT_DATE   # ro'yxat uchun UPDATED_AT talab qilindi
      (Eslatma: statistikadagi "bugun bajarilgan" created_at bo'yicha edi —
       bu yerda maxsus ravishda updated_at ishlatilmoqda.)
    """
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        rows = await conn.fetch(
            SELECT_BASE + """
            WHERE co.status = 'completed'::connection_order_status
              AND DATE(co.updated_at) = CURRENT_DATE
            ORDER BY co.updated_at DESC, co.id DESC
            LIMIT $1 OFFSET $2;
            """,
            limit, offset
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()


async def list_cancelled_orders(limit: int = 20, offset: int = 0) -> List[Dict[str, Any]]:
    """
    ❌ BEKOR QILINGANLAR:
      is_active = FALSE
    """
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        rows = await conn.fetch(
            SELECT_BASE + """
            WHERE co.is_active = FALSE
            ORDER BY co.updated_at DESC NULLS LAST, co.id DESC
            LIMIT $1 OFFSET $2;
            """,
            limit, offset
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()
