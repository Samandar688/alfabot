import asyncpg
from config import settings
from typing import Optional

async def get_or_create_user(telegram_id: int, username: Optional[str], full_name: Optional[str] = None) -> str:
    """telegram_id bo'yicha userni tekshiradi, bo'lmasa 'client' rolida yaratadi.
    
    Args:
        telegram_id: Telegram foydalanuvchi IDsi
        username: Telegram foydalanuvchi nomi (ixtiyoriy)
        full_name: Foydalanuvchi to'liq ismi (ixtiyoriy)
        
    Returns:
        str: Foydalanuvchi roli
    """
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        user = await conn.fetchrow(
            'SELECT role, full_name FROM users WHERE telegram_id = $1',
            telegram_id
        )

        if user:
            # Update username and full_name if they are provided and different
            update_fields = []
            params = []
            param_count = 1
            
            if username is not None and user.get('username') != username:
                update_fields.append(f'username = ${param_count}')
                params.append(username)
                param_count += 1
                
            if full_name is not None and user.get('full_name') != full_name:
                update_fields.append(f'full_name = ${param_count}')
                params.append(full_name)
                param_count += 1
            
            if update_fields:
                params.append(telegram_id)
                await conn.execute(
                    f"UPDATE users SET {', '.join(update_fields)} WHERE telegram_id = ${param_count}",
                    *params
                )
                
            return user['role']
        else:
            await conn.execute(
                """
                INSERT INTO users (telegram_id, username, full_name, role)
                VALUES ($1, $2, $3, $4)
                """,
                telegram_id, username, full_name, "client"
            )
            return "client"
    finally:
        await conn.close()

async def find_user_by_telegram_id(telegram_id: int) -> Optional[asyncpg.Record]:
    """Finds a user by their Telegram ID."""
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        user = await conn.fetchrow(
            'SELECT * FROM users WHERE telegram_id = $1',
            telegram_id
        )
        return user
    finally:
        await conn.close()

async def find_user_by_phone(phone: str) -> Optional[asyncpg.Record]:
    """Finds a user by their phone number."""
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        user = await conn.fetchrow(
            'SELECT * FROM users WHERE phone = $1',
            phone
        )
        return user
    finally:
        await conn.close()

async def update_user_phone(telegram_id: int, phone: str) -> bool:
    """Updates the phone number of a user by their Telegram ID."""
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        result = await conn.execute(
            'UPDATE users SET phone = $1 WHERE telegram_id = $2',
            phone, telegram_id
        )
        return result != 'UPDATE 0'
    finally:
        await conn.close()

async def update_user_role(telegram_id: int, new_role: str) -> bool:
    """Updates the role of a user by their Telegram ID."""
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        result = await conn.execute(
            'UPDATE users SET role = $1 WHERE telegram_id = $2',
            new_role, telegram_id
        )
        return result != 'UPDATE 0'
    finally:
        await conn.close()

async def update_user_full_name(telegram_id: int, full_name: str) -> bool:
    """Foydalanuvchi to'liq ismini yangilaydi.
    
    Args:
        telegram_id: Telegram foydalanuvchi IDsi
        full_name: Yangi to'liq ism
        
    Returns:
        bool: Muvaffaqiyatli yangilangan bo'lsa True, aks holda False
    """
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        result = await conn.execute(
            'UPDATE users SET full_name = $1 WHERE telegram_id = $2',
            full_name, telegram_id
        )
        return result != 'UPDATE 0'
    finally:
        await conn.close()
