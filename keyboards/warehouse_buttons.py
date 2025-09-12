from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_warehouse_main_menu(lang: str = "uz") -> ReplyKeyboardMarkup:
    inbox = "📥 Inbox"
    inventory = "📦 Inventarizatsiya" if lang == "uz" else "📦 Инвентаризация"
    orders = "📋 Buyurtmalar" if lang == "uz" else "📋 Заказы"
    statistics = "📊 Statistikalar" if lang == "uz" else "📊 Статистика"
    export = "📤 Export" if lang == "uz" else "📤 Экспорт"
    change_lang = "🌐 Tilni o'zgartirish" if lang == "uz" else "🌐 Изменить язык"

    keyboard = [
        [KeyboardButton(text=inbox), KeyboardButton(text=inventory)],
        [KeyboardButton(text=orders), KeyboardButton(text=statistics)],
        [KeyboardButton(text=export), KeyboardButton(text=change_lang)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_inventory_actions_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    uz = {
        "add": "➕ Mahsulot qo'shish",
        "update": "✏️ Mahsulotni yangilash",
        "low": "⚠️ Kam zaxira",
        "out": "❌ Tugagan mahsulotlar",
        "search": "🔎 Qidirish",
        "all": "📄 Barcha mahsulotlar",
        "back": "◀️ Orqaga",
    }
    ru = {
        "add": "➕ Добавить товар",
        "update": "✏️ Обновить товар",
        "low": "⚠️ Низкий запас",
        "out": "❌ Закончились",
        "search": "🔎 Поиск",
        "all": "📄 Все товары",
        "back": "◀️ Назад",
    }
    T = uz if lang == "uz" else ru

    keyboard = [
        [KeyboardButton(text=T["add"]),    KeyboardButton(text=T["update"])],
        [KeyboardButton(text=T["low"]),    KeyboardButton(text=T["out"])],
        [KeyboardButton(text=T["search"]), KeyboardButton(text=T["all"])],
        [KeyboardButton(text=T["back"])],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# --- STATISTIKA MENYUSI (rasmga mos) ---

def get_warehouse_statistics_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """
    RASMDAGI TUGMALARGA 1:1 MOS:
    📊 Inventarizatsiya statistikasi
    📦 Buyurtmalar statistikasi
    ⚠️ Kam zaxira statistikasi
    💰 Moliyaviy hisobot
    📊 Vaqt oralig'idagi statistika
    🔙 Orqaga
    """
    uz = {
        "inv": "📊 Inventarizatsiya statistikasi",
        "ord": "📦 Buyurtmalar statistikasi",
        "low": "⚠️ Kam zaxira statistikasi",
        "fin": "💰 Moliyaviy hisobot",
        "range": "📊 Vaqt oralig'idagi statistika",
        "back": "🔙 Orqaga",
    }
    ru = {
        "inv": "📊 Статистика инвентаризации",
        "ord": "📦 Статистика заказов",
        "low": "⚠️ Статистика низких запасов",
        "fin": "💰 Финансовый отчет",
        "range": "📊 Статистика за период",
        "back": "🔙 Назад",
    }
    T = uz if lang == "uz" else ru
    keyboard = [
        [KeyboardButton(text=T["inv"])],
        [KeyboardButton(text=T["ord"])],
        [KeyboardButton(text=T["low"])],
        [KeyboardButton(text=T["fin"])],
        [KeyboardButton(text=T["range"])],
        [KeyboardButton(text=T["back"])],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_stats_period_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """
    Rasmning o‘ng tomonidagi tugmalar: (reply keyboard, inline EMAS)
    📆 Oylik statistika | 📊 Kunlik statistika
    📅 Haftalik statistika | 📈 Yillik statistika
    🔙 Orqaga
    """
    uz = {
        "daily": "📊 Kunlik statistika",
        "weekly": "📅 Haftalik statistika",
        "monthly": "📆 Oylik statistika",
        "yearly": "📈 Yillik statistika",
        "back": "🔙 Orqaga",
    }
    ru = {
        "daily": "📊 Дневная статистика",
        "weekly": "📅 Недельная статистика",
        "monthly": "📆 Месячная статистика",
        "yearly": "📈 Годовая статистика",
        "back": "🔙 Назад",
    }
    T = uz if lang == "uz" else ru
    keyboard = [
        [KeyboardButton(text=T["monthly"]), KeyboardButton(text=T["daily"])],
        [KeyboardButton(text=T["weekly"]),  KeyboardButton(text=T["yearly"])],
        [KeyboardButton(text=T["back"])],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_warehouse_export_types_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Export types selection keyboard"""
    keyboard = [
        [InlineKeyboardButton(text="📦 Inventarizatsiya", callback_data="warehouse_export_inventory")],
        [InlineKeyboardButton(text="📊 Statistika", callback_data="warehouse_export_statistics")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_warehouse_export_formats_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Export formats selection keyboard"""
    keyboard = [
        [InlineKeyboardButton(text="CSV", callback_data="warehouse_format_csv")],
        [InlineKeyboardButton(text="Excel", callback_data="warehouse_format_xlsx")],
        [InlineKeyboardButton(text="Word", callback_data="warehouse_format_docx")],
        [InlineKeyboardButton(text="PDF", callback_data="warehouse_format_pdf")],
        [InlineKeyboardButton(text="◀️ Orqaga", callback_data="warehouse_export_back_types")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)