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
    smart_service_text = "🛜 Smart Service" if lang == "uz" else "🛜 Smart Service"
    contact_operator_text = "📞 Operator bilan bog'lanish" if lang == "uz" else "📞 Связаться с оператором"
    cabinet_text = "👤 Kabinet" if lang == "uz" else "👤 Кабинет"
    bot_guide_text = "📄 Bot qo'llanmasi" if lang == "uz" else " 📄Инструкция по использованию бота"
    change_language_text = "🌐 Tilni o'zgartirish" if lang == "uz" else "🌐 Изменить язык"
    
    buttons = [
        [
            KeyboardButton(text=connection_order_text),
            KeyboardButton(text=service_order_text)    
        ],
        [
            KeyboardButton(text=smart_service_text)
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

def get_client_profile_reply_keyboard(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Reply keyboard for client profile (cabinet) section"""
    view_info_text = "👀 Ma'lumotlarni ko'rish" if lang == 'uz' else "👀 Просмотр информации"
    view_orders_text = "📋 Mening arizalarim" if lang == 'uz' else "📋 Мои заявки"
    edit_name_text = "✏️ Ismni o'zgartirish" if lang == 'uz' else "✏️ Изменить имя"
    back_text = "◀️ Orqaga" if lang == 'uz' else "◀️ Назад"

    keyboard = [
        [KeyboardButton(text=view_info_text)],
        [KeyboardButton(text=view_orders_text)],
        [KeyboardButton(text=edit_name_text)],
        [KeyboardButton(text=back_text)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_smart_service_categories_keyboard(lang="uz"):
    """SmartService kategoriyalarini tanlash klaviaturasi"""
    categories = [
        ("🏠 Aqlli uy va avtomatlashtirilgan xizmatlar", "cat_smart_home"),
        ("🔒 Xavfsizlik va kuzatuv tizimlari", "cat_security"),
        ("🌐 Internet va tarmoq xizmatlari", "cat_internet"),
        ("⚡ Energiya va yashil texnologiyalar", "cat_energy"),
        ("📺 Multimediya va aloqa tizimlari", "cat_multimedia"),
        ("🔧 Maxsus va qo'shimcha xizmatlar", "cat_special")
    ]
    
    keyboard = []
    for text, callback_data in categories:
        keyboard.append([InlineKeyboardButton(text=text, callback_data=callback_data)])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_smart_service_types_keyboard(category, lang="uz"):
    """Tanlangan kategoriya bo'yicha xizmat turlarini ko'rsatish"""
    service_types = {
        "aqlli_avtomatlashtirilgan_xizmatlar": [
            ("1) Aqlli uy tizimlarini o'rnatish va sozlash", "srv_smart_home_setup"),
            ("2) Aqlli yoritish (Smart Lighting) tizimlari", "srv_smart_lighting"),
            ("3) Aqlli termostat va iqlim nazarati tizimlari", "srv_smart_thermostat"),
            ("4) Smart Lock - internet orqali boshqariladigan eshik qulfi tizimlari", "srv_smart_lock"),
            ("5) Aqlli rozetalar va energiya monitoring tizimlari", "srv_smart_outlets"),
            ("6) Uyni masofadan boshqarish qurilmalari yagona uzim orqali boshqarish", "srv_remote_control"),
            ("7) Aqlli pardalari va jaluz tizimlari", "srv_smart_curtains"),
            ("8) Aqlli malahiy texnika integratsiyasi", "srv_appliance_integration")
        ],
        "xavfsizlik_kuzatuv_tizimlari": [
            ("1) Videokuzatuv kameralarini o'rnatish (IP va analog)", "srv_cctv_cameras"),
            ("2) Kamera arxiv tizimlari va bulutli saqlash xizmatlari", "srv_camera_storage"),
            ("3) Domofon tizimlarini o'rnatish", "srv_intercom"),
            ("4) Xavfsizlik signalizatsiyasi va harakat sensorlarini o'rnatish", "srv_security_alarm"),
            ("5) Yong'in signalizatsiyasi tizimlari", "srv_fire_alarm"),
            ("6) Gaz sizish va suv toshqinga qarshi tizimlar", "srv_gas_flood_protection"),
            ("7) Yuzni tanish (Face Recognition) tizimlari", "srv_face_recognition"),
            ("8) Avtomobil nomerini aniqlash tizimlari", "srv_automatic_gates")
        ],
        "internet_tarmoq_xizmatlari": [
            ("1) Wi-Fi tarmoqlarini o'rnatish va sozlash", "srv_wifi_setup"),
            ("2) Wi-Fi qamrov zonasini kengaytirish (Access Point)", "srv_wifi_extender"),
            ("3) Mobil aloqa signalini kuchaytirish (Repeater)", "srv_signal_booster"),
            ("4) Ofis va uy uchun lokal tarmoq (LAN) qurish", "srv_lan_setup"),
            ("5) Internet provayder xizmatlarini ulash", "srv_internet_provider"),
            ("6) Server va NAS qurilmalarini o'rnatish", "srv_server_nas"),
            ("7) Bulutli fayl almashinish va zaxira tizimlari", "srv_cloud_storage"),
            ("8) VPN va xavfsiz internet ulanishlarini tashkil qilish", "srv_vpn_setup")
        ],
        "energiya_yashil_texnologiyalar": [
            ("1) Quyosh panellarini o'rnatish va ulash", "srv_solar_panels"),
            ("2) Quyosh batareyalari orqali energiya saqlash tizimlari", "srv_solar_batteries"),
            ("3) Shamol generatorlarini o'rnatish", "srv_wind_generators"),
            ("4) Elektr energiyasini tejovchi yoritish tizimlari", "srv_energy_saving_lighting"),
            ("5) Avtomatik sug'orish tizimlari (Smart Irrigation)", "srv_smart_irrigation")
        ],
        "multimediya_aloqa_tizimlari": [
            ("1) Smart TV o'rnatish va ulash", "srv_smart_tv"),
            ("2) Uy kinoteatri tizimlari o'rnatish", "srv_home_cinema"),
            ("3) Audio tizimlar (multiroom)", "srv_multiroom_audio"),
            ("4) IP Telefoniya va mini ATS tizimlarini tashkil qilish", "srv_ip_telephony"),
            ("5) Video konferensiya tizimlari", "srv_video_conference"),
            ("6) Interaktiv taqdimot tizimlari (proyektor, LED ekran)", "srv_presentation_systems")
        ],
        "maxsus_qoshimcha_xizmatlar": [
            ("1) Aqlli ofis tizimlarini o'rnatish", "srv_smart_office"),
            ("2) Data markaz (Server room) loyihalash va montaj qilish", "srv_data_center"),
            ("3) Qurilma va tizimlar uchun texnik xizmat ko'rsatish", "srv_technical_support"),
            ("4) Dasturiy ta'minotni o'rnatish va yangilash", "srv_software_install"),
            ("5) IoT (Internet of Things) qurilmalarini integratsiya qilish", "srv_iot_integration"),
            ("6) Qurilmalarni masofadan boshqarish tizimlarini sozlash", "srv_remote_management"),
            ("7) Sun'iy intellekt asosidagi uy va ofis boshqaruv tizimlari", "srv_ai_management")
        ]
    }
    
    keyboard = []
    for text, callback_data in service_types.get(category, []):
        keyboard.append([InlineKeyboardButton(text=text, callback_data=callback_data)])
    
    # Orqaga tugmasi
    keyboard.append([InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_categories")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_smart_service_confirmation_keyboard(lang="uz"):
    """SmartService tasdiqlash klaviaturasi"""
    confirm_text = "✅ Tasdiqlash" if lang == "uz" else "✅ Подтвердить"
    cancel_text = "❌ Bekor qilish" if lang == "uz" else "❌ Отменить"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=confirm_text, callback_data="confirm_smart_service"),
            InlineKeyboardButton(text=cancel_text, callback_data="cancel_smart_service")
        ]
    ])
    return keyboard

def get_rating_keyboard(request_id: int, request_type: str) -> InlineKeyboardMarkup:
    """
    Reyting keyboard yaratish (1-5 yulduz)
    """
    keyboard = []
    
    # Yulduzlar qatorlari
    for i in range(1, 6):
        stars_text = "⭐" * i
        keyboard.append([
            InlineKeyboardButton(
                text=stars_text,
                callback_data=f"rate:{request_id}:{request_type}:{i}"
            )
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_skip_comment_keyboard(request_id: int, request_type: str) -> InlineKeyboardMarkup:
    """
    Izoh o'tkazib yuborish keyboard
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="O'tkazib yuborish",
                callback_data=f"skip_comment:{request_id}:{request_type}"
            )
        ]
    ])
    return keyboard