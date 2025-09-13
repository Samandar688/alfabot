from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from database.warehouse_queries import get_all_materials, search_materials, get_material_by_id
from database.technician_queries import fetch_technician_materials, fetch_assigned_qty
from database.jm_inbox_queries import db_get_user_by_id
from database.warehouse_queries import get_users_by_role
from keyboards.warehouse_buttons import get_warehouse_main_menu
from filters.role_filter import RoleFilter
from states.warehouse_states import TechnicianMaterialStates

router = Router()

@router.message(RoleFilter("warehouse"), F.text.in_(["📦 Teknik xodimga mahsulot berish", "📦 Отдать материал технике"]))
async def technician_material_menu(message: Message, state: FSMContext):
    """Texnikka material berish menyusi"""
    await state.set_state(TechnicianMaterialStates.select_technician)
    
    # Barcha texniklarni olish
    technicians = await get_users_by_role("technician")
    
    if not technicians:
        await message.answer(
            "❌ Hozirda tizimda texnik xodimlar mavjud emas.",
            reply_markup=get_warehouse_main_menu("uz")
        )
        await state.clear()
        return
    
    # Texniklarni inline keyboard qilish
    keyboard = []
    for tech in technicians:
        full_name = tech.get('full_name', '').strip()
        
        keyboard.append([
            InlineKeyboardButton(
                text=f"👨‍🔧 {full_name}",
                callback_data=f"select_tech_{tech['id']}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_warehouse_menu")
    ])
    
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    await message.answer(
        "👨‍🔧 Qaysi texnik xodimga material berishni xohlaysiz?\n\n"
        "Texnik xodimni tanlang:",
        reply_markup=reply_markup
    )

@router.callback_query(F.data.startswith("select_tech_"))
async def select_technician(callback: CallbackQuery, state: FSMContext):
    """Texnikni tanlash"""
    tech_id = int(callback.data.split("_")[-1])
    
    # Texnik ma'lumotlarini olish
    technician = await db_get_user_by_id(tech_id)
    if not technician:
        await callback.answer("❌ Texnik topilmadi!", show_alert=True)
        return
    
    # State ga texnik ID sini saqlash
    await state.update_data(technician_id=tech_id)
    await state.set_state(TechnicianMaterialStates.select_material)
    
    # Texnikning mavjud materiallarini ko'rsatish
    tech_materials = await fetch_technician_materials(tech_id)
    
    full_name = technician.get('full_name', '').strip()
    if not full_name:
        full_name = f"ID: {tech_id}"
    
    message_text = f"👨‍🔧 **{full_name}** texnikining mavjud materiallari:\n\n"
    
    if tech_materials:
        message_text += "📦 **Mavjud materiallar:**\n"
        for material in tech_materials:
            message_text += f"• {material['name']} - {material['stock_quantity']} dona\n"
    else:
        message_text += "📦 Hozirda texnikda materiallar mavjud emas.\n"
    
    message_text += "\n🔍 Qo'shish uchun material tanlang:"
    
    # Ombordagi barcha materiallarni ko'rsatish
    warehouse_materials = await get_all_materials()
    
    if not warehouse_materials:
        await callback.message.edit_text(
            message_text + "\n\n❌ Omborda materiallar mavjud emas.",
            parse_mode="Markdown"
        )
        await state.clear()
        return
    
    # Materiallarni inline keyboard qilish
    keyboard = []
    for material in warehouse_materials:
        if material['quantity'] > 0:  # Faqat mavjud materiallar
            keyboard.append([
                InlineKeyboardButton(
                    text=f"📦 {material['name']} ({material['quantity']} dona)",
                    callback_data=f"select_material_{material['id']}"
                )
            ])
    
    if not keyboard:
        await callback.message.edit_text(
            message_text + "\n\n❌ Omborda mavjud materiallar yo'q.",
            parse_mode="Markdown"
        )
        await state.clear()
        return
    
    keyboard.append([
        InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_tech_selection")
    ])
    
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    await callback.message.edit_text(
        message_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("select_material_"))
async def select_material(callback: CallbackQuery, state: FSMContext):
    """Materialni tanlash"""
    material_id = int(callback.data.split("_")[-1])
    
    # Material ma'lumotlarini olish
    material = await get_material_by_id(material_id)
    if not material:
        await callback.answer("❌ Material topilmadi!", show_alert=True)
        return
    
    if material['quantity'] <= 0:
        await callback.answer("❌ Bu material omborda mavjud emas!", show_alert=True)
        return
    
    # State ga material ID sini saqlash
    await state.update_data(material_id=material_id)
    await state.set_state(TechnicianMaterialStates.enter_quantity)
    
    # State dan texnik ID sini olish
    data = await state.get_data()
    tech_id = data.get('technician_id')
    
    # Texnikning bu materialdagi mavjud miqdorini olish
    current_qty = await fetch_assigned_qty(tech_id, material_id)
    
    await callback.message.edit_text(
        f"📦 **{material['name']}**\n\n"
        f"💰 Narxi: {material.get('price', 'Belgilanmagan')}\n"
        f"📊 Omborda mavjud: {material['quantity']} dona\n"
        f"👨‍🔧 Texnikda mavjud: {current_qty} dona\n\n"
        f"❓ Texnikka necha dona bermoqchisiz?\n"
        f"(1 dan {material['quantity']} gacha raqam kiriting)",
        parse_mode="Markdown"
    )

