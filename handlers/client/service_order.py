from datetime import datetime
from aiogram import F
from aiogram.types import (
    Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup,
    FSInputFile, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
)
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from asyncpg import DatabaseDroppedError
from keyboards.client_buttons import (
    get_client_main_menu,
    zayavka_type_keyboard,
    geolocation_keyboard,
    media_attachment_keyboard,
    get_client_regions_keyboard,
    get_contact_keyboard,
    # confirmation_keyboard  # ← tashqi keyboard’ni o‘zgartirmaslik uchun biz lokalini ishlatamiz
)
from states.client_states import ServiceOrderStates
from database.queries import get_user_language
from database.client_queries import (
    find_user_by_telegram_id,
    create_service_order,
    get_user_phone_by_telegram_id,
    update_user_phone_by_telegram_id
)
from config import settings
from loader import bot

from aiogram import Router
import logging

logger = logging.getLogger(__name__)
router = Router()

# ---------- Yordamchi: region nomlarini normallashtirish ----------
REGION_CODE_TO_UZ: dict = {
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

def normalize_region(region_code: str) -> str:
    return REGION_CODE_TO_UZ.get(region_code, region_code)

# ---------- Lokal tasdiqlash inline klaviaturasi (tashqi faylni o‘zgartirmaslik uchun) ----------
def confirmation_inline_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm_service_yes"),
        InlineKeyboardButton(text="🔁 Qayta yuborish", callback_data="confirm_service_no"),
    ]])

# ---------- Start: Texnik xizmat oqimi ----------
@router.message(F.text.in_(["🔧 Texnik xizmat", "🔧 Техническая служба"]))
async def start_service_order(message: Message, state: FSMContext):
    try:
        await state.update_data(telegram_id=message.from_user.id)

        # Telefon bor-yo‘qligini tekshiramiz; bo‘lmasa contact so‘raymiz
        phone = await get_user_phone_by_telegram_id(message.from_user.id)
        if not phone:
            await message.answer(
                "Iltimos, raqamingizni jo'nating (tugma orqali).",
                reply_markup=get_contact_keyboard()
            )
            return
        else:
            await state.update_data(phone=phone)

        await message.answer(
            "🔧 <b>Texnik xizmat arizasi</b>\n\n"
            "📍 Qaysi hududda xizmat kerak?",
            reply_markup=get_client_regions_keyboard(),
            parse_mode='HTML'
        )
        await state.set_state(ServiceOrderStates.selecting_region)

    except Exception as e:
        logger.error(f"Error: {e}")
        await message.answer("❌ Xatolik yuz berdi.")

# ---------- Contact qabul qilish ----------
@router.message(F.contact)
async def handle_contact_for_service_order(message: Message, state: FSMContext):
    try:
        if not message.contact:
            return
        if message.contact.user_id and message.contact.user_id != message.from_user.id:
            await message.answer(
                "Iltimos, faqat o'zingizning raqamingizni yuboring.",
                reply_markup=get_contact_keyboard()
            )
            return

        phone_number = message.contact.phone_number
        await update_user_phone_by_telegram_id(message.from_user.id, phone_number)
        await state.update_data(phone=phone_number, telegram_id=message.from_user.id)

        await message.answer(
            "✅ Raqam qabul qilindi. Endi xizmat kerak bo'lgan hududni tanlang:",
            reply_markup=get_client_regions_keyboard()
        )
        await state.set_state(ServiceOrderStates.selecting_region)

    except Exception as e:
        logger.error(f"Error in handle_contact_for_service_order: {e}")
        await message.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")

