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
    """Regions selection keyboard for client (UZ/RU labels, stable callback_data)."""

    labels_uz = {
        "toshkent_city": "Toshkent shahri",
        "toshkent_region": "Toshkent viloyati",
        "andijon": "Andijon",
        "fergana": "Farg'ona",
        "namangan": "Namangan",
        "sirdaryo": "Sirdaryo",
        "jizzax": "Jizzax",
        "samarkand": "Samarqand",
        "bukhara": "Buxoro",
        "navoi": "Navoiy",
        "kashkadarya": "Qashqadaryo",
        "surkhandarya": "Surxondaryo",
        "khorezm": "Xorazm",
        "karakalpakstan": "Qoraqalpog'iston",
    }

    labels_ru = {
        "toshkent_city": "г. Ташкент",
        "toshkent_region": "Ташкентская область",
        "andijon": "Андижан",
        "fergana": "Фергана",
        "namangan": "Наманган",
        "sirdaryo": "Сырдарья",
        "jizzax": "Джизак",
        "samarkand": "Самарканд",
        "bukhara": "Бухара",
        "navoi": "Навои",
        "kashkadarya": "Кашкадарья",
        "surkhandarya": "Сурхандарья",
        "khorezm": "Хорезм",
        "karakalpakstan": "Каракалпакстан",
    }

    L = labels_ru if lang == 'ru' else labels_uz

    rows = [
        [("toshkent_city",), ("toshkent_region",)],
        [("andijon",), ("fergana",)],
        [("namangan",), ("sirdaryo",)],
        [("jizzax",), ("samarkand",)],
        [("bukhara",), ("navoi",)],
        [("kashkadarya",), ("surkhandarya",)],
        [("khorezm",), ("karakalpakstan",)],
    ]

    keyboard = []
    for row in rows:
        keyboard.append([
            InlineKeyboardButton(
                text=L[key],
                callback_data=f"region_{key}"
            ) for (key,) in row
        ])

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


def get_smart_service_categories_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """SmartService kategoriyalarini tanlash klaviaturasi (uz/ru)"""
    categories_uz = [
        ("🏠 Aqlli uy va avtomatlashtirilgan xizmatlar", "cat_smart_home"),
        ("🔒 Xavfsizlik va kuzatuv tizimlari", "cat_security"),
        ("🌐 Internet va tarmoq xizmatlari", "cat_internet"),
        ("⚡ Energiya va yashil texnologiyalar", "cat_energy"),
        ("📺 Multimediya va aloqa tizimlari", "cat_multimedia"),
        ("🔧 Maxsus va qo'shimcha xizmatlar", "cat_special"),
    ]
    categories_ru = [
        ("🏠 Умный дом и автоматизация", "cat_smart_home"),
        ("🔒 Безопасность и видеонаблюдение", "cat_security"),
        ("🌐 Интернет и сети", "cat_internet"),
        ("⚡ Энергия и зелёные технологии", "cat_energy"),
        ("📺 Мультимедиа и коммуникации", "cat_multimedia"),
        ("🔧 Специальные и доп. услуги", "cat_special"),
    ]
    categories = categories_ru if lang == "ru" else categories_uz

    keyboard = [[InlineKeyboardButton(text=text, callback_data=cb)] for text, cb in categories]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# ====== LABEL LUG‘ATLAR ======
CATEGORY_LABELS = {
    "cat_smart_home": {"uz": "🏠 Aqlli uy va avtomatlashtirilgan xizmatlar", "ru": "🏠 Умный дом и автоматизация"},
    "cat_security":   {"uz": "🔒 Xavfsizlik va kuzatuv tizimlari",          "ru": "🔒 Безопасность и видеонаблюдение"},
    "cat_internet":   {"uz": "🌐 Internet va tarmoq xizmatlari",             "ru": "🌐 Интернет и сети"},
    "cat_energy":     {"uz": "⚡ Energiya va yashil texnologiyalar",         "ru": "⚡ Энергия и зелёные технологии"},
    "cat_multimedia": {"uz": "📺 Multimediya va aloqa tizimlari",            "ru": "📺 Мультимедиа и коммуникации"},
    "cat_special":    {"uz": "🔧 Maxsus va qo'shimcha xizmatlar",            "ru": "🔧 Специальные и доп. услуги"},
}

