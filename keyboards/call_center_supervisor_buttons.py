from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_call_center_supervisor_main_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    if lang == 'ru':
        keyboard = [
            [KeyboardButton(text="📥 Входящие"), KeyboardButton(text="📝 Заказы")],
            [KeyboardButton(text="👥 Управление сотрудниками")],
            [KeyboardButton(text="🔌 Создать заявку на подключение"), KeyboardButton(text="🔧 Создать техническую заявку")],
            [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="📤 Экспорт")],
            [KeyboardButton(text="🌐 Изменить язык")],
        ]
    else:
        keyboard = [
            [KeyboardButton(text="📥 Inbox"), KeyboardButton(text="📝 Buyurtmalar")],
            [KeyboardButton(text="👥 Xodimlar boshqaruvi")],
            [KeyboardButton(text="🔌 Ulanish arizasi yaratish"), KeyboardButton(text="🔧 Texnik xizmat yaratish")],
            [KeyboardButton(text="📊 Statistikalar"), KeyboardButton(text="📤 Export")],
            [KeyboardButton(text="🌐 Tilni o'zgartirish")],
        ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

