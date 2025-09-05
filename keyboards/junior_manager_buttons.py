from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_junior_manager_main_menu(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Kichik menejer uchun bosh menyu — 6 ta tugma."""
    inbox_text = "📥 Inbox"
    view_apps_text = "📋 Arizalarni ko'rish" if lang == "uz" else "📋 Просмотр заявок"
    create_connection_text = "🔌 Ulanish arizasi yaratish" if lang == "uz" else "🔌 Создать заявку"
    client_search_text = "🔍 Mijoz qidiruv" if lang == "uz" else "🔍 Поиск клиентов"
    statistics_text = "📊 Statistika" if lang == "uz" else "📊 Статистика"
    change_lang_text = "🌐 Tilni o'zgartirish" if lang == "uz" else "🌐 Изменить язык"

    keyboard = [
        [KeyboardButton(text=inbox_text), KeyboardButton(text=view_apps_text)],
        [KeyboardButton(text=create_connection_text), KeyboardButton(text=client_search_text)],
        [KeyboardButton(text=statistics_text), KeyboardButton(text=change_lang_text)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
