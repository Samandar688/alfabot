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
            WHERE role = $1 AND COALESCE(is_blocked, FALSE) = FALSE
            ORDER BY full_name NULLS LAST, id
            """,
            role,
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()


async def fetch_controller_inbox(limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Controller uchun faqat statusi 'in_controller' bo‘lgan arizalarni qaytaradi.
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
              AND co.status = 'in_controller'
            ORDER BY co.created_at DESC, co.id DESC
            LIMIT $1 OFFSET $2
            """,
            limit,
            offset,
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()


async def assign_to_technician(request_id: int | str, tech_id: int, actor_id: int) -> None:
    """
    Controller -> Technician yuborish:
      - connections jadvalida (connecion_id, sender_id, recipient_id, created_at, updated_at) yozuv yaratish
        (agar shu (connecion_id, recipient_id) bo'yicha bor bo'lsa, faqat sender_id va updated_at yangilanadi)
      - connection_orders.status = 'in_technician'
    Eslatma: ustun nomi ataylab 'connecion_id' (xatolik bilan) ishlatilmoqda.
    """
    # '8_2025' kabi kelganda 8 ni olish
    try:
        request_id_int = int(str(request_id).split("_")[0])
    except Exception:
        request_id_int = int(request_id)

    conn = await asyncpg.connect(settings.DB_URL)
    try:
        async with conn.transaction():
            # 1) Texnik mavjudligini tekshirish
            tech_exists = await conn.fetchval(
                "SELECT 1 FROM users WHERE id = $1 AND role = 'technician'",
                tech_id
            )
            if not tech_exists:
                raise ValueError("Technician not found")

            # 2) connections: (connecion_id, recipient_id) bo'yicha upsert
            existing = await conn.fetchrow(
                """
                SELECT id
                FROM connections
                WHERE connecion_id = $1
                  AND recipient_id = $2
                LIMIT 1
                """,
                request_id_int, tech_id
            )

            if existing:
                # faqat sender_id va updated_at ni yangilaymiz
                await conn.execute(
                    """
                    UPDATE connections
                    SET sender_id  = $1,
                        updated_at = NOW()
                    WHERE id = $2
                    """,
                    actor_id, existing["id"]
                )
            else:
                # faqat kerakli ustunlarni to'ldirib yangi qator qo'shamiz
                await conn.execute(
                    """
                    INSERT INTO connections (
                        connecion_id,  -- (xatoli nom) order id
                        sender_id,     -- controller (yuboruvchi)
                        recipient_id,  -- technician (qabul qiluvchi)
                        created_at,
                        updated_at
                    )
                    VALUES ($1, $2, $3, NOW(), NOW())
                    """,
                    request_id_int, actor_id, tech_id
                )

            # 3) Ariza statusini 'in_technician' ga o'tkazish
            await conn.execute(
                """
                UPDATE connection_orders
                SET status = 'in_technician',
                    updated_at = NOW()
                WHERE id = $1
                """,
                request_id_int
            )
    finally:
        await conn.close()