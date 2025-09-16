from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime

from database.admin_system_status_queries import (
    get_system_overview,
    get_orders_by_status,
    get_recent_activity,
    get_performance_metrics,
    get_database_info
)
from keyboards.admin_buttons import get_system_status_keyboard

router = Router()

@router.message(F.text.in_(["🔧 Tizim holati", "🔧 Состояние системы"]))
async def status_handler(message: Message, state: FSMContext = None):
    """Tizim holati asosiy menyusi"""
    if state:
        await state.clear()
    
    lang = "uz"  # Default til, kerak bo'lsa user tilini olish mumkin
    
    text = "🔧 **Tizim holati boshqaruvi**\n\n"
    text += "Quyidagi bo'limlardan birini tanlang:" if lang == "uz" else "Выберите один из следующих разделов:"
    
    await message.answer(
        text,
        reply_markup=get_system_status_keyboard(lang),
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "system_overview")
async def system_overview_handler(callback: CallbackQuery):
    """Tizimning umumiy ko'rinishi"""
    await callback.answer()
    
    try:
        stats = await get_system_overview()
        
        text = "📊 **Tizimning umumiy ko'rinishi**\n\n"
        
        # Foydalanuvchilar statistikasi
        text += f"👥 **Foydalanuvchilar:**\n"
        text += f"• Jami: {stats['total_users']}\n"
        text += f"• Faol: {stats['active_users']}\n"
        text += f"• Bloklangan: {stats['blocked_users']}\n\n"
        
        # Rollar bo'yicha
        text += f"👤 **Rollar bo'yicha:**\n"
        for role, count in stats['users_by_role'].items():
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
            }.get(role, role)
            text += f"• {role_name}: {count}\n"
        
        text += f"\n📝 **Zayavkalar:**\n"
        text += f"• Ulanish: {stats['total_connection_orders']}\n"
        text += f"• Texnik: {stats['total_technician_orders']}\n"
        text += f"• Xodim: {stats['total_saff_orders']}\n\n"
        
        text += f"📅 **Bugungi zayavkalar:**\n"
        text += f"• Ulanish: {stats['today_connection_orders']}\n"
        text += f"• Texnik: {stats['today_technician_orders']}\n\n"
        
        text += f"🕐 Yangilangan: {datetime.now().strftime('%H:%M:%S')}"
        
        await callback.message.edit_text(
            text,
            reply_markup=get_system_status_keyboard(),
            parse_mode="Markdown"
        )
        
    except Exception as e:
        await callback.message.edit_text(
            f"❌ Xatolik yuz berdi: {str(e)}",
            reply_markup=get_system_status_keyboard()
        )

@router.callback_query(F.data == "system_close")
async def system_close_handler(callback: CallbackQuery):
    """Tizim holati menyusini yopish"""
    await callback.answer()
    
    try:
        # Xabarni o'chirish
        await callback.message.delete()
        
    except Exception as e:
        # Agar o'chirib bo'lmasa, oddiy xabar bilan almashtirish
        await callback.message.edit_text(
            "✅ Tizim holati menyusi yopildi.",
            reply_markup=None
        )

@router.callback_query(F.data == "system_orders")
async def system_orders_handler(callback: CallbackQuery):
    """Zayavkalar holati"""
    await callback.answer()
    
    try:
        orders_data = await get_orders_by_status()
        
        text = "📝 **Zayavkalar holati**\n\n"
        
        # Ulanish zayavkalari
        text += "🔗 **Ulanish zayavkalari:**\n"
        for status, count in orders_data['connection_orders'].items():
            status_name = {
                'new': 'Yangi',
                'in_manager': 'Menejerda',
                'in_junior_manager': 'Kichik Menejerda',
                'in_controller': 'Nazoratchida',
                'in_technician': 'Texnikda',
                'in_technician_work': 'Texnik ishda',
                'completed': 'Bajarilgan'
            }.get(status, status)
            text += f"• {status_name}: {count}\n"
        
        text += "\n🔧 **Texnik zayavkalar:**\n"
        for status, count in orders_data['technician_orders'].items():
            status_name = {
                'new': 'Yangi',
                'in_controller': 'Nazoratchida',
                'in_technician': 'Texnikda',
                'in_technician_work': 'Texnik ishda',
                'completed': 'Bajarilgan'
            }.get(status, status)
            text += f"• {status_name}: {count}\n"
        
        text += "\n👥 **Xodim zayavkalari:**\n"
        for status, count in orders_data['saff_orders'].items():
            status_name = {
                'new': 'Yangi',
                'in_manager': 'Menejerda',
                'in_junior_manager': 'Kichik Menejerda',
                'in_controller': 'Nazoratchida',
                'completed': 'Bajarilgan'
            }.get(status, status)
            text += f"• {status_name}: {count}\n"
        
        text += f"\n🕐 Yangilangan: {datetime.now().strftime('%H:%M:%S')}"
        
        await callback.message.edit_text(
            text,
            reply_markup=get_system_status_keyboard(),
            parse_mode="Markdown"
        )
        
    except Exception as e:
        await callback.message.edit_text(
            f"❌ Xatolik yuz berdi: {str(e)}",
            reply_markup=get_system_status_keyboard()
        )

