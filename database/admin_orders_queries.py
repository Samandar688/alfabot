import asyncpg
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from config import settings
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def get_connection():
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        yield conn
    finally:
        await conn.close()

# ==================== DASHBOARD STATISTIKALARI ====================
async def get_dashboard_statistics() -> Dict[str, Any]:
    """
    Umumiy dashboard uchun statistikalarni olish
    """
    try:
        async with get_connection() as conn:
            # Bugungi statistika
            today = datetime.now().date()
            
            # Bugungi zayavkalar soni
            today_connection = await conn.fetchval(
                "SELECT COUNT(*) FROM connection_orders WHERE DATE(created_at) = $1",
                today
            )
            today_technician = await conn.fetchval(
                "SELECT COUNT(*) FROM technician_orders WHERE DATE(created_at) = $1",
                today
            )
            today_saff = await conn.fetchval(
                "SELECT COUNT(*) FROM saff_orders WHERE DATE(created_at) = $1",
                today
            )
            
            today_total = today_connection + today_technician + today_saff
            
            # Bu hafta statistikasi
            week_start = today - timedelta(days=today.weekday())
            week_total = await conn.fetchval(
                """
                SELECT 
                    (SELECT COUNT(*) FROM connection_orders WHERE DATE(created_at) >= $1) +
                    (SELECT COUNT(*) FROM technician_orders WHERE DATE(created_at) >= $1) +
                    (SELECT COUNT(*) FROM saff_orders WHERE DATE(created_at) >= $1)
                """,
                week_start
            )
            
            # O'tgan hafta statistikasi
            prev_week_start = week_start - timedelta(days=7)
            prev_week_end = week_start - timedelta(days=1)
            prev_week_total = await conn.fetchval(
                """
                SELECT 
                    (SELECT COUNT(*) FROM connection_orders WHERE DATE(created_at) BETWEEN $1 AND $2) +
                    (SELECT COUNT(*) FROM technician_orders WHERE DATE(created_at) BETWEEN $1 AND $2) +
                    (SELECT COUNT(*) FROM saff_orders WHERE DATE(created_at) BETWEEN $1 AND $2)
                """,
                prev_week_start, prev_week_end
            )
            
            # Kritik zayavkalar (3 kundan ortiq)
            critical_date = datetime.now() - timedelta(days=3)
            critical_count = await conn.fetchval(
                """
                SELECT 
                    (SELECT COUNT(*) FROM connection_orders WHERE created_at < $1 AND status != 'completed') +
                    (SELECT COUNT(*) FROM technician_orders WHERE created_at < $1 AND status != 'completed') +
                    (SELECT COUNT(*) FROM saff_orders WHERE created_at < $1 AND status != 'completed')
                """,
                critical_date
            )
            
            # Kechikkan zayavkalar (1 haftadan ortiq)
            delayed_date = datetime.now() - timedelta(days=7)
            delayed_count = await conn.fetchval(
                """
                SELECT 
                    (SELECT COUNT(*) FROM connection_orders WHERE created_at < $1 AND status != 'completed') +
                    (SELECT COUNT(*) FROM technician_orders WHERE created_at < $1 AND status != 'completed') +
                    (SELECT COUNT(*) FROM saff_orders WHERE created_at < $1 AND status != 'completed')
                """,
                delayed_date
            )
            
            return {
                'today_total': today_total,
                'today_connection': today_connection,
                'today_technician': today_technician,
                'today_saff': today_saff,
                'week_total': week_total,
                'prev_week_total': prev_week_total,
                'week_change': week_total - prev_week_total,
                'critical_count': critical_count,
                'delayed_count': delayed_count
            }
            
    except Exception as e:
        logger.error(f"Dashboard statistikalarini olishda xatolik: {e}")
        return {
            'today_total': 0, 'today_connection': 0, 'today_technician': 0, 'today_saff': 0,
            'week_total': 0, 'prev_week_total': 0, 'week_change': 0,
            'critical_count': 0, 'delayed_count': 0
        }

