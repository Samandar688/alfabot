from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from database.client_queries import find_user_by_telegram_id, get_user_orders_count, get_user_orders_paginated, get_region_name_by_id
from database.queries import get_user_language, update_user_full_name
from keyboards.client_buttons import get_client_main_menu, get_client_profile_reply_keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from states.client_states import ProfileEditStates

router = Router()

@router.message(F.text.in_(["👤 Kabinet", "👤 Кабинет"]))
async def profile_handler(message: Message):
    user_lang = await get_user_language(message.from_user.id)
    
    cabinet_texts = {
        "ru": (
            "🏠 <b>Личный кабинет</b>\n\n"
            "💡 Выберите нужное действие из меню:"
        ),
        "uz": (
            "🏠 <b>Shaxsiy kabinet</b>\n\n"
            "💡 Quyidagi menyudan kerakli amalni tanlang:"
        ),
    }
    
    await message.answer(
        cabinet_texts.get(user_lang, cabinet_texts["uz"]),
        parse_mode="HTML",
        reply_markup=get_client_profile_reply_keyboard(user_lang)
    )


@router.message(F.text.in_(["👀 Ma'lumotlarni ko'rish", "👀 Просмотр информации"]))
async def view_info_handler(message: Message):
    user_lang = await get_user_language(message.from_user.id)
    telegram_id = message.from_user.id
    
    # Get user information from database
    user_info = await find_user_by_telegram_id(telegram_id)
    
    if not user_info:
        error_text = (
            "❌ Пользователь не найден в базе данных."
            if user_lang == "ru" else
            "❌ Foydalanuvchi ma'lumotlar bazasida topilmadi."
        )
        await message.answer(error_text, parse_mode="HTML")
        return
    
    if user_lang == "ru":
        text = "👀 <b>Просмотр информации</b>\n\n"
        text += f"🆔 ID: {user_info['id']}\n"
        text += f"👤 Имя: {user_info.get('full_name', 'Не указано')}\n"
        text += f"📱 Телефон: {user_info.get('phone', 'Не указан')}\n"
        text += f"🏷️ Роль: {user_info.get('role', 'Не указана')}\n"
        text += f"📅 Дата регистрации: {_fmt_dt(user_info.get('created_at', 'Не указана'))}\n"
        if user_info.get('username'):
            text += f"📧 Username: @{user_info['username']}\n"
    else:
        text = "👀 <b>Ma'lumotlarni ko'rish</b>\n\n"
        text += f"🆔 ID: {user_info['id']}\n"
        text += f"👤 Ism: {user_info.get('full_name', 'Ko\'rsatilmagan')}\n"
        text += f"📱 Telefon: {user_info.get('phone', 'Ko\'rsatilmagan')}\n"
        text += f"🏷️ Rol: {user_info.get('role', 'Ko\'rsatilmagan')}\n"
        text += f"📅 Ro'yxatdan o'tgan: {_fmt_dt(user_info.get('created_at', 'Ko\'rsatilmagan'))}\n"
        if user_info.get('username'):
            text += f"📧 Username: @{user_info['username']}\n"
    
    await message.answer(text, parse_mode="HTML")

from datetime import datetime

# ... your existing imports and code above remain unchanged ...

@router.message(F.text.in_(["📋 Mening arizalarim", "📋 Мои заявки"]))
async def my_orders_handler(message: Message, state: FSMContext):
    await show_orders_with_state(message, state, 0)

def _fmt_dt(value) -> str:
    # created_at string yoki datetime bo‘lishi mumkin — xavfsiz formatlash
    if isinstance(value, datetime):
        return value.strftime('%d.%m.%Y %H:%M')
    try:
        # ISO string bo‘lsa
        return datetime.fromisoformat(str(value)).strftime('%d.%m.%Y %H:%M')
    except Exception:
        return str(value)

