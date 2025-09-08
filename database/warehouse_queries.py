import asyncpg
from typing import Optional, Dict, Any
from decimal import Decimal
from config import settings

async def create_material(
    name: str,
    quantity: int,
    price: Optional[Decimal] = None,
    description: Optional[str] = None,
    serial_number: Optional[str] = None,  # hozircha None yuboramiz
) -> Dict[str, Any]:
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        row = await conn.fetchrow(
            """
            INSERT INTO materials (name, price, description, quantity, serial_number, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, NOW(), NOW())
            RETURNING id, name, price, description, quantity, serial_number, created_at, updated_at
            """,
            name, price, description, quantity, serial_number
        )
        return dict(row)
    finally:
        await conn.close()