# ---------- Region tanlash ----------
@router.callback_query(F.data.startswith("region_"), StateFilter(ServiceOrderStates.selecting_region))
async def select_region(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)

        region_code = callback.data.replace("region_", "", 1)
        region_name = normalize_region(region_code)

        await state.update_data(selected_region=region_name, region=region_name)

        await callback.message.answer(
            "Abonent turini tanlang:",
            reply_markup=zayavka_type_keyboard(),
            parse_mode='HTML'
        )
        await state.set_state(ServiceOrderStates.selecting_abonent_type)

    except Exception as e:
        logger.error(f"Error: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)

# ---------- Abonent turini tanlash ----------
@router.callback_query(F.data.startswith("zayavka_type_"), StateFilter(ServiceOrderStates.selecting_abonent_type))
async def select_abonent_type(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)

        abonent_type = callback.data.split("_")[-1].upper()
        await state.update_data(abonent_type=abonent_type)

        await callback.message.answer("🆔 Abonent ID raqamingizni kiriting:")
        await state.set_state(ServiceOrderStates.waiting_for_contact)

    except Exception as e:
        logger.error(f"Error: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)

# ---------- Abonent ID kiritish ----------
@router.message(StateFilter(ServiceOrderStates.waiting_for_contact), F.text)
async def get_abonent_id(message: Message, state: FSMContext):
    try:
        await state.update_data(abonent_id=message.text)

        await message.answer("📝 Muammoni batafsil yozing:")
        await state.set_state(ServiceOrderStates.entering_reason)

    except Exception as e:
        logger.error(f"Error: {e}")
        await message.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")

# ---------- Sabab / Muammo matni ----------
@router.message(StateFilter(ServiceOrderStates.entering_reason), F.text)
async def get_reason(message: Message, state: FSMContext):
    try:
        await state.update_data(reason=message.text)

        await message.answer("📍 Manzilingizni kiriting:")
        await state.set_state(ServiceOrderStates.entering_address)

    except Exception as e:
        logger.error(f"Error: {e}")
        await message.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")

# ---------- Manzil ----------
@router.message(StateFilter(ServiceOrderStates.entering_address), F.text)
async def get_address(message: Message, state: FSMContext):
    try:
        await state.update_data(address=message.text)

        await message.answer(
            "📷 Muammo rasmi yoki videosini yuborasizmi?",
            reply_markup=media_attachment_keyboard()
        )
        await state.set_state(ServiceOrderStates.asking_for_media)

    except Exception as e:
        logger.error(f"Error: {e}")
        await message.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")

# ---------- Media yuborish qarori ----------
@router.callback_query(F.data.in_(["attach_media_yes", "attach_media_no"]), StateFilter(ServiceOrderStates.asking_for_media))
async def ask_for_media(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)

        if callback.data == "attach_media_yes":
            await callback.message.answer("📷 Rasm yoki video yuboring:")
            await state.set_state(ServiceOrderStates.waiting_for_media)
        else:
            await ask_for_geolocation(callback.message, state)

    except Exception as e:
        logger.error(f"Error: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)

# ---------- Media qabul qilish ----------
@router.message(StateFilter(ServiceOrderStates.waiting_for_media), F.photo | F.video)
async def get_media(message: Message, state: FSMContext):
    try:
        if message.photo:
            media_id = message.photo[-1].file_id
            media_type = 'photo'
        elif message.video:
            media_id = message.video.file_id
            media_type = 'video'
        else:
            media_id = None
            media_type = None

        await state.update_data(media_id=media_id, media_type=media_type)
        await ask_for_geolocation(message, state)

    except Exception as e:
        logger.error(f"Error: {e}")
        await message.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")

# ---------- Geolokatsiya so‘rash ----------
async def ask_for_geolocation(message: Message, state: FSMContext):
    await message.answer(
        "📍 Geolokatsiya yuborasizmi?",
        reply_markup=geolocation_keyboard()
    )
    await state.set_state(ServiceOrderStates.asking_for_location)

# ---------- Geolokatsiya qarori ----------
@router.callback_query(F.data.in_(["send_location_yes", "send_location_no"]), StateFilter(ServiceOrderStates.asking_for_location))
async def geo_decision(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)

        if callback.data == "send_location_yes":
            location_keyboard = ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True)]],
                resize_keyboard=True,
                one_time_keyboard=True
            )
            await callback.message.answer("📍 Joylashuvingizni yuboring:", reply_markup=location_keyboard)
            await state.set_state(ServiceOrderStates.waiting_for_location)
        else:
            # Lokatsiyasiz ham avval tasdiqlash ekranini ko‘rsatamiz
            await show_service_order_confirmation(callback.message, state)

    except Exception as e:
        logger.error(f"Error: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)

# ---------- Lokatsiyani qabul qilish (location obyekti) ----------
@router.message(StateFilter(ServiceOrderStates.waiting_for_location), F.location)
async def get_geo(message: Message, state: FSMContext):
    try:
        await state.update_data(geo=message.location)

        await message.answer("✅ Joylashuv qabul qilindi!", reply_markup=ReplyKeyboardRemove())
        await show_service_order_confirmation(message, state)

    except Exception as e:
        logger.error(f"Error: {e}")
        await message.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")

# ---------- Lokatsiyani matn bilan kiritish holati ----------
@router.message(StateFilter(ServiceOrderStates.waiting_for_location), F.text)
async def get_location_text(message: Message, state: FSMContext):
    try:
        await state.update_data(location=message.text)
        await message.answer("✅ Joylashuv qabul qilindi!", reply_markup=ReplyKeyboardRemove())
        await show_service_order_confirmation(message, state)

    except Exception as e:
        logger.error(f"Error: {e}")
        await message.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")

# ---------- Tasdiqlash oynasi (yakuniy xulosa) ----------
async def show_service_order_confirmation(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        region = data.get('selected_region') or data.get('region')
        geo = data.get('geo')
        location_text = data.get('location')

        if geo:
            geo_text = f"{geo.latitude}, {geo.longitude}"
        elif location_text:
            geo_text = location_text
        else:
            geo_text = "Berilmagan"

        summary_msg = (
            "📋 <b>Texnik xizmat arizasi ma'lumotlari:</b>\n\n"
            f"🌍 <b>Hudud:</b> {region}\n"
            f"👤 <b>Abonent turi:</b> {data.get('abonent_type')}\n"
            f"🆔 <b>Abonent ID:</b> {data.get('abonent_id')}\n"
            f"📞 <b>Telefon:</b> {data.get('phone')}\n"
            f"📝 <b>Muammo:</b> {data.get('reason')}\n"
            f"📍 <b>Manzil:</b> {data.get('address')}\n"
            f"🗺 <b>Joylashuv:</b> {geo_text}\n"
            f"📷 <b>Media:</b> {'✅ Mavjud' if data.get('media_id') else '❌ Yo`q'}\n\n"
            "Ma'lumotlar to‘g‘rimi?"
        )
        await message.answer(summary_msg, reply_markup=confirmation_inline_kb(), parse_mode="HTML")
        await state.set_state(ServiceOrderStates.confirming_service)

    except Exception as e:
        logger.error(f"Error in show_service_order_confirmation: {e}")
        await message.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")

# ---------- YAKUNIY TASDIQLASH / QAYTA BOSHLASH ----------
@router.callback_query(F.data.in_(["confirm_service_yes", "confirm_service_no"]), StateFilter(ServiceOrderStates.confirming_service))
async def handle_service_confirmation(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)

        if callback.data == "confirm_service_yes":
            # Tasdiqlash → DBga yozish
            data = await state.get_data()
            geo = data.get('geo')
            await finish_service_order(callback.message, state, geo=geo)
        else:
            # Qayta yuborish → boshidan
            await callback.message.answer(
                "🔄 Ariza qayta boshlanmoqda...\n\nIltimos, hududni tanlang:",
                reply_markup=get_client_regions_keyboard()
            )
            await state.clear()
            await state.set_state(ServiceOrderStates.selecting_region)

    except Exception as e:
        logger.error(f"Error in handle_service_confirmation: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)



# ---------- Yaratish (finish) — sizdagi mavjud versiya; faqat chaqiruv yo‘li to‘g‘rilandi ----------
async def finish_service_order(message: Message, state: FSMContext, geo=None):
    try:
        data = await state.get_data()
        region = data.get('selected_region') or data.get('region')
        region_db_value = (region or '').lower()

        user_record = await find_user_by_telegram_id(data['telegram_id'])
        user = dict(user_record) if user_record is not None else {}

        if geo:
            geo_str = f"{geo.latitude},{geo.longitude}"
        elif data.get('location'):
            geo_str = data.get('location')
        else:
            geo_str = None

        request_id = await create_service_order(
            user.get('id'),
            region_db_value,
            data.get('abonent_id'),
            data.get('address'),
            data.get('reason'),
            data.get('media_id'),
            geo_str
        )
        print(f"Sending notification to group: {settings.ZAYAVKA_GROUP_ID}")
        if settings.ZAYAVKA_GROUP_ID:
            print(f"Group ID: {settings.ZAYAVKA_GROUP_ID}")
            try:
                print(f"Request ID: {request_id}")
                geo_text = ""
                if geo:
                    geo_text = f"\n📍 <b>Lokatsiya:</b> <a href='https://maps.google.com/?q={geo.latitude},{geo.longitude}'>Google Maps</a>"
                elif data.get('location'):
                    geo_text = f"\n📍 <b>Lokatsiya:</b> {data.get('location')}"

                phone_for_msg = data.get('phone') or user.get('phone') or '-'
                print(f"Phone for message: {phone_for_msg}")
                group_msg = (
                    f"🔧 <b>YANGI TEXNIK XIZMAT ARIZASI</b>\n"
                    f"{'='*30}\n"
                    f"🆔 <b>ID:</b> <code>{request_id}</code>\n"
                    f"👤 <b>Mijoz:</b> {user.get('full_name', '-')}\n"
                    f"📞 <b>Tel:</b> {phone_for_msg}\n"
                    f"🏢 <b>Region:</b> {region}\n"
                    f"🏢 <b>Abonent:</b> {data.get('abonent_type')} - {data.get('abonent_id')}\n"
                    f"📍 <b>Manzil:</b> {data.get('address')}\n"
                    f"📝 <b>Muammo:</b> {((data.get('reason') or data.get('description') or '')[:100])}...\n"
                    f"{geo_text}\n"
                    f"📷 <b>Media:</b> {'✅ Mavjud' if data.get('media_id') else '❌ Yo`q'}\n"
                    f"🕐 <b>Vaqt:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                    f"{'='*30}"
                )
                print(f"Group message: {group_msg}")

                await bot.send_message(
                    chat_id=settings.ZAYAVKA_GROUP_ID,
                    text=group_msg,
                    parse_mode='HTML'
                )
                print(f"Message sent to group {settings.ZAYAVKA_GROUP_ID}")

                if data.get('media_id'):
                    if data.get('media_type') == 'photo':
                        await bot.send_photo(
                            chat_id=settings.ZAYAVKA_GROUP_ID,
                            photo=data['media_id'],
                            caption=None,
                            parse_mode='HTML'
                        )
                    elif data.get('media_type') == 'video':
                        await bot.send_video(
                            chat_id=settings.ZAYAVKA_GROUP_ID,
                            video=data['media_id'],
                            caption=None,
                            parse_mode='HTML'
                        )
                print(f"Media sent to group {settings.ZAYAVKA_GROUP_ID}")

                if geo:
                    await bot.send_location(
                        settings.ZAYAVKA_GROUP_ID,
                        latitude=geo.latitude,
                        longitude=geo.longitude
                    )
                print(f"Location sent to group {settings.ZAYAVKA_GROUP_ID}")

            except Exception as group_error:
                logger.error(f"Group notification error: {group_error}")
                print(f"Group notification error: {group_error}")
                try:
                    await bot.send_message(
                        chat_id=settings.ADMIN_GROUP_ID, 
                        text=f"⚠️ Guruhga xabar yuborishda xato:\n{group_msg}\n\nXato: {group_error}",
                        parse_mode='HTML'
                    )
                except:
                    pass

        await message.answer(
            f"✅ <b>Texnik xizmat arizangiz qabul qilindi!</b>\n\n"
            f"🆔 Ariza raqami: <code>{request_id}</code>\n"
            f"📍 Hudud: {region}\n"
            f"🏢 Abonent ID: {data.get('abonent_id')}\n"
            f"📍 Manzil: {data.get('address')}\n"
            f"⏰ Texnik mutaxassis tez orada bog'lanadi!\n",
            parse_mode='HTML',
            reply_markup=get_client_main_menu()
        )
        print(f"Order ID: {request_id}")

        await state.clear()

    except Exception as e:
        logger.error(f"Error in finish_service_order: {e}")
        logger.error(f"Full error details: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        await message.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.", reply_markup=get_client_main_menu())
        await state.clear()

# ---------- Bekor qilish (ixtiyoriy) ----------
@router.callback_query(F.data == "service_cancel")
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer("Bekor qilindi")
        await callback.message.edit_reply_markup(reply_markup=None)

        await state.clear()
        await callback.message.answer(
            "❌ Texnik xizmat arizasi bekor qilindi",
            reply_markup=get_client_main_menu()
        )
    except Exception as e:
        logger.error(f"Error in cancel_order: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)
