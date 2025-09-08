from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from typing import List, Dict, Any


def get_contact_keyboard(lang="uz"):
    share_contact_text = "📱 Kontakt ulashish" if lang == "uz" else "📱 Поделиться контактом"
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=share_contact_text, request_contact=True)]],
        resize_keyboard=True
    )
    return keyboard

def get_client_main_menu(lang="uz"):
    service_order_text = "🔧 Texnik xizmat" if lang == "uz" else "🔧 Техническая служба"
    connection_order_text = "🔌 Ulanish uchun ariza" if lang == "uz" else "🔌 Заявка на подключение"
    contact_operator_text = "📞 Operator bilan bog'lanish" if lang == "uz" else "📞 Связаться с оператором"
    cabinet_text = "👤 Kabinet" if lang == "uz" else "👤 Кабинет"
    bot_guide_text = "Bot qo'llanmasi" if lang == "uz" else "Инструкция по использованию бота"
    change_language_text = "🌐 Til o'zgartirish" if lang == "uz" else "🌐 Изменить язык"
    
    buttons = [
        [
            KeyboardButton(text=connection_order_text),
            KeyboardButton(text=service_order_text)    
        ],
        [
            KeyboardButton(text=contact_operator_text),
            KeyboardButton(text=cabinet_text)
        ],
        [
            KeyboardButton(text=bot_guide_text),
            KeyboardButton(text=change_language_text)
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard

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

def media_attachment_keyboard(lang="uz"):
    """Media biriktirish klaviaturasi - 2 tilda"""
    yes_text = "✅ Ha" if lang == "uz" else "✅ Да"
    no_text = "❌ Yo'q" if lang == "uz" else "❌ Нет"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=yes_text, callback_data="attach_media_yes")],
        [InlineKeyboardButton(text=no_text, callback_data="attach_media_no")]
    ])
    return keyboard

def geolocation_keyboard(lang="uz"):
    """Geolokatsiya klaviaturasi - 2 tilda"""
    yes_text = "✅ Ha" if lang == "uz" else "✅ Да"
    no_text = "❌ Yo'q" if lang == "uz" else "❌ Нет"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=yes_text, callback_data="send_location_yes")],
        [InlineKeyboardButton(text=no_text, callback_data="send_location_no")]
    ])
    return keyboard

def confirmation_keyboard(lang="uz"):
    """Tasdiqlash klaviaturasi - 2 tilda"""
    confirm_text = "✅ Tasdiqlash" if lang == "uz" else "✅ Подтвердить"
    resend_text = "🔄 Qayta yuborish" if lang == "uz" else "🔄 Отправить заново"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=confirm_text, callback_data="confirm_zayavka"),
            InlineKeyboardButton(text=resend_text, callback_data="resend_zayavka")
        ]
    ])
    return keyboard

def get_client_tariff_selection_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Tariff selection keyboard for client"""
    keyboard = [
        [
            InlineKeyboardButton(text="Hammasi birga 4", callback_data="tariff_xammasi_birga_4"),
            InlineKeyboardButton(text="Hammasi birga 3+", callback_data="tariff_xammasi_birga_3_plus")
        ],
        [
            InlineKeyboardButton(text="Hammasi birga 3", callback_data="tariff_xammasi_birga_3"),
            InlineKeyboardButton(text="Hammasi birga 2", callback_data="tariff_xammasi_birga_2")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

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

def get_contact_options_keyboard(lang: str = "uz"):

    call_text = "📞 Qo'ng'iroq qilish" if lang == "uz" else "📞 Позвонить"
    chat_text = "💬 Onlayn chat" if lang == "uz" else "💬 Онлайн-чат"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=call_text)],
            [KeyboardButton(text=chat_text, web_app=WebAppInfo(url="https://webapp-gamma-three.vercel.app/"))],
            [KeyboardButton(text=back_text)],
        ],
        resize_keyboard=True,
    )

    return reply_keyboard