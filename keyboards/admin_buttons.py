from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_main_menu(lang: str = "uz") -> ReplyKeyboardMarkup:

    statistics_text = "📊 Statistika" if lang == "uz" else "📊 Статистика"
    users_text = "👥 Foydalanuvchilar" if lang == "uz" else "👥 Пользователи"
    orders_text = "📝 Zayavkalar" if lang == "uz" else "📝 Заявки"
    settings_text = "⚙️ Sozlamalar" if lang == "uz" else "⚙️ Настройки"
    export_text = "📤 Export" if lang == "uz" else "📤 Экспорт"
    language_text = "🌐 Til" if lang == "uz" else "🌐 Язык"
    status_text = "🔧 Tizim holati" if lang == "uz" else "🔧 Состояние системы"

    keyboard = [
        [KeyboardButton(text=statistics_text), KeyboardButton(text=users_text)],
        [KeyboardButton(text=orders_text), KeyboardButton(text=settings_text)],
        [KeyboardButton(text=export_text), KeyboardButton(text=language_text)],
        [KeyboardButton(text=status_text)],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=False)


def get_user_management_keyboard(lang="uz"):
    """Foydalanuvchi boshqaruv klaviaturasi - 2 tilda"""
    all_users_text = "👥 Barcha foydalanuvchilar" if lang == "uz" else "👥 Все пользователи"
    staff_text = "👤 Xodimlar" if lang == "uz" else "👤 Сотрудники"
    block_text = "🔒 Bloklash/Blokdan chiqarish" if lang == "uz" else "🔒 Блокировка/Разблокировка"
    role_text = "🔄 Rolni o'zgartirish" if lang == "uz" else "🔄 Изменить роль"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=all_users_text),
                KeyboardButton(text=staff_text)
            ],
            [
                KeyboardButton(text=block_text),
                KeyboardButton(text=role_text)
            ],
            [
                KeyboardButton(text=back_text)
            ]
        ],
        resize_keyboard=True
    )

def get_inline_role_selection() -> InlineKeyboardMarkup:
    """Returns inline keyboard for role selection"""
    keyboard = [
        [
            InlineKeyboardButton(text="👤 Admin", callback_data="role_admin"),
            InlineKeyboardButton(text="👤 Mijoz", callback_data="role_client")
        ],
        [
            InlineKeyboardButton(text="👤 Menejer", callback_data="role_manager"),
            InlineKeyboardButton(text="👤 Junior Manager", callback_data="role_junior_manager")
        ],
        [
            InlineKeyboardButton(text="👤 Controller", callback_data="role_controller"),
            InlineKeyboardButton(text="👤 Texnik", callback_data="role_technician")
        ],
        [
            InlineKeyboardButton(text="👤 Ombor", callback_data="role_warehouse"),
            InlineKeyboardButton(text="👤 Call Center", callback_data="role_callcenter_operator")
        ],
        [
            InlineKeyboardButton(text="👤 Call Center Supervisor", callback_data="role_callcenter_supervisor")
        ],
        [
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="role_cancel")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_inline_search_method() -> InlineKeyboardMarkup:
    """Returns inline keyboard for search method selection"""
    keyboard = [
        [
            InlineKeyboardButton(text="🆔 Telegram ID orqali", callback_data="search_telegram_id"),
            InlineKeyboardButton(text="📱 Telefon raqam orqali", callback_data="search_phone")
        ],
        [
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="search_cancel")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
