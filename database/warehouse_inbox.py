import asyncpg
from typing import List, Dict, Any, Optional
from config import settings


async def _conn():
    """Database connection helper"""
    return await asyncpg.connect(settings.DB_URL)


# ==================== CONNECTION ORDERS ====================

async def fetch_warehouse_connection_orders(
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Omborda turgan ulanish arizalari (connection_orders) - status: 'in_warehouse'
    """
    conn = await _conn()
    try:
        rows = await conn.fetch(
            """
            SELECT
                co.id,
                co.address,
                co.region,
                co.status,
                co.created_at,
                co.updated_at,
                co.notes,
                co.jm_notes,
                u.full_name AS client_name,
                u.phone AS client_phone,
                u.telegram_id AS client_telegram_id,
                t.name AS tariff_name
            FROM connection_orders co
            LEFT JOIN users u ON u.id = co.user_id
            LEFT JOIN tarif t ON t.id = co.tarif_id
            WHERE co.status = 'in_warehouse'
              AND co.is_active = TRUE
            ORDER BY co.created_at DESC
            LIMIT $1 OFFSET $2
            """,
            limit, offset
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()


async def count_warehouse_connection_orders() -> int:
    """
    Omborda turgan ulanish arizalari soni
    """
    conn = await _conn()
    try:
        count = await conn.fetchval(
            """
            SELECT COUNT(*)
            FROM connection_orders
            WHERE status = 'in_warehouse'
              AND is_active = TRUE
            """
        )
        return int(count or 0)
    finally:
        await conn.close()


# ==================== TECHNICIAN ORDERS ====================

async def fetch_warehouse_technician_orders(
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Omborda turgan texnik xizmat arizalari (technician_orders) - status: 'in_warehouse'
    """
    conn = await _conn()
    try:
        rows = await conn.fetch(
            """
            SELECT
                to_.id,
                to_.region,
                to_.address,
                to_.abonent_id,
                to_.description,
                to_.description_ish,
                to_.status,
                to_.created_at,
                to_.updated_at,
                to_.notes,
                u.full_name AS client_name,
                u.phone AS client_phone,
                u.telegram_id AS client_telegram_id
            FROM technician_orders to_
            LEFT JOIN users u ON u.id = to_.user_id
            WHERE to_.status = 'in_warehouse'
              AND to_.is_active = TRUE
            ORDER BY to_.created_at DESC
            LIMIT $1 OFFSET $2
            """,
            limit, offset
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()


async def count_warehouse_technician_orders() -> int:
    """
    Omborda turgan texnik xizmat arizalari soni
    """
    conn = await _conn()
    try:
        count = await conn.fetchval(
            """
            SELECT COUNT(*)
            FROM technician_orders
            WHERE status = 'in_warehouse'
              AND is_active = TRUE
            """
        )
        return int(count or 0)
    finally:
        await conn.close()


# ==================== STAFF ORDERS (SAFF_ORDERS) ====================

async def fetch_warehouse_staff_orders(
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Omborda turgan xodim arizalari (saff_orders) - status: 'in_warehouse'
    """
    conn = await _conn()
    try:
        rows = await conn.fetch(
            """
            SELECT
                so.id,
                so.phone,
                so.region,
                so.abonent_id,
                so.address,
                so.description,
                so.status,
                so.type_of_zayavka,
                so.created_at,
                so.updated_at,
                u.full_name AS client_name,
                u.phone AS client_phone,
                u.telegram_id AS client_telegram_id,
                t.name AS tariff_name
            FROM saff_orders so
            LEFT JOIN users u ON u.id = so.user_id
            LEFT JOIN tarif t ON t.id = so.tarif_id
            WHERE so.status = 'in_warehouse'
              AND so.is_active = TRUE
            ORDER BY so.created_at DESC
            LIMIT $1 OFFSET $2
            """,
            limit, offset
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()


async def count_warehouse_staff_orders() -> int:
    """
    Omborda turgan xodim arizalari soni
    """
    conn = await _conn()
    try:
        count = await conn.fetchval(
            """
            SELECT COUNT(*)
            FROM saff_orders
            WHERE status = 'in_warehouse'
              AND is_active = TRUE
            """
        )
        return int(count or 0)
    finally:
        await conn.close()


# ==================== UMUMIY FUNKSIYALAR ====================

async def get_all_warehouse_orders_count() -> Dict[str, int]:
    """
    Barcha ombor arizalari sonini qaytaradi
    """
    connection_count = await count_warehouse_connection_orders()
    technician_count = await count_warehouse_technician_orders()
    staff_count = await count_warehouse_staff_orders()
    
    return {
        "connection_orders": connection_count,
        "technician_orders": technician_count,
        "staff_orders": staff_count,
        "total": connection_count + technician_count + staff_count
    }


async def get_warehouse_order_by_id_and_type(order_id: int, order_type: str) -> Optional[Dict[str, Any]]:
    """
    ID va tur bo'yicha bitta arizani olish
    order_type: 'connection', 'technician', 'staff'
    """
    conn = await _conn()
    try:
        if order_type == 'connection':
            row = await conn.fetchrow(
                """
                SELECT
                    co.id,
                    co.address,
                    co.region,
                    co.status,
                    co.created_at,
                    co.notes,
                    co.jm_notes,
                    u.full_name AS client_name,
                    u.phone AS client_phone,
                    t.name AS tariff_name
                FROM connection_orders co
                LEFT JOIN users u ON u.id = co.user_id
                LEFT JOIN tarif t ON t.id = co.tarif_id
                WHERE co.id = $1 AND co.status = 'in_warehouse' AND co.is_active = TRUE
                """,
                order_id
            )
        elif order_type == 'technician':
            row = await conn.fetchrow(
                """
                SELECT
                    to_.id,
                    to_.region,
                    to_.address,
                    to_.abonent_id,
                    to_.description,
                    to_.status,
                    to_.created_at,
                    to_.notes,
                    u.full_name AS client_name,
                    u.phone AS client_phone
                FROM technician_orders to_
                LEFT JOIN users u ON u.id = to_.user_id
                WHERE to_.id = $1 AND to_.status = 'in_warehouse' AND to_.is_active = TRUE
                """,
                order_id
            )
        elif order_type == 'staff':
            row = await conn.fetchrow(
                """
                SELECT
                    so.id,
                    so.phone,
                    so.region,
                    so.abonent_id,
                    so.address,
                    so.description,
                    so.status,
                    so.type_of_zayavka,
                    so.created_at,
                    u.full_name AS client_name,
                    t.name AS tariff_name
                FROM saff_orders so
                LEFT JOIN users u ON u.id = so.user_id
                LEFT JOIN tarif t ON t.id = so.tarif_id
                WHERE so.id = $1 AND so.status = 'in_warehouse' AND so.is_active = TRUE
                """,
                order_id
            )
        else:
            return None
            
        return dict(row) if row else None
    finally:
        await conn.close()


# ==================== MATERIAL REQUESTS ====================

async def fetch_material_requests_by_connection_orders(
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Ulanish arizalariga bog'langan material so'rovlari
    """
    conn = await _conn()
    try:
        rows = await conn.fetch(
            """
            SELECT
                mr.id,
                mr.description,
                mr.quantity,
                mr.price,
                mr.total_price,
                mr.connection_order_id,
                co.address,
                co.region,
                u.full_name AS client_name,
                u.phone AS client_phone,
                m.name AS material_name,
                co.created_at AS order_created_at
            FROM material_requests mr
            JOIN connection_orders co ON co.id = mr.connection_order_id
            LEFT JOIN users u ON u.id = co.user_id
            LEFT JOIN materials m ON m.id = mr.material_id
            WHERE mr.connection_order_id IS NOT NULL
            ORDER BY co.created_at DESC
            LIMIT $1 OFFSET $2
            """,
            limit, offset
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()


async def fetch_material_requests_by_technician_orders(
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Texnik xizmat arizalariga bog'langan material so'rovlari
    """
    conn = await _conn()
    try:
        rows = await conn.fetch(
            """
            SELECT
                mr.id,
                mr.description,
                mr.quantity,
                mr.price,
                mr.total_price,
                mr.technician_order_id,
                to_.address,
                to_.region,
                to_.abonent_id,
                to_.description AS order_description,
                u.full_name AS client_name,
                u.phone AS client_phone,
                m.name AS material_name,
                to_.created_at AS order_created_at
            FROM material_requests mr
            JOIN technician_orders to_ ON to_.id = mr.technician_order_id
            LEFT JOIN users u ON u.id = to_.user_id
            LEFT JOIN materials m ON m.id = mr.material_id
            WHERE mr.technician_order_id IS NOT NULL
            ORDER BY to_.created_at DESC
            LIMIT $1 OFFSET $2
            """,
            limit, offset
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()


async def fetch_material_requests_by_staff_orders(
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Xodim arizalariga bog'langan material so'rovlari
    """
    conn = await _conn()
    try:
        rows = await conn.fetch(
            """
            SELECT
                mr.id,
                mr.description,
                mr.quantity,
                mr.price,
                mr.total_price,
                mr.saff_order_id,
                so.address,
                so.region,
                so.abonent_id,
                so.description AS order_description,
                so.type_of_zayavka,
                u.full_name AS client_name,
                u.phone AS client_phone,
                m.name AS material_name,
                so.created_at AS order_created_at
            FROM material_requests mr
            JOIN saff_orders so ON so.id = mr.saff_order_id
            LEFT JOIN users u ON u.id = so.user_id
            LEFT JOIN materials m ON m.id = mr.material_id
            WHERE mr.saff_order_id IS NOT NULL
            ORDER BY so.created_at DESC
            LIMIT $1 OFFSET $2
            """,
            limit, offset
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()


async def count_material_requests_by_connection_orders() -> int:
    """
    Ulanish arizalariga bog'langan material so'rovlari soni
    """
    conn = await _conn()
    try:
        count = await conn.fetchval(
            """
            SELECT COUNT(*)
            FROM material_requests mr
            JOIN connection_orders co ON co.id = mr.connection_order_id
            WHERE mr.connection_order_id IS NOT NULL
            """
        )
        return int(count or 0)
    finally:
        await conn.close()


async def count_material_requests_by_technician_orders() -> int:
    """
    Texnik xizmat arizalariga bog'langan material so'rovlari soni
    """
    conn = await _conn()
    try:
        count = await conn.fetchval(
            """
            SELECT COUNT(*)
            FROM material_requests mr
            JOIN technician_orders to_ ON to_.id = mr.technician_order_id
            WHERE mr.technician_order_id IS NOT NULL
            """
        )
        return int(count or 0)
    finally:
        await conn.close()


async def count_material_requests_by_staff_orders() -> int:
    """
    Xodim arizalariga bog'langan material so'rovlari soni
    """
    conn = await _conn()
    try:
        count = await conn.fetchval(
            """
            SELECT COUNT(*)
            FROM material_requests mr
            JOIN saff_orders so ON so.id = mr.saff_order_id
            WHERE mr.saff_order_id IS NOT NULL
            """
        )
        return int(count or 0)
    finally:
        await conn.close()


async def get_all_material_requests_count() -> Dict[str, int]:
    """
    Barcha material so'rovlari sonini qaytaradi
    """
    connection_count = await count_material_requests_by_connection_orders()
    technician_count = await count_material_requests_by_technician_orders()
    staff_count = await count_material_requests_by_staff_orders()
    
    return {
        "connection_orders": connection_count,
        "technician_orders": technician_count,
        "staff_orders": staff_count,
        "total": connection_count + technician_count + staff_count
    }