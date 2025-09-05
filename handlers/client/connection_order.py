from datetime import datetime
import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from keyboards.client_buttons import (
    get_client_main_menu,
    zayavka_type_keyboard,
    geolocation_keyboard,
    get_client_tariff_selection_keyboard,
    confirmation_keyboard,
    get_client_regions_keyboard
)
from states.client_states import ConnectionOrderStates
from config import settings
from database.client_queries import ensure_user, get_or_create_tarif_by_code, create_connection_order
from loader import bot


logger = logging.getLogger(__name__)

router = Router()


# Region code -> Uzbek name normalization
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
    """Convert internal region code to Uzbek display/storage name."""
    return REGION_CODE_TO_UZ.get(region_code, region_code)


@router.message(F.text.in_(["🔌 Ulanish uchun ariza", "🔌 Заявка на подключение"]))
async def start_connection_order_client(message: Message, state: FSMContext):
    try:
        await message.answer(
            "🔌 <b>Yangi ulanish arizasi</b>\n\n"
            "📍 Qaysi regionda ulanmoqchisiz?",
            reply_markup=get_client_regions_keyboard(),
            parse_mode='HTML'
        )
        
        await state.set_state(ConnectionOrderStates.selecting_region)
        
    except Exception as e:
        logger.error(f"Error in start_connection_order_client: {e}")
        await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")


