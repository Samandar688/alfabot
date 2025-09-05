from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

def get_call_center_main_keyboard(lang: str = 'uz') -> ReplyKeyboardMarkup:
    if lang == 'ru':
        webapp_text = "💬 Онлайн Чат Web App"
        keyboard = [
            [KeyboardButton(text="📥 Входящие"), KeyboardButton(text="📋 Заказы")],
            [KeyboardButton(text="🔍 Поиск клиента")],
            [KeyboardButton(text="🔌 Создать заявку на подключение"), KeyboardButton(text="🔧 Создать техническую заявку")],
            [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="🌐 Изменить язык")],
            [KeyboardButton(text=webapp_text, web_app=WebAppInfo(url="https://webapp-gamma-three.vercel.app/"))],
        ]
    else:
        webapp_text = "💬 Onlayn Chat Web App"
        keyboard = [
            [KeyboardButton(text="📥 Inbox"), KeyboardButton(text="📋 Buyurtmalar")],
            [KeyboardButton(text="🔍 Mijoz qidirish")],
            [KeyboardButton(text="🔌 Ulanish arizasi yaratish"), KeyboardButton(text="🔧 Texnik xizmat yaratish")],
            [KeyboardButton(text="📊 Statistikalar"), KeyboardButton(text="🌐 Tilni o'zgartirish")],
            [KeyboardButton(text=webapp_text, web_app=WebAppInfo(url="https://webapp-gamma-three.vercel.app/"))],
        ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

