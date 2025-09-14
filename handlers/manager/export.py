from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
from keyboards.manager_buttons import get_manager_export_types_keyboard, get_manager_export_formats_keyboard
from database.manager_export import (
    get_manager_connection_orders_for_export,
    get_manager_statistics_for_export,
    get_manager_employees_for_export,
    get_manager_reports_for_export
)
from utils.export_utils import ExportUtils
from states.manager_states import ManagerExportStates
import logging
from filters.role_filter import RoleFilter
from datetime import datetime

router = Router()
router.message.filter(RoleFilter("manager"))
logger = logging.getLogger(__name__)

@router.message(F.text.in_(["📤 Export", "📤 Экспорт"]))
async def export_handler(message: Message, state: FSMContext):
    """Main export handler - shows export types"""
    try:
        await state.clear()
        keyboard = get_manager_export_types_keyboard()
        await message.answer(
            "📊 <b>Menejerlar uchun hisobotlar</b>\n\n"
            "Quyidagi hisobot turlaridan birini tanlang:",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Export handler error: {e}")
        await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

@router.callback_query(F.data == "manager_export_orders")
async def export_orders_handler(callback: CallbackQuery, state: FSMContext):
    """Handle orders export selection"""
    try:
        await state.update_data(export_type="orders")
        keyboard = get_manager_export_formats_keyboard()
        await callback.message.edit_text(
            "📋 <b>Buyurtmalar ro'yxati</b>\n\n"
            "Export formatini tanlang:",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Export orders handler error: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

@router.callback_query(F.data == "manager_export_statistics")
async def export_statistics_handler(callback: CallbackQuery, state: FSMContext):
    """Handle statistics export selection"""
    try:
        await state.update_data(export_type="statistics")
        keyboard = get_manager_export_formats_keyboard()
        await callback.message.edit_text(
            "📊 <b>Statistika hisoboti</b>\n\n"
            "Export formatini tanlang:",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Export statistics handler error: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

@router.callback_query(F.data == "manager_export_employees")
async def export_employees_handler(callback: CallbackQuery, state: FSMContext):
    """Handle employees export selection"""
    try:
        await state.update_data(export_type="employees")
        keyboard = get_manager_export_formats_keyboard()
        await callback.message.edit_text(
            "👥 <b>Xodimlar ro'yxati</b>\n\n"
            "Export formatini tanlang:",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Export employees handler error: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

@router.callback_query(F.data == "manager_export_reports")
async def export_reports_handler(callback: CallbackQuery, state: FSMContext):
    """Handle reports export selection"""
    try:
        await state.update_data(export_type="reports")
        keyboard = get_manager_export_formats_keyboard()
        await callback.message.edit_text(
            "📈 <b>Hisobotlar</b>\n\n"
            "Export formatini tanlang:",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Export reports handler error: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

@router.callback_query(F.data.startswith("manager_format_"))
async def export_format_handler(callback: CallbackQuery, state: FSMContext):
    """Handle export format selection and generate file"""
    try:
        format_type = callback.data.split("_")[-1]  # csv, xlsx, docx, pdf
        data = await state.get_data()
        export_type = data.get("export_type", "orders")
        
        # Show processing message
        await callback.message.edit_text(
            "⏳ <b>Hisobot tayyorlanmoqda...</b>\n\n"
            "Iltimos, kuting...",
            parse_mode="HTML"
        )
        
        # Get data based on export type
        if export_type == "orders":
            raw_data = await get_manager_connection_orders_for_export()
            title = "Buyurtmalar ro'yxati"
            filename_base = "buyurtmalar"
            headers = ["ID", "Buyurtma raqami", "Mijoz ismi", "Telefon", "Mijoz abonent ID", "Hudud", "Manzil", "Uzunlik", "Kenglik", "Tarif", "Tarif rasmi", "Ulanish sanasi", "Yangilangan sana", "Holati", "Reyting", "Izohlar", "JM izohlar", "Menejer", "Menejer telefon", "Akt raqami", "Akt fayl yo'li", "Akt yaratilgan", "Mijozga yuborilgan", "Akt reytingi", "Akt izohi"]
            
        elif export_type == "statistics":
            stats = await get_manager_statistics_for_export()
            raw_data = []
            title = "Statistika hisoboti"
            filename_base = "statistika"
            
            def add_section(title):
                nonlocal raw_data
                raw_data.append(["", ""])
                raw_data.append([f"🔹 {title.upper()}", ""])
                raw_data.append(["-" * 30, "-" * 30])
            
            def add_row(label, value, indent=0):
                nonlocal raw_data
                prefix = "  " * indent
                raw_data.append([f"{prefix}{label}", str(value) if value is not None else "0"])
            
            # 1. Asosiy statistika
            add_section("Umumiy statistika")
            add_row("📊 Jami buyurtmalar:", stats['summary']['total_orders'])
            add_row("🆕 Yangi arizalar:", stats['summary']['new_orders'])
            add_row("🔄 Jarayondagi arizalar:", stats['summary']['in_progress_orders'])
            add_row("✅ Yakunlangan arizalar:", stats['summary']['completed_orders'])
            add_row("📈 Yakunlangan arizalar foizi:", f"{stats['summary']['completion_rate']}%")
            add_row("👥 Yagona mijozlar:", stats['summary']['unique_clients'])
            add_row("📋 Foydalanilgan tarif rejalari:", stats['summary']['unique_tariffs_used'])
            
            # 2. Menejerlar bo'yicha statistika
            if stats['by_manager']:
                add_section("Menejerlar bo'yicha statistika")
                for i, manager in enumerate(stats['by_manager'], 1):
                    manager_name = f"👤 {i}. {manager['manager_name']}"
                    phone = manager['manager_phone'] or 'Tel. yo\'q'
                    add_row(manager_name, "", 0)
                    add_row("  📞 Telefon:", phone, 1)
                    add_row("  📊 Jami buyurtmalar:", manager['total_orders'], 1)
                    add_row("  ✅ Yakunlangan:", manager['completed_orders'], 1)
                    raw_data.append(["", ""])  # Empty row after each manager
            
            # 3. Oylik statistika
            if stats['monthly_trends']:
                add_section("Oylik statistika (6 oy)")
                for month_data in stats['monthly_trends']:
                    month = month_data['month']
                    add_row(f"🗓️ {month}:", "", 0)
                    add_row("  📊 Jami:", month_data['total_orders'], 1)
                    add_row("  🆕 Yangi:", month_data['new_orders'], 1)
                    add_row("  ✅ Yakunlangan:", month_data['completed_orders'], 1)
            
            # 4. Tarif rejalari bo'yicha statistika
            if stats['by_tariff']:
                add_section("Tarif rejalari bo'yicha statistika")
                for tariff in stats['by_tariff']:
                    add_row(f"📋 {tariff['tariff_name']}", "", 0)
                    add_row("  📊 Buyurtmalar soni:", tariff['total_orders'], 1)
                    add_row("  👥 Mijozlar soni:", tariff['unique_clients'], 1)
            
            # 5. So'nggi faollik
            if stats['recent_activity']:
                add_section("So'nggi faollik (30 kun)")
                for activity in stats['recent_activity']:
                    if activity['recent_orders'] > 0:
                        last_active = activity['last_activity'].strftime('%Y-%m-%d')
                        add_row(
                            f"👤 {activity['manager_name']}",
                            f"📅 So'nggi: {last_active}",
                            0
                        )
                        add_row("  📊 Arizalar soni:", activity['recent_orders'], 1)
                
            headers = ["Ko'rsatkich", "Qiymat"]
            
        elif export_type == "employees":
            raw_data = await get_manager_employees_for_export()
            title = "Xodimlar ro'yxati"
            filename_base = "xodimlar"
            headers = ["ID", "Ism-sharif", "Telefon", "Lavozim", "Holati", "Qo'shilgan sana"]
            
        elif export_type == "reports":
            raw_data = await get_manager_reports_for_export()
            title = "Hisobotlar"
            filename_base = "hisobotlar"
            headers = ["ID", "Sarlavha", "Tavsif", "Yaratuvchi", "Yaratilgan sana", "Yangilangan sana"]
        
        else:
            await callback.message.answer("❌ Noto'g'ri hisobot turi")
            return
        
        # Ensure data is in the correct format (list of dicts)
        if not isinstance(raw_data, list):
            raw_data = [raw_data] if raw_data is not None else []
            
        if raw_data and not isinstance(raw_data[0], dict):
            # If raw_data is a list of non-dict items, convert to list of dicts
            if all(hasattr(item, '_asdict') for item in raw_data):
                # Handle SQLAlchemy/asyncpg row objects
                raw_data = [dict(row) for row in raw_data]
            else:
                # Handle simple lists
                raw_data = [{"value": str(item)} for item in raw_data]
        
        # Generate file based on format
        export_utils = ExportUtils()
        file_data = None
        
        try:
            if format_type == "csv":
                if not raw_data:
                    raise ValueError("No data to export")
                file_data = export_utils.to_csv(raw_data, headers=headers)
                file_to_send = BufferedInputFile(
                    file_data.getvalue().encode('utf-8'), 
                    filename=f"export_{int(datetime.now().timestamp())}.csv"
                )
            elif format_type == "xlsx":
                file_data = export_utils.generate_excel(raw_data, sheet_name=export_type, title=title)
                file_to_send = BufferedInputFile(
                    file_data.getvalue(), 
                    filename=f"export_{int(datetime.now().timestamp())}.xlsx"
                )
            elif format_type == "docx":
                file_data = export_utils.generate_word(raw_data, title=title)
                file_to_send = BufferedInputFile(
                    file_data.getvalue(), 
                    filename=f"export_{int(datetime.now().timestamp())}.docx"
                )
            elif format_type == "pdf":
                file_data = export_utils.generate_pdf(raw_data, title=title)
                file_to_send = BufferedInputFile(
                    file_data.getvalue(), 
                    filename=f"export_{int(datetime.now().timestamp())}.pdf"
                )
            else:
                await callback.message.answer("❌ Noto'g'ri format")
                return
        except Exception as e:
            logger.error(f"Error generating file: {e}")
            await callback.message.answer("❌ Fayl yaratishda xatolik yuz berdi")
            return
        
        # Send the file
        try:
            await callback.message.answer_document(
                document=file_to_send,
                caption=f"📊 Eksport fayli - {export_type} ({format_type.upper()})",
                disable_notification=True
            )
        except Exception as e:
            logger.error(f"Error sending file: {e}")
            await callback.message.answer("❌ Fayl yuborishda xatolik yuz berdi")
            
        # Show export types keyboard again
        keyboard = get_manager_export_types_keyboard()
        await callback.message.answer(
            "✅ Hisobot muvaffaqiyatli yuklab olindi.\n"
            "Yana qanday hisobot kerak?",
            reply_markup=keyboard
        )
            
    except Exception as e:
        logger.error(f"Export format handler error: {e}", exc_info=True)
        await callback.message.answer("❌ Hisobot yaratishda xatolik yuz berdi")
    finally:
        await callback.answer()

@router.callback_query(F.data == "manager_export_back_types")
async def export_back_to_types_handler(callback: CallbackQuery, state: FSMContext):
    """Go back to export types selection"""
    try:
        await state.update_data(export_type=None)
        keyboard = get_manager_export_types_keyboard()
        await callback.message.edit_text(
            "📊 <b>Menejerlar uchun hisobotlar</b>\n\n"
            "Quyidagi hisobot turlaridan birini tanlang:",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Export back to types handler error: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

@router.callback_query(F.data == "manager_export_end")
async def export_end_handler(callback: CallbackQuery, state: FSMContext):
    """End export session"""
    try:
        await state.clear()
        await callback.message.delete()
        await callback.answer("📊 Hisobot oynasi yopildi", show_alert=False)
    except Exception as e:
        logger.error(f"Export end handler error: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)