SERVICE_LABELS = {
    "srv_smart_home_setup": {"uz": "Aqlli uy tizimlarini o'rnatish va sozlash", "ru": "Установка и настройка системы умного дома"},
    "srv_smart_lighting": {"uz": "Aqlli yoritish (Smart Lighting) tizimlari", "ru": "Умное освещение (Smart Lighting)"},
    "srv_smart_thermostat": {"uz": "Aqlli termostat va iqlim nazarati", "ru": "Умный термостат и климат-контроль"},
    "srv_smart_lock": {"uz": "Smart Lock — internet orqali boshqariladigan qulflar", "ru": "Smart Lock — умный замок (через интернет)"},
    "srv_smart_outlets": {"uz": "Aqlli rozetalar va energiya monitoringi", "ru": "Умные розетки и мониторинг энергии"},
    "srv_remote_control": {"uz": "Uyni masofadan boshqarish qurilmalari", "ru": "Дистанционное управление домом"},
    "srv_smart_curtains": {"uz": "Aqlli pardalar va jaluzlar", "ru": "Умные шторы и жалюзи"},
    "srv_appliance_integration": {"uz": "Aqlli maishiy texnika integratsiyasi", "ru": "Интеграция умной бытовой техники"},

    "srv_cctv_cameras": {"uz": "Videokuzatuv kameralarini o'rnatish (IP/analog)", "ru": "Установка видеонаблюдения (IP/аналог)"},
    "srv_camera_storage": {"uz": "Kamera arxiv tizimlari, bulutli saqlash", "ru": "Архив и облачное хранение видео"},
    "srv_intercom": {"uz": "Domofon tizimlari", "ru": "Домофонные системы"},
    "srv_security_alarm": {"uz": "Xavfsizlik signalizatsiyasi va sensorlar", "ru": "Охранная сигнализация и датчики"},
    "srv_fire_alarm": {"uz": "Yong'in signalizatsiyasi tizimlari", "ru": "Пожарная сигнализация"},
    "srv_gas_flood_protection": {"uz": "Gaz sizishi/suv toshqiniga qarshi tizimlar", "ru": "Системы защиты от утечки газа/потопа"},
    "srv_face_recognition": {"uz": "Yuzni tanish (Face Recognition) tizimlari", "ru": "Распознавание лиц (Face Recognition)"},
    "srv_automatic_gates": {"uz": "Avtomatik eshik/darvoza boshqaruvi", "ru": "Автоматические двери/ворота"},

    "srv_wifi_setup": {"uz": "Wi-Fi tarmoqlarini o'rnatish va sozlash", "ru": "Установка и настройка Wi-Fi"},
    "srv_wifi_extender": {"uz": "Wi-Fi qamrovini kengaytirish (Access Point)", "ru": "Расширение покрытия Wi-Fi (Access Point)"},
    "srv_signal_booster": {"uz": "Mobil aloqa signalini kuchaytirish (Repeater)", "ru": "Усиление мобильной связи (Repeater)"},
    "srv_lan_setup": {"uz": "Ofis/uy uchun lokal tarmoq (LAN) qurish", "ru": "Построение локальной сети (LAN)"},
    "srv_internet_provider": {"uz": "Internet provayder xizmatlarini ulash", "ru": "Подключение услуг интернет-провайдера"},
    "srv_server_nas": {"uz": "Server va NAS qurilmalarini o'rnatish", "ru": "Установка серверов и NAS"},
    "srv_cloud_storage": {"uz": "Bulutli fayl almashish va zaxira", "ru": "Обмен файлами и резервное копирование в облаке"},
    "srv_vpn_setup": {"uz": "VPN va xavfsiz ulanishlar", "ru": "VPN и защищённые подключения"},

    "srv_solar_panels": {"uz": "Quyosh panellarini o'rnatish va ulash", "ru": "Установка и подключение солнечных панелей"},
    "srv_solar_batteries": {"uz": "Quyosh batareyalari bilan energiya saqlash", "ru": "Хранение энергии на солнечных батареях"},
    "srv_wind_generators": {"uz": "Shamol generatorlarini o'rnatish", "ru": "Установка ветрогенераторов"},
    "srv_energy_saving_lighting": {"uz": "Energiya tejamkor yoritish tizimlari", "ru": "Энергоэффективное освещение"},
    "srv_smart_irrigation": {"uz": "Avtomatik sug'orish (Smart Irrigation)", "ru": "Автополив (Smart Irrigation)"},

    "srv_smart_tv": {"uz": "Smart TV o'rnatish va ulash", "ru": "Установка и подключение Smart TV"},
    "srv_home_cinema": {"uz": "Uy kinoteatri tizimlari", "ru": "Домашний кинотеатр"},
    "srv_multiroom_audio": {"uz": "Audio tizimlar (multiroom)", "ru": "Аудиосистемы (multiroom)"},
    "srv_ip_telephony": {"uz": "IP-telefoniya, mini-ATS", "ru": "IP-телефония, мини-АТС"},
    "srv_video_conference": {"uz": "Video konferensiya tizimlari", "ru": "Системы видеоконференций"},
    "srv_presentation_systems": {"uz": "Interaktiv taqdimot (proyektor/LED)", "ru": "Интерактивные презентации (проектор/LED)"},

    "srv_smart_office": {"uz": "Aqlli ofis tizimlari", "ru": "Системы умного офиса"},
    "srv_data_center": {"uz": "Data-markaz (Server room) loyihalash va montaj", "ru": "Дата-центр (Server room): проектирование и монтаж"},
    "srv_technical_support": {"uz": "Qurilma/tizimlar uchun texnik xizmat", "ru": "Техобслуживание устройств/систем"},
    "srv_software_install": {"uz": "Dasturiy ta'minotni o'rnatish/yangilash", "ru": "Установка/обновление ПО"},
    "srv_iot_integration": {"uz": "IoT qurilmalarini integratsiya qilish", "ru": "Интеграция IoT-устройств"},
    "srv_remote_management": {"uz": "Masofaviy boshqaruv tizimlari", "ru": "Системы удалённого управления"},
    "srv_ai_management": {"uz": "Sun'iy intellekt asosidagi boshqaruv", "ru": "AI-управление домом/офисом"},
}

