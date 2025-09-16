from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
import asyncpg
import re
from config import settings
from typing import Optional
from filters.role_filter import RoleFilter
from database.queries import (
    find_user_by_telegram_id,
    find_user_by_phone,
    update_user_role
)
from database.admin_queries import (
    get_all_users_paginated,
    get_users_by_role_paginated,
    search_users_paginated,
    get_user_statistics,
    toggle_user_block_status
)
from datetime import datetime
from keyboards.admin_buttons import (
    get_user_management_keyboard,
    get_inline_role_selection,
    get_inline_search_method,
    get_admin_main_menu
)

router = Router()
router.message.filter(RoleFilter("admin")) 
class UserRoleChange(StatesGroup):
    waiting_for_search_method = State()
    waiting_for_telegram_id = State()
    waiting_for_phone = State()
    waiting_for_new_role = State()

class UsersPagination(StatesGroup):
    viewing_all_users = State()
    viewing_staff_users = State()

class UserBlockManagement(StatesGroup):
    waiting_for_user_search = State()


ROLE_MAPPING = {
    'role_admin': 'admin',
    'role_client': 'client',
    'role_manager': 'manager',
    'role_junior_manager': 'junior_manager',
    'role_controller': 'controller',
    'role_technician': 'technician',
    'role_warehouse': 'warehouse',
    'role_callcenter_operator': 'callcenter_operator',
    'role_callcenter_supervisor': 'callcenter_supervisor'
}

@router.message(F.text.in_(["👥 Foydalanuvchilar", "👥 Пользователи"]))
async def users_handler(message: Message):
    await message.answer(
        "👥 Foydalanuvchilar boshqaruvi",
        reply_markup=get_user_management_keyboard()
    )


@router.message(F.text.in_(["👥 Barcha foydalanuvchilar", "👥 Все пользователи"]))
async def all_users_handler(message: Message, state: FSMContext):
    """Faqat client foydalanuvchilarni ko'rsatish (paginatsiya bilan)"""
    await state.set_state(UsersPagination.viewing_all_users)
    await show_users_page(message, state, page=1, user_type="client")


@router.message(F.text.in_(["👤 Xodimlar", "👤 Сотрудники"]))
async def staff_handler(message: Message, state: FSMContext):
    """Xodimlarni ko'rsatish (client bo'lmagan foydalanuvchilar)"""
    await state.set_state(UsersPagination.viewing_staff_users)
    await show_users_page(message, state, page=1, user_type="staff")


@router.message(F.text.in_(["🔒 Bloklash/Blokdan chiqarish", "🔒 Блокировка/Разблокировка"]))
async def block_user_handler(message: Message, state: FSMContext):
    await state.set_state(UserBlockManagement.waiting_for_user_search)
    await message.answer(
        "🔒 <b>Foydalanuvchini bloklash/blokdan chiqarish</b>\n\n"
        "Quyidagi usullardan birini tanlang:\n\n"
        "📱 <b>Telefon raqam</b> - masalan: +998901234567\n"
        "🆔 <b>Telegram ID</b> - masalan: 123456789\n"
        "👤 <b>Username</b> - masalan: @username\n\n"
        "❌ Bekor qilish uchun /cancel yozing",
        parse_mode='HTML'
    )


