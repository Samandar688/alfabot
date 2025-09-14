from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List, Dict, Any, Optional


def get_controller_main_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    if lang == 'uz':
        keyboard = [
            [KeyboardButton(text="📥 Inbox"), KeyboardButton(text="📋 Arizalarni ko'rish")],
            [KeyboardButton(text="🔌 Ulanish arizasi yaratish"), KeyboardButton(text="🔧 Texnik xizmat yaratish")],
            [KeyboardButton(text="🕐 Real vaqtda kuzatish"), KeyboardButton(text="📊 Monitoring")],
            [KeyboardButton(text="👥 Xodimlar faoliyati"), KeyboardButton(text="📤 Export")],
            [KeyboardButton(text="🌐 Tilni o'zgartirish")]
        ]
    else:
        keyboard = [
            [KeyboardButton(text="📥 Входящие"), KeyboardButton(text="📋 Просмотр заявок")],
            [KeyboardButton(text="🔌 Создать заявку на подключение"), KeyboardButton(text="🔧 Создать техническую заявку")],
            [KeyboardButton(text="🕐 Мониторинг в реальном времени"), KeyboardButton(text="📊 Мониторинг")],
            [KeyboardButton(text="👥 Активность сотрудников"), KeyboardButton(text="📤 Экспорт")],
            [KeyboardButton(text="🌐 Изменить язык")]
        ]
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_controller_export_types_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Controller export turlari klaviaturasi (uz/ru)."""
    lang = (lang or 'uz').lower()

    if lang == "ru":
        keyboard = [
            [InlineKeyboardButton(text="📋 Техн. заявки", callback_data="controller_export_tech_requests")],
            [InlineKeyboardButton(text="📊 Статистика", callback_data="controller_export_statistics")],
            [InlineKeyboardButton(text="👥 Сотрудники", callback_data="controller_export_employees")],
            [InlineKeyboardButton(text="📈 Отчеты", callback_data="controller_export_reports")],
            [InlineKeyboardButton(text="🚫 Выход", callback_data="controller_export_end")],
        ]
    else:  
        keyboard = [
            [InlineKeyboardButton(text="📋 Texnik arizalar", callback_data="controller_export_tech_requests")],
            [InlineKeyboardButton(text="📊 Statistika", callback_data="controller_export_statistics")],
            [InlineKeyboardButton(text="👥 Xodimlar", callback_data="controller_export_employees")],
            [InlineKeyboardButton(text="📈 Hisobotlar", callback_data="controller_export_reports")],
            [InlineKeyboardButton(text="🚫 Yopish", callback_data="controller_export_end")],
        ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_controller_export_formats_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Manager export formats selection keyboard"""
    if lang == "uz":
        keyboard = [
            [InlineKeyboardButton(text="CSV", callback_data="controller_format_csv")],
            [InlineKeyboardButton(text="Excel", callback_data="controller_format_xlsx")],
            [InlineKeyboardButton(text="Word", callback_data="controller_format_docx")],
            [InlineKeyboardButton(text="PDF", callback_data="controller_format_pdf")],
            [InlineKeyboardButton(text="◀️ Orqaga", callback_data="controller_export_back_types")]
        ]
    else:     
        keyboard = [
            [InlineKeyboardButton(text="CSV", callback_data="controller_format_csv")],
            [InlineKeyboardButton(text="Excel", callback_data="controller_format_xlsx")],
            [InlineKeyboardButton(text="Word", callback_data="controller_format_docx")],
            [InlineKeyboardButton(text="PDF", callback_data="controller_format_pdf")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="controller_export_back_types")]
        ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

