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


async def fetch_manager_inbox(limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Return list of connection orders that are in status 'new' or 'in_manager'.
    Includes joined client name/phone and tariff name.
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
            limit,
            offset,
        )
        # Convert id to string if handlers expect str; keep as-is otherwise
        result: List[Dict[str, Any]] = []
        for r in rows:
            item = dict(r)
            # Handlers use str(item["id"]) safely, so keep numeric ID
            result.append(item)
        return result
    finally:
        await conn.close()


async def assign_to_junior_manager(request_id: int | str, jm_id: int, actor_id: int) -> None:
    """
    Move connection order to junior manager workflow by updating its status
    to 'in_junior_manager' and create/update Connection record.
    'request_id' maps to connection_orders.id.
    'jm_id' is the ID of the junior manager (recipient).
    'actor_id' is the ID of the manager (sender).
    """
    # Some handlers might pass string IDs; normalize to int when possible
    try:
        request_id_int = int(str(request_id).split("_")[0])
    except Exception:
        request_id_int = int(request_id)  # Let it raise if not numeric

    conn = await asyncpg.connect(settings.DB_URL)
    try:
        async with conn.transaction():
            # Ensure JM exists
            jm_exists = await conn.fetchval(
                "SELECT 1 FROM users WHERE id = $1 AND role = 'junior_manager'",
                jm_id,
            )
            if not jm_exists:
                raise ValueError("Junior manager not found")

            # Check if connection already exists for this order
            existing_connection = await conn.fetchrow(
                "SELECT id FROM connections WHERE connecion_id = $1",
                request_id_int
            )


            if existing_connection:
                # Update existing connection
                await conn.execute(
                    """
                    UPDATE connections 
                    SET recipient_id = $1,
                        updated_at = NOW()
                    WHERE connecion_id = $2
                    RETURNING id
                    """,
                    jm_id,
                    request_id_int
                )
            else:
                # Create new connection
                await conn.execute(
                    """
                    INSERT INTO connections (
                        connecion_id,
                        sender_id,
                        recipient_id,
                        created_at,
                        updated_at
                    )
                    VALUES ($1, $2, $3, NOW(), NOW())
                    """,
                    request_id_int,
                    actor_id,  # manager who is sending
                    jm_id      # junior manager who is receiving
                )

            # Update order status
            await conn.execute(
                """
                UPDATE connection_orders
                SET status = 'in_junior_manager',
                    jm_notes = COALESCE(jm_notes,'') ||
                        CASE WHEN jm_notes IS NULL OR jm_notes = '' THEN '' ELSE E'\n' END ||
                        ('Assigned to JM ID ' || $2::text || ' by user ' || $3::text),
                    updated_at = NOW()
                WHERE id = $1
                RETURNING id
                """,
                request_id_int,
                str(jm_id),
                str(actor_id),
            )

            # Fetch order info and create inbox message
            order_row = await conn.fetchrow(
                """
                SELECT co.id,
                       co.region AS region_code,
                       co.address,
                       u.full_name AS client_name,
                       u.phone      AS client_phone,
                       t.name       AS tariff
                FROM connection_orders co
                LEFT JOIN users u ON u.id = co.user_id
                LEFT JOIN tarif t ON t.id = co.tarif_id
                WHERE co.id = $1
                """,
                request_id_int,
            )

            if order_row:
                o = dict(order_row)
                title = f"Manager'dan yangi ariza — {o.get('client_name') or ''}"
                desc_parts = []
                if o.get("tariff"):
                    desc_parts.append(f"Tarif: {o['tariff']}")
                if o.get("client_phone"):
                    desc_parts.append(f"Telefon: {o['client_phone']}")
                if o.get("address"):
                    desc_parts.append(f"Manzil: {o['address']}")
                description = " | ".join(desc_parts) or "Yangi ariza yuborildi"

                pass
    finally:
        await conn.close()
