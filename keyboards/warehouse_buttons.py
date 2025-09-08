from typing import List

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)


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
        "back": "◀️ Orqaga",   # rasmga mos
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