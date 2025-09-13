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
    req_id = int(str(request_id).split("_")[0]) if isinstance(request_id, str) else int(request_id)
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        async with conn.transaction():
            ok = await conn.fetchval("SELECT 1 FROM users WHERE id=$1 AND role='technician'", tech_id)
            if not ok:
                raise ValueError("Technician not found")

            row_old = await conn.fetchrow(
                "SELECT status FROM connection_orders WHERE id=$1 FOR UPDATE", req_id
            )
            if not row_old or row_old["status"] != "in_controller":
                raise ValueError("Order is not in 'in_controller' status")
            old_status = row_old["status"]

            row_new = await conn.fetchrow("""
                UPDATE connection_orders
                   SET status='between_controller_technician'::connection_order_status,
                       updated_at=NOW()
                 WHERE id=$1 AND status='in_controller'::connection_order_status
             RETURNING status
            """, req_id)
            if not row_new:
                raise ValueError("Failed to update order status")
            new_status = row_new["status"]

            # 👉 Faqat INSERT
            await conn.execute("""
                INSERT INTO connections(
                    connecion_id, sender_id, recipient_id,
                    sender_status, recipient_status,
                    created_at, updated_at
                )
                VALUES ($1,$2,$3,$4::connection_order_status,$5::connection_order_status,NOW(),NOW())
            """, req_id, actor_id, tech_id, old_status, new_status)
    finally:
        await conn.close()

# --- YANGI: Texnik xizmat arizalari ro‘yxati (technician_orders) ---
async def fetch_controller_inbox_tech(limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Controller uchun technician_orders jadvalidan statusi 'in_controller' bo‘lgan arizalarni qaytaradi.
    UI bilan mos bo‘lishi uchun 'client_name', 'client_phone', 'tariff' aliaslari ham qaytariladi.
    """
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        rows = await conn.fetch(
            """
            SELECT
                to2.id,
                to2.address,
                to2.region,
                to2.status,
                to2.created_at,
                u.full_name AS client_name,
                u.phone     AS client_phone,
                NULL        AS tariff          -- technician_orders uchun tarif yo‘q, UI ga mos bo‘lishi uchun NULL qaytaramiz
            FROM technician_orders AS to2
            LEFT JOIN users u ON u.id = to2.user_id
            WHERE to2.is_active = TRUE
              AND to2.status = 'in_controller'
            ORDER BY to2.created_at DESC, to2.id DESC
            LIMIT $1 OFFSET $2
            """,
            limit,
            offset,
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()

# --- YANGI: technician_orders uchun assign ---
async def assign_to_technician_for_tech(request_id: int | str, tech_id: int, actor_id: int) -> None:
    """
    technician_orders jadvali uchun biriktirish:
      - Hozirgi status 'in_controller' bo‘lsa -> 'between_controller_technician' ga o‘tkazadi
      - Aloqa jadvaliga (connections) yozuv qo‘shadi (sizdagi struktura/nomlar bilan moslang)
    """
    req_id = int(str(request_id).split("_")[0]) if isinstance(request_id, str) else int(request_id)
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        async with conn.transaction():
            # 1) Texnik rolini tekshirish
            ok = await conn.fetchval(
                "SELECT 1 FROM users WHERE id=$1 AND role='technician'",
                tech_id
            )
            if not ok:
                raise ValueError("Technician not found")

            # 2) Eski statusni qulflash va tekshirish
            row_old = await conn.fetchrow(
                "SELECT status FROM technician_orders WHERE id=$1 FOR UPDATE",
                req_id
            )
            if not row_old or row_old["status"] != "in_controller":
                raise ValueError("Order is not in 'in_controller' status")
            old_status = row_old["status"]

            # 3) Yangi statusga o‘tkazish
            row_new = await conn.fetchrow(
                """
                UPDATE technician_orders
                   SET status='between_controller_technician'::technician_order_status,
                       updated_at=NOW()
                 WHERE id=$1 AND status='in_controller'::technician_order_status
             RETURNING status
                """,
                req_id
            )
            if not row_new:
                raise ValueError("Failed to update order status")
            new_status = row_new["status"]

            # 4) Aloqa jadvaliga yozish (sizdagi ustun nomlarini moslang!)
            #   Eslatma: avvalgi kodingizda 'connecion_id' yozuvi bor edi — typo bo‘lishi mumkin.
            #   To‘g‘ri ustun nom(lar)ini connections jadvalingizga moslang.
            await conn.execute(
                """
                INSERT INTO connections(
                    connecion_id,            -- TODO: Agar bu typo bo‘lsa, to‘g‘risi bilan almashtiring: connection_id
                    sender_id,
                    recipient_id,
                    sender_status,
                    recipient_status,
                    created_at,
                    updated_at
                )
                VALUES ($1,$2,$3,$4::technician_order_status,$5::technician_order_status,NOW(),NOW())
                """,
                req_id, actor_id, tech_id, old_status, new_status
            )
    finally:
        await conn.close()
