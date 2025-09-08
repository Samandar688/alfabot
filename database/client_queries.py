import asyncpg
from config import settings
from typing import Optional

async def find_user_by_telegram_id(telegram_id: int) -> Optional[asyncpg.Record]:
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        result = await conn.fetchrow(
            """
            SELECT * FROM users WHERE telegram_id = $1
            """
        , telegram_id)
        return result
    finally:
        await conn.close()

async def create_service_order(user_id: int, region: str, abonent_id: str, address: str, description: str, media: str, geo: str) -> int:
    """Create a service order in technician_orders table.

    technician_orders schema:
      user_id BIGINT, region_id INTEGER, abonent_id TEXT, address TEXT,
      media TEXT, longitude DOUBLE PRECISION, latitude DOUBLE PRECISION,
      description TEXT, status technician_order_status DEFAULT 'new', ...
    """
    latitude = None
    longitude = None
    if geo:
        try:
            lat_str, lon_str = geo.split(",", 1)
            latitude = float(lat_str)
            longitude = float(lon_str)
        except Exception:
            latitude = None
            longitude = None

    conn = await asyncpg.connect(settings.DB_URL)
    try:
        row = await conn.fetchrow(
            """
            INSERT INTO technician_orders (user_id, region_id, abonent_id, address, media, longitude, latitude, description, status)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING id
            """,
            user_id, None, abonent_id, address, media, longitude, latitude, description, 'in_controller'
        )
        return row["id"]
    finally:
        await conn.close()

# -----------------------------
# Connection order helpers
# -----------------------------

async def ensure_user(telegram_id: int, full_name: Optional[str], username: Optional[str]) -> asyncpg.Record:
    """Create user if not exists with sequential ID; return row."""
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        # Avval mavjud userni tekshirish
        existing_user = await conn.fetchrow(
            "SELECT * FROM users WHERE telegram_id = $1",
            telegram_id
        )
        
        if existing_user:
            # Mavjud userni yangilash
            row = await conn.fetchrow(
                """
                UPDATE users 
                SET full_name = $2, username = $3, updated_at = NOW()
                WHERE telegram_id = $1
                RETURNING *
                """,
                telegram_id, full_name, username
            )
            return row
        else:
            # Ketma-ket ID bilan yangi user yaratish
            row = await conn.fetchrow(
                """
                SELECT * FROM create_user_sequential($1, $2, $3, NULL, 'client'::user_role)
                """,
                telegram_id, username, full_name
            )
            return row
    finally:
        await conn.close()

def _tariff_code_to_name(code: str) -> str:
    mapping = {
        "tariff_xammasi_birga_4": "Hammasi birga 4",
        "tariff_xammasi_birga_3_plus": "Hammasi birga 3+",
        "tariff_xammasi_birga_3": "Hammasi birga 3",
        "tariff_xammasi_birga_2": "Hammasi birga 2",
    }
    return mapping.get(code, code)

async def get_or_create_tarif_by_code(code: str) -> int:
    """Return existing tarif id by code. Does NOT create new rows."""
    name = _tariff_code_to_name(code)
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        tid = await conn.fetchval("SELECT id FROM tarif WHERE name = $1", name)
        return tid
    finally:
        await conn.close()

async def create_connection_order(user_id: int, region: str, address: str, tarif_id: Optional[int], latitude: Optional[float], longitude: Optional[float]) -> int:
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        row = await conn.fetchrow(
            """
            INSERT INTO connection_orders (user_id, region, address, tarif_id, latitude, longitude, status)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id
            """,
            user_id, region, address, tarif_id, latitude, longitude, 'in_manager'
        )
        return row["id"]
    finally:
        await conn.close()

# -----------------------------
# Phone helpers
# -----------------------------

async def get_user_phone_by_telegram_id(telegram_id: int) -> Optional[str]:
    """Return user's phone by telegram_id or None."""
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        return await conn.fetchval(
            "SELECT phone FROM users WHERE telegram_id = $1",
            telegram_id
        )
    finally:
        await conn.close()

async def update_user_phone_by_telegram_id(telegram_id: int, phone: str) -> bool:
    """Update user's phone by telegram_id; return True if updated."""
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        result = await conn.execute(
            "UPDATE users SET phone = $1 WHERE telegram_id = $2",
            phone, telegram_id
        )
        return result != 'UPDATE 0'
    finally:
        await conn.close()

