# database/technician_queries.py
import asyncpg
from typing import List, Dict, Any, Optional
from config import settings

# ----------------- YORDAMCHI -----------------
async def _conn():
    return await asyncpg.connect(settings.DB_URL)

def _as_dicts(rows):
    return [dict(r) for r in rows]

# ----------------- INBOX -----------------
async def fetch_technician_inbox(
    technician_id: int,
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Texnikga oxirgi biriktirish bo‘yicha faol arizalar.
    """
    conn = await _conn()
    try:
        rows = await conn.fetch(
            """
            WITH last_conn AS (
                SELECT
                    c.*,
                    ROW_NUMBER() OVER (
                        PARTITION BY c.connecion_id, c.recipient_id
                        ORDER BY c.created_at DESC, c.id DESC
                    ) AS rn
                FROM connections c
                WHERE c.recipient_id = $1
            )
            SELECT
                co.id,
                co.address,
                co.region,
                co.status,
                co.created_at,
                u.full_name AS client_name,
                u.phone      AS client_phone,
                t.name       AS tariff
            FROM last_conn c
            JOIN connection_orders co ON co.id = c.connecion_id
            LEFT JOIN users u ON u.id = co.user_id
            LEFT JOIN tarif t ON t.id = co.tarif_id
            WHERE
                c.rn = 1
                AND co.is_active = TRUE
                AND co.status IN (
                    'between_controller_technician'::connection_order_status,
                    'in_technician'::connection_order_status,
                    'in_technician_work'::connection_order_status
                )
            ORDER BY
                CASE co.status
                    WHEN 'between_controller_technician'::connection_order_status THEN 0
                    WHEN 'in_technician'::connection_order_status                 THEN 1
                    WHEN 'in_technician_work'::connection_order_status            THEN 2
                    ELSE 3
                END,
                co.created_at DESC,
                co.id DESC
            LIMIT $2 OFFSET $3
            """,
            technician_id, limit, offset
        )
        return _as_dicts(rows)
    finally:
        await conn.close()

async def count_technician_inbox(technician_id: int) -> int:
    conn = await _conn()
    try:
        cnt = await conn.fetchval(
            """
            WITH last_conn AS (
                SELECT
                    c.*,
                    ROW_NUMBER() OVER (
                        PARTITION BY c.connecion_id, c.recipient_id
                        ORDER BY c.created_at DESC, c.id DESC
                    ) AS rn
                FROM connections c
                WHERE c.recipient_id = $1
            )
            SELECT COUNT(*)
            FROM last_conn c
            JOIN connection_orders co ON co.id = c.connecion_id
            WHERE
                c.rn = 1
                AND co.is_active = TRUE
                AND co.status IN (
                    'between_controller_technician'::connection_order_status,
                    'in_technician'::connection_order_status,
                    'in_technician_work'::connection_order_status
                )
            """,
            technician_id
        )
        return int(cnt or 0)
    finally:
        await conn.close()

# ----------------- STATUSLAR -----------------
async def cancel_technician_request(applications_id: int, technician_id: int) -> None:
    conn = await _conn()
    try:
        async with conn.transaction():
            await conn.execute(
                """
                UPDATE connection_orders
                   SET is_active = FALSE,
                       updated_at = NOW()
                 WHERE id = $1
                """,
                applications_id
            )
    finally:
        await conn.close()

async def accept_technician_work(applications_id: int, technician_id: int) -> bool:
    conn = await _conn()
    try:
        async with conn.transaction():
            row_old = await conn.fetchrow(
                "SELECT status FROM connection_orders WHERE id=$1 FOR UPDATE",
                applications_id
            )
            if not row_old or row_old["status"] != 'between_controller_technician':
                return False

            row_new = await conn.fetchrow(
                """
                UPDATE connection_orders
                   SET status = 'in_technician'::connection_order_status,
                       updated_at = NOW()
                 WHERE id=$1 AND status='between_controller_technician'::connection_order_status
             RETURNING status
                """,
                applications_id
            )
            if not row_new:
                return False

            await conn.execute(
                """
                INSERT INTO connections (
                    connecion_id, sender_id, recipient_id,
                    sender_status, recipient_status, created_at, updated_at
                )
                VALUES ($1, $2, $2,
                        'between_controller_technician'::connection_order_status,
                        'in_technician'::connection_order_status,
                        NOW(), NOW())
                """,
                applications_id, technician_id
            )
            return True
    finally:
        await conn.close()

async def start_technician_work(applications_id: int, technician_id: int) -> bool:
    conn = await _conn()
    try:
        async with conn.transaction():
            row_old = await conn.fetchrow(
                "SELECT status FROM connection_orders WHERE id=$1 FOR UPDATE",
                applications_id
            )
            if not row_old or row_old["status"] != 'in_technician':
                return False

            row_new = await conn.fetchrow(
                """
                UPDATE connection_orders
                   SET status='in_technician_work'::connection_order_status,
                       updated_at=NOW()
                 WHERE id=$1 AND status='in_technician'::connection_order_status
             RETURNING status
                """,
                applications_id
            )
            if not row_new:
                return False

            await conn.execute(
                """
                INSERT INTO connections(
                    connecion_id, sender_id, recipient_id,
                    sender_status, recipient_status,
                    created_at, updated_at
                )
                VALUES ($1, $2, $2,
                        'in_technician'::connection_order_status,
                        'in_technician_work'::connection_order_status,
                        NOW(), NOW())
                """,
                applications_id, technician_id
            )
            return True
    finally:
        await conn.close()

async def finish_technician_work(applications_id: int, technician_id: int) -> bool:
    """
    Finish work -> status = 'completed'
    """
    new_status = 'completed'

    conn = await _conn()
    try:
        async with conn.transaction():
            row_old = await conn.fetchrow(
                "SELECT status FROM connection_orders WHERE id=$1 FOR UPDATE",
                applications_id
            )
            if not row_old or row_old["status"] != 'in_technician_work':
                return False

            ok = await conn.fetchrow(
                """
                UPDATE connection_orders
                   SET status = $2::connection_order_status,
                       updated_at = NOW()
                 WHERE id = $1 AND status = 'in_technician_work'::connection_order_status
             RETURNING id
                """,
                applications_id, new_status
            )
            if not ok:
                return False

            # history
            await conn.execute(
                """
                INSERT INTO connections (
                    connecion_id, sender_id, recipient_id,
                    sender_status, recipient_status, created_at, updated_at
                )
                VALUES ($1, $2, $2,
                        'in_technician_work'::connection_order_status,
                        $3::connection_order_status,
                        NOW(), NOW())
                """,
                applications_id, technician_id, new_status
            )
            return True
    finally:
        await conn.close()

# ----------------- MATERIALLAR -----------------
async def fetch_technician_materials(user_id: int) -> List[Dict[str, Any]]:
    conn = await _conn()
    try:
        rows = await conn.fetch(
            """
            SELECT
              m.id          AS material_id,
              m.name,
              m.price,
              m.serial_number,
              t.quantity    AS stock_quantity
            FROM material_and_technician t
            JOIN materials m ON m.id = t.material_id
            WHERE t.user_id = $1
              AND t.quantity > 0
            ORDER BY m.name
            """,
            user_id
        )
        return _as_dicts(rows)
    finally:
        await conn.close()

async def fetch_material_by_id(material_id: int) -> Optional[Dict[str, Any]]:
    conn = await _conn()
    try:
        row = await conn.fetchrow(
            "SELECT id, name, price, serial_number FROM materials WHERE id=$1",
            material_id
        )
        return dict(row) if row else None
    finally:
        await conn.close()

async def fetch_assigned_qty(user_id: int, material_id: int) -> int:
    """Texnikka biriktirilgan joriy qoldiq."""
    conn = await _conn()
    try:
        row = await conn.fetchrow(
            """
            SELECT COALESCE(quantity, 0) AS qty
            FROM material_and_technician
            WHERE user_id = $1 AND material_id = $2
            """,
            user_id, material_id
        )
        return int(row["qty"]) if row else 0
    finally:
        await conn.close()

# database/technician_queries.py
async def upsert_material_request_and_decrease_stock(
    user_id: int,
    applications_id: int,
    material_id: int,
    add_qty: int,
) -> None:
    if add_qty <= 0:
        raise ValueError("Miqdor 0 dan katta bo‘lishi kerak")

    conn = await _conn()
    try:
        async with conn.transaction():
            # Texnikdagi qoldiqni lock bilan tekshirish
            row = await conn.fetchrow(
                """
                SELECT quantity
                FROM material_and_technician
                WHERE user_id = $1 AND material_id = $2
                FOR UPDATE
                """,
                user_id, material_id
            )
            left_now = int(row["quantity"]) if row else 0
            if add_qty > left_now:
                raise ValueError(f"Sizga biriktirilgan miqdor: {left_now} dona")

            # AYNAN SIZ AYTGANDAY: material_requests ga yozish
            # mapping: $1=user_id, $2=applications_id, $3=material_id, $4=qty
            await conn.execute(
                """
                INSERT INTO material_requests (user_id, applications_id, material_id, description)
                VALUES ($1, $2, $3, ($4)::int::text)
                ON CONFLICT (user_id, applications_id, material_id)
                DO UPDATE SET
                    description = (
                        COALESCE(NULLIF(material_requests.description, '')::int, 0)
                        + ($4)::int
                    )::text
                """,
                user_id, applications_id, material_id, add_qty
            )

            # Texnik qoldig‘idan ayirish
            await conn.execute(
                """
                UPDATE material_and_technician
                SET quantity = quantity - $3
                WHERE user_id = $1 AND material_id = $2
                """,
                user_id, material_id, add_qty
            )
    finally:
        await conn.close()

async def fetch_selected_materials_for_request(
    user_id: int,
    applications_id: int
) -> List[Dict[str, Any]]:
    conn = await _conn()
    try:
        rows = await conn.fetch(
            """
            SELECT
                mr.material_id,
                m.name,
                m.price,
                mr.description AS description
            FROM material_requests mr
            JOIN materials m ON m.id = mr.material_id
            WHERE mr.user_id = $1
              AND mr.applications_id = $2
            ORDER BY m.name
            """,
            user_id, applications_id
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()


# YANGI: Texnik xizmat arizalari (technician_orders) bo‘yicha texnikka biriktirilgan ro‘yxat
async def fetch_technician_inbox_tech(
    technician_id: int,
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Texnik xizmat arizalari: oxirgi biriktirish bo‘yicha (connections) texnikka tegishlilari.
    Amal tugmalari hozircha ko‘rsatilmaydi (faqat ro‘yxat).
    """
    conn = await _conn()
    try:
        rows = await conn.fetch(
            """
            WITH last_conn AS (
                SELECT
                    c.*,
                    ROW_NUMBER() OVER (
                        PARTITION BY c.connecion_id, c.recipient_id
                        ORDER BY c.created_at DESC, c.id DESC
                    ) AS rn
                FROM connections c
                WHERE c.recipient_id = $1
            )
            SELECT
                to2.id,
                to2.address,
                to2.region,
                to2.status,
                to2.created_at,
                u.full_name AS client_name,
                u.phone     AS client_phone,
                NULL        AS tariff   -- UI mosligi uchun
            FROM last_conn c
            JOIN technician_orders to2 ON to2.id = c.connecion_id
            LEFT JOIN users u ON u.id = to2.user_id
            WHERE
                c.rn = 1
                AND to2.is_active = TRUE
                AND to2.status IN (
                    'between_controller_technician',  -- enum nomi sizdagi bilan mos
                    'in_technician',
                    'in_technician_work'
                )
            ORDER BY
                CASE to2.status
                    WHEN 'between_controller_technician' THEN 0
                    WHEN 'in_technician'                 THEN 1
                    WHEN 'in_technician_work'            THEN 2
                    ELSE 3
                END,
                to2.created_at DESC,
                to2.id DESC
            LIMIT $2 OFFSET $3
            """,
            technician_id, limit, offset
        )
        return _as_dicts(rows)
    finally:
        await conn.close()



# --- YANGI: texnik xizmat arizalari INBOX (technician_orders) ---
async def fetch_technician_inbox_tech(
    technician_id: int,
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Texnik xizmat arizalari: oxirgi biriktirish bo‘yicha texnikka tegishli faol arizalar.
    """
    conn = await _conn()
    try:
        rows = await conn.fetch(
            """
            WITH last_conn AS (
                SELECT
                    c.*,
                    ROW_NUMBER() OVER (
                        PARTITION BY c.connecion_id, c.recipient_id
                        ORDER BY c.created_at DESC, c.id DESC
                    ) AS rn
                FROM connections c
                WHERE c.recipient_id = $1
            )
            SELECT
                to2.id,
                to2.address,
                to2.region,
                to2.status,
                to2.created_at,
                u.full_name AS client_name,
                u.phone     AS client_phone,
                NULL        AS tariff     -- UI mosligi uchun
            FROM last_conn c
            JOIN technician_orders to2 ON to2.id = c.connecion_id
            LEFT JOIN users u ON u.id = to2.user_id
            WHERE
                c.rn = 1
                AND to2.is_active = TRUE
                AND to2.status IN ('between_controller_technician','in_technician','in_technician_work')
            ORDER BY
                CASE to2.status
                    WHEN 'between_controller_technician' THEN 0
                    WHEN 'in_technician'                 THEN 1
                    WHEN 'in_technician_work'            THEN 2
                    ELSE 3
                END,
                to2.created_at DESC,
                to2.id DESC
            LIMIT $2 OFFSET $3
            """,
            technician_id, limit, offset
        )
        return _as_dicts(rows)
    finally:
        await conn.close()


# --- YANGI: texnik xizmat arizasini qabul qilish (between_controller_technician -> in_technician) ---
async def accept_technician_work_for_tech(applications_id: int, technician_id: int) -> bool:
    conn = await _conn()
    try:
        async with conn.transaction():
            row_old = await conn.fetchrow(
                "SELECT status FROM technician_orders WHERE id=$1 FOR UPDATE",
                applications_id
            )
            if not row_old or row_old["status"] != 'between_controller_technician':
                return False

            row_new = await conn.fetchrow(
                """
                UPDATE technician_orders
                   SET status = 'in_technician',
                       updated_at = NOW()
                 WHERE id=$1 AND status='between_controller_technician'
             RETURNING status
                """,
                applications_id
            )
            if not row_new:
                return False

            try:
                await conn.execute(
                    """
                    INSERT INTO connections(
                        connecion_id, sender_id, recipient_id,
                        sender_status, recipient_status, created_at, updated_at
                    )
                    VALUES ($1, $2, $2, 'between_controller_technician', 'in_technician', NOW(), NOW())
                    """,
                    applications_id, technician_id
                )
            except Exception:
                pass  # tur mos kelmasa ham oqim to‘xtamasin
            return True
    finally:
        await conn.close()


# --- YANGI: ishni boshlash (in_technician -> in_technician_work) ---
async def start_technician_work_for_tech(applications_id: int, technician_id: int) -> bool:
    conn = await _conn()
    try:
        async with conn.transaction():
            row_old = await conn.fetchrow(
                "SELECT status FROM technician_orders WHERE id=$1 FOR UPDATE",
                applications_id
            )
            if not row_old or row_old["status"] != 'in_technician':
                return False

            row_new = await conn.fetchrow(
                """
                UPDATE technician_orders
                   SET status='in_technician_work',
                       updated_at=NOW()
                 WHERE id=$1 AND status='in_technician'
             RETURNING status
                """,
                applications_id
            )
            if not row_new:
                return False

            try:
                await conn.execute(
                    """
                    INSERT INTO connections(
                        connecion_id, sender_id, recipient_id,
                        sender_status, recipient_status, created_at, updated_at
                    )
                    VALUES ($1, $2, $2, 'in_technician', 'in_technician_work', NOW(), NOW())
                    """,
                    applications_id, technician_id
                )
            except Exception:
                pass
            return True
    finally:
        await conn.close()


# --- YANGI: diagnostika matnini saqlash (technician_orders.description_ish) ---
async def save_technician_diagnosis(applications_id: int, technician_id: int, text: str) -> None:
    conn = await _conn()
    try:
        async with conn.transaction():
            await conn.execute(
                """
                UPDATE technician_orders
                   SET description_ish = $2,
                       updated_at = NOW()
                 WHERE id = $1
                """,
                applications_id, text
            )
    finally:
        await conn.close()


# --- (ixtiyoriy) Bekor qilish (technician_orders) ---
async def cancel_technician_request_for_tech(applications_id: int, technician_id: int) -> None:
    conn = await _conn()
    try:
        async with conn.transaction():
            await conn.execute(
                "UPDATE technician_orders SET is_active = FALSE, updated_at = NOW() WHERE id=$1",
                applications_id
            )
    finally:
        await conn.close()


# --- YANGI: texnik xizmat arizasini yakunlash (technician_orders -> completed) ---
async def finish_technician_work_for_tech(applications_id: int, technician_id: int) -> bool:
    conn = await _conn()
    try:
        async with conn.transaction():
            row_old = await conn.fetchrow(
                "SELECT status FROM technician_orders WHERE id=$1 FOR UPDATE",
                applications_id
            )
            if not row_old or row_old["status"] != 'in_technician_work':
                return False

            ok = await conn.fetchrow(
                """
                UPDATE technician_orders
                   SET status='completed',
                       updated_at=NOW()
                 WHERE id=$1 AND status='in_technician_work'
             RETURNING id
                """,
                applications_id
            )
            if not ok:
                return False

            # (ixtiyoriy) tarixga yozish
            try:
                await conn.execute(
                    """
                    INSERT INTO connections(
                        connecion_id, sender_id, recipient_id,
                        sender_status, recipient_status, created_at, updated_at
                    )
                    VALUES ($1, $2, $2, 'in_technician_work', 'completed', NOW(), NOW())
                    """,
                    applications_id, technician_id
                )
            except Exception:
                pass

            return True
    finally:
        await conn.close()


# ====== SAFF ORDERS (Xodim arizalari) uchun funksiyalar ======

async def fetch_technician_inbox_saff(
    technician_id: int,
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Saff orders uchun texnikka biriktirilgan ro'yxat
    """
    conn = await _conn()
    try:
        with conn.transaction():
            # Saff orders uchun last_conn view yaratish
            await conn.execute("""
                CREATE OR REPLACE VIEW last_conn_saff AS
                WITH ranked_conns AS (
                    SELECT 
                        connecion_id, sender_id, recipient_id,
                        sender_status, recipient_status, technician_id, saff_id,
                        ROW_NUMBER() OVER (PARTITION BY connecion_id ORDER BY created_at DESC) as rn
                    FROM connections
                    WHERE connecion_id IN (SELECT id FROM saff_orders WHERE is_active = true)
                )
                SELECT * FROM ranked_conns WHERE rn = 1
            """)
            
            rows = await conn.fetch("""
                SELECT 
                    so.id,
                    so.phone,
                    so.region,
                    so.abonent_id,
                    so.address,
                    so.description,
                    so.status,
                    so.created_at,
                    u.full_name,
                    u.telegram_id,
                    NULL        AS tariff   -- UI mosligi uchun
                FROM last_conn_saff c
                JOIN saff_orders so ON so.id = c.connecion_id
                LEFT JOIN users u ON u.id = so.user_id
                WHERE
                    c.rn = 1
                    AND so.is_active = TRUE
                    AND so.status IN ('between_controller_technician','in_technician','in_technician_work')
                    AND c.technician_id = $1
                ORDER BY so.created_at DESC
                LIMIT $2 OFFSET $3
            """, technician_id, limit, offset)
            
            return _as_dicts(rows)
    finally:
        await conn.close()

async def accept_technician_work_for_saff(applications_id: int, technician_id: int) -> bool:
    """
    Saff order uchun texnik ishni qabul qilish
    """
    conn = await _conn()
    try:
        async with conn.transaction():
            row_old = await conn.fetchrow(
                "SELECT status FROM saff_orders WHERE id=$1 FOR UPDATE",
                applications_id
            )
            if not row_old or row_old["status"] != 'between_controller_technician':
                return False

            row_new = await conn.fetchrow(
                """
                UPDATE saff_orders
                   SET status = 'in_technician',
                       updated_at = NOW()
                 WHERE id=$1 AND status='between_controller_technician'
             RETURNING status
                """,
                applications_id
            )
            if not row_new:
                return False

            # Connections jadvaliga yozish
            await conn.execute(
                """
                INSERT INTO connections(
                    connecion_id, sender_id, recipient_id,
                    sender_status, recipient_status, technician_id, created_at, updated_at
                )
                VALUES ($1, $2, $2, 'in_technician', 'in_technician', $2, NOW(), NOW())
                """,
                applications_id, technician_id
            )

            return True
    finally:
        await conn.close()

async def start_technician_work_for_saff(applications_id: int, technician_id: int) -> bool:
    """
    Saff order uchun texnik ishni boshlash
    """
    conn = await _conn()
    try:
        async with conn.transaction():
            row_old = await conn.fetchrow(
                "SELECT status FROM saff_orders WHERE id=$1 FOR UPDATE",
                applications_id
            )
            if not row_old or row_old["status"] != 'in_technician':
                return False

            row_new = await conn.fetchrow(
                """
                UPDATE saff_orders
                   SET status='in_technician_work',
                       updated_at=NOW()
                 WHERE id=$1 AND status='in_technician'
             RETURNING status
                """,
                applications_id
            )
            if not row_new:
                return False

            # Connections jadvaliga yozish
            await conn.execute(
                """
                INSERT INTO connections(
                    connecion_id, sender_id, recipient_id,
                    sender_status, recipient_status, technician_id, created_at, updated_at
                )
                VALUES ($1, $2, $2, 'in_technician_work', 'in_technician_work', $2, NOW(), NOW())
                """,
                applications_id, technician_id
            )

            return True
    finally:
        await conn.close()

async def finish_technician_work_for_saff(applications_id: int, technician_id: int) -> bool:
    """
    Saff order uchun texnik ishni yakunlash
    """
    conn = await _conn()
    try:
        async with conn.transaction():
            row_old = await conn.fetchrow(
                "SELECT status FROM saff_orders WHERE id=$1 FOR UPDATE",
                applications_id
            )
            if not row_old or row_old["status"] != 'in_technician_work':
                return False

            row_new = await conn.fetchrow(
                """
                UPDATE saff_orders
                   SET status = 'completed',
                       updated_at = NOW()
                 WHERE id = $1 AND status = 'in_technician_work'
             RETURNING id
                """,
                applications_id
            )
            if not row_new:
                return False

            # Connections jadvaliga yozish
            try:
                await conn.execute(
                    """
                    INSERT INTO connections(
                        connecion_id, sender_id, recipient_id,
                        sender_status, recipient_status, technician_id, created_at, updated_at
                    )
                    VALUES ($1, $2, $2, 'in_technician_work', 'completed', $2, NOW(), NOW())
                    """,
                    applications_id, technician_id
                )
            except Exception:
                pass

            return True
    finally:
        await conn.close()