import asyncpg
from typing import List, Dict, Any, Optional
from config import settings



async def _conn():
    return await asyncpg.connect(settings.DB_URL)

async def ccs_count_active() -> int:
    conn = await _conn()
    try:
        row = await conn.fetchrow("""
            SELECT COUNT(*) AS c
            FROM saff_orders
            WHERE status = 'in_call_center_supervisor'
              AND is_active = TRUE
        """)
        return int(row["c"])
    finally:
        await conn.close()

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


async def ccs_fetch_by_offset(offset: int) -> Optional[Dict[str, Any]]:
    conn = await _conn()
    try:
        row = await conn.fetchrow("""
            SELECT
                so.id, so.phone, so.abonent_id, so.region, so.address,
                so.tarif_id, t.name AS tariff_name, so.description,
                so.created_at, u.full_name
            FROM saff_orders AS so
            LEFT JOIN public.tarif AS t ON t.id = so.tarif_id
            LEFT JOIN public.users AS u ON u.id = NULLIF(so.abonent_id, '')::int
            WHERE so.status = 'in_call_center_supervisor'
              AND so.is_active = TRUE
            ORDER BY so.created_at ASC, so.id ASC   -- ✅ id qo‘shildi
            OFFSET $1
            LIMIT 1
        """, offset)
        return dict(row) if row else None
    finally:
        await conn.close()

async def ccs_send_to_control(order_id: int, supervisor_id: Optional[int] = None) -> None:
    conn = await _conn()
    try:
        # 1️⃣ Controller id sini olish
        controller = await conn.fetchrow("""
            SELECT id
            FROM users
            WHERE role = 'controller'
            ORDER BY id ASC
            LIMIT 1
        """)
        if not controller:
            raise Exception("Controller topilmadi")

        controller_id = controller["id"]

        # 2️⃣ saff_orders dagi user_id ni olish (ya’ni sender_id sifatida ishlatamiz)
        saff_order = await conn.fetchrow("""
            SELECT user_id
            FROM saff_orders
            WHERE id = $1
        """, order_id)

        if not saff_order or not saff_order["user_id"]:
            raise Exception(f"saff_orders.id={order_id} uchun user_id topilmadi")

        sender_user_id = saff_order["user_id"]

        # 3️⃣ saff_orders jadvalini yangilash
        await conn.execute("""
            UPDATE saff_orders
               SET status = 'in_controller',
                   updated_at = NOW()
             WHERE id = $1
        """, order_id)

        # 4️⃣ connections jadvaliga yozuv qo‘shish
        await conn.execute("""
            INSERT INTO connections (
                sender_id, recipient_id, connecion_id, technician_id, saff_id,
                created_at, updated_at, sender_status, recipient_status
            )
            VALUES ($1, $2, NULL, NULL, $3, NOW(), NOW(),
                    'in_call_center_supervisor', 'in_controller')
        """, sender_user_id, controller_id, order_id)

    finally:
        await conn.close()


async def ccs_cancel(order_id: int) -> None:
    conn = await _conn()
    try:
        await conn.execute("""
            UPDATE saff_orders
               SET status = 'cancelled',
                   is_active = FALSE,
                   updated_at = NOW()
             WHERE id = $1
        """, order_id)
    finally:
        await conn.close()


