from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from typing import Optional

from database.queries import (
    find_user_by_telegram_id,
    find_user_by_phone,
    update_user_role
)
from keyboards.admin_buttons import (
    get_user_management_keyboard,
    get_inline_role_selection,
    get_inline_search_method,
    get_admin_main_menu
)

router = Router()

class UserRoleChange(StatesGroup):
    waiting_for_search_method = State()
    waiting_for_telegram_id = State()
    waiting_for_phone = State()
    waiting_for_new_role = State()


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
        "👥 Foydalanuvchilar boshqaruvi\n\nBu yerda barcha foydalanuvchilar ro'yxati ko'rsatiladi.\n\n👤 Rol: Admin",
        reply_markup=get_user_management_keyboard()
    )


@router.message(F.text.in_(["👥 Barcha foydalanuvchilar", "👥 Все пользователи"]))
async def all_users_handler(message: Message):
    await message.answer("👥 Barcha foydalanuvchilar ro'yxati\n\nBu yerda barcha foydalanuvchilar ko'rsatiladi.\n\n👤 Rol: Admin")


@router.message(F.text.in_(["👤 Xodimlar", "👤 Сотрудники"]))
async def staff_handler(message: Message):
    await message.answer("👤 Xodimlar ro'yxati\n\nBu yerda xodimlar ro'yxati ko'rsatiladi.\n\n👤 Rol: Admin")


@router.message(F.text.in_(["🔒 Bloklash/Blokdan chiqarish", "🔒 Блокировка/Разблокировка"]))
async def block_user_handler(message: Message):
    await message.answer("🔒 Foydalanuvchini bloklash/blokdan chiqarish\n\nBu yerda foydalanuvchi bloklanadi yoki blokdan chiqariladi.\n\n👤 Rol: Admin")


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
    
    if not phone.startswith('998') or not phone[1:].isdigit() or len(phone) != 12:
        await message.answer("❌ Xato! Telefon raqami 998XXXXXXXXX formatida bo'lishi kerak.")
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


@router.message(F.text.in_(["◀️ Orqaga", "◀️ Назад"]))
async def back_to_main_handler(message: Message):
    await message.answer(
        "⬅️ Asosiy menyuga qaytdingiz\n\n👤 Rol: Admin",
        reply_markup=None
    )
    await message.answer(
        "Bosh menyu", 
        reply_markup=get_admin_main_menu()
    )