# ==================== BUGUNGI STATISTIKA ====================
async def get_today_statistics() -> Dict[str, Any]:
    """
    Bugungi batafsil statistikalarni olish
    """
    try:
        async with get_connection() as conn:
            today = datetime.now().date()
            
            # Connection orders statistikasi
            connection_stats = await conn.fetchrow(
                """
                SELECT 
                    COUNT(*) as total,
                    COUNT(*) FILTER (WHERE status = 'new') as new,
                    COUNT(*) FILTER (WHERE status IN ('in_manager', 'in_junior_manager', 'in_controller', 'in_technician', 'in_diagnostics', 'in_repairs', 'in_warehouse', 'in_technician_work', 'between_controller_technician')) as in_progress,
                    COUNT(*) FILTER (WHERE status = 'completed') as completed
                FROM connection_orders 
                WHERE DATE(created_at) = $1
                """,
                today
            )
            
            # Technician orders statistikasi
            technician_stats = await conn.fetchrow(
                """
                SELECT 
                    COUNT(*) as total,
                    COUNT(*) FILTER (WHERE status = 'new') as new,
                    COUNT(*) FILTER (WHERE status IN ('in_controller', 'in_technician', 'in_diagnostics', 'in_repairs', 'in_warehouse', 'in_technician_work', 'between_controller_technician')) as in_progress,
                    COUNT(*) FILTER (WHERE status = 'completed') as completed
                FROM technician_orders 
                WHERE DATE(created_at) = $1
                """,
                today
            )
            
            # Saff orders statistikasi
            saff_stats = await conn.fetchrow(
                """
                SELECT 
                    COUNT(*) as total,
                    COUNT(*) FILTER (WHERE status = 'new') as new,
                    COUNT(*) FILTER (WHERE status IN ('in_manager', 'in_junior_manager', 'in_controller', 'in_technician', 'in_technician_work')) as in_progress,
                    COUNT(*) FILTER (WHERE status = 'completed') as completed
                FROM saff_orders 
                WHERE DATE(created_at) = $1
                """,
                today
            )
            
            total_all = connection_stats['total'] + technician_stats['total'] + saff_stats['total']
            
            return {
                'connection_total': connection_stats['total'],
                'connection_new': connection_stats['new'],
                'connection_in_progress': connection_stats['in_progress'],
                'connection_completed': connection_stats['completed'],
                'technician_total': technician_stats['total'],
                'technician_new': technician_stats['new'],
                'technician_in_progress': technician_stats['in_progress'],
                'technician_completed': technician_stats['completed'],
                'saff_total': saff_stats['total'],
                'saff_new': saff_stats['new'],
                'saff_in_progress': saff_stats['in_progress'],
                'saff_completed': saff_stats['completed'],
                'total_all': total_all
            }
            
    except Exception as e:
        logger.error(f"Bugungi statistikalarni olishda xatolik: {e}")
        return {
            'connection_total': 0, 'connection_new': 0, 'connection_in_progress': 0, 'connection_completed': 0,
            'technician_total': 0, 'technician_new': 0, 'technician_in_progress': 0, 'technician_completed': 0,
            'saff_total': 0, 'saff_new': 0, 'saff_in_progress': 0, 'saff_completed': 0,
            'total_all': 0
        }

# ==================== HAFTALIK TREND ====================
async def get_weekly_trend() -> List[Dict[str, Any]]:
    """
    Haftalik trend ma'lumotlarini olish
    """
    try:
        async with get_connection() as conn:
            today = datetime.now().date()
            week_start = today - timedelta(days=today.weekday())
            
            trend_data = []
            day_names = ['Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba', 'Yakshanba']
            
            for i in range(7):
                day_date = week_start + timedelta(days=i)
                day_name = day_names[i]
                
                # Har bir kun uchun statistika
                connection_count = await conn.fetchval(
                    "SELECT COUNT(*) FROM connection_orders WHERE DATE(created_at) = $1",
                    day_date
                )
                technician_count = await conn.fetchval(
                    "SELECT COUNT(*) FROM technician_orders WHERE DATE(created_at) = $1",
                    day_date
                )
                saff_count = await conn.fetchval(
                    "SELECT COUNT(*) FROM saff_orders WHERE DATE(created_at) = $1",
                    day_date
                )
                
                total_count = connection_count + technician_count + saff_count
                
                trend_data.append({
                    'day_name': day_name,
                    'date': day_date,
                    'total': total_count,
                    'connection': connection_count,
                    'technician': technician_count,
                    'saff': saff_count
                })
            
            return trend_data
            
    except Exception as e:
        logger.error(f"Haftalik trend ma'lumotlarini olishda xatolik: {e}")
        return []