@router.message(UserBlockManagement.waiting_for_user_search)
async def process_user_search_for_block(message: Message, state: FSMContext):
    search_text = message.text.strip()
    
    if search_text.lower() in ['/cancel', 'bekor qilish', 'cancel']:
        await state.clear()
        await message.answer("❌ Bloklash jarayoni bekor qilindi.", parse_mode='HTML')
        return
    
    user = None
    
    # Telegram ID bo'yicha qidirish (faqat raqamlar)
    if search_text.isdigit() and not search_text.startswith('+'):
        telegram_id = int(search_text)
        user = await find_user_by_telegram_id(telegram_id)
    
    # Telefon raqam bo'yicha qidirish
    elif search_text.startswith('+') or (search_text.replace(' ', '').isdigit() and len(search_text.replace(' ', '')) >= 9):
        clean_phone = search_text.replace(' ', '').replace('-', '')
        user = await find_user_by_phone(clean_phone)
    
    # Username bo'yicha qidirish
    elif search_text.startswith('@'):
        username = search_text[1:]  # @ belgisini olib tashlash
        conn = await asyncpg.connect(settings.DB_URL)
        try:
            user_data = await conn.fetchrow(
                "SELECT * FROM users WHERE username = $1", username
            )
            if user_data:
                user = dict(user_data)
        finally:
            await conn.close()
    
    if not user:
        await message.answer(
            "❌ Foydalanuvchi topilmadi!\n\n"
            "Iltimos, to'g'ri ma'lumot kiriting:\n"
            "📱 Telefon: +998901234567\n"
            "🆔 Telegram ID: 123456789\n"
            "👤 Username: @username",
            parse_mode='HTML'
        )
        return
    
    # Foydalanuvchi ma'lumotlarini ko'rsatish va bloklash/blokdan chiqarish
    block_status = "🔴 Bloklangan" if user.get('is_blocked') else "🟢 Faol"
    action_text = "blokdan chiqarish" if user.get('is_blocked') else "bloklash"
    action_emoji = "🔓" if user.get('is_blocked') else "🔒"
    
    user_info = f"👤 <b>Topilgan foydalanuvchi:</b>\n\n"
    user_info += f"📝 <b>Ism:</b> {user.get('full_name', 'Noma\'lum')}\n"
    user_info += f"🆔 <b>Telegram ID:</b> <code>{user.get('telegram_id')}</code>\n"
    user_info += f"📱 <b>Telefon:</b> {user.get('phone', 'Noma\'lum')}\n"
    if user.get('username'):
        user_info += f"👤 <b>Username:</b> @{user.get('username')}\n"
    user_info += f"🎭 <b>Rol:</b> {user.get('role', 'client')}\n"
    user_info += f"📊 <b>Holat:</b> {block_status}\n\n"
    
    # Bloklash/blokdan chiqarish
    success = await toggle_user_block_status(user['telegram_id'])
    
    if success:
        new_status = "🔴 Bloklangan" if not user.get('is_blocked') else "🟢 Faol"
        user_info += f"✅ <b>Muvaffaqiyatli {action_text} qilindi!</b>\n"
        user_info += f"📊 <b>Yangi holat:</b> {new_status}"
    else:
        user_info += f"❌ <b>Xatolik yuz berdi!</b>\n"
        user_info += f"Foydalanuvchini {action_text} qilib bo'lmadi."
    
    await state.clear()
    await message.answer(user_info, parse_mode='HTML')

@router.message(F.text == "🔄 Rolni o'zgartirish")
async def change_user_role(message: Message, state: FSMContext):
    """Start the role change process by asking for search method"""
    await message.answer(
        "Foydalanuvchini qanday qidirmoqchisiz?",
        reply_markup=get_inline_search_method()
    )
    await state.set_state(UserRoleChange.waiting_for_search_method)


@router.callback_query(F.data.startswith('search_'))
async def process_search_method(callback: CallbackQuery, state: FSMContext):
    search_type = callback.data

    if search_type == 'search_telegram_id':
        await callback.message.edit_text(
            "Foydalanuvchining Telegram ID raqamini yuboring:",
            reply_markup=None
        )
        await state.set_state(UserRoleChange.waiting_for_telegram_id)

    elif search_type == 'search_phone':
        await callback.message.edit_text(
            "Foydalanuvchining telefon raqamini yuboring (998XXXXXXXXX formatida):",
            reply_markup=None
        )
        await state.set_state(UserRoleChange.waiting_for_phone)

    else:
        await state.clear()
        await callback.message.edit_text(
            "❌ Rol o'zgartirish bekor qilindi.",
            reply_markup=None
        )
        await callback.message.answer(
            "Foydalanuvchilar paneli",
            reply_markup=get_user_management_keyboard()
        )

    await callback.answer()



