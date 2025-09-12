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
    """Zayavkalar asosiy menusi ReplyKeyboard ko'rinishida"""
    dashboard_text = "📊 Umumiy dashboard" if lang == "uz" else "📊 Общая панель"
    connection_text = "🔌 Ulanish zayavkalari" if lang == "uz" else "🔌 Заявки на подключение"
    technician_text = "🔧 Texnik zayavkalar" if lang == "uz" else "🔧 Технические заявки"
    saff_text = "👥 Xodim zayavkalari" if lang == "uz" else "👥 Заявки сотрудников"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"

    keyboard = [
        [KeyboardButton(text=dashboard_text), KeyboardButton(text=connection_text)],
        [KeyboardButton(text=technician_text), KeyboardButton(text=saff_text)],
        [KeyboardButton(text=back_text)]
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# handlers/admin/orders.py uchun
def get_applications_main_menu_inline(lang: str = "uz") -> InlineKeyboardMarkup:
    """Zayavkalar asosiy menusi InlineKeyboard ko'rinishida"""
    dashboard_text = "📊 Umumiy dashboard" if lang == "uz" else "📊 Общая панель"
    connection_text = "🔌 Ulanish zayavkalari" if lang == "uz" else "🔌 Заявки на подключение"
    technician_text = "🔧 Texnik zayavkalar" if lang == "uz" else "🔧 Технические заявки"
    saff_text = "👥 Xodim zayavkalari" if lang == "uz" else "👥 Заявки сотрудников"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"

    keyboard = [
        [InlineKeyboardButton(text=dashboard_text, callback_data="app_dashboard")],
        [InlineKeyboardButton(text=connection_text, callback_data="app_connection_orders")],
        [InlineKeyboardButton(text=technician_text, callback_data="app_technician_orders")],
        [InlineKeyboardButton(text=saff_text, callback_data="app_saff_orders")],
        [InlineKeyboardButton(text=back_text, callback_data="applications_back_to_main")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# handlers/admin/orders.py uchun
def get_applications_dashboard_menu(lang: str = "uz") -> InlineKeyboardMarkup:
    """Dashboard menusi klaviaturasi"""
    today_text = "📈 Bugungi statistika" if lang == "uz" else "📈 Сегодняшняя статистика"
    weekly_text = "📊 Haftalik trend" if lang == "uz" else "📊 Недельный тренд"
    critical_text = "🚨 Kritik zayavkalar" if lang == "uz" else "🚨 Критические заявки"
    delayed_text = "⏰ Kechikkan zayavkalar" if lang == "uz" else "⏰ Просроченные заявки"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = [
        [InlineKeyboardButton(text=today_text, callback_data="app_today_stats")],
        [InlineKeyboardButton(text=weekly_text, callback_data="app_weekly_trend")],
        [InlineKeyboardButton(text=critical_text, callback_data="app_critical_orders")],
        [InlineKeyboardButton(text=delayed_text, callback_data="app_delayed_orders")],
        [InlineKeyboardButton(text=back_text, callback_data="app_back_to_main")]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# handlers/admin/orders.py uchun
def get_applications_type_menu(app_type: str, lang: str = "uz") -> InlineKeyboardMarkup:
    """Ariza turlari menyusi"""
    back_text = "🔙 Orqaga" if lang == "uz" else "🔙 Назад"
    
    keyboard = [
        [InlineKeyboardButton(text=back_text, callback_data="applications_main")]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# handlers/admin/orders.py uchun
def get_applications_filter_menu(app_type: str, lang: str = "uz") -> InlineKeyboardMarkup:
    """Ariza filtrlash menyusi"""
    back_text = "🔙 Orqaga" if lang == "uz" else "🔙 Назад"
    
    keyboard = [
        [InlineKeyboardButton(text=back_text, callback_data=f"{app_type}_orders")]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# handlers/admin/orders.py uchun
def get_back_to_main_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Asosiy menyuga qaytish klaviaturasi"""
    back_text = "🔙 Asosiy menyu" if lang == "uz" else "🔙 Главное меню"
    
    keyboard = [
        [InlineKeyboardButton(text=back_text, callback_data="applications_main")]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)








# handlers/admin/orders.py uchun
def get_applications_pagination_keyboard(current_page: int, total_pages: int, has_prev: bool, has_next: bool, app_type: str, action: str = "list") -> InlineKeyboardMarkup:
    """Zayavkalar paginatsiyasi uchun klaviatura
    
    Args:
        current_page: Joriy sahifa raqami
        total_pages: Jami sahifalar soni
        has_prev: Oldingi sahifa mavjudligi
        has_next: Keyingi sahifa mavjudligi
        app_type: Zayavka turi (connection, technician, saff)
        action: Harakat turi (list, search, filter)
    
    Returns:
        InlineKeyboardMarkup: Paginatsiya klaviaturasi
    """
    keyboard = []
    
    # Navigatsiya tugmalari
    nav_row = []
    
    if has_prev:
        # Birinchi sahifa
        if current_page > 2:
            nav_row.append(InlineKeyboardButton(text="⏪ 1", callback_data=f"app_{app_type}_{action}_page_1"))
        
        # Oldingi sahifa
        nav_row.append(InlineKeyboardButton(text="◀️ Oldingi", callback_data=f"app_{app_type}_{action}_page_{current_page-1}"))
    
    # Joriy sahifa ko'rsatkichi
    nav_row.append(InlineKeyboardButton(text=f"📄 {current_page}/{total_pages}", callback_data="current_page"))
    
    if has_next:
        # Keyingi sahifa
        nav_row.append(InlineKeyboardButton(text="Keyingi ▶️", callback_data=f"app_{app_type}_{action}_page_{current_page+1}"))
        
        # Oxirgi sahifa
        if current_page < total_pages - 1:
            nav_row.append(InlineKeyboardButton(text=f"{total_pages} ⏩", callback_data=f"app_{app_type}_{action}_page_{total_pages}"))
    
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
            page_row.append(InlineKeyboardButton(text=str(page), callback_data=f"app_{app_type}_{action}_page_{page}"))
    
    if len(page_row) > 1:  
        keyboard.append(page_row)
    
    # Orqaga qaytish tugmasi
    keyboard.append([
        InlineKeyboardButton(text="◀️ Orqaga", callback_data=f"app_{app_type}_orders")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# handlers/admin/orders.py uchun
def get_application_details_keyboard(app_id: int, app_type: str, lang: str = "uz") -> InlineKeyboardMarkup:
    """Zayavka tafsilotlari uchun klaviatura"""
    edit_text = "✏️ Tahrirlash" if lang == "uz" else "✏️ Редактировать"
    status_text = "🔄 Statusni o'zgartirish" if lang == "uz" else "🔄 Изменить статус"
    history_text = "📜 Tarix" if lang == "uz" else "📜 История"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = [
        [InlineKeyboardButton(text=edit_text, callback_data=f"app_{app_type}_edit_{app_id}")],
        [InlineKeyboardButton(text=status_text, callback_data=f"app_{app_type}_status_{app_id}")],
        [InlineKeyboardButton(text=history_text, callback_data=f"app_{app_type}_history_{app_id}")],
        [InlineKeyboardButton(text=back_text, callback_data=f"app_{app_type}_list")]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)



