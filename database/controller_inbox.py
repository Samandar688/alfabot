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
    Return list of connection orders that are in status 'in_controller' or 'in_technician'.
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
              AND co.status IN ('in_controller','in_technician')
            ORDER BY co.created_at DESC, co.id DESC
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


async def assign_to_technician(request_id: int | str, tech_id: int, actor_id: int) -> None:
    """
    Move connection order to technician workflow by updating its status
    to 'in_technician' and create/update Connection record.
    'request_id' maps to connection_orders.id.
    'tech_id' is the ID of the technician (recipient).
    'actor_id' is the ID of the controller (sender).
    """
    try:
        request_id_int = int(str(request_id).split("_")[0])
    except Exception:
        request_id_int = int(request_id)

    conn = await asyncpg.connect(settings.DB_URL)
    try:
        async with conn.transaction():
            # Ensure technician exists
            tech_exists = await conn.fetchval(
                "SELECT 1 FROM users WHERE id = $1 AND role = 'technician'",
                tech_id,
            )
            if not tech_exists:
                raise ValueError("Technician not found")

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
                    SET technician_id = $1,
                        updated_at = NOW()
                    WHERE connecion_id = $2
                    RETURNING id
                    """,
                    tech_id,
                    request_id_int
                )
            else:
                # Create new connection
                await conn.execute(
                    """
                    INSERT INTO connections (
                        connecion_id,
                        sender_id,
                        technician_id,
                        created_at,
                        updated_at
                    )
                    VALUES ($1, $2, $3, NOW(), NOW())
                    """,
                    request_id_int,
                    actor_id,  # controller who is sending
                    tech_id    # technician who is receiving
                )

            # Update order status
            await conn.execute(
                """
                UPDATE connection_orders
                SET status = 'in_technician',
                    controller_notes = COALESCE(controller_notes,'') ||
                        CASE WHEN controller_notes IS NULL OR controller_notes = '' THEN '' ELSE E'\n' END ||
                        ('Assigned to Technician ID ' || $2::text || ' by user ' || $3::text),
                    updated_at = NOW()
                WHERE id = $1
                RETURNING id
                """,
                request_id_int,
                str(tech_id),
                str(actor_id),
            )
    finally:
        await conn.close()