# ==================== KRITIK ZAYAVKALAR ====================
async def get_critical_orders(limit: int = 20) -> List[Dict[str, Any]]:
    """
    Kritik zayavkalarni olish (3 kundan ortiq)
    """
    try:
        async with get_connection() as conn:
            critical_date = datetime.now() - timedelta(days=3)
            
            # Connection orders
            connection_orders = await conn.fetch(
                """
                SELECT id, status, created_at, address, 'connection' as type
                FROM connection_orders 
                WHERE created_at < $1 AND status != 'completed'
                ORDER BY created_at ASC
                LIMIT $2
                """,
                critical_date, limit // 3
            )
            
            # Technician orders
            technician_orders = await conn.fetch(
                """
                SELECT id, status, created_at, address, 'technician' as type
                FROM technician_orders 
                WHERE created_at < $1 AND status != 'completed'
                ORDER BY created_at ASC
                LIMIT $2
                """,
                critical_date, limit // 3
            )
            
            # Saff orders
            saff_orders = await conn.fetch(
                """
                SELECT id, status, created_at, address, 'saff' as type
                FROM saff_orders 
                WHERE created_at < $1 AND status != 'completed'
                ORDER BY created_at ASC
                LIMIT $2
                """,
                critical_date, limit // 3
            )
            
            # Barcha zayavkalarni birlashtirish
            all_orders = list(connection_orders) + list(technician_orders) + list(saff_orders)
            
            # Vaqt bo'yicha saralash
            all_orders.sort(key=lambda x: x['created_at'])
            
            return [dict(order) for order in all_orders[:limit]]
            
    except Exception as e:
        logger.error(f"Kritik zayavkalarni olishda xatolik: {e}")
        return []

# ==================== KECHIKKAN ZAYAVKALAR ====================
async def get_delayed_orders(limit: int = 20) -> List[Dict[str, Any]]:
    """
    Kechikkan zayavkalarni olish (1 haftadan ortiq)
    """
    try:
        async with get_connection() as conn:
            delayed_date = datetime.now() - timedelta(days=7)
            
            # Connection orders
            connection_orders = await conn.fetch(
                """
                SELECT id, status, created_at, address, 'connection' as type
                FROM connection_orders 
                WHERE created_at < $1 AND status != 'completed'
                ORDER BY created_at ASC
                LIMIT $2
                """,
                delayed_date, limit // 3
            )
            
            # Technician orders
            technician_orders = await conn.fetch(
                """
                SELECT id, status, created_at, address, 'technician' as type
                FROM technician_orders 
                WHERE created_at < $1 AND status != 'completed'
                ORDER BY created_at ASC
                LIMIT $2
                """,
                delayed_date, limit // 3
            )
            
            # Saff orders
            saff_orders = await conn.fetch(
                """
                SELECT id, status, created_at, address, 'saff' as type
                FROM saff_orders 
                WHERE created_at < $1 AND status != 'completed'
                ORDER BY created_at ASC
                LIMIT $2
                """,
                delayed_date, limit // 3
            )
            
            # Barcha zayavkalarni birlashtirish
            all_orders = list(connection_orders) + list(technician_orders) + list(saff_orders)
            
            # Vaqt bo'yicha saralash
            all_orders.sort(key=lambda x: x['created_at'])
            
            return [dict(order) for order in all_orders[:limit]]
            
    except Exception as e:
        logger.error(f"Kechikkan zayavkalarni olishda xatolik: {e}")
        return []