async def show_orders_with_state(message: Message, state: FSMContext, idx: int = 0):
    user_lang = await get_user_language(message.from_user.id)
    telegram_id = message.from_user.id

    # Get all orders for the user
    orders = await get_user_orders_paginated(telegram_id, offset=0, limit=1000)

    if not orders:
        text = (
            "📋 <b>Мои заявки</b>\n\n❌ У вас пока нет заявок."
            if user_lang == "ru" else
            "📋 <b>Mening arizalarim</b>\n\n❌ Sizda hali arizalar yo'q."
        )
        await message.answer(text, parse_mode="HTML")
        return

    # Store orders in state
    await state.update_data(orders=orders, idx=idx, lang=user_lang)
    
    # Show the order at the given index
    await render_order_card(message, orders, idx, user_lang)

async def render_order_card(target, orders: list, idx: int, user_lang: str):
    if idx < 0 or idx >= len(orders):
        return
    
    order = orders[idx]
    
    # Turi nomi (ikkala formatni ham qo'llab-quvvatlaymiz)
    otype = (order.get('order_type') or '').lower()
    is_conn = otype in ('connection', 'connection_request')
    
    if user_lang == "ru":
        title = "📋 <b>Мои заявки</b>"
        order_type_text = "🔗 Подключение" if is_conn else "🔧 Техническая заявка"

        text = f"{title}\n\n"
        text += f"<b>Заявка #{order['id']}</b>\n"
        text += f"📝 Тип: {order_type_text}\n"
        text += f"📍 Регион: {get_region_name_by_id(order.get('region', '-'))}\n"
        text += f"🏠 Адрес: {order.get('address','-')}\n"
        if order.get('abonent_id'):
            text += f"🆔 ID абонента: {order['abonent_id']}\n"
        if order.get('description'):
            text += f"📄 Описание: {order['description']}\n"
        text += f"📅 Создана: {_fmt_dt(order.get('created_at'))}\n"
        text += f"\n🗂️ <i>Заявка {idx + 1} / {len(orders)}</i>"

    else:
        title = "📋 <b>Mening arizalarim</b>"
        order_type_text = "🔗 Ulanish" if is_conn else "🔧 Texnik ariza"

        text = f"{title}\n\n"
        text += f"<b>Ariza #{order['id']}</b>\n"
        text += f"📝 Turi: {order_type_text}\n"
        text += f"📍 Hudud: {get_region_name_by_id(order.get('region', '-'))}\n"
        text += f"🏠 Manzil: {order.get('address','-')}\n"
        if order.get('abonent_id'):
            text += f"🆔 Abonent ID: {order['abonent_id']}\n"
        if order.get('description'):
            text += f"📄 Tavsif: {order['description']}\n"
        text += f"📅 Yaratildi: {_fmt_dt(order.get('created_at'))}\n"
        text += f"\n🗂️ <i>Ariza {idx + 1} / {len(orders)}</i>"

    # Create navigation keyboard
    keyboard = []
    nav_buttons = []
    
    if idx > 0:
        prev_text = "⬅️ Oldingi" if user_lang == "uz" else "⬅️ Предыдущая"
        nav_buttons.append(InlineKeyboardButton(text=prev_text, callback_data=f"client_orders_prev_{idx}"))
    
    if idx < len(orders) - 1:
        next_text = "Keyingi ➡️" if user_lang == "uz" else "Следующая ➡️"
        nav_buttons.append(InlineKeyboardButton(text=next_text, callback_data=f"client_orders_next_{idx}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)

    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard) if keyboard else None
    
    # Handle both Message and CallbackQuery
    if isinstance(target, CallbackQuery):
        # It's a CallbackQuery - use message.edit_text
        await target.message.edit_text(text, parse_mode="HTML", reply_markup=reply_markup)
    else:
        # It's a Message - use answer
        await target.answer(text, parse_mode="HTML", reply_markup=reply_markup)

@router.callback_query(F.data.startswith("client_orders_prev_"))
async def prev_order_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    orders = data.get("orders", [])
    idx = int(callback.data.replace("client_orders_prev_", "")) - 1
    
    if idx < 0 or idx >= len(orders):
        return
    
    await state.update_data(idx=idx)
    user_lang = data.get("lang", "uz")
    await render_order_card(callback, orders, idx, user_lang)

@router.callback_query(F.data.startswith("client_orders_next_"))
async def next_order_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    orders = data.get("orders", [])
    idx = int(callback.data.replace("client_orders_next_", "")) + 1
    
    if idx < 0 or idx >= len(orders):
        return
    
    await state.update_data(idx=idx)
    user_lang = data.get("lang", "uz")
    await render_order_card(callback, orders, idx, user_lang)




@router.message(F.text.in_(["✏️ Ismni o'zgartirish", "✏️ Изменить имя"]))
async def edit_name_handler(message: Message, state: FSMContext):
    user_lang = await get_user_language(message.from_user.id)
    telegram_id = message.from_user.id
    
    # Get current user information
    user_info = await find_user_by_telegram_id(telegram_id)
    
    if not user_info:
        error_text = (
            "❌ Пользователь не найден в базе данных."
            if user_lang == "ru" else
            "❌ Foydalanuvchi ma'lumotlar bazasida topilmadi."
        )
        await message.answer(error_text, parse_mode="HTML")
        return
    
    current_name = user_info.get('full_name', 'Ko\'rsatilmagan')
    
    if user_lang == "ru":
        text = f"✏️ <b>Изменить имя</b>\n\n"
        text += f"👤 Текущее имя: <b>{current_name}</b>\n\n"
        text += "📝 Введите новое имя (минимум 3 символа):"
    else:
        text = f"✏️ <b>Ismni o'zgartirish</b>\n\n"
        text += f"👤 Hozirgi ism: <b>{current_name}</b>\n\n"
        text += "📝 Yangi ismingizni kiriting (kamida 3 ta belgi):"
    
    await state.set_state(ProfileEditStates.waiting_for_new_name)
    await message.answer(text, parse_mode="HTML")

@router.message(ProfileEditStates.waiting_for_new_name)
async def process_new_name(message: Message, state: FSMContext):
    """Process user's new name input."""
    user_lang = await get_user_language(message.from_user.id)
    new_name = message.text.strip()
    
    # Basic validation
    if len(new_name) < 3:
        error_text = (
            "❌ Имя должно содержать минимум 3 символа. Попробуйте еще раз:"
            if user_lang == "ru" else
            "❌ Ism kamida 3 ta belgidan iborat bo'lishi kerak. Qaytadan urinib ko'ring:"
        )
        await message.answer(error_text, parse_mode="HTML")
        return
    
    # Update name in database
    try:
        await update_user_full_name(message.from_user.id, new_name)
        await state.clear()
        
        success_text = (
            f"✅ <b>Имя успешно изменено!</b>\n\n👤 Новое имя: <b>{new_name}</b>"
            if user_lang == "ru" else
            f"✅ <b>Ism muvaffaqiyatli o'zgartirildi!</b>\n\n👤 Yangi ism: <b>{new_name}</b>"
        )
        await message.answer(success_text, parse_mode="HTML", reply_markup=get_client_profile_reply_keyboard(user_lang))
        
    except Exception as e:
        error_text = (
            "❌ Ошибка при сохранении имени. Попробуйте позже."
            if user_lang == "ru" else
            "❌ Ismni saqlashda xatolik yuz berdi. Keyinroq urinib ko'ring."
        )
        await message.answer(error_text, parse_mode="HTML")
        await state.clear()

@router.message(F.text.in_(["◀️ Orqaga", "◀️ Назад"]))
async def back_to_main_menu_handler(message: Message):
    user_lang = await get_user_language(message.from_user.id)
    
    if user_lang == "ru":
        text = "🏠 Добро пожаловать в главное меню!"
    else:
        text = "🏠 Bosh menyuga xush kelibsiz!"
    
    await message.answer(
        text,
        reply_markup=get_client_main_menu(user_lang)
    )