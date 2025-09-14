# database/junior_manager_stats_queries.py
from __future__ import annotations
from typing import Dict, Optional
import asyncpg
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from config import settings

# ---------- UTIL: kolonkalarni autodetect ----------
async def _detect_conn_fk_col(conn) -> str:
    q = """
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name='connections' AND column_name = ANY($1::text[])
    """
    rows = await conn.fetch(q, ['connection_id', 'connecion_id'])
    cols = [r['column_name'] for r in rows]
    return cols[0] if cols else 'connecion_id'  # default: sizdagi typo

async def _resolve_app_user_id(conn, telegram_id: int) -> Optional[int]:
    # users jadvalidagi telegram ustun nomi qanday bo‘lishidan qat’i nazar aniqlaymiz
    qcols = """
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name='users' AND column_name = ANY($1::text[])
    """
    rows = await conn.fetch(qcols, ['telegram_id', 'tg_id', 'chat_id'])
    cols = [r['column_name'] for r in rows]
    if not cols:
        return None
    where = " OR ".join([f"{c}::text = $1::text" for c in cols])
    sql = f"SELECT id FROM users WHERE {where} LIMIT 1"
    row = await conn.fetchrow(sql, str(telegram_id))
    return int(row['id']) if row and row['id'] is not None else None

# ---------- UTIL: vaqt oynalari ----------
def _today_utc_range(tz: ZoneInfo) -> tuple[datetime, datetime]:
    now_local = datetime.now(tz)
    start_local = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
    end_local = start_local + timedelta(days=1)
    return start_local.astimezone(timezone.utc), end_local.astimezone(timezone.utc)

def _since_utc_range(days: int) -> tuple[datetime, datetime]:
    now_utc = datetime.now(timezone.utc)
    start_utc = now_utc - timedelta(days=days)
    return start_utc, now_utc

# ---------- Core query for one window ----------
async def _window_counts(conn, user_id: int, fk_col: str, start_utc: datetime, end_utc: datetime) -> Dict[str, int]:
    # JM qabul qilganlari (recipient sifatida)
    # JM controllerga yuborganlari (sender sifatida → recipient_status='in_controller')
    # JM yuborganlariga tegishli completed connection_orders
    sql = f"""
    WITH received AS (
        SELECT id
        FROM connections
        WHERE recipient_id = $1
          AND recipient_status = 'in_junior_manager'
          AND created_at >= $2 AND created_at < $3
    ),
    sent AS (
        SELECT DISTINCT {fk_col} AS order_id
        FROM connections
        WHERE sender_id = $1
          AND sender_status = 'in_junior_manager'
          AND recipient_status = 'in_controller'
          AND created_at >= $2 AND created_at < $3
    )
    SELECT
      (SELECT COUNT(*) FROM received)                         AS received_cnt,
      (SELECT COUNT(*) FROM sent)                             AS sent_cnt,
      (SELECT COUNT(*) 
         FROM connection_orders co
         JOIN sent s ON s.order_id = co.id
        WHERE (co.status)::text = 'completed')                AS completed_cnt;
    """
    row = await conn.fetchrow(sql, user_id, start_utc, end_utc)
    return {
        "received": int(row["received_cnt"] or 0),
        "sent_to_controller": int(row["sent_cnt"] or 0),
        "completed_from_sent": int(row["completed_cnt"] or 0),
    }

# ---------- Public API ----------
async def get_jm_stats_for_telegram(telegram_id: int, tz: ZoneInfo) -> Optional[Dict[str, Dict[str, int]]]:
    conn = await asyncpg.connect(settings.DB_URL)
    try:
        user_id = await _resolve_app_user_id(conn, telegram_id)
        if user_id is None:
            return None
        fk_col = await _detect_conn_fk_col(conn)

        # oynalar
        t_start, t_end = _today_utc_range(tz)
        d7 = _since_utc_range(7)
        d10 = _since_utc_range(10)
        d30 = _since_utc_range(30)

        today = await _window_counts(conn, user_id, fk_col, t_start, t_end)
        last7 = await _window_counts(conn, user_id, fk_col, *d7)
        last10 = await _window_counts(conn, user_id, fk_col, *d10)
        last30 = await _window_counts(conn, user_id, fk_col, *d30)

        return {"today": today, "7d": last7, "10d": last10, "30d": last30}
    finally:
        await conn.close()