# ==================== COMMON PAGINATION UTILS ====================
def _calc_pagination(total: int, page: int, per_page: int) -> Tuple[int, bool, bool]:
    total_pages = max(1, (total + per_page - 1) // per_page)
    has_next = page < total_pages
    has_prev = page > 1
    return total_pages, has_prev, has_next

# ==================== CONNECTION ORDERS ====================
async def get_connection_orders_list(page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    try:
        async with get_connection() as conn:
            total = await conn.fetchval("SELECT COUNT(*) FROM connection_orders")
            offset = (page - 1) * per_page
            rows = await conn.fetch(
                """
                SELECT id, user_id, region, address, status, created_at
                FROM connection_orders
                ORDER BY created_at DESC
                LIMIT $1 OFFSET $2
                """,
                per_page, offset
            )
            total_pages, has_prev, has_next = _calc_pagination(total, page, per_page)
            return {
                'items': [dict(r) for r in rows],
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': total_pages,
                'has_prev': has_prev,
                'has_next': has_next,
            }
    except Exception as e:
        logger.error(f"Connection orders ro'yxatini olishda xatolik: {e}")
        return {'items': [], 'total': 0, 'page': page, 'per_page': per_page, 'total_pages': 1, 'has_prev': False, 'has_next': False}

async def search_connection_orders(query: str, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    try:
        async with get_connection() as conn:
            like = f"%{query}%"
            total = await conn.fetchval(
                """
                SELECT COUNT(*) FROM connection_orders
                WHERE CAST(id AS TEXT) ILIKE $1 OR address ILIKE $1 OR region ILIKE $1
                """, like
            )
            offset = (page - 1) * per_page
            rows = await conn.fetch(
                """
                SELECT id, user_id, region, address, status, created_at
                FROM connection_orders
                WHERE CAST(id AS TEXT) ILIKE $1 OR address ILIKE $1 OR region ILIKE $1
                ORDER BY created_at DESC
                LIMIT $2 OFFSET $3
                """, like, per_page, offset
            )
            total_pages, has_prev, has_next = _calc_pagination(total, page, per_page)
            return {'items': [dict(r) for r in rows], 'total': total, 'page': page, 'per_page': per_page, 'total_pages': total_pages, 'has_prev': has_prev, 'has_next': has_next}
    except Exception as e:
        logger.error(f"Connection orders qidirishda xatolik: {e}")
        return {'items': [], 'total': 0, 'page': page, 'per_page': per_page, 'total_pages': 1, 'has_prev': False, 'has_next': False}

async def filter_connection_orders(status: Optional[str] = None, region: Optional[str] = None, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    try:
        async with get_connection() as conn:
            conditions = []
            params: List[Any] = []
            if status:
                params.append(status)
                conditions.append(f"status = ${len(params)}")
            if region:
                params.append(region)
                conditions.append(f"region ILIKE ${len(params)}")
                params[-1] = f"%{params[-1]}%"
            if date_from:
                params.append(date_from)
                conditions.append(f"created_at >= ${len(params)}")
            if date_to:
                params.append(date_to)
                conditions.append(f"created_at <= ${len(params)}")

            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            total = await conn.fetchval(f"SELECT COUNT(*) FROM connection_orders {where_clause}", *params)
            offset = (page - 1) * per_page
            rows = await conn.fetch(
                f"""
                SELECT id, user_id, region, address, status, created_at
                FROM connection_orders
                {where_clause}
                ORDER BY created_at DESC
                LIMIT ${len(params)+1} OFFSET ${len(params)+2}
                """,
                *params, per_page, offset
            )
            total_pages, has_prev, has_next = _calc_pagination(total, page, per_page)
            return {'items': [dict(r) for r in rows], 'total': total, 'page': page, 'per_page': per_page, 'total_pages': total_pages, 'has_prev': has_prev, 'has_next': has_next}
    except Exception as e:
        logger.error(f"Connection orders filterlashda xatolik: {e}")
        return {'items': [], 'total': 0, 'page': page, 'per_page': per_page, 'total_pages': 1, 'has_prev': False, 'has_next': False}

# ==================== TECHNICIAN ORDERS ====================
async def get_technician_orders_list(page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    try:
        async with get_connection() as conn:
            total = await conn.fetchval("SELECT COUNT(*) FROM technician_orders")
            offset = (page - 1) * per_page
            rows = await conn.fetch(
                """
                SELECT id, user_id, abonent_id, address, status, created_at
                FROM technician_orders
                ORDER BY created_at DESC
                LIMIT $1 OFFSET $2
                """,
                per_page, offset
            )
            total_pages, has_prev, has_next = _calc_pagination(total, page, per_page)
            return {'items': [dict(r) for r in rows], 'total': total, 'page': page, 'per_page': per_page, 'total_pages': total_pages, 'has_prev': has_prev, 'has_next': has_next}
    except Exception as e:
        logger.error(f"Technician orders ro'yxatini olishda xatolik: {e}")
        return {'items': [], 'total': 0, 'page': page, 'per_page': per_page, 'total_pages': 1, 'has_prev': False, 'has_next': False}

async def search_technician_orders(query: str, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    try:
        async with get_connection() as conn:
            like = f"%{query}%"
            total = await conn.fetchval(
                """
                SELECT COUNT(*) FROM technician_orders
                WHERE CAST(id AS TEXT) ILIKE $1 OR abonent_id ILIKE $1 OR address ILIKE $1
                """, like
            )
            offset = (page - 1) * per_page
            rows = await conn.fetch(
                """
                SELECT id, user_id, abonent_id, address, status, created_at
                FROM technician_orders
                WHERE CAST(id AS TEXT) ILIKE $1 OR abonent_id ILIKE $1 OR address ILIKE $1
                ORDER BY created_at DESC
                LIMIT $2 OFFSET $3
                """, like, per_page, offset
            )
            total_pages, has_prev, has_next = _calc_pagination(total, page, per_page)
            return {'items': [dict(r) for r in rows], 'total': total, 'page': page, 'per_page': per_page, 'total_pages': total_pages, 'has_prev': has_prev, 'has_next': has_next}
    except Exception as e:
        logger.error(f"Technician orders qidirishda xatolik: {e}")
        return {'items': [], 'total': 0, 'page': page, 'per_page': per_page, 'total_pages': 1, 'has_prev': False, 'has_next': False}

async def filter_technician_orders(status: Optional[str] = None, technician_id: Optional[int] = None, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    try:
        async with get_connection() as conn:
            conditions = []
            params: List[Any] = []
            if status:
                params.append(status)
                conditions.append(f"status = ${len(params)}")
            if technician_id:
                params.append(technician_id)
                conditions.append(f"user_id = ${len(params)}")
            if date_from:
                params.append(date_from)
                conditions.append(f"created_at >= ${len(params)}")
            if date_to:
                params.append(date_to)
                conditions.append(f"created_at <= ${len(params)}")
            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            total = await conn.fetchval(f"SELECT COUNT(*) FROM technician_orders {where_clause}", *params)
            offset = (page - 1) * per_page
            rows = await conn.fetch(
                f"""
                SELECT id, user_id, abonent_id, address, status, created_at
                FROM technician_orders
                {where_clause}
                ORDER BY created_at DESC
                LIMIT ${len(params)+1} OFFSET ${len(params)+2}
                """,
                *params, per_page, offset
            )
            total_pages, has_prev, has_next = _calc_pagination(total, page, per_page)
            return {'items': [dict(r) for r in rows], 'total': total, 'page': page, 'per_page': per_page, 'total_pages': total_pages, 'has_prev': has_prev, 'has_next': has_next}
    except Exception as e:
        logger.error(f"Technician orders filterlashda xatolik: {e}")
        return {'items': [], 'total': 0, 'page': page, 'per_page': per_page, 'total_pages': 1, 'has_prev': False, 'has_next': False}

# ==================== SAFF ORDERS ====================
async def get_saff_orders_list(page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    try:
        async with get_connection() as conn:
            total = await conn.fetchval("SELECT COUNT(*) FROM saff_orders")
            offset = (page - 1) * per_page
            rows = await conn.fetch(
                """
                SELECT id, user_id, phone, address, status, type_of_zayavka, created_at
                FROM saff_orders
                ORDER BY created_at DESC
                LIMIT $1 OFFSET $2
                """,
                per_page, offset
            )
            total_pages, has_prev, has_next = _calc_pagination(total, page, per_page)
            return {'items': [dict(r) for r in rows], 'total': total, 'page': page, 'per_page': per_page, 'total_pages': total_pages, 'has_prev': has_prev, 'has_next': has_next}
    except Exception as e:
        logger.error(f"Saff orders ro'yxatini olishda xatolik: {e}")
        return {'items': [], 'total': 0, 'page': page, 'per_page': per_page, 'total_pages': 1, 'has_prev': False, 'has_next': False}

async def search_saff_orders(query: str, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    try:
        async with get_connection() as conn:
            like = f"%{query}%"
            total = await conn.fetchval(
                """
                SELECT COUNT(*) FROM saff_orders
                WHERE CAST(id AS TEXT) ILIKE $1 OR phone ILIKE $1 OR address ILIKE $1
                """, like
            )
            offset = (page - 1) * per_page
            rows = await conn.fetch(
                """
                SELECT id, user_id, phone, address, status, type_of_zayavka, created_at
                FROM saff_orders
                WHERE CAST(id AS TEXT) ILIKE $1 OR phone ILIKE $1 OR address ILIKE $1
                ORDER BY created_at DESC
                LIMIT $2 OFFSET $3
                """, like, per_page, offset
            )
            total_pages, has_prev, has_next = _calc_pagination(total, page, per_page)
            return {'items': [dict(r) for r in rows], 'total': total, 'page': page, 'per_page': per_page, 'total_pages': total_pages, 'has_prev': has_prev, 'has_next': has_next}
    except Exception as e:
        logger.error(f"Saff orders qidirishda xatolik: {e}")
        return {'items': [], 'total': 0, 'page': page, 'per_page': per_page, 'total_pages': 1, 'has_prev': False, 'has_next': False}

async def filter_saff_orders(status: Optional[str] = None, creator_user_id: Optional[int] = None, type_of_zayavka: Optional[str] = None, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    try:
        async with get_connection() as conn:
            conditions = []
            params: List[Any] = []
            if status:
                params.append(status)
                conditions.append(f"status = ${len(params)}")
            if creator_user_id:
                params.append(creator_user_id)
                conditions.append(f"user_id = ${len(params)}")
            if type_of_zayavka:
                params.append(type_of_zayavka)
                conditions.append(f"type_of_zayavka = ${len(params)}")
            if date_from:
                params.append(date_from)
                conditions.append(f"created_at >= ${len(params)}")
            if date_to:
                params.append(date_to)
                conditions.append(f"created_at <= ${len(params)}")
            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            total = await conn.fetchval(f"SELECT COUNT(*) FROM saff_orders {where_clause}", *params)
            offset = (page - 1) * per_page
            rows = await conn.fetch(
                f"""
                SELECT id, user_id, phone, address, status, type_of_zayavka, created_at
                FROM saff_orders
                {where_clause}
                ORDER BY created_at DESC
                LIMIT ${len(params)+1} OFFSET ${len(params)+2}
                """,
                *params, per_page, offset
            )
            total_pages, has_prev, has_next = _calc_pagination(total, page, per_page)
            return {'items': [dict(r) for r in rows], 'total': total, 'page': page, 'per_page': per_page, 'total_pages': total_pages, 'has_prev': has_prev, 'has_next': has_next}
    except Exception as e:
        logger.error(f"Saff orders filterlashda xatolik: {e}")
        return {'items': [], 'total': 0, 'page': page, 'per_page': per_page, 'total_pages': 1, 'has_prev': False, 'has_next': False}