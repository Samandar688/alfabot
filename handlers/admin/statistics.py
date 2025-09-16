from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from filters.role_filter import RoleFilter
from keyboards.admin_buttons import get_statistics_keyboard
from database.admin_queries import get_user_statistics
from database.admin_system_status_queries import get_system_overview
from database.manager_export import get_manager_statistics_for_export
from database.controller_export import get_controller_statistics_for_export

router = Router()
router.message.filter(RoleFilter("admin"))
router.callback_query.filter(RoleFilter("admin"))

@router.message(F.text.in_(["📊 Statistika", "📊 Татистика"]))
async def statistics_handler(message: Message):
    """Admin statistika bo'limi - asosiy menyu"""
    text = "📊 **Admin Statistika Bo'limi**\n\n"
    text += "Quyidagi bo'limlardan birini tanlang:"
    
    await message.answer(
        text,
        reply_markup=get_statistics_keyboard(),
        parse_mode="Markdown"
    )

# Umumiy ko'rinish
@router.callback_query(F.data == "stats_overview")
async def stats_overview_handler(callback: CallbackQuery):
    """Umumiy statistika ko'rinishi"""
    await callback.answer()
    
    try:
        # Tizim umumiy ma'lumotlari
        system_stats = await get_system_overview()
        
        text = "📈 **Umumiy Ko'rinish**\n\n"
        
        # Foydalanuvchilar
        text += f"👥 **Foydalanuvchilar:**\n"
        text += f"• Jami: {system_stats['total_users']}\n"
        text += f"• Faol: {system_stats['active_users']}\n"
        text += f"• Bloklangan: {system_stats['blocked_users']}\n\n"
        
        # Buyurtmalar
        text += f"📋 **Buyurtmalar:**\n"
        text += f"• Ulanish: {system_stats['total_connection_orders']}\n"
        text += f"• Texnik: {system_stats['total_technician_orders']}\n"
        text += f"• Saff: {system_stats['total_saff_orders']}\n\n"
        
        # Bugungi buyurtmalar
        text += f"📅 **Bugungi buyurtmalar:**\n"
        text += f"• Ulanish: {system_stats['today_connection_orders']}\n"
        text += f"• Texnik: {system_stats['today_technician_orders']}\n"
        
        await callback.message.edit_text(
            text,
            reply_markup=get_statistics_keyboard(),
            parse_mode="Markdown"
        )
    except Exception as e:
        await callback.message.edit_text(
            "❌ Statistika ma'lumotlarini yuklashda xatolik yuz berdi.",
            reply_markup=get_statistics_keyboard()
        )

# Foydalanuvchilar statistikasi
@router.callback_query(F.data == "stats_users")
async def stats_users_handler(callback: CallbackQuery):
    """Foydalanuvchilar statistikasi"""
    await callback.answer()
    
    try:
        user_stats = await get_user_statistics()
        
        text = "👥 **Foydalanuvchilar Statistikasi**\n\n"
        text += f"📊 **Umumiy ma'lumotlar:**\n"
        text += f"• Jami foydalanuvchilar: {user_stats['total_users']}\n"
        text += f"• Faol foydalanuvchilar: {user_stats['active_users']}\n"
        text += f"• Bloklangan: {user_stats['blocked_users']}\n\n"
        
        text += f"👤 **Rollar bo'yicha:**\n"
        for role_stat in user_stats['role_statistics']:
            role_name = {
                'admin': 'Admin',
                'client': 'Mijoz',
                'manager': 'Menejer',
                'junior_manager': 'Kichik menejer',
                'controller': 'Nazoratchi',
                'technician': 'Texnik',
                'warehouse': 'Ombor',
                'callcenter_supervisor': 'Call center supervisor',
                'callcenter_operator': 'Call center operator'
            }.get(role_stat['role'], role_stat['role'])
            text += f"• {role_name}: {role_stat['count']}\n"
        
        await callback.message.edit_text(
            text,
            reply_markup=get_statistics_keyboard(),
            parse_mode="Markdown"
        )
    except Exception as e:
        await callback.message.edit_text(
            "❌ Foydalanuvchilar statistikasini yuklashda xatolik yuz berdi.",
            reply_markup=get_statistics_keyboard()
        )

# Ulanish buyurtmalari statistikasi
@router.callback_query(F.data == "stats_connection_orders")
async def stats_connection_orders_handler(callback: CallbackQuery):
    """Ulanish buyurtmalari statistikasi"""
    await callback.answer()
    
    try:
        manager_stats = await get_manager_statistics_for_export()
        
        text = "📋 **Ulanish Buyurtmalari Statistikasi**\n\n"
        
        if manager_stats and 'summary' in manager_stats:
            summary = manager_stats['summary']
            text += f"📊 **Umumiy ma'lumotlar:**\n"
            text += f"• Jami buyurtmalar: {summary['total_orders']}\n"
            text += f"• Yangi: {summary['new_orders']}\n"
            text += f"• Jarayonda: {summary['in_progress_orders']}\n"
            text += f"• Yakunlangan: {summary['completed_orders']}\n"
            text += f"• Yakunlanish foizi: {summary['completion_rate']}%\n"
            text += f"• Yagona mijozlar: {summary['unique_clients']}\n"
            text += f"• Tarif rejalari: {summary['unique_tariffs_used']}\n"
        else:
            text += "📊 Hozircha buyurtmalar mavjud emas."
        
        await callback.message.edit_text(
            text,
            reply_markup=get_statistics_keyboard(),
            parse_mode="Markdown"
        )
    except Exception as e:
        await callback.message.edit_text(
            "❌ Ulanish buyurtmalari statistikasini yuklashda xatolik yuz berdi.",
            reply_markup=get_statistics_keyboard()
        )