# Kategoriya -> xizmat kodlari ro'yxati
CATEGORY_TO_SERVICES = {
    "cat_smart_home": [
        "srv_smart_home_setup", "srv_smart_lighting", "srv_smart_thermostat",
        "srv_smart_lock", "srv_smart_outlets", "srv_remote_control",
        "srv_smart_curtains", "srv_appliance_integration",
    ],
    "cat_security": [
        "srv_cctv_cameras", "srv_camera_storage", "srv_intercom",
        "srv_security_alarm", "srv_fire_alarm", "srv_gas_flood_protection",
        "srv_face_recognition", "srv_automatic_gates",
    ],
    "cat_internet": [
        "srv_wifi_setup", "srv_wifi_extender", "srv_signal_booster",
        "srv_lan_setup", "srv_internet_provider", "srv_server_nas",
        "srv_cloud_storage", "srv_vpn_setup",
    ],
    "cat_energy": [
        "srv_solar_panels", "srv_solar_batteries", "srv_wind_generators",
        "srv_energy_saving_lighting", "srv_smart_irrigation",
    ],
    "cat_multimedia": [
        "srv_smart_tv", "srv_home_cinema", "srv_multiroom_audio",
        "srv_ip_telephony", "srv_video_conference", "srv_presentation_systems",
    ],
    "cat_special": [
        "srv_smart_office", "srv_data_center", "srv_technical_support",
        "srv_software_install", "srv_iot_integration", "srv_remote_management",
        "srv_ai_management",
    ],
}



def get_smart_service_types_keyboard(category_key: str, lang: str = "uz") -> InlineKeyboardMarkup:
    """category_key = 'cat_*' kodi bo'yicha xizmat turlarini chiqaradi."""
    srv_codes = CATEGORY_TO_SERVICES.get(category_key, [])
    rows = []
    for srv in srv_codes:
        label = SERVICE_LABELS.get(srv, {}).get(lang, SERVICE_LABELS.get(srv, {}).get("uz", srv))
        rows.append([InlineKeyboardButton(text=label, callback_data=srv)])

    back_text = "◀️ Назад" if lang == "ru" else "◀️ Orqaga"
    rows.append([InlineKeyboardButton(text=back_text, callback_data="back_to_categories")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


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