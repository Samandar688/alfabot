import asyncpg
from typing import Any, Dict, List, Optional
from config import settings

# 1) Telegram ID -> users
async def db_get_user_by_telegram_id(telegram_id: int) -> Optional[Dict[str, Any]]:
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        row = await conn.fetchrow(
            """
            SELECT id, telegram_id, role, language, full_name, username, phone, region, address,
                   abonent_id, is_blocked, created_at, updated_at
            FROM users
            WHERE telegram_id = $1
            LIMIT 1
            """,
            telegram_id,
        )
        return dict(row) if row else None
    finally:
        await conn.close()

# 2) users.id -> connections (recipient_id bo‘yicha)
#    Diqqat: jadvalda ustun "connecion_id" va "saff_id" bo‘lgani uchun alias ishlatyapmiz.
async def db_get_connections_by_recipient(recipient_id: int, limit: int = 20) -> List[Dict[str, Any]]:
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        rows = await conn.fetch(
            """
            SELECT
                id,
                user_id,
                sender_id,
                recipient_id,
                connecion_id AS connection_id,  -- ✅ alias (order_id)
                technician_id,
                saff_id       AS staff_id,      -- ✅ alias
                created_at,
                updated_at
            FROM connections
            WHERE recipient_id = $1
            ORDER BY created_at DESC
            LIMIT $2
            """,
            recipient_id, limit
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()

# 3) connection_orders: connections.connecion_id -> connection_orders.id
#    Eslatma: parametr nomi 'order_id', ammo moslik uchun funksiya nomi qoldirildi.
async def db_get_connection_order_by_connection_id(order_id: int) -> Optional[Dict[str, Any]]:
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        row = await conn.fetchrow(
            """
            SELECT
                id,
                user_id,
                region,
                address,
                status,
                created_at,
                updated_at
            FROM connection_orders
            WHERE id = $1
            LIMIT 1
            """,
            order_id
        )
        return dict(row) if row else None
    finally:
        await conn.close()

# 4) users.id -> user (full_name, phone olish uchun)
async def db_get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        row = await conn.fetchrow(
            """
            SELECT id, full_name, phone, language, role
            FROM users
            WHERE id = $1
            LIMIT 1
            """,
            user_id
        )
        return dict(row) if row else None
    finally:
        await conn.close()

# ==================== YANGI FUNKSIYALAR (JM oqimi uchun) ====================

# JM Inbox: faqat 'in_junior_manager' dagi arizalar.
# connections (recipient_id = JM id) JOIN connection_orders(id = connecion_id) LEFT JOIN users(order.user_id)
async def db_get_jm_inbox_items(recipient_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        rows = await conn.fetch(
            """
            SELECT
                c.id                   AS connection_record_id,
                c.user_id              AS connection_user_id,
                c.sender_id,
                c.recipient_id,
                c.connecion_id         AS connection_id,      -- order_id
                c.technician_id,
                c.saff_id              AS staff_id,
                c.created_at           AS connection_created_at,

                co.id                  AS order_id,           -- = connection_id
                co.created_at          AS order_created_at,
                co.region              AS order_region,
                co.address             AS order_address,
                co.status              AS order_status,
                co.user_id             AS order_user_id,

                u.full_name            AS client_full_name,
                u.phone                AS client_phone
            FROM connections c
            JOIN connection_orders co ON co.id = c.connecion_id
            LEFT JOIN users u         ON u.id  = co.user_id
            WHERE c.recipient_id = $1
              AND co.status = 'in_junior_manager'::connection_order_status
            ORDER BY co.created_at DESC
            LIMIT $2
            """,
            recipient_id, limit
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()

# Order JM ga tegishli-yo'qligini tekshirish:
# (connection_orders.id = order_id bo'lishi va connections.recipient_id = jm_id bo'lishi shart)
async def db_check_order_ownership(order_id: int, jm_id: int) -> bool:
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        row = await conn.fetchrow(
            """
            SELECT 1
            FROM connections c
            WHERE c.recipient_id = $2
              AND c.connecion_id = $1
            LIMIT 1
            """,
            order_id, jm_id
        )
        return bool(row)
    finally:
        await conn.close()

# Controller'ga yuborish: statusni 'in_controller' ga o'zgartirish (faqat hozir 'in_junior_manager' bo'lsa)
async def db_move_order_to_controller(order_id: int) -> bool:
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        row = await conn.fetchrow(
            """
            UPDATE connection_orders
               SET status    = 'in_controller'::connection_order_status,
                   updated_at = now()
             WHERE id        = $1
               AND status    = 'in_junior_manager'::connection_order_status
         RETURNING id
            """,
            order_id
        )
        return bool(row)
    finally:
        await conn.close()