async def fetch_call_center_supervisor_inbox_tech(limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        rows = await conn.fetch(
            """
            SELECT
                to2.id,
                to2.address,
                to2.region,
                to2.status,
                to2.description,
                to2.media,
                to2.created_at,
                u.full_name AS client_name,
                u.phone     AS client_phone,
                NULL        AS tariff
            FROM technician_orders AS to2
            LEFT JOIN users u ON u.id = to2.user_id
            WHERE to2.is_active = TRUE
              AND to2.status = 'in_call_center_supervisor'
            ORDER BY to2.created_at DESC, to2.id DESC
            LIMIT $1 OFFSET $2
            """,
            limit,
            offset,
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()


async def assign_to_operator_for_tech(request_id: int | str, tech_id: int, actor_id: int) -> None:
    """
    technician_orders: in_call_center_supervisor -> in_call_center_operator
    connections: callcenter_supervisor -> callcenter_operator (technician_id)
    """
    req_id = int(str(request_id).split("_")[0]) if isinstance(request_id, str) else int(request_id)
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        async with conn.transaction():
            ok = await conn.fetchval(
                """
                SELECT 1 FROM users
                WHERE id = $1
                  AND role::text = 'callcenter_operator'
                  AND COALESCE(is_blocked, FALSE) = FALSE
                """,
                tech_id,
            )
            if not ok:
                raise ValueError("operator not found or blocked")

            row_old = await conn.fetchrow(
                "SELECT status FROM technician_orders WHERE id=$1 FOR UPDATE",
                req_id,
            )
            if not row_old or row_old["status"] != "in_call_center_supervisor":
                raise ValueError("Order is not in 'in_call_center_supervisor' status")
            old_status = row_old["status"]

            await conn.execute(
                """
                UPDATE technician_orders
                   SET status='in_call_center_operator'::technician_order_status,
                       updated_at=NOW()
                 WHERE id=$1 AND status='in_call_center_supervisor'::technician_order_status
                """,
                req_id,
            )

            await conn.execute(
                """
                INSERT INTO connections(
                    technician_id,
                    sender_id,
                    recipient_id,
                    sender_status,
                    recipient_status,
                    created_at,
                    updated_at
                )
                VALUES ($1,$2,$3,$4,'in_call_center_operator',NOW(),NOW())
                """,
                req_id, actor_id, tech_id, old_status,
            )
    finally:
        await conn.close()

# =============================
# FILE: database/ccs_technician_inbox_queries.py
# Queries for technician orders inbox under Call Center Supervisor
# =============================



async def _conn():
    return await asyncpg.connect(settings.DB_URL)

async def tech_count_active() -> int:
    conn = await _conn()
    try:
        row = await conn.fetchrow(
            """
            SELECT COUNT(*) AS c
            FROM technician_orders
            WHERE is_active = TRUE
              AND status = 'in_call_center_supervisor'
            """
        )
        return int(row["c"]) if row else 0
    finally:
        await conn.close()

async def tech_fetch_by_offset(offset: int) -> Optional[Dict[str, Any]]:
    conn = await _conn()
    try:
        row = await conn.fetchrow(
            """
            SELECT
                to2.id,
                to2.address,
                to2.region,
                to2.status,
                to2.description,
                to2.media,
                to2.created_at,
                u.full_name AS client_name,
                u.phone     AS client_phone
            FROM technician_orders AS to2
            LEFT JOIN users u ON u.id = to2.user_id
            WHERE to2.is_active = TRUE
              AND to2.status = 'in_call_center_supervisor'
            ORDER BY to2.created_at DESC, to2.id DESC
            OFFSET $1
            LIMIT 1
            """,
            offset,
        )
        return dict(row) if row else None
    finally:
        await conn.close()

async def list_operators_with_load() -> List[Dict[str, Any]]:
    conn = await _conn()
    try:
        rows = await conn.fetch(
            """
            WITH ops AS (
                SELECT id, COALESCE(full_name, username::text) AS full_name
                FROM users
                WHERE role = 'callcenter_operator' AND COALESCE(is_blocked, FALSE) = FALSE
            ),
            active_orders AS (
                SELECT id
                FROM technician_orders
                WHERE is_active = TRUE
                  AND status = 'in_call_center_operator'
            ),
            last_map AS (
                SELECT DISTINCT ON (c.technician_id)
                       c.technician_id,
                       c.recipient_id
                FROM connections c
                WHERE c.technician_id IS NOT NULL
                  AND c.recipient_status = 'in_call_center_operator'
                ORDER BY c.technician_id, c.created_at DESC, c.id DESC
            ),
            load AS (
                SELECT lm.recipient_id AS operator_id, COUNT(*) AS c
                FROM last_map lm
                JOIN active_orders ao ON ao.id = lm.technician_id
                GROUP BY lm.recipient_id
            )
            SELECT o.id,
                   o.full_name,
                   COALESCE(l.c, 0) AS active_count
            FROM ops o
            LEFT JOIN load l ON l.operator_id = o.id
            ORDER BY active_count ASC, o.full_name ASC
            """
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()



async def assign_to_operator_for_tech(request_id: int | str, tech_id: int, actor_id: int) -> None:
    """
    technician_orders: in_call_center_supervisor -> in_call_center_operator
    connections: supervisor (sender) -> operator (recipient), technician_id=order_id
    """
    req_id = int(str(request_id).split("_")[0]) if isinstance(request_id, str) else int(request_id)
    conn = await _conn()
    try:
        async with conn.transaction():
            # 1) Operator tekshiruvi
            ok = await conn.fetchval(
                """
                SELECT 1 FROM users
                WHERE id = $1
                  AND role::text = 'callcenter_operator'
                  AND COALESCE(is_blocked, FALSE) = FALSE
                """,
                tech_id,
            )
            if not ok:
                raise ValueError("operator not found or blocked")

            # 2) Buyurtma statusini tekshirish va bloklash
            row_old = await conn.fetchrow(
                "SELECT status FROM technician_orders WHERE id=$1 FOR UPDATE",
                req_id,
            )
            if not row_old or row_old["status"] != "in_call_center_supervisor":
                raise ValueError("Order is not in 'in_call_center_supervisor' status")
            old_status = row_old["status"]

            # 3) Statusni operator bosqichiga o‘tkazish (USTUN YO‘Q: assigned_operator_id ishlatilmaydi)
            await conn.execute(
                """
                UPDATE technician_orders
                   SET status='in_call_center_operator'::technician_order_status,
                       updated_at=NOW()
                 WHERE id=$1 AND status='in_call_center_supervisor'::technician_order_status
                """,
                req_id,
            )

            # 4) connections ga log: technician_id = shu texnik ariza ID
            await conn.execute(
                """
                INSERT INTO connections(
                    sender_id,
                    recipient_id,
                    connecion_id,
                    technician_id,
                    saff_id,
                    created_at,
                    updated_at,
                    sender_status,
                    recipient_status
                )
                VALUES ($1, $2, NULL, $3, NULL, NOW(), NOW(), $4, 'in_call_center_operator')
                """,
                actor_id,        # $1 - supervisor (sender)
                tech_id,         # $2 - operator (recipient)
                req_id,          # $3 - technician_order id
                old_status,      # $4 - old status (in_call_center_supervisor)
            )
    finally:
        await conn.close()