# Texnik buyurtmalar statistikasi
@router.callback_query(F.data == "stats_tech_orders")
async def stats_tech_orders_handler(callback: CallbackQuery):
    """Texnik buyurtmalar statistikasi"""
    await callback.answer()
    
    try:
        controller_stats = await get_controller_statistics_for_export()
        
        text = "🔧 **Texnik Buyurtmalar Statistikasi**\n\n"
        
        if controller_stats and 'summary' in controller_stats:
            summary = controller_stats['summary']
            text += f"📊 **Umumiy ma'lumotlar:**\n"
            text += f"• Jami arizalar: {summary['total_requests']}\n"
            text += f"• Yangi: {summary['new_requests']}\n"
            text += f"• Jarayonda: {summary['in_progress_requests']}\n"
            text += f"• Yakunlangan: {summary['completed_requests']}\n"
            text += f"• Yakunlanish foizi: {summary['completion_rate']}%\n"
            text += f"• Yagona mijozlar: {summary['unique_clients']}\n"
            text += f"• Muammo turlari: {summary['unique_problem_types']}\n"
        else:
            text += "📊 Hozircha texnik arizalar mavjud emas."
        
        await callback.message.edit_text(
            text,
            reply_markup=get_statistics_keyboard(),
            parse_mode="Markdown"
        )
    except Exception as e:
        await callback.message.edit_text(
            "❌ Texnik buyurtmalar statistikasini yuklashda xatolik yuz berdi.",
            reply_markup=get_statistics_keyboard()
        )

# Rollar bo'yicha statistika
@router.callback_query(F.data == "stats_by_roles")
async def stats_by_roles_handler(callback: CallbackQuery):
    """Rollar bo'yicha batafsil statistika"""
    await callback.answer()
    
    try:
        system_stats = await get_system_overview()
        
        text = "👤 **Rollar Bo'yicha Batafsil Statistika**\n\n"
        
        if 'users_by_role' in system_stats:
            for role, count in system_stats['users_by_role'].items():
                role_name = {
                    'admin': '👑 Admin',
                    'client': '👤 Mijoz',
                    'manager': '👨‍💼 Menejer',
                    'junior_manager': '👨‍💻 Kichik menejer',
                    'controller': '🔍 Nazoratchi',
                    'technician': '🔧 Texnik',
                    'warehouse': '📦 Ombor',
                    'callcenter_supervisor': '📞 Call center supervisor',
                    'callcenter_operator': '☎️ Call center operator'
                }.get(role, f"❓ {role}")
                text += f"{role_name}: **{count}**\n"
        else:
            text += "📊 Rol statistikasi mavjud emas."
        
        await callback.message.edit_text(
            text,
            reply_markup=get_statistics_keyboard(),
            parse_mode="Markdown"
        )
    except Exception as e:
        await callback.message.edit_text(
            "❌ Rollar statistikasini yuklashda xatolik yuz berdi.",
            reply_markup=get_statistics_keyboard()
        )

# Oylik statistika
@router.callback_query(F.data == "stats_monthly")
async def stats_monthly_handler(callback: CallbackQuery):
    """Oylik statistika tendensiyalari"""
    await callback.answer()
    
    try:
        manager_stats = await get_manager_statistics_for_export()
        controller_stats = await get_controller_statistics_for_export()
        
        text = "📊 **Oylik Statistika (Oxirgi 6 oy)**\n\n"
        
        # Ulanish buyurtmalari oylik
        if manager_stats and 'monthly_trends' in manager_stats and manager_stats['monthly_trends']:
            text += "📋 **Ulanish buyurtmalari:**\n"
            for month_data in manager_stats['monthly_trends'][:3]:  # Faqat oxirgi 3 oy
                text += f"• {month_data['month']}: {month_data['total_orders']} (✅ {month_data['completed_orders']})\n"
            text += "\n"
        
        # Texnik buyurtmalar oylik
        if controller_stats and 'monthly_trends' in controller_stats and controller_stats['monthly_trends']:
            text += "🔧 **Texnik buyurtmalar:**\n"
            for month_data in controller_stats['monthly_trends'][:3]:  # Faqat oxirgi 3 oy
                text += f"• {month_data['month']}: {month_data['total_requests']} (✅ {month_data['completed_requests']})\n"
        
        if not (manager_stats.get('monthly_trends') or controller_stats.get('monthly_trends')):
            text += "📊 Oylik statistika ma'lumotlari mavjud emas."
        
        await callback.message.edit_text(
            text,
            reply_markup=get_statistics_keyboard(),
            parse_mode="Markdown"
        )
    except Exception as e:
        await callback.message.edit_text(
            "❌ Oylik statistikani yuklashda xatolik yuz berdi.",
            reply_markup=get_statistics_keyboard()
        )

# Close statistics menu
@router.callback_query(F.data == "stats_close")
async def close_statistics_handler(callback: CallbackQuery):
    """Close statistics menu and return to main menu"""
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(
        "Statistika bo'limi yopildi",
    )