@router.callback_query(F.data == "system_performance")
async def system_performance_handler(callback: CallbackQuery):
    """Ishlash ko'rsatkichlari"""
    await callback.answer()
    
    try:
        metrics = await get_performance_metrics()
        
        text = "⚡ **Ishlash ko'rsatkichlari**\n\n"
        
        text += f"📈 **Bajarilish foizi:**\n"
        text += f"• Ulanish zayavkalari: {metrics['connection_completion_rate']:.1f}%\n"
        text += f"• Texnik zayavkalar: {metrics['technician_completion_rate']:.1f}%\n\n"
        
        text += f"⏱ **O'rtacha bajarilish vaqti:**\n"
        text += f"• {metrics['avg_completion_hours']:.1f} soat\n\n"
        
        text += f"🏆 **Eng faol xodimlar:**\n"
        for staff in metrics['active_staff'][:5]:
            text += f"• {staff['full_name']} ({staff['role']}): {staff['activity_count']} faoliyat\n"
        
        text += f"\n🕐 Yangilangan: {datetime.now().strftime('%H:%M:%S')}"
        
        await callback.message.edit_text(
            text,
            reply_markup=get_system_status_keyboard(),
            parse_mode="Markdown"
        )
        
    except Exception as e:
        await callback.message.edit_text(
            f"❌ Xatolik yuz berdi: {str(e)}",
            reply_markup=get_system_status_keyboard()
        )

@router.callback_query(F.data == "system_activity")
async def system_activity_handler(callback: CallbackQuery):
    """So'nggi faoliyat"""
    await callback.answer()
    
    try:
        activities = await get_recent_activity()
        
        text = "🔄 **So'nggi 10ta faoliyat**\n\n"
        
        if not activities:
            text += "Hech qanday faoliyat topilmadi."
        else:
            for activity in activities[:10]:
                activity_type = {
                    'connection_order': '🔗 Ulanish',
                    'technician_order': '🔧 Texnik',
                    'saff_order': '👥 Xodim'
                }.get(activity['type'], activity['type'])
                
                status_name = {
                    'new': 'Yangi',
                    'in_manager': 'Menejerda',
                    'in_junior_manager': 'Kichik Menejerda', 
                    'in_controller': 'Nazoratchida',
                    'in_technician': 'Texnikda',
                    'in_technician_work': 'Texnik ishda',
                    'in_diagnostics': 'Diagnostikada',
                    'in_repairs': 'Ta\'mirda',
                    'in_warehouse': 'Omborda',
                    'completed': 'Bajarilgan',
                    'betweencontrollertechnician': 'Nazoratchi → Texnik',
                    'between_controller_technician': 'Nazoratchi → Texnik',
                    'pending': 'Kutilmoqda',
                    'assigned': 'Tayinlangan',
                    'cancelled': 'Bekor qilingan'
                }.get(activity['status'], activity['status'])
                
                time_str = activity['updated_at'].strftime('%H:%M')
                text += f"• {activity_type} #{activity['id']} - {status_name} ({time_str})\n"
        
        text += f"\n🕐 Yangilangan: {datetime.now().strftime('%H:%M:%S')}"
        
        await callback.message.edit_text(
            text,
            reply_markup=get_system_status_keyboard(),
            parse_mode="Markdown"
        )
        
    except Exception as e:
        await callback.message.edit_text(
            f"❌ Xatolik yuz berdi: {str(e)}",
            reply_markup=get_system_status_keyboard()
        )

@router.callback_query(F.data == "system_database")
async def system_database_handler(callback: CallbackQuery):
    """Ma'lumotlar bazasi haqida ma'lumot"""
    await callback.answer()
    
    try:
        db_info = await get_database_info()
        
        text = "💾 **Ma'lumotlar bazasi**\n\n"
        
        text += f"📊 **Umumiy hajm:** {db_info['database_size']}\n"
        text += f"🔗 **Faol ulanishlar:** {db_info['active_connections']}\n\n"
        
        text += f"📋 **Jadvallar hajmi:**\n"
        for table in db_info['table_sizes'][:8]:
            text += f"• {table['tablename']}: {table['size']}\n"
        
        text += f"\n🕐 Yangilangan: {datetime.now().strftime('%H:%M:%S')}"
        
        await callback.message.edit_text(
            text,
            reply_markup=get_system_status_keyboard(),
            parse_mode="Markdown"
        )
        
    except Exception as e:
        await callback.message.edit_text(
            f"❌ Xatolik yuz berdi: {str(e)}",
            reply_markup=get_system_status_keyboard()
        )

@router.callback_query(F.data == "system_refresh")
async def system_refresh_handler(callback: CallbackQuery):
    """Tizim holatini yangilash"""
    await callback.answer("🔄 Yangilanmoqda...")
    
    try:
        # Yangilangan asosiy menyu matnini yaratish
        lang = "uz"  # Default til
        
        text = f"🔧 **Tizim holati boshqaruvi**\n\n"
        text += f"Quyidagi bo'limlardan birini tanlang:\n\n"
        text += f"📊 **Umumiy ko'rinish** - Tizim statistikasi\n"
        text += f"📋 **Zayavkalar holati** - Barcha zayavkalar\n"
        text += f"⚡ **Ishlash ko'rsatkichlari** - Tizim samaradorligi\n"
        text += f"🔄 **So'nggi faoliyat** - Oxirgi 10tasi\n"
        text += f"💾 **Ma'lumotlar bazasi** - DB holati\n\n"
        text += f"🕐 Yangilangan: {datetime.now().strftime('%H:%M:%S')}"
        
        # Xabarni edit qilish
        await callback.message.edit_text(
            text,
            reply_markup=get_system_status_keyboard(lang),
            parse_mode="Markdown"
        )
        
    except Exception as e:
        await callback.message.edit_text(
            f"❌ Xatolik yuz berdi: {str(e)}",
            reply_markup=get_system_status_keyboard()
        )
