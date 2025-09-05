from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def get_technician_main_menu(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Technician main menu with 4 reply buttons: Language, Inbox, Tasks, Reports"""
    change_language_text = "🌐 Tilni o'zgartirish" if lang == "uz" else "🌐 Изменить язык"
    inbox_text = "📥 Inbox"
    tasks_text = "📋 Vazifalarim" if lang == "uz" else "📋 Мои задачи"
    reports_text = "📊 Hisobotlarim" if lang == "uz" else "📊 Мои отчеты"

    keyboard = [
        [KeyboardButton(text=change_language_text)],
        [KeyboardButton(text=inbox_text)],
        [KeyboardButton(text=tasks_text)],
        [KeyboardButton(text=reports_text)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

