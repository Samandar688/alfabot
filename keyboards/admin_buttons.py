from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# ========== Umumiy (admin) ==========

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

# ========== Admin Users (handlers/admin/users.py) ==========
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

# handlers/admin/users.py uchun
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


# Bu bo'lim: users.py
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


# handlers/admin/users.py uchun
def get_users_pagination_keyboard(current_page: int, total_pages: int, has_prev: bool, has_next: bool, user_type: str = "all") -> InlineKeyboardMarkup:
    """Foydalanuvchilar paginatsiyasi uchun klaviatura
    
    Args:
        current_page: Joriy sahifa raqami
        total_pages: Jami sahifalar soni
        has_prev: Oldingi sahifa mavjudligi
        has_next: Keyingi sahifa mavjudligi
        user_type: Foydalanuvchi turi (all, staff)
    
    Returns:
        InlineKeyboardMarkup: Paginatsiya klaviaturasi
    """
    keyboard = []
    
    # Navigatsiya tugmalari
    nav_row = []
    
    if has_prev:
        # Birinchi sahifa
        if current_page > 2:
            nav_row.append(InlineKeyboardButton(text="⏪ 1", callback_data=f"users_page_{user_type}_1"))
        
        # Oldingi sahifa
        nav_row.append(InlineKeyboardButton(text="◀️ Oldingi", callback_data=f"users_page_{user_type}_{current_page-1}"))
    
    # Joriy sahifa ko'rsatkichi
    nav_row.append(InlineKeyboardButton(text=f"📄 {current_page}/{total_pages}", callback_data="current_page"))
    
    if has_next:
        # Keyingi sahifa
        nav_row.append(InlineKeyboardButton(text="Keyingi ▶️", callback_data=f"users_page_{user_type}_{current_page+1}"))
        
        # Oxirgi sahifa
        if current_page < total_pages - 1:
            nav_row.append(InlineKeyboardButton(text=f"{total_pages} ⏩", callback_data=f"users_page_{user_type}_{total_pages}"))
    
    if nav_row:
        keyboard.append(nav_row)
    
    # Sahifa raqamlari (joriy sahifa atrofida)
    page_row = []
    start_page = max(1, current_page - 2)
    end_page = min(total_pages, current_page + 2)
    
    for page in range(start_page, end_page + 1):
        if page == current_page:
            page_row.append(InlineKeyboardButton(text=f"• {page} •", callback_data="current_page"))
        else:
            page_row.append(InlineKeyboardButton(text=str(page), callback_data=f"users_page_{user_type}_{page}"))
    
    if len(page_row) > 1:  
        keyboard.append(page_row)
    
    # Orqaga qaytish tugmasi
    keyboard.append([
        InlineKeyboardButton(text="◀️ Orqaga", callback_data="users_back_to_menu")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# ========== Admin Orders (handlers/admin/orders.py) ==========
def get_applications_main_menu(lang: str = "uz") -> ReplyKeyboardMarkup:
    connection_text = "🔌 Ulanish zayavkalari" if lang == "uz" else "🔌 Заявки на подключение"
    technician_text = "🔧 Texnik zayavkalar" if lang == "uz" else "🔧 Технические заявки"
    saff_text = "👥 Xodim zayavkalari" if lang == "uz" else "👥 Заявки сотрудников"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"

    keyboard = [
        [KeyboardButton(text=technician_text), KeyboardButton(text=connection_text)],
        [KeyboardButton(text=saff_text), KeyboardButton(text=back_text)]
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# ========== Admin Orders Navigation (handlers/admin/orders.py) ==========
def get_orders_navigation_keyboard(current_index: int, total_orders: int, order_type: str, lang: str = "uz") -> InlineKeyboardMarkup:
    """
    Zayavkalar orasida navigatsiya uchun inline keyboard
    """
    keyboard = []
    
    # Navigation tugmalari
    nav_buttons = []
    
    # Oldingi tugma
    if current_index > 0:
        prev_text = "⬅️ Oldingi" if lang == "uz" else "⬅️ Предыдущий"
        nav_buttons.append(InlineKeyboardButton(
            text=prev_text,
            callback_data=f"admin_order_prev_{order_type}_{current_index-1}"
        ))
    
    # Keyingi tugma
    if current_index < total_orders - 1:
        next_text = "Keyingi ➡️" if lang == "uz" else "Следующий ➡️"
        nav_buttons.append(InlineKeyboardButton(
            text=next_text,
            callback_data=f"admin_order_next_{order_type}_{current_index+1}"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Orqaga tugma
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    keyboard.append([InlineKeyboardButton(
        text=back_text,
        callback_data="admin_orders_back"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
