"""
Universal Error Logger - Centralized logging system

Bu modul barcha xatolarni markazlashtirilgan tarzda log qiladi.
"""

import logging
import traceback
from typing import Optional, Dict, Any
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log", encoding="utf-8")
    ]
)

def get_universal_logger(name: str = "AlfaConnectBot") -> logging.Logger:
    """Universal logger olish"""
    return logging.getLogger(name)

def log_error(
    error: Exception,
    context: str = "",
    user_id: Optional[int] = None,
    additional_data: Optional[Dict[str, Any]] = None
) -> None:
    """Xatolarni log qilish"""
    logger = get_universal_logger()
    
    error_data = {
        "timestamp": datetime.now().isoformat(),
        "error_type": type(error).__name__,
        "error_message": str(error),
        "context": context,
        "user_id": user_id,
        "traceback": traceback.format_exc()
    }
    
    if additional_data:
        error_data.update(additional_data)
    
    logger.error(f"ERROR: {json.dumps(error_data, ensure_ascii=False)}")

def log_info(message: str, context: str = "", user_id: Optional[int] = None) -> None:
    """Info log qilish"""
    logger = get_universal_logger()
    logger.info(f"INFO: {context} | {message} | User: {user_id}")

def log_warning(message: str, context: str = "", user_id: Optional[int] = None) -> None:
    """Warning log qilish"""
    logger = get_universal_logger()
    logger.warning(f"WARNING: {context} | {message} | User: {user_id}")

def log_debug(message: str, context: str = "", user_id: Optional[int] = None) -> None:
    """Debug log qilish"""
    logger = get_universal_logger()
    logger.debug(f"DEBUG: {context} | {message} | User: {user_id}")
