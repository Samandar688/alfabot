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