@router.message(UserRoleChange.waiting_for_telegram_id)
async def process_telegram_id(message: Message, state: FSMContext):
    telegram_id = message.text.strip()

    if not telegram_id.isdigit():
        await message.answer("❌ Xato! Telegram ID raqami bo'lishi kerak.")
        return

    user = await find_user_by_telegram_id(int(telegram_id))
    await process_user_found(message, state, user)


@router.message(UserRoleChange.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    
    # Telefon raqami formatini tekshirish - turli formatlarni qo'llab-quvvatlash
    phone_pattern = re.compile(r"^\+?998\s?\d{2}\s?\d{3}\s?\d{2}\s?\d{2}$|^\+?998\d{9}$|^998\d{9}$|^\d{9}$")
    
    if not phone_pattern.match(phone):
        await message.answer("❌ Xato! Telefon raqami quyidagi formatlardan birida bo'lishi kerak:\n"
                           "• +998901234567\n"
                           "• 998901234567\n"
                           "• 901234567\n"
                           "• +998 90 123 45 67")
        return
        
    user = await find_user_by_phone(phone)
    await process_user_found(message, state, user)


async def process_user_found(message: Message, state: FSMContext, user):
    if user:
        await state.update_data(telegram_id=user['telegram_id'])
        await state.set_state(UserRoleChange.waiting_for_new_role)
        
        role_display = {
            'admin': '👑 Admin',
            'client': '👤 Mijoz',
            'manager': '👔 Menejer',
            'junior_manager': '👔 Junior Menejer',
            'controller': '👤 Controller',
            'technician': '🔧 Texnik',
            'warehouse': '📦 Ombor',
            'callcenter_operator': '📞 Call Center',
            'callcenter_supervisor': '📞 Call Center Supervisor'
        }.get(user['role'], user['role'])
        
        await message.answer(
            f"✅ Foydalanuvchi topildi!\n\n"
            f"🆔 Telegram ID: {user['telegram_id']}\n"
            f"👤 Foydalanuvchi: {user['full_name'] or user['username'] or 'N/A'}\n"
            f"📱 Telefon: {user['phone'] or 'N/A'}\n"
            f"👤 Hozirgi rol: {role_display}\n\n"
            "Yangi rolni tanlang:",
            reply_markup=get_inline_role_selection()
        )
    else:
        await message.answer("❌ Foydalanuvchi topilmadi. Qaytadan urinib ko'ring.")


@router.callback_query(F.data.startswith('role_'))
async def process_role_selection(callback: CallbackQuery, state: FSMContext):
    """Handle role selection from inline keyboard"""
    role_key = callback.data
    
    if role_key == 'role_cancel':
        await state.clear()
        await callback.message.edit_text(
            "❌ Rol o'zgartirish bekor qilindi.",
            reply_markup=None
        )
        await callback.message.answer(
            "Foydalanuvchilar paneli",
            reply_markup=get_user_management_keyboard()
        )
    else:
        role_value = ROLE_MAPPING.get(role_key)
        if not role_value:
            await callback.answer("❌ Xato! Noto'g'ri rol tanlandi.", show_alert=True)
            return
            
        data = await state.get_data()
        telegram_id = data.get('telegram_id')
        
        if not telegram_id:
            await callback.answer("❌ Xatolik: Foydalanuvchi topilmadi.", show_alert=True)
            return
            
        success = await update_user_role(telegram_id, role_value)
        
        if success:
            role_display = callback.message.reply_markup.inline_keyboard
            role_name = next((btn.text for row in role_display for btn in row if btn.callback_data == role_key), role_value)
            
            await callback.message.edit_text(
                f"✅ Foydalanuvchi roli muvaffaqiyatli o'zgartirildi!\n"
                f"👤 Yangi rol: {role_name}",
                reply_markup=None
            )
            await callback.message.answer(
                "Bosh menyu",
                reply_markup=get_user_management_keyboard()
            )
        else:
            await callback.message.edit_text(
                "❌ Xatolik: Rolni o'zgartirishda xatolik yuz berdi.",
                reply_markup=None
            )
            await callback.message.answer(
                "Bosh menyu",
                reply_markup=get_admin_main_menu()
            )
        
        await state.clear()
    
    await callback.answer()


def format_user_info(user: dict, index: int) -> str:
    """Mijoz ma'lumotlarini muvozanatli formatda tayyorlash
    
    Args:
        user: Foydalanuvchi ma'lumotlari
        index: Tartib raqami
    
    Returns:
        str: Formatlangan mijoz ma'lumotlari
    """
    # Ro'yxatdan o'tgan vaqtni formatlash
    created_at = user.get('created_at')
    if created_at:
        if isinstance(created_at, str):
            try:
                created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                formatted_date = created_date.strftime("%d.%m.%Y")
            except:
                formatted_date = "Noma'lum"
        else:
            formatted_date = created_at.strftime("%d.%m.%Y")
    else:
        formatted_date = "Noma'lum"
    
    # Mijoz ma'lumotlarini muvozanatli formatlash
    user_info = f"👤 <b>{index}.</b> {user.get('full_name', 'Noma\'lum')}\n"
    user_info += f"    🆔 <b>ID:</b> <code>{user.get('telegram_id')}</code>\n"
    user_info += f"    📱 <b>Telefon:</b> {user.get('phone', 'Noma\'lum')}\n"
    
    # Username mavjud bo'lsa
    if user.get('username'):
        user_info += f"    👤 <b>Username:</b> @{user.get('username')}\n"
    
    # Rol ma'lumotini ko'rsatish
    role = user.get('role', 'Noma\'lum')
    role_display = {
        'admin': '👑 Admin',
        'client': '👤 Mijoz',
        'manager': '👨‍💼 Menejer',
        'junior_manager': '👨‍💼 Kichik Menejer',
        'controller': '🎛️ Nazoratchi',
        'technician': '🔧 Texnik',
        'warehouse': '📦 Ombor',
        'callcenter_operator': '📞 Call Center',
        'callcenter_supervisor': '📞 Call Center Boshlig\'i'
    }.get(role, f'🚀 {role.title()}')
    
    user_info += f"    🚀 <b>Rol:</b> {role_display}\n"
    user_info += f"    📅 <b>Sana:</b> {formatted_date}\n\n"
    
    return user_info


async def show_users_page(message: Message, state: FSMContext, page: int = 1, user_type: str = "all"):
    """Foydalanuvchilar sahifasini ko'rsatish"""
    try:
        if user_type == "all":
            data = await get_all_users_paginated(page=page, per_page=5)
            title = "👥 Barcha foydalanuvchilar"
        elif user_type == "staff":
            # Barcha rollarni olish (client dan boshqa)
            staff_roles = ['admin', 'manager', 'junior_manager', 'controller', 'technician', 'warehouse', 'callcenter_operator', 'callcenter_supervisor']
            # Hozircha barcha foydalanuvchilarni olamiz, keyin filtrlash mumkin
            data = await get_all_users_paginated(page=page, per_page=5)
            # Staff foydalanuvchilarni filtrlash
            staff_users = [user for user in data['users'] if user['role'] in staff_roles]
            data['users'] = staff_users
            data['total'] = len(staff_users)
            title = "👤 Xodimlar ro'yxati"
        elif user_type == "client":
            data = await get_users_by_role_paginated(page=page, per_page=5, role="client")
            title = "👤 Mijozlar ro'yxati"
        else:
            await message.answer("❌ Noto'g'ri foydalanuvchi turi!", parse_mode='Markdown')
            return

        if not data['users']:
            await message.answer(f"{title}\n\n📭 Foydalanuvchilar topilmadi.", parse_mode='Markdown')
            return

        # Sarlavha va statistika
        text = f"{title}\n\n"
        text += f"📊 Jami: {data['total']} ta | Sahifa: {data['page']}/{data['total_pages']}\n\n"
        if user_type == "client":
            text += "📋 <b>Mijozlar ro'yxati:</b>\n\n"
        elif user_type == "staff":
            text += "📋 <b>Xodimlar ro'yxati:</b>\n\n"
        else:
            text += "📋 <b>Foydalanuvchilar ro'yxati:</b>\n\n"
        
        # Foydalanuvchilar ro'yxatini formatlash
        for i, user in enumerate(data['users'], 1):
            text += format_user_info(user, i)
        
        # Paginatsiya tugmalari
        from keyboards.admin_buttons import get_users_pagination_keyboard
        keyboard = get_users_pagination_keyboard(
            current_page=data['page'],
            total_pages=data['total_pages'],
            has_prev=data['has_prev'],
            has_next=data['has_next'],
            user_type=user_type
        )
        
        await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
        
    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {str(e)}", parse_mode='Markdown')


@router.callback_query(F.data.startswith('users_page_'))
async def handle_users_pagination(callback: CallbackQuery, state: FSMContext):
    """Foydalanuvchilar paginatsiyasini boshqarish"""
    try:
        # Callback data: users_page_TYPE_PAGE
        parts = callback.data.split('_')
        if len(parts) >= 4:
            user_type = parts[2]  # all, staff yoki client
            page = int(parts[3])
            
            # Eski xabarni o'chirish va yangi xabar yuborish o'rniga
            # Xabar matnini yangilash
            if user_type == "all":
                data = await get_all_users_paginated(page=page, per_page=5)
                title = "👥 Barcha foydalanuvchilar"
            elif user_type == "staff":
                staff_roles = ['admin', 'manager', 'junior_manager', 'controller', 'technician', 'warehouse', 'callcenter_operator', 'callcenter_supervisor']
                data = await get_all_users_paginated(page=page, per_page=5)
                staff_users = [user for user in data['users'] if user['role'] in staff_roles]
                data['users'] = staff_users
                data['total'] = len(staff_users)
                title = "👤 Xodimlar ro'yxati"
            elif user_type == "client":
                data = await get_users_by_role_paginated(page=page, per_page=5, role="client")
                title = "👤 Mijozlar ro'yxati"
            else:
                await callback.answer("❌ Noto'g'ri foydalanuvchi turi!", show_alert=True)
                return

            if not data['users']:
                await callback.message.edit_text(f"{title}\n\n📭 Foydalanuvchilar topilmadi.", parse_mode='Markdown')
                return

            # Sarlavha va statistika
            text = f"{title}\n\n"
            text += f"📊 Jami: {data['total']} ta | Sahifa: {data['page']}/{data['total_pages']}\n\n"
            if user_type == "client":
                text += "📋 **Mijozlar ro'yxati:**\n\n"
            elif user_type == "staff":
                text += "📋 **Xodimlar ro'yxati:**\n\n"
            else:
                text += "📋 **Foydalanuvchilar ro'yxati:**\n\n"
            
            # Foydalanuvchilar ro'yxatini formatlash
            for i, user in enumerate(data['users'], 1):
                text += format_user_info(user, i)
            
            # Paginatsiya tugmalari
            from keyboards.admin_buttons import get_users_pagination_keyboard
            keyboard = get_users_pagination_keyboard(
                current_page=data['page'],
                total_pages=data['total_pages'],
                has_prev=data['has_prev'],
                has_next=data['has_next'],
                user_type=user_type
            )
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
        
    except Exception as e:
        await callback.answer(f"❌ Xatolik: {str(e)}", show_alert=True)
    
    await callback.answer()


@router.callback_query(F.data == 'users_back_to_menu')
async def users_back_to_menu(callback: CallbackQuery, state: FSMContext):
    """Foydalanuvchilar menyusiga qaytish"""
    await state.clear()
    await callback.message.edit_text(
        "Foydalanuvchilar paneli",
        reply_markup=None
    )
    await callback.message.answer(
        "Foydalanuvchilar paneli",
        reply_markup=get_user_management_keyboard()
    )
    await callback.answer()


@router.message(F.text.in_(["◀️ Orqaga", "◀️ Назад"]))
async def back_to_main_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Admin paneli",
        reply_markup=get_admin_main_menu()
    )
