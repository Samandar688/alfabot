import asyncpg
from typing import List, Dict, Any
from config import settings

def _norm_request_id(request_id: int | str) -> int:
    try:
        return int(str(request_id).split("_")[0])
    except Exception:
        return int(request_id)

async def fetch_technician_inbox(
    technician_id: int,
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Texnikka biriktirilgan va statusi 'in_technician' bo‘lgan arizalar.
    connections jadvalidagi ustun nomi: connecion_id (xato yozilgan)
    >>> DIQQAT: recipient_id bo‘yicha filtrlaymiz!
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
            FROM connections c
            JOIN connection_orders co ON co.id = c.connecion_id
            LEFT JOIN users u ON u.id = co.user_id
            LEFT JOIN tarif t ON t.id = co.tarif_id
            WHERE co.is_active = TRUE
              AND c.recipient_id = $1          -- <== shu yer o'zgardi
              AND co.status = 'in_technician'
            ORDER BY co.created_at DESC, co.id DESC
            LIMIT $2 OFFSET $3
            """,
            technician_id, limit, offset
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()

async def count_technician_inbox(technician_id: int) -> int:
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        cnt = await conn.fetchval(
            """
            SELECT COUNT(*)
            FROM connections c
            JOIN connection_orders co ON co.id = c.connecion_id
            WHERE co.is_active = TRUE
              AND c.recipient_id = $1          -- <== shu yer o'zgardi
              AND co.status = 'in_technician'
            """,
            technician_id
        )
        return int(cnt or 0)
    finally:
        await conn.close()

# Agar Controller -> Technician yuborish funksiyangiz hamon technician_id ni ishlatsa, uni ham shunday qiling:
async def assign_to_technician(request_id: int | str, tech_id: int, actor_id: int) -> None:
    """
    connections: faqat connecion_id, sender_id, recipient_id, created_at, updated_at
    order: status = 'in_technician'
    """
    req_id = _norm_request_id(request_id)
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        async with conn.transaction():
            tech_exists = await conn.fetchval(
                "SELECT 1 FROM users WHERE id = $1 AND role = 'technician'", tech_id
            )
            if not tech_exists:
                raise ValueError("Technician not found")

            existing = await conn.fetchrow(
                """
                SELECT id FROM connections
                WHERE connecion_id = $1 AND recipient_id = $2
                LIMIT 1
                """,
                req_id, tech_id
            )
            if existing:
                await conn.execute(
                    "UPDATE connections SET sender_id=$1, updated_at=NOW() WHERE id=$2",
                    actor_id, existing["id"]
                )
            else:
                await conn.execute(
                    """
                    INSERT INTO connections (connecion_id, sender_id, recipient_id, created_at, updated_at)
                    VALUES ($1, $2, $3, NOW(), NOW())
                    """,
                    req_id, actor_id, tech_id
                )

            await conn.execute(
                "UPDATE connection_orders SET status='in_technician', updated_at=NOW() WHERE id=$1",
                req_id
            )
    finally:
        await conn.close()
