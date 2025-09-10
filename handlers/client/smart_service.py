from datetime import datetime
from aiogram import F, Router
from aiogram.types import (
    Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, KeyboardButton, Location
)
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from keyboards.client_buttons import (
    get_client_main_menu,
    get_smart_service_categories_keyboard,
    get_smart_service_types_keyboard,
    get_smart_service_confirmation_keyboard,
    geolocation_keyboard
)
from states.client_states import SmartServiceStates
from database.queries import get_user_language
from database.client_queries import (
    find_user_by_telegram_id,
    create_smart_service_order
)
from config import settings
from loader import bot

import logging

logger = logging.getLogger(__name__)
router = Router()

# SmartService kategoriya mapping
CATEGORY_MAPPING = {
    "cat_smart_home": {
        "key": "aqlli_avtomatlashtirilgan_xizmatlar",
        "name": "🏠 Aqlli uy va avtomatlashtirilgan xizmatlar"
    },
    "cat_security": {
        "key": "xavfsizlik_kuzatuv_tizimlari", 
        "name": "🔒 Xavfsizlik va kuzatuv tizimlari"
    },
    "cat_internet": {
        "key": "internet_tarmoq_xizmatlari",
        "name": "🌐 Internet va tarmoq xizmatlari"
    },
    "cat_energy": {
        "key": "energiya_yashil_texnologiyalar",
        "name": "⚡ Energiya va yashil texnologiyalar"
    },
    "cat_multimedia": {
        "key": "multimediya_aloqa_tizimlari",
        "name": "📺 Multimediya va aloqa tizimlari"
    },
    "cat_special": {
        "key": "maxsus_qoshimcha_xizmatlar",
        "name": "🔧 Maxsus va qo'shimcha xizmatlar"
    }
}

# Service type mapping
SERVICE_TYPE_MAPPING = {
    # Smart Home Services
    "srv_smart_home_setup": "aqlli_uy_tizimlarini_ornatish_sozlash",
    "srv_smart_lighting": "aqlli_yoritish_smart_lighting_tizimlari",
    "srv_smart_thermostat": "aqlli_termostat_iqlim_nazarati_tizimlari",
    "srv_smart_lock": "smart_lock_internet_boshqariladigan_eshik_qulfi",
    "srv_smart_outlets": "aqlli_rozetalar_energiya_monitoring_tizimlari",
    "srv_remote_control": "uyni_masofadan_boshqarish_qurilmalari_uzim",
    "srv_smart_curtains": "aqlli_pardalari_jaluz_tizimlari",
    "srv_appliance_integration": "aqlli_malahiy_texnika_integratsiyasi",
    
    # Security Services
    "srv_cctv_cameras": "videokuzatuv_kameralarini_ornatish_ip_va_analog",
    "srv_camera_storage": "kamera_arxiv_tizimlari_bulutli_saqlash_xizmatlari",
    "srv_intercom": "domofon_tizimlari_ornatish",
    "srv_security_alarm": "xavfsizlik_signalizatsiyasi_harakat_sensorlari",
    "srv_fire_alarm": "yong_signalizatsiyasi_tizimlari",
    "srv_gas_flood_protection": "gaz_sizish_sav_toshqinliqqa_qarshi_tizimlar",
    "srv_face_recognition": "yuzni_tanish_face_recognition_tizimlari",
    "srv_automatic_gates": "avtomatik_eshik_darvoza_boshqaruv_tizimlari",
    
    # Internet Services
    "srv_wifi_setup": "wi_fi_tarmoqlarini_ornatish_sozlash",
    "srv_wifi_extender": "wi_fi_qamrov_zonasini_kengaytirish_access_point",
    "srv_signal_booster": "mobil_aloqa_signalini_kuchaytirish_repeater",
    "srv_lan_setup": "ofis_va_uy_uchun_lokal_tarmoq_lan_qurish",
    "srv_internet_provider": "internet_provayder_xizmatlarini_ulash",
    "srv_server_nas": "server_va_nas_qurilmalarini_ornatish",
    "srv_cloud_storage": "bulutli_fayl_almashish_zaxira_tizimlari",
    "srv_vpn_setup": "vpn_va_xavfsiz_internet_ulanishlarini_tashkil",
    
    # Energy Services
    "srv_solar_panels": "quyosh_panellarini_ornatish_ulash",
    "srv_solar_batteries": "quyosh_batareyalari_orqali_energiya_saqlash",
    "srv_wind_generators": "shamol_generatorlarini_ornatish",
    "srv_energy_saving_lighting": "elektr_energiyasini_tejovchi_yoritish_tizimlari",
    "srv_smart_irrigation": "avtomatik_suv_orish_tizimlari_smart_irrigation",
    
    # Multimedia Services
    "srv_smart_tv": "smart_tv_ornatish_ulash",
    "srv_home_cinema": "uy_kinoteatri_tizimlari_ornatish",
    "srv_multiroom_audio": "audio_tizimlar_multiroom",
    "srv_ip_telephony": "ip_telefoniya_mini_ats_tizimlarini_tashkil",
    "srv_video_conference": "video_konferensiya_tizimlari",
    "srv_presentation_systems": "interaktiv_taqdimot_tizimlari_proyektor_led",
    
    # Special Services
    "srv_smart_office": "aqlli_ofis_tizimlarini_ornatish",
    "srv_data_center": "data_markaz_server_room_loyihalash_montaj",
    "srv_technical_support": "qurilma_tizimlar_uchun_texnik_xizmat_korsatish",
    "srv_software_install": "dasturiy_taminotni_ornatish_yangilash",
    "srv_iot_integration": "iot_internet_of_things_qurilmalarini_integratsiya",
    "srv_remote_management": "qurilmalarni_masofadan_boshqarish_tizimlarini_sozlash",
    "srv_ai_management": "suniy_intellekt_asosidagi_uy_ofis_boshqaruv"
}

