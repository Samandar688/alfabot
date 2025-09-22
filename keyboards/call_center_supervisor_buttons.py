from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_call_center_supervisor_main_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    if lang == 'ru':
        keyboard = [
            [KeyboardButton(text="📥 Входящие")],
            [KeyboardButton(text="👥 Активность сотрудников")],
            [KeyboardButton(text="🔌 Создать заявку на подключение"), KeyboardButton(text="🔧 Создать техническую заявку")],
            [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="📤 Экспорт")],
            [KeyboardButton(text="🌐 Изменить язык")],
        ]
    else:
        keyboard = [
            [KeyboardButton(text="📥 Inbox")],
            [KeyboardButton(text="👥 Xodimlar faoliyati")],
            [KeyboardButton(text="🔌 Ulanish arizasi yaratish"), KeyboardButton(text="🔧 Texnik xizmat yaratish")],
            [KeyboardButton(text="📊 Statistikalar"), KeyboardButton(text="📤 Export")],
            [KeyboardButton(text="🌐 Tilni o'zgartirish")],
        ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)



def zayavka_type_keyboard(lang="uz"):
    """Zayavka turini tanlash klaviaturasi - 2 tilda"""
    person_physical_text = "👤 Jismoniy shaxs" if lang == "uz" else "👤 Физическое лицо"
    person_legal_text = "🏢 Yuridik shaxs" if lang == "uz" else "🏢 Юридическое лицо"
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=person_physical_text, callback_data="zayavka_type_b2c")],
            [InlineKeyboardButton(text=person_legal_text, callback_data="zayavka_type_b2b")]
        ]
    )
    return keyboard

def get_operator_tariff_selection_keyboard() -> InlineKeyboardMarkup:
    """Tariff selection keyboard for CALL-CENTER OPERATOR (UZ only)."""
    keyboard = [
        [
            InlineKeyboardButton(text="Hammasi birga 4", callback_data="op_tariff_xammasi_birga_4"),
            InlineKeyboardButton(text="Hammasi birga 3+", callback_data="op_tariff_xammasi_birga_3_plus"),
        ],
        [
            InlineKeyboardButton(text="Hammasi birga 3", callback_data="op_tariff_xammasi_birga_3"),
            InlineKeyboardButton(text="Hammasi birga 2", callback_data="op_tariff_xammasi_birga_2"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def confirmation_keyboard(lang="uz"):
    """Tasdiqlash klaviaturasi - 2 tilda"""
    confirm_text = "✅ Tasdiqlash" if lang == "uz" else "✅ Подтвердить"
    resend_text = "🔄 Qayta yuborish" if lang == "uz" else "🔄 Отправить заново"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=confirm_text, callback_data="confirm_zayavka_call_center"),
            InlineKeyboardButton(text=resend_text, callback_data="resend_zayavka_call_center")
        ]
    ])
    return keyboard

def confirmation_keyboard_tech_service(lang="uz"):
    """Tasdiqlash klaviaturasi - 2 tilda"""
    confirm_text = "✅ Tasdiqlash" if lang == "uz" else "✅ Подтвердить"
    resend_text = "🔄 Qayta yuborish" if lang == "uz" else "🔄 Отправить заново"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=confirm_text, callback_data="confirm_zayavka_call_center_tech_service"),
            InlineKeyboardButton(text=resend_text, callback_data="resend_zayavka_call_center_tech_service")
        ]
    ])
    return keyboard

def get_client_regions_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Regions selection keyboard for client"""
    keyboard = [
        [
            InlineKeyboardButton(text="Toshkent shahri", callback_data="region_toshkent_city"),
            InlineKeyboardButton(text="Toshkent viloyati", callback_data="region_toshkent_region")
        ],
        [
            InlineKeyboardButton(text="Andijon", callback_data="region_andijon"),
            InlineKeyboardButton(text="Farg'ona", callback_data="region_fergana")
        ],
        [
            InlineKeyboardButton(text="Namangan", callback_data="region_namangan"),
            InlineKeyboardButton(text="Sirdaryo", callback_data="region_sirdaryo")
        ],
        [
            InlineKeyboardButton(text="Jizzax", callback_data="region_jizzax"),
            InlineKeyboardButton(text="Samarqand", callback_data="region_samarkand")
        ],
        [
            InlineKeyboardButton(text="Buxoro", callback_data="region_bukhara"),
            InlineKeyboardButton(text="Navoiy", callback_data="region_navoi")
        ],
        [
            InlineKeyboardButton(text="Qashqadaryo", callback_data="region_kashkadarya"),
            InlineKeyboardButton(text="Surxondaryo", callback_data="region_surkhandarya")
        ],
        [
            InlineKeyboardButton(text="Xorazm", callback_data="region_khorezm"),
            InlineKeyboardButton(text="Qoraqalpog'iston", callback_data="region_karakalpakstan")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_ccs_export_types_keyboard():
    """Call Center Supervisor export types keyboard"""
    keyboard = InlineKeyboardBuilder()
    
    keyboard.row(
        InlineKeyboardButton(text="📋 Buyurtmalar", callback_data="ccs_export_orders"),
        InlineKeyboardButton(text="📊 Statistika", callback_data="ccs_export_statistics")
    )
    keyboard.row(
        InlineKeyboardButton(text="👥 Operatorlar", callback_data="ccs_export_employees"),
        InlineKeyboardButton(text="📈 Hisobotlar", callback_data="ccs_export_reports")
    )
    keyboard.row(
        InlineKeyboardButton(text="❌ Yopish", callback_data="ccs_export_end")
    )
    
    return keyboard.as_markup()

def get_ccs_export_formats_keyboard():
    """Call Center Supervisor export formats keyboard"""
    keyboard = InlineKeyboardBuilder()
    
    keyboard.row(
        InlineKeyboardButton(text="📄 CSV", callback_data="ccs_format_csv"),
        InlineKeyboardButton(text="📊 Excel", callback_data="ccs_format_xlsx")
    )
    keyboard.row(
        InlineKeyboardButton(text="📝 Word", callback_data="ccs_format_docx"),
        InlineKeyboardButton(text="📋 PDF", callback_data="ccs_format_pdf")
    )
    keyboard.row(
        InlineKeyboardButton(text="🔙 Orqaga", callback_data="ccs_export_back_types"),
        InlineKeyboardButton(text="❌ Yopish", callback_data="ccs_export_end")
    )
    
    return keyboard.as_markup()