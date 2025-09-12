# database/manager_inbox.py
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


async def get_users_by_role(role: str) -> List[Dict[str, Any]]:
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        rows = await conn.fetch(
            """
            SELECT id, full_name, username, phone, telegram_id
              FROM users
             WHERE role = $1
               AND COALESCE(is_blocked, FALSE) = FALSE
             ORDER BY full_name NULLS LAST, id
            """,
            role,
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()


async def fetch_manager_inbox(limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Manager ko‘rishi uchun: statusi 'new' yoki 'in_manager' bo‘lgan arizalar.
    """
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        rows = await conn.fetch(
            """
            SELECT
                co.id,
                co.address,
                co.region,
                co.status,
                co.created_at,
                u.full_name AS client_name,
                u.phone      AS client_phone,
                t.name       AS tariff
            FROM connection_orders co
            LEFT JOIN users u ON u.id = co.user_id
            LEFT JOIN tarif t ON t.id = co.tarif_id
            WHERE co.is_active = TRUE
              AND co.status IN ('new','in_manager')
            ORDER BY co.created_at DESC, co.id DESC
            LIMIT $1 OFFSET $2
            """,
            limit, offset,
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()


# database/manager_inbox.py (yoki shunga mos faylda)
import asyncpg
from config import settings

async def assign_to_junior_manager(request_id: int | str, jm_id: int, actor_id: int) -> None:
    """
    Manager -> Junior Manager:
      1) connection_orders.status: old -> 'in_junior_manager'
      2) connections: HAR DOIM yangi qator INSERT
         sender_id=manager(actor_id), recipient_id=jm_id,
         sender_status=old_status, recipient_status=new_status
    """
    # '8_2025' kabi bo‘lsa ham 8 ni olamiz
    try:
        request_id_int = int(str(request_id).split("_")[0])
    except Exception:
        request_id_int = int(request_id)

    conn = await asyncpg.connect(settings.DB_URL)
    try:
        async with conn.transaction():
            # JM mavjudmi?
            jm_exists = await conn.fetchval(
                "SELECT 1 FROM users WHERE id = $1 AND role = 'junior_manager'",
                jm_id,
            )
            if not jm_exists:
                raise ValueError("Junior manager topilmadi")

            # 1) Eski statusni lock bilan o‘qiymiz
            row_old = await conn.fetchrow(
                """
                SELECT status
                  FROM connection_orders
                 WHERE id = $1
                 FOR UPDATE
                """,
                request_id_int
            )
            if not row_old:
                raise ValueError("Ariza topilmadi")

            old_status: str = row_old["status"]

            # 2) Yangi statusga o‘tkazamiz
            row_new = await conn.fetchrow(
                """
                UPDATE connection_orders
                   SET status     = 'in_junior_manager'::connection_order_status,
                       updated_at = NOW()
                 WHERE id = $1
             RETURNING status
                """,
                request_id_int
            )
            new_status: str = row_new["status"]  # 'in_junior_manager'

            # 3) TARIX: HAR DOIM YANGI QATOR KIRITAMIZ
            await conn.execute(
                """
                INSERT INTO connections (
                    connecion_id,
                    sender_id,
                    recipient_id,
                    sender_status,
                    recipient_status,
                    created_at,
                    updated_at
                )
                VALUES (
                    $1,
                    $2,
                    $3,
                    $4::connection_order_status,
                    $5::connection_order_status,
                    NOW(),
                    NOW()
                )
                """,
                request_id_int,
                actor_id,          # manager
                jm_id,             # junior manager
                old_status,        # masalan: 'in_manager' yoki 'new'
                new_status         # 'in_junior_manager'
            )
    finally:
        await conn.close()