# SmartService boshlash
@router.message(F.text.in_(["🛜 Smart Service"]))
async def start_smart_service(message: Message, state: FSMContext):
    try:
        await state.update_data(telegram_id=message.from_user.id)
        
        await message.answer(
            "🛜 <b>Smart Service</b>\n\n"
            "Quyidagi kategoriyalardan birini tanlang:",
            reply_markup=get_smart_service_categories_keyboard(),
            parse_mode='HTML'
        )
        await state.set_state(SmartServiceStates.selecting_category)
        
    except Exception as e:
        logger.error(f"Error in start_smart_service: {e}")
        await message.answer("❌ Xatolik yuz berdi.")

# Kategoriya tanlash
@router.callback_query(F.data.startswith("cat_"), StateFilter(SmartServiceStates.selecting_category))
async def handle_category_selection(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        
        callback_data = callback.data
        category_info = CATEGORY_MAPPING.get(callback_data)
        
        if not category_info:
            await callback.answer("Noto'g'ri kategoriya", show_alert=True)
            return
            
        category_key = category_info["key"]
        category_name = category_info["name"]
        
        await state.update_data(selected_category=category_key)
        
        await callback.message.edit_text(
            f"🛜 <b>SmartService</b>\n\n"
            f"📂 <b>Kategoriya:</b> {category_name}\n\n"
            f"Quyidagi xizmat turlaridan birini tanlang:",
            reply_markup=get_smart_service_types_keyboard(category_key),
            parse_mode='HTML'
        )
        await state.set_state(SmartServiceStates.selecting_service_type)
        
    except Exception as e:
        logger.error(f"Error in handle_category_selection: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)

# Fallback handler for old callback data format
@router.callback_query(F.data.startswith("category_"), StateFilter(SmartServiceStates.selecting_category))
async def handle_old_category_selection(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        
        callback_data = callback.data
        logger.info(f"Received old callback data: {callback_data}")
        
        # Extract category from old format
        category = callback.data.replace("category_", "")
        
        # Map old category names to new ones
        old_to_new_mapping = {
            "aqlli_avtomatlashtirilgan_xizmatlar": "cat_smart_home",
            "xavfsizlik_kuzatuv_tizimlari": "cat_security", 
            "internet_tarmoq_xizmatlari": "cat_internet",
            "energiya_yashil_texnologiyalar": "cat_energy",
            "multimediya_aloqa_tizimlari": "cat_multimedia",
            "maxsus_qoshimcha_xizmatlar": "cat_special"
        }
        
        new_callback = old_to_new_mapping.get(category)
        if new_callback:
            category_info = CATEGORY_MAPPING.get(new_callback)
            if category_info:
                category_key = category_info["key"]
                category_name = category_info["name"]
                
                await state.update_data(selected_category=category_key)
                
                await callback.message.edit_text(
                    f"🛜 <b>SmartService</b>\n\n"
                    f"📂 <b>Kategoriya:</b> {category_name}\n\n"
                    f"Quyidagi xizmat turlaridan birini tanlang:",
                    reply_markup=get_smart_service_types_keyboard(category_key),
                    parse_mode='HTML'
                )
                await state.set_state(SmartServiceStates.selecting_service_type)
                return
        
        await callback.answer("Eski format - qayta urinib ko'ring", show_alert=True)
        
    except Exception as e:
        logger.error(f"Error in handle_old_category_selection: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)

# Xizmat turi tanlash
@router.callback_query(F.data.startswith("srv_"), StateFilter(SmartServiceStates.selecting_service_type))
async def handle_service_type_selection(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        
        callback_data = callback.data
        logger.info(f"Received service callback data: {callback_data}")
        
        service_type = SERVICE_TYPE_MAPPING.get(callback_data)
        if not service_type:
            logger.error(f"Service type not found for callback data: {callback_data}")
            await callback.answer("Noto'g'ri xizmat turi", show_alert=True)
            return
            
        await state.update_data(selected_service_type=service_type)
        
        await callback.message.edit_text(
            "🛜 <b>SmartService</b>\n\n"
            "📍 <b>Manzil kiriting:</b>\n"
            "Xizmat ko'rsatish kerak bo'lgan to'liq manzilni yozing.",
            parse_mode='HTML'
        )
        await state.set_state(SmartServiceStates.entering_address)
        
    except Exception as e:
        logger.error(f"Error in handle_service_type_selection: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)

# Fallback handler for old service callback data format
@router.callback_query(F.data.startswith("service_"), StateFilter(SmartServiceStates.selecting_service_type))
async def handle_old_service_type_selection(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        
        callback_data = callback.data
        logger.info(f"Received old service callback data: {callback_data}")
        
        # Extract service type from old format
        service_type = callback.data.replace("service_", "")
        await state.update_data(selected_service_type=service_type)
        
        await callback.message.edit_text(
            "🛜 <b>SmartService</b>\n\n"
            "📍 <b>Manzil kiriting:</b>\n"
            "Xizmat ko'rsatish kerak bo'lgan to'liq manzilni yozing.",
            parse_mode='HTML'
        )
        await state.set_state(SmartServiceStates.entering_address)
        
    except Exception as e:
        logger.error(f"Error in handle_old_service_type_selection: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)

# Orqaga qaytish
@router.callback_query(F.data == "back_to_categories", StateFilter(SmartServiceStates.selecting_service_type))
async def back_to_categories(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        
        await callback.message.edit_text(
            "🛜 <b>SmartService</b>\n\n"
            "Quyidagi kategoriyalardan birini tanlang:",
            reply_markup=get_smart_service_categories_keyboard(),
            parse_mode='HTML'
        )
        await state.set_state(SmartServiceStates.selecting_category)
        
    except Exception as e:
        logger.error(f"Error in back_to_categories: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)

# Manzil kiritish
@router.message(StateFilter(SmartServiceStates.entering_address))
async def handle_address_input(message: Message, state: FSMContext):
    try:
        address = message.text.strip()
        if len(address) < 10:
            await message.answer(
                "❌ Manzil juda qisqa. Iltimos, to'liq manzil kiriting."
            )
            return
            
        await state.update_data(address=address)
        
        await message.answer(
            "📍 <b>Lokatsiya yuborish</b>\n\n"
            "Aniq manzilni aniqlash uchun lokatsiyangizni yuborishni xohlaysizmi?",
            reply_markup=geolocation_keyboard(),
            parse_mode='HTML'
        )
        await state.set_state(SmartServiceStates.asking_for_location)
        
    except Exception as e:
        logger.error(f"Error in handle_address_input: {e}")
        await message.answer("❌ Xatolik yuz berdi.")

# Lokatsiya so'rash
@router.callback_query(F.data.in_(["send_location_yes", "send_location_no"]), StateFilter(SmartServiceStates.asking_for_location))
async def handle_location_request(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        
        if callback.data == "send_location_yes":
            location_keyboard = ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="📍 Lokatsiya yuborish", request_location=True)]],
                resize_keyboard=True
            )
            await callback.message.answer(
                "📍 Lokatsiyangizni yuboring:",
                reply_markup=location_keyboard
            )
            await state.set_state(SmartServiceStates.waiting_for_location)
        else:
            await show_confirmation(callback.message, state)
            
    except Exception as e:
        logger.error(f"Error in handle_location_request: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)

# Lokatsiya qabul qilish
@router.message(F.location, StateFilter(SmartServiceStates.waiting_for_location))
async def handle_location(message: Message, state: FSMContext):
    try:
        location = message.location
        await state.update_data(
            latitude=location.latitude,
            longitude=location.longitude
        )
        
        await show_confirmation(message, state)
        
    except Exception as e:
        logger.error(f"Error in handle_location: {e}")
        await message.answer("❌ Xatolik yuz berdi.")

# Tasdiqlash ko'rsatish
async def show_confirmation(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        category = data.get('selected_category')
        service_type = data.get('selected_service_type')
        address = data.get('address')
        
        # Find category name from mapping
        category_name = category
        for cat_info in CATEGORY_MAPPING.values():
            if cat_info["key"] == category:
                category_name = cat_info["name"]
                break
        
        # Service type nomini olish
        service_name = service_type.replace('_', ' ').title()
        
        location_text = ""
        if data.get('latitude') and data.get('longitude'):
            location_text = f"\n📍 <b>Lokatsiya:</b> <a href='https://maps.google.com/?q={data['latitude']},{data['longitude']}'>Google Maps</a>"
        
        confirmation_text = (
            f"🛜 <b>SmartService Arizasi</b>\n"
            f"{'='*30}\n"
            f"📂 <b>Kategoriya:</b> {category_name}\n"
            f"🔧 <b>Xizmat turi:</b> {service_name}\n"
            f"📍 <b>Manzil:</b> {address}{location_text}\n\n"
            f"✅ Ariza yaratilsinmi?"
        )
        
        await message.answer(
            confirmation_text,
            reply_markup=get_smart_service_confirmation_keyboard(),
            parse_mode='HTML'
        )
        await state.set_state(SmartServiceStates.confirming_order)
        
    except Exception as e:
        logger.error(f"Error in show_confirmation: {e}")
        await message.answer("❌ Xatolik yuz berdi.")

# Tasdiqlash
@router.callback_query(F.data.in_(["confirm_smart_service", "cancel_smart_service"]), StateFilter(SmartServiceStates.confirming_order))
async def handle_confirmation(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        
        if callback.data == "confirm_smart_service":
            await finish_smart_service_order(callback.message, state)
        else:
            await callback.message.answer(
                "❌ SmartService arizasi bekor qilindi.",
                reply_markup=get_client_main_menu()
            )
            await state.clear()
            
    except Exception as e:
        logger.error(f"Error in handle_confirmation: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)

# Arizani yakunlash
async def finish_smart_service_order(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        
        user_record = await find_user_by_telegram_id(data['telegram_id'])
        user = dict(user_record) if user_record is not None else {}
        
        order_id = await create_smart_service_order(
            user.get('id'),
            data.get('selected_category'),
            data.get('selected_service_type'),
            data.get('address'),
            data.get('latitude'),
            data.get('longitude')
        )
        
        # Menejerga xabar yuborish
        try:
            # Find category name from mapping
            category = data.get('selected_category')
            category_name = category
            for cat_info in CATEGORY_MAPPING.values():
                if cat_info["key"] == category:
                    category_name = cat_info["name"]
                    break
                    
            service_name = data.get('selected_service_type', '').replace('_', ' ').title()
            
            location_text = ""
            if data.get('latitude') and data.get('longitude'):
                location_text = f"\n📍 <b>Lokatsiya:</b> <a href='https://maps.google.com/?q={data['latitude']},{data['longitude']}'>Google Maps</a>"
            
            group_msg = (
                f"🛜 <b>YANGI SMARTSERVICE ARIZASI</b>\n"
                f"{'='*30}\n"
                f"🆔 <b>ID:</b> <code>{order_id}</code>\n"
                f"👤 <b>Mijoz:</b> {user.get('full_name', 'Noma\'lum')}\n"
                f"📞 <b>Telefon:</b> {user.get('phone', 'Noma\'lum')}\n"
                f"📂 <b>Kategoriya:</b> {category_name}\n"
                f"🔧 <b>Xizmat turi:</b> {service_name}\n"
                f"📍 <b>Manzil:</b> {data.get('address')}"
                f"{location_text}\n"
                f"🕐 <b>Vaqt:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                f"{'='*30}"
            )
            
            if settings.ZAYAVKA_GROUP_ID:
                await bot.send_message(
                    chat_id=settings.ZAYAVKA_GROUP_ID,
                    text=group_msg,
                    parse_mode='HTML'
                )
                
        except Exception as group_error:
            logger.error(f"Group notification error: {group_error}")
        
        await message.answer(
            f"✅ <b>SmartService arizangiz qabul qilindi!</b>\n\n"
            f"🆔 Ariza raqami: <code>{order_id}</code>\n"
            f"📂 Kategoriya: {category_name}\n"
            f"📍 Manzil: {data.get('address')}\n"
            f"⏰ Menejer tez orada bog'lanadi!\n",
            parse_mode='HTML',
            reply_markup=get_client_main_menu()
        )
        
        await state.clear()
        
    except Exception as e:
        logger.error(f"Error in finish_smart_service_order: {e}")
        await message.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.", reply_markup=get_client_main_menu())
        await state.clear()