@router.message(TechnicianMaterialStates.enter_quantity)
async def enter_quantity(message: Message, state: FSMContext):
    """Miqdorni kiritish"""
    try:
        quantity = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Iltimos, faqat raqam kiriting!")
        return
    
    if quantity <= 0:
        await message.answer("❌ Miqdor 0 dan katta bo'lishi kerak!")
        return
    
    # State dan ma'lumotlarni olish
    data = await state.get_data()
    tech_id = data.get('technician_id')
    material_id = data.get('material_id')
    
    # Material ma'lumotlarini tekshirish
    material = await get_material_by_id(material_id)
    if not material or material['quantity'] < quantity:
        await message.answer(
            f"❌ Omborda yetarli material yo'q!\n"
            f"Mavjud: {material['quantity'] if material else 0} dona"
        )
        return
    
    # Texnik ma'lumotlarini olish
    technician = await db_get_user_by_id(tech_id)
    full_name = technician.get('full_name', '').strip()
    if not full_name:
        full_name = f"ID: {tech_id}"
    
    # Tasdiqlash uchun keyboard
    keyboard = [
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"confirm_assign_{tech_id}_{material_id}_{quantity}"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_assign")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    await message.answer(
        f"📋 **Tasdiqlash**\n\n"
        f"👨‍🔧 Texnik: {full_name}\n"
        f"📦 Material: {material['name']}\n"
        f"📊 Miqdor: {quantity} dona\n\n"
        f"❓ Materialni texnikka berishni tasdiqlaysizmi?",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("confirm_assign_"))
async def confirm_assignment(callback: CallbackQuery, state: FSMContext):
    """Material berishni tasdiqlash"""
    try:
        parts = callback.data.split("_")
        tech_id = int(parts[2])
        material_id = int(parts[3])
        quantity = int(parts[4])
        
        # Material va texnik ma'lumotlarini olish
        material = await get_material_by_id(material_id)
        technician = await db_get_user_by_id(tech_id)
        
        if not material or not technician:
            await callback.answer("❌ Ma'lumotlar topilmadi!", show_alert=True)
            return
        
        if material['quantity'] < quantity:
            await callback.answer("❌ Omborda yetarli material yo'q!", show_alert=True)
            return
        
        # Material berishni amalga oshirish
        import asyncpg
        from config import settings
        
        conn = await asyncpg.connect(settings.DB_URL)
        try:
            async with conn.transaction():
                # Ombordagi materialni kamaytirish
                await conn.execute(
                    "UPDATE materials SET quantity = quantity - $1 WHERE id = $2",
                    quantity, material_id
                )
                
                # Texnikka material berish (material_and_technician jadvaliga qo'shish)
                await conn.execute(
                    """
                    INSERT INTO material_and_technician (user_id, material_id, quantity)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (user_id, material_id)
                    DO UPDATE SET quantity = material_and_technician.quantity + $3
                    """,
                    tech_id, material_id, quantity
                )
        finally:
            await conn.close()
        
        full_name = technician.get('full_name', '').strip()
        if not full_name:
            full_name = f"ID: {tech_id}"
        
        await callback.message.edit_text(
            f"✅ **Muvaffaqiyatli bajarildi!**\n\n"
            f"👨‍🔧 Texnik: {full_name}\n"
            f"📦 Material: {material['name']}\n"
            f"📊 Berilgan miqdor: {quantity} dona\n\n"
            f"Material texnikka muvaffaqiyatli berildi!",
            parse_mode="Markdown"
        )
        
        await state.clear()
        
        # Asosiy menyuga qaytish
        await callback.message.answer(
            "🏠 Asosiy menyu:",
            reply_markup=get_warehouse_main_menu("uz")
        )
        
    except Exception as e:
        await callback.answer(f"❌ Xatolik yuz berdi: {str(e)}", show_alert=True)
        await state.clear()

@router.callback_query(F.data == "cancel_assign")
async def cancel_assignment(callback: CallbackQuery, state: FSMContext):
    """Material berishni bekor qilish"""
    await callback.message.edit_text(
        "❌ Material berish bekor qilindi."
    )
    await state.clear()
    
    await callback.message.answer(
        "🏠 Asosiy menyu:",
        reply_markup=get_warehouse_main_menu("uz")
    )

@router.callback_query(F.data == "back_to_warehouse_menu")
async def back_to_warehouse_menu(callback: CallbackQuery, state: FSMContext):
    """Warehouse menyusiga qaytish"""
    await callback.message.delete()
    await state.clear()
    
    await callback.message.answer(
        "🏠 Asosiy menyu:",
        reply_markup=get_warehouse_main_menu("uz")
    )

@router.callback_query(F.data == "back_to_tech_selection")
async def back_to_tech_selection(callback: CallbackQuery, state: FSMContext):
    """Texnik tanlashga qaytish"""
    await state.set_state(TechnicianMaterialStates.select_technician)
    
    # Barcha texniklarni olish
    technicians = await get_users_by_role("technician")
    
    if not technicians:
        await callback.message.edit_text(
            "❌ Hozirda tizimda texnik xodimlar mavjud emas."
        )
        await state.clear()
        return
    
    # Texniklarni inline keyboard qilish
    keyboard = []
    for tech in technicians:
        full_name = tech.get('full_name', '').strip()
        if not full_name:
            full_name = f"ID: {tech['id']}"
        
        keyboard.append([
            InlineKeyboardButton(
                text=f"👨‍🔧 {full_name}",
                callback_data=f"select_tech_{tech['id']}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_warehouse_menu")
    ])
    
    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    await callback.message.edit_text(
        "👨‍🔧 Qaysi texnik xodimga material berishni xohlaysiz?\n\n"
        "Texnik xodimni tanlang:",
        reply_markup=reply_markup
    )