@router.callback_query(F.data.startswith("region_"), StateFilter(ConnectionOrderStates.selecting_region))
async def select_region_old_client(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        
        # to‘g‘ri parslash
        region_code = callback.data.replace("region_", "", 1)  
        region_name = normalize_region(region_code)
        
        await state.update_data(selected_region=region_name)
        
        await callback.message.answer(
            "Ulanish turini tanlang:",
            reply_markup=zayavka_type_keyboard()
        )
        
        await state.set_state(ConnectionOrderStates.selecting_connection_type)
    except Exception as e:
        logger.error(f"Error in select_region_old_client: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)


@router.callback_query(F.data.startswith("zayavka_type_"), StateFilter(ConnectionOrderStates.selecting_connection_type))
async def select_connection_type_client(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        
        connection_type = callback.data.split("_")[-1]  
        await state.update_data(connection_type=connection_type)
        
        
        try:
            photo = FSInputFile("static/image.png")
            await callback.message.answer_photo(
                photo=photo,
                caption="📋 <b>Tariflardan birini tanlang:</b>\n\n",
                reply_markup=get_client_tariff_selection_keyboard(),
                parse_mode='HTML'
            )
        except Exception as img_error:
            logger.warning(f"Could not send tariff image: {img_error}")
            await callback.message.answer(
                "📋 <b>Tariflardan birini tanlang:</b>\n\n",
                reply_markup=get_client_tariff_selection_keyboard(),
                parse_mode='HTML'
            )
        await state.set_state(ConnectionOrderStates.selecting_tariff)
        
    except Exception as e:
        logger.error(f"Error in select_connection_type_client: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)

@router.callback_query(F.data.in_(["tariff_xammasi_birga_4", "tariff_xammasi_birga_3_plus", "tariff_xammasi_birga_3", "tariff_xammasi_birga_2"]))
async def select_tariff_client(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        
        tariff_code = callback.data
        await state.update_data(selected_tariff=tariff_code)
        
        await callback.message.answer("📍 Manzilingizni kiriting:")
        
        await state.set_state(ConnectionOrderStates.entering_address)
        
    except Exception as e:
        logger.error(f"Error in select_tariff_client: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)

@router.message(StateFilter(ConnectionOrderStates.entering_address))
async def get_connection_address_client(message: Message, state: FSMContext):
    try:
        await state.update_data(address=message.text)
        await message.answer(
            "Geolokatsiya yuborasizmi?",
            reply_markup=geolocation_keyboard('uz')
        )
        
        await state.set_state(ConnectionOrderStates.asking_for_geo)
        
    except Exception as e:
        logger.error(f"Error in get_connection_address_client: {e}")
        await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

@router.callback_query(F.data.in_(["send_location_yes", "send_location_no"]), StateFilter(ConnectionOrderStates.asking_for_geo))
async def ask_for_geo_client(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
        await callback.message.edit_reply_markup(reply_markup=None)
        
        if callback.data == "send_location_yes":
            
            location_keyboard = ReplyKeyboardMarkup(
                keyboard=[[
                    KeyboardButton(
                        text="📍 Joylashuvni yuborish",
                        request_location=True
                    )
                ]],
                resize_keyboard=True,
                one_time_keyboard=True
            )
            
            await callback.message.answer(
                "📍 Joylashuvingizni yuboring:",
                reply_markup=location_keyboard
            )
            
            await state.set_state(ConnectionOrderStates.waiting_for_geo)
        else:
            await finish_connection_order_client(callback, state, geo=None)
        
    except Exception as e:
        logger.error(f"Error in ask_for_geo_client: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)

@router.message(StateFilter(ConnectionOrderStates.waiting_for_geo), F.location)
async def get_geo_client(message: Message, state: FSMContext):
    try:
        await state.update_data(geo=message.location)
        
        await message.answer(
            "✅ Joylashuv qabul qilindi!",
            reply_markup=ReplyKeyboardRemove()
        )
        
        await finish_connection_order_client(message, state, geo=message.location)
        
    except Exception as e:
        logger.error(f"Error in get_geo_client: {e}")
        await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

async def finish_connection_order_client(message_or_callback, state: FSMContext, geo=None):
    """Client uchun complete connection request submission"""
    try:
        data = await state.get_data()

        region = data.get('selected_region', data.get('region', 'toshkent shahri'))
        connection_type = data.get('connection_type', 'standard')
        tariff_code = data.get('selected_tariff', 'tariff_xammasi_birga_4')
        # Map code to display name
        code_to_name = {
            "tariff_xammasi_birga_4": "Hammasi birga 4",
            "tariff_xammasi_birga_3_plus": "Hammasi birga 3+",
            "tariff_xammasi_birga_3": "Hammasi birga 3",
            "tariff_xammasi_birga_2": "Hammasi birga 2",
        }
        tariff_display = code_to_name.get(tariff_code, tariff_code)
        address = data.get('address', '-')
        
        # Tasdiqlash xabari
        text = (
            f"🏛️ <b>Hudud:</b> {region.title()}\n"
            f"🔌 <b>Ulanish turi:</b> {connection_type.upper()}\n"
            f"💳 <b>Tarif:</b> {tariff_display}\n"
            f"🏠 <b>Manzil:</b> {address}\n"
            f"📍 <b>Geolokatsiya:</b> {'✅ Yuborilgan' if geo else '❌ Yuborilmagan'}\n\n"
            f"Ma'lumotlar to'g'rimi?"
        )
        
        if hasattr(message_or_callback, "message"):
            await message_or_callback.message.answer(
                text,
                parse_mode='HTML',
                reply_markup=confirmation_keyboard()
            )
        else:
            await message_or_callback.answer(
                text,
                parse_mode='HTML',
                reply_markup=confirmation_keyboard()
            )
        
        await state.set_state(ConnectionOrderStates.confirming_connection)
        
    except Exception as e:
        logger.error(f"Error in finish_connection_order_client: {e}")
        if hasattr(message_or_callback, "message"):
            await message_or_callback.message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
        else:
            await message_or_callback.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

@router.callback_query(F.data == "confirm_zayavka", StateFilter(ConnectionOrderStates.confirming_connection))
async def confirm_connection_order_client(callback: CallbackQuery, state: FSMContext):
    """Client zayavkasini tasdiqlash va database'ga yozish"""
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer("⏳ Zayavka yaratilmoaqda...")
        
        data = await state.get_data()
        
        region = (data.get('selected_region') or data.get('region') or 'toshkent shahri').lower()

        user_row = await ensure_user(callback.from_user.id, callback.from_user.full_name, callback.from_user.username)
        user_id = user_row["id"]
        user_phone = user_row.get("phone") if isinstance(user_row, dict) else user_row["phone"]

        tariff_code = data.get('selected_tariff')
        tarif_id = await get_or_create_tarif_by_code(tariff_code) if tariff_code else None
        code_to_name = {
            "tariff_xammasi_birga_4": "Hammasi birga 4",
            "tariff_xammasi_birga_3_plus": "Hammasi birga 3+",
            "tariff_xammasi_birga_3": "Hammasi birga 3",
            "tariff_xammasi_birga_2": "Hammasi birga 2",
        }
        tariff_name = code_to_name.get(tariff_code, tariff_code) if tariff_code else None

        # Agar tarif topilmasa, yangi yaratmasdan foydalanuvchidan qayta tanlashni so'raymiz
        if tariff_code and not tarif_id:
            await callback.message.answer(
                "❌ Tanlangan tarif topilmadi. Iltimos, quyidagi ro'yxatdan tarifni qayta tanlang.",
                reply_markup=get_client_tariff_selection_keyboard()
            )
            await state.set_state(ConnectionOrderStates.selecting_tariff)
            return

        # Geo
        geo_data = data.get('geo')
        latitude = getattr(geo_data, 'latitude', None) if geo_data else None
        longitude = getattr(geo_data, 'longitude', None) if geo_data else None

        
        request_id = await create_connection_order(
            user_id=user_id,
            region=region,
            address=data.get('address', 'Kiritilmagan'),
            tarif_id=tarif_id,
            latitude=latitude,
            longitude=longitude
        )

        if settings.ZAYAVKA_GROUP_ID:
            try:
                geo_text = ""
                if geo_data:
                    geo_text = f"\n📍 <b>Lokatsiya:</b> <a href='https://maps.google.com/?q={geo_data.latitude},{geo_data.longitude}'>Google Maps</a>"
                
                phone_for_msg = data.get('phone') or user_phone or '-'
                group_msg = (
                    f"🔌 <b>YANGI ULANISH ARIZASI</b>\n"
                    f"{'='*30}\n"
                    f"🆔 <b>ID:</b> <code>{request_id}</code>\n"
                    f"👤 <b>Mijoz:</b> {callback.from_user.full_name}\n"
                    f"📞 <b>Tel:</b> {phone_for_msg}\n"
                    f"🏢 <b>Region:</b> {region.title()}\n"
                    f"🔌 <b>Turi:</b> {data.get('connection_type', 'B2C').upper()}\n"
                    f"💳 <b>Tarif:</b> {tariff_name}\n"
                    f"📍 <b>Manzil:</b> {data.get('address')}"
                    f"{geo_text}\n"
                    f"🕐 <b>Vaqt:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                    f"{'='*30}"
                )
                
                await bot.send_message(
                    chat_id=settings.ZAYAVKA_GROUP_ID,
                    text=group_msg,
                    parse_mode='HTML'
                )
            except Exception as group_error:
                # Group notification error - handle silently
                pass
        
        # # Manager'larga qisqa xabar yuborish (1 qatorli)
        # managers = await get_managers_by_region(region)
        # for manager in managers:
        #     try:
        #         # Qisqa 1 qatorli xabar
        #         short_msg = f"🔌 Yangi ariza #{request_id} | {user.get('full_name')} | {region.title()} | {data.get('selected_tariff')}"
                
        #         await bot.send_message(
        #             chat_id=manager['telegram_id'],
        #             text=short_msg
        #         )
        #     except Exception as notify_error:
        #         # Manager notification error - handle silently
        #         pass
        
        # Success message
        phone_for_msg = data.get('phone') or user_phone or '-'
        success_msg = (
            f"✅ <b>Arizangiz muvaffaqiyatli qabul qilindi!</b>\n\n"
            f"🆔 Ariza raqami: <code>{request_id}</code>\n"
            f"📍 Region: {region.title()}\n"
            f"💳 Tarif: {tariff_name}\n"
            f"📞 Telefon: {phone_for_msg}\n"
            f"📍 Manzil: {data.get('address')}\n\n"
            f"⏰ Menejerlarimiz tez orada siz bilan bog'lanadi!\n"
        )
        
        await callback.message.answer(success_msg, parse_mode='HTML')
        
        # Main menu
        from keyboards.client_buttons import get_main_menu_keyboard
        await callback.message.answer(
            "Bosh menyu:",
            reply_markup=get_main_menu_keyboard('uz')
        )
        
        await state.clear()
        
    except Exception as e:
        pass

@router.callback_query(F.data == "resend_zayavka", StateFilter(ConnectionOrderStates.confirming_connection))
async def resend_connection_order_client(callback: CallbackQuery, state: FSMContext):
    """Client zayavkasini qayta yuborish"""
    try:
        await callback.answer("Qayta yuborish...")
        await callback.message.edit_reply_markup(reply_markup=None)
        
        await state.clear()     
        
        await callback.message.answer(
            "🔌 <b>Yangi ulanish arizasi</b>\n\n"
            "📍 Qaysi regionda ulanmoqchisiz?",
            reply_markup=get_client_regions_keyboard(),
            parse_mode='HTML'
        )
        
        await state.set_state(ConnectionOrderStates.selecting_region)
        
    except Exception as e:
        try:
            logger.error(f"Error in resend_connection_order_client: {e}")
        except NameError:
            print(f"Fallback log: Error in resend_connection_order_client: {e}")
            try:
                import logging
                basic_logger = logging.getLogger(__name__)
                basic_logger.error(f"Error in resend_connection_order_client: {e}")
            except:
                pass
        
        await callback.answer("Xatolik yuz berdi", show_alert=True)

