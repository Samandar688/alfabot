from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from keyboards.admin_buttons import (
    get_applications_main_menu,
    get_applications_main_menu_inline,
    get_applications_dashboard_menu,
    get_applications_type_menu,
    get_applications_filter_menu,
    get_back_to_main_keyboard
)
from states.admin_states import ApplicationsStates
from database.admin_orders_queries import (
    get_dashboard_statistics,
    get_today_statistics,
    get_weekly_trend,
    get_critical_orders,
    get_delayed_orders,
    get_connection_orders_list,
    search_connection_orders,
    filter_connection_orders,
    get_technician_orders_list,
    search_technician_orders,
    filter_technician_orders,
    get_saff_orders_list,
    search_saff_orders,
    filter_saff_orders,
)
from datetime import datetime, timedelta

# ==================== INLINE CALLBACK HANDLERS AND FLOWS ADDED BELOW ====================

router = Router()

# ==================== ASOSIY ZAYAVKALAR MENU ====================
@router.message(F.text.in_(["📝 Zayavkalar", "📝 Заявки"]))
async def orders_main_handler(message: Message, state: FSMContext):
    """Zayavkalar asosiy menusi"""
    await state.set_state(ApplicationsStates.main_menu)
    
    lang = "uz"  # Default language
    
    text = (
        "📝 **Zayavkalar boshqaruvi**\n\n"
        "Quyidagi bo'limlardan birini tanlang:\n\n"
        "📊 **Umumiy dashboard** - Barcha statistikalar\n"
        "🔌 **Ulanish zayavkalari** - Connection orders\n"
        "🔧 **Texnik zayavkalar** - Technician orders\n"
        "👥 **Xodim zayavkalari** - Staff orders"
    )
    
    await message.answer(
        text,
        reply_markup=get_applications_main_menu(lang),
        parse_mode="Markdown"
    )

# ==================== UMUMIY DASHBOARD ====================
@router.message(F.text.in_(["📊 Umumiy dashboard", "📊 Общая панель"]))
async def dashboard_handler(message: Message, state: FSMContext):
    """Umumiy dashboard ko'rsatish"""
    await state.set_state(ApplicationsStates.dashboard)
    
    try:
        # Dashboard statistikalarini olish
        stats = await get_dashboard_statistics()
        
        text = (
            "📊 **UMUMIY DASHBOARD**\n\n"
            f"📈 **Bugungi statistika:**\n"
            f"   • Jami zayavkalar: {stats['today_total']}\n"
            f"   • Ulanish: {stats['today_connection']}\n"
            f"   • Texnik: {stats['today_technician']}\n"
            f"   • Xodim: {stats['today_saff']}\n\n"
            f"📊 **Haftalik trend:**\n"
            f"   • Bu hafta: {stats['week_total']}\n"
            f"   • O'tgan hafta: {stats['prev_week_total']}\n"
            f"   • O'zgarish: {stats['week_change']:+d}\n\n"
            f"🚨 **Kritik zayavkalar:** {stats['critical_count']}\n"
            f"⏰ **Kechikkan zayavkalar:** {stats['delayed_count']}"
        )
        
        await message.answer(
            text,
            reply_markup=get_applications_dashboard_menu("uz"),
            parse_mode="Markdown"
        )
        
    except Exception as e:
        await message.answer(
            "❌ Dashboard ma'lumotlarini yuklashda xatolik yuz berdi."
        )

# ==================== BUGUNGI STATISTIKA ====================
@router.message(F.text.in_(["📈 Bugungi statistika", "📈 Сегодняшняя статистика"]))
async def today_statistics_handler(message: Message):
    """Bugungi batafsil statistika"""
    try:
        stats = await get_today_statistics()
        
        text = (
            "📈 **BUGUNGI BATAFSIL STATISTIKA**\n\n"
            f"🔌 **Ulanish zayavkalari:** {stats['connection_total']}\n"
            f"   • Yangi: {stats['connection_new']}\n"
            f"   • Jarayonda: {stats['connection_in_progress']}\n"
            f"   • Tugallangan: {stats['connection_completed']}\n\n"
            f"🔧 **Texnik zayavkalar:** {stats['technician_total']}\n"
            f"   • Yangi: {stats['technician_new']}\n"
            f"   • Jarayonda: {stats['technician_in_progress']}\n"
            f"   • Tugallangan: {stats['technician_completed']}\n\n"
            f"👥 **Xodim zayavkalari:** {stats['saff_total']}\n"
            f"   • Yangi: {stats['saff_new']}\n"
            f"   • Jarayonda: {stats['saff_in_progress']}\n"
            f"   • Tugallangan: {stats['saff_completed']}\n\n"
            f"📊 **Jami:** {stats['total_all']}"
        )
        
        await message.answer(text, parse_mode="Markdown")
        
    except Exception as e:
        await message.answer("❌ Statistika ma'lumotlarini yuklashda xatolik yuz berdi.")

# ==================== HAFTALIK TREND ====================
@router.message(F.text.in_(["📊 Haftalik trend", "📊 Недельный тренд"]))
async def weekly_trend_handler(message: Message):
    """Haftalik trend ko'rsatish"""
    try:
        trend_data = await get_weekly_trend()
        
        text = "📊 **HAFTALIK TREND**\n\n"
        
        for day_data in trend_data:
            day_name = day_data['day_name']
            total = day_data['total']
            connection = day_data['connection']
            technician = day_data['technician']
            saff = day_data['saff']
            
            text += f"📅 **{day_name}:** {total}\n"
            text += f"   🔌 {connection} | 🔧 {technician} | 👥 {saff}\n\n"
        
        await message.answer(text, parse_mode="Markdown")
        
    except Exception as e:
        await message.answer("❌ Haftalik trend ma'lumotlarini yuklashda xatolik yuz berdi.")

# ==================== KRITIK ZAYAVKALAR ====================
@router.message(F.text.in_(["🚨 Kritik zayavkalar", "🚨 Критические заявки"]))
async def critical_orders_handler(message: Message):
    """Kritik zayavkalarni ko'rsatish"""
    try:
        critical_orders = await get_critical_orders()
        
        if not critical_orders:
            await message.answer("✅ Hozirda kritik zayavkalar yo'q.")
            return
        
        text = "🚨 **KRITIK ZAYAVKALAR**\n\n"
        
        for order in critical_orders:
            order_type = "🔌" if order['type'] == 'connection' else "🔧" if order['type'] == 'technician' else "👥"
            text += f"{order_type} **#{order['id']}** - {order['status']}\n"
            text += f"   📅 {order['created_at'].strftime('%d.%m.%Y %H:%M')}\n"
            text += f"   📍 {order['address'] or 'Manzil ko\'rsatilmagan'}\n\n"
        
        await message.answer(text, parse_mode="Markdown")
        
    except Exception as e:
        await message.answer("❌ Kritik zayavkalar ma'lumotlarini yuklashda xatolik yuz berdi.")

# ==================== KECHIKKAN ZAYAVKALAR ====================
@router.message(F.text.in_(["⏰ Kechikkan zayavkalar", "⏰ Просроченные заявки"]))
async def delayed_orders_handler(message: Message):
    """Kechikkan zayavkalarni ko'rsatish"""
    try:
        delayed_orders = await get_delayed_orders()
        
        if not delayed_orders:
            await message.answer("✅ Hozirda kechikkan zayavkalar yo'q.")
            return
        
        text = "⏰ **KECHIKKAN ZAYAVKALAR**\n\n"
        
        for order in delayed_orders:
            order_type = "🔌" if order['type'] == 'connection' else "🔧" if order['type'] == 'technician' else "👥"
            days_delayed = (datetime.now() - order['created_at']).days
            
            text += f"{order_type} **#{order['id']}** - {order['status']}\n"
            text += f"   📅 {order['created_at'].strftime('%d.%m.%Y %H:%M')}\n"
            text += f"   ⏰ {days_delayed} kun kechikkan\n"
            text += f"   📍 {order['address'] or 'Manzil ko\'rsatilmagan'}\n\n"
        
        await message.answer(text, parse_mode="Markdown")
        
    except Exception as e:
        await message.answer("❌ Kechikkan zayavkalar ma'lumotlarini yuklashda xatolik yuz berdi.")

# ==================== ULANISH ZAYAVKALARI ====================
@router.message(F.text.in_(["🔌 Ulanish zayavkalari", "🔌 Заявки на подключение"]))
async def connection_orders_handler(message: Message, state: FSMContext):
    """Ulanish zayavkalari bo'limi"""
    await state.set_state(ApplicationsStates.connection_orders)
    
    text = (
        "🔌 **ULANISH ZAYAVKALARI**\n\n"
        "Quyidagi amallardan birini tanlang:"
    )
    
    await message.answer(
        text,
        reply_markup=get_applications_type_menu("connection", "uz"),
        parse_mode="Markdown"
    )

# ==================== TEXNIK ZAYAVKALAR ====================
@router.message(F.text.in_(["🔧 Texnik zayavkalar", "🔧 Технические заявки"]))
async def technician_orders_handler(message: Message, state: FSMContext):
    """Texnik zayavkalar bo'limi"""
    await state.set_state(ApplicationsStates.technician_orders)
    
    text = (
        "🔧 **TEXNIK ZAYAVKALAR**\n\n"
        "Quyidagi amallardan birini tanlang:"
    )
    
    await message.answer(
        text,
        reply_markup=get_applications_type_menu("technician", "uz"),
        parse_mode="Markdown"
    )

# ==================== XODIM ZAYAVKALARI ====================
@router.message(F.text.in_(["👥 Xodim zayavkalari", "👥 Заявки сотрудников"]))
async def saff_orders_handler(message: Message, state: FSMContext):
    """Xodim zayavkalari bo'limi"""
    await state.set_state(ApplicationsStates.saff_orders)
    
    text = (
        "👥 **XODIM ZAYAVKALARI**\n\n"
        "Quyidagi amallardan birini tanlang:"
    )
    
    await message.answer(
        text,
        reply_markup=get_applications_type_menu("saff", "uz"),
        parse_mode="Markdown"
    )

# ==================== ORQAGA QAYTISH ====================
@router.message(F.text.in_(["◀️ Orqaga", "◀️ Назад"]))
async def back_handler(message: Message, state: FSMContext):
    """Orqaga qaytish"""
    current_state = await state.get_state()
    
    if current_state in [ApplicationsStates.dashboard, ApplicationsStates.connection_orders, 
                        ApplicationsStates.technician_orders, ApplicationsStates.saff_orders]:
        # Asosiy zayavkalar menusiga qaytish
        await orders_main_handler(message, state)
    else:
        # State ni tozalash
        await state.clear()
        await message.answer(
            "🏠 Asosiy menyuga qaytdingiz."
        )

# -------------------- MAIN INLINE NAVIGATION --------------------
@router.callback_query(F.data == "app_dashboard")
async def cb_open_dashboard(call: CallbackQuery, state: FSMContext):
    await state.set_state(ApplicationsStates.dashboard)
    try:
        stats = await get_dashboard_statistics()
        text = (
            "📊 **UMUMIY DASHBOARD**\n\n"
            f"📈 **Bugungi statistika:**\n"
            f"   • Jami zayavkalar: {stats['today_total']}\n"
            f"   • Ulanish: {stats['today_connection']}\n"
            f"   • Texnik: {stats['today_technician']}\n"
            f"   • Xodim: {stats['today_saff']}\n\n"
            f"📊 **Haftalik trend:**\n"
            f"   • Bu hafta: {stats['week_total']}\n"
            f"   • O'tgan hafta: {stats['prev_week_total']}\n"
            f"   • O'zgarish: {stats['week_change']:+d}\n\n"
            f"🚨 **Kritik zayavkalar:** {stats['critical_count']}\n"
            f"⏰ **Kechikkan zayavkalar:** {stats['delayed_count']}"
        )
        await call.message.edit_text(text, reply_markup=get_applications_dashboard_menu("uz"), parse_mode="Markdown")
    except TelegramBadRequest:
        await call.message.answer(text, reply_markup=get_applications_dashboard_menu("uz"), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "app_connection_orders")
async def cb_open_connection(call: CallbackQuery, state: FSMContext):
    await state.set_state(ApplicationsStates.connection_orders)
    text = (
        "🔌 **ULANISH ZAYAVKALARI**\n\n"
        "Quyidagi amallardan birini tanlang:"
    )
    try:
        await call.message.edit_text(text, reply_markup=get_applications_type_menu("connection", "uz"), parse_mode="Markdown")
    except TelegramBadRequest:
        await call.message.answer(text, reply_markup=get_applications_type_menu("connection", "uz"), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "app_technician_orders")
async def cb_open_technician(call: CallbackQuery, state: FSMContext):
    await state.set_state(ApplicationsStates.technician_orders)
    text = (
        "🔧 **TEXNIK ZAYAVKALAR**\n\n"
        "Quyidagi amallardan birini tanlang:"
    )
    try:
        await call.message.edit_text(text, reply_markup=get_applications_type_menu("technician", "uz"), parse_mode="Markdown")
    except TelegramBadRequest:
        await call.message.answer(text, reply_markup=get_applications_type_menu("technician", "uz"), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "app_saff_orders")
async def cb_open_saff(call: CallbackQuery, state: FSMContext):
    await state.set_state(ApplicationsStates.saff_orders)
    text = (
        "👥 **XODIM ZAYAVKALARI**\n\n"
        "Quyidagi amallardan birini tanlang:"
    )
    try:
        await call.message.edit_text(text, reply_markup=get_applications_type_menu("saff", "uz"), parse_mode="Markdown")
    except TelegramBadRequest:
        await call.message.answer(text, reply_markup=get_applications_type_menu("saff", "uz"), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "app_back_to_main")
async def cb_back_to_main(call: CallbackQuery, state: FSMContext):
    await state.set_state(ApplicationsStates.main_menu)
    text = (
        "📝 **Zayavkalar boshqaruvi**\n\n"
        "Quyidagi bo'limlardan birini tanlang:\n\n"
        "📊 **Umumiy dashboard** - Barcha statistikalar\n"
        "🔌 **Ulanish zayavkalari** - Connection orders\n"
        "🔧 **Texnik zayavkalar** - Technician orders\n"
        "👥 **Xodim zayavkalari** - Staff orders"
    )
    try:
        await call.message.edit_text(text, reply_markup=get_applications_main_menu_inline("uz"), parse_mode="Markdown")
    except TelegramBadRequest:
        await call.message.answer(text, parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "applications_back_to_main")
async def applications_back_to_main_handler(call: CallbackQuery):
    """Asosiy menyuga qaytish"""
    text = "🏠 *Asosiy menyu*\n\nKerakli bo'limni tanlang:"
    
    try:
        await call.message.edit_text(text, reply_markup=get_applications_main_menu("uz"), parse_mode="Markdown")
    except TelegramBadRequest:
        await call.message.answer(text, reply_markup=get_applications_main_menu("uz"), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "connection_orders")
async def connection_orders_handler(call: CallbackQuery):
    """Ulanish buyurtmalari"""
    text = "📞 *Ulanish buyurtmalari*\n\nKerakli amalni tanlang:"
    
    try:
        await call.message.edit_text(text, reply_markup=get_applications_type_menu("connection", "uz"), parse_mode="Markdown")
    except TelegramBadRequest:
        await call.message.answer(text, reply_markup=get_applications_type_menu("connection", "uz"), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "technician_orders")
async def technician_orders_handler(call: CallbackQuery):
    """Texnik buyurtmalar"""
    text = "🔧 *Texnik buyurtmalar*\n\nKerakli amalni tanlang:"
    
    try:
        await call.message.edit_text(text, reply_markup=get_applications_type_menu("technician", "uz"), parse_mode="Markdown")
    except TelegramBadRequest:
        await call.message.answer(text, reply_markup=get_applications_type_menu("technician", "uz"), parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "saff_orders")
async def saff_orders_handler(call: CallbackQuery):
    """Saff buyurtmalari"""
    text = "📋 *Saff buyurtmalari*\n\nKerakli amalni tanlang:"
    
    try:
        await call.message.edit_text(text, reply_markup=get_applications_type_menu("saff", "uz"), parse_mode="Markdown")
    except TelegramBadRequest:
        await call.message.answer(text, reply_markup=get_applications_type_menu("saff", "uz"), parse_mode="Markdown")
    await call.answer()

# -------------------- DASHBOARD SUBMENU --------------------
@router.callback_query(F.data == "app_today_stats")
async def cb_today_stats(call: CallbackQuery):
    try:
        stats = await get_today_statistics()
        text = (
            "📈 **BUGUNGI BATAFSIL STATISTIKA**\n\n"
            f"🔌 **Ulanish zayavkalari:** {stats['connection_total']}\n"
            f"   • Yangi: {stats['connection_new']}\n"
            f"   • Jarayonda: {stats['connection_in_progress']}\n"
            f"   • Tugallangan: {stats['connection_completed']}\n\n"
            f"🔧 **Texnik zayavkalar:** {stats['technician_total']}\n"
            f"   • Yangi: {stats['technician_new']}\n"
            f"   • Jarayonda: {stats['technician_in_progress']}\n"
            f"   • Tugallangan: {stats['technician_completed']}\n\n"
            f"👥 **Xodim zayavkalari:** {stats['saff_total']}\n"
            f"   • Yangi: {stats['saff_new']}\n"
            f"   • Jarayonda: {stats['saff_in_progress']}\n"
            f"   • Tugallangan: {stats['saff_completed']}\n\n"
            f"📊 **Jami:** {stats['total_all']}"
        )
        await call.message.edit_text(text, parse_mode="Markdown")
    except TelegramBadRequest:
        await call.message.answer(text, parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "app_weekly_trend")
async def cb_weekly_trend(call: CallbackQuery):
    try:
        trend_data = await get_weekly_trend()
        text = "📊 **HAFTALIK TREND**\n\n"
        for day_data in trend_data:
            text += f"📅 **{day_data['day_name']}:** {day_data['total']}\n"
            text += f"   🔌 {day_data['connection']} | 🔧 {day_data['technician']} | 👥 {day_data['saff']}\n\n"
        await call.message.edit_text(text, parse_mode="Markdown")
    except TelegramBadRequest:
        await call.message.answer(text, parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "app_critical_orders")
async def cb_critical_orders(call: CallbackQuery):
    try:
        critical_orders = await get_critical_orders()
        if not critical_orders:
            await call.message.edit_text("✅ Hozirda kritik zayavkalar yo'q.")
        else:
            text = "🚨 **KRITIK ZAYAVKALAR**\n\n"
            for order in critical_orders:
                order_type = "🔌" if order['type'] == 'connection' else "🔧" if order['type'] == 'technician' else "👥"
                text += f"{order_type} **#{order['id']}** - {order['status']}\n"
                text += f"   📅 {order['created_at'].strftime('%d.%m.%Y %H:%M')}\n"
                text += f"   📍 {order['address'] or 'Manzil ko\'rsatilmagan'}\n\n"
            await call.message.edit_text(text, parse_mode="Markdown")
    except TelegramBadRequest:
        await call.message.answer(text, parse_mode="Markdown")
    await call.answer()

@router.callback_query(F.data == "app_delayed_orders")
async def cb_delayed_orders(call: CallbackQuery):
    try:
        delayed_orders = await get_delayed_orders()
        if not delayed_orders:
            await call.message.edit_text("✅ Hozirda kechikkan zayavkalar yo'q.")
        else:
            text = "⏰ **KECHIKKAN ZAYAVKALAR**\n\n"
            for order in delayed_orders:
                order_type = "🔌" if order['type'] == 'connection' else "🔧" if order['type'] == 'technician' else "👥"
                days_delayed = (datetime.now() - order['created_at']).days
                text += f"{order_type} **#{order['id']}** - {order['status']}\n"
                text += f"   📅 {order['created_at'].strftime('%d.%m.%Y %H:%M')}\n"
                text += f"   ⏰ {days_delayed} kun kechikkan\n"
                text += f"   📍 {order['address'] or 'Manzil ko\'rsatilmagan'}\n\n"
            await call.message.edit_text(text, parse_mode="Markdown")
    except TelegramBadRequest:
        await call.message.answer(text, parse_mode="Markdown")
    await call.answer()

# -------------------- LISTING HELPERS --------------------
def _format_connection_list(items) -> str:
    if not items:
        return "🔍 Hech narsa topilmadi."
    lines = ["📋 Ulanish zayavkalari:"]
    for r in items:
        lines.append(f"#${r['id']} • {r.get('region') or '-'} • {r.get('status')}\n📍 {r.get('address') or '-'} • {r['created_at'].strftime('%d.%m.%Y')}")
    return "\n\n".join(lines)

def _format_technician_list(items) -> str:
    if not items:
        return "🔍 Hech narsa topilmadi."
    lines = ["📋 Texnik zayavkalar:"]
    for r in items:
        lines.append(f"#${r['id']} • {r.get('abonent_id') or '-'} • {r.get('status')}\n📍 {r.get('address') or '-'} • {r['created_at'].strftime('%d.%m.%Y')}")
    return "\n\n".join(lines)

def _format_saff_list(items) -> str:
    if not items:
        return "🔍 Hech narsa topilmadi."
    lines = ["📋 Xodim zayavkalari:"]
    for r in items:
        lines.append(f"#${r['id']} • {r.get('type_of_zayavka')} • {r.get('status')}\n📞 {r.get('phone') or '-'} • 📍 {r.get('address') or '-'} • {r['created_at'].strftime('%d.%m.%Y')}")
    return "\n\n".join(lines)

async def _send_list(message: Message, app_type: str, result: dict, action: str = "list"):
    items = result['items']

    if app_type == 'connection':
        text = _format_connection_list(items)
    elif app_type == 'technician':
        text = _format_technician_list(items)
    else:
        text = _format_saff_list(items)

    await message.answer(
        text,
        reply_markup=get_applications_type_menu(app_type, "uz"),
        parse_mode="Markdown"
    )

async def _edit_list(call: CallbackQuery, app_type: str, result: dict, action: str = "list"):
    items = result['items']

    if app_type == 'connection':
        text = _format_connection_list(items)
    elif app_type == 'technician':
        text = _format_technician_list(items)
    else:
        text = _format_saff_list(items)

    markup = get_applications_type_menu(app_type, "uz")
    try:
        await call.message.edit_text(text, reply_markup=markup, parse_mode="Markdown")
    except TelegramBadRequest:
        await call.message.answer(text, reply_markup=markup, parse_mode="Markdown")

# -------------------- LIST CALLBACKS --------------------
@router.callback_query(F.data == "app_connection_list")
async def cb_connection_list(call: CallbackQuery):
    data = await get_connection_orders_list(page=1)
    await _edit_list(call, 'connection', data, 'list')
    await call.answer()

@router.callback_query(F.data == "app_technician_list")
async def cb_technician_list(call: CallbackQuery):
    data = await get_technician_orders_list(page=1)
    await _edit_list(call, 'technician', data, 'list')
    await call.answer()

@router.callback_query(F.data == "app_saff_list")
async def cb_saff_list(call: CallbackQuery):
    data = await get_saff_orders_list(page=1)
    await _edit_list(call, 'saff', data, 'list')
    await call.answer()

@router.callback_query(F.data.regexp(r"^app_(connection|technician|saff)_(list|search|filter)_page_\\d+$"))
async def cb_pagination(call: CallbackQuery, state: FSMContext):
    parts = call.data.split('_')
    app_type, action, _, page_str = parts[1], parts[2], parts[3], parts[4]
    page = int(page_str)
    data_state = await state.get_data()

    if action == 'list':
        if app_type == 'connection':
            result = await get_connection_orders_list(page=page)
        elif app_type == 'technician':
            result = await get_technician_orders_list(page=page)
        else:
            result = await get_saff_orders_list(page=page)
    elif action == 'search':
        query = data_state.get('search_query', '')
        if app_type == 'connection':
            result = await search_connection_orders(query, page=page)
        elif app_type == 'technician':
            result = await search_technician_orders(query, page=page)
        else:
            result = await search_saff_orders(query, page=page)
    else:
        filters = data_state.get('filters', {})
        if app_type == 'connection':
            result = await filter_connection_orders(
                status=filters.get('status'),
                region=filters.get('region'),
                date_from=filters.get('date_from'),
                date_to=filters.get('date_to'),
                page=page
            )
        elif app_type == 'technician':
            result = await filter_technician_orders(
                status=filters.get('status'),
                technician_id=filters.get('technician_id'),
                date_from=filters.get('date_from'),
                date_to=filters.get('date_to'),
                page=page
            )
        else:
            result = await filter_saff_orders(
                status=filters.get('status'),
                creator_user_id=filters.get('creator_user_id'),
                type_of_zayavka=filters.get('type_of_zayavka'),
                date_from=filters.get('date_from'),
                date_to=filters.get('date_to'),
                page=page
            )

    await _edit_list(call, app_type, result, action)
    await call.answer()

# -------------------- SEARCH FLOW --------------------
@router.callback_query(F.data.regexp(r"^app_(connection|technician|saff)_search$"))
async def cb_search_start(call: CallbackQuery, state: FSMContext):
    app_type = call.data.split('_')[1]
    await state.update_data(app_type=app_type)
    await state.set_state(ApplicationsStates.waiting_for_search_query)
    if app_type == 'connection':
        tip = "ID, telefon yoki manzil"
    elif app_type == 'technician':
        tip = "abonent ID yoki telefon"
    else:
        tip = "ID, telefon yoki manzil"
    await call.message.answer(f"🔎 Qidiruv so'zini kiriting ({tip}):")
    await call.answer()

@router.message(ApplicationsStates.waiting_for_search_query)
async def on_search_query(message: Message, state: FSMContext):
    data = await state.get_data()
    app_type = data.get('app_type')
    query = message.text.strip()
    await state.update_data(search_query=query)
    if app_type == 'connection':
        result = await search_connection_orders(query, page=1)
    elif app_type == 'technician':
        result = await search_technician_orders(query, page=1)
    else:
        result = await search_saff_orders(query, page=1)
    await _send_list(message, app_type, result, 'search')

# -------------------- FILTER FLOW --------------------
@router.callback_query(F.data.regexp(r"^app_(connection|technician|saff)_filter$"))
async def cb_filter_menu(call: CallbackQuery, state: FSMContext):
    app_type = call.data.split('_')[1]
    await state.update_data(app_type=app_type, filters={})
    try:
        await call.message.edit_text("📊 Filtrlash turini tanlang:", reply_markup=get_applications_filter_menu(app_type, "uz"))
    except TelegramBadRequest:
        await call.message.answer("📊 Filtrlash turini tanlang:", reply_markup=get_applications_filter_menu(app_type, "uz"))
    await call.answer()

@router.callback_query(F.data.regexp(r"^app_(connection|technician|saff)_filter_status$"))
async def cb_filter_status(call: CallbackQuery, state: FSMContext):
    await state.update_data(pending_filter='status')
    await state.set_state(ApplicationsStates.waiting_for_filter_selection)
    try:
        await call.message.edit_text("Status kiriting (masalan: new, in_manager, completed ...):")
    except TelegramBadRequest:
        await call.message.answer("Status kiriting (masalan: new, in_manager, completed ...):")
    await call.answer()

@router.callback_query(F.data.regexp(r"^app_connection_filter_region$"))
async def cb_filter_region(call: CallbackQuery, state: FSMContext):
    await state.update_data(pending_filter='region')
    await state.set_state(ApplicationsStates.waiting_for_filter_selection)
    try:
        await call.message.edit_text("Hudud nomini kiriting (qisman ham bo'ladi):")
    except TelegramBadRequest:
        await call.message.answer("Hudud nomini kiriting (qisman ham bo'ladi):")
    await call.answer()

@router.callback_query(F.data.regexp(r"^app_saff_filter_creator$"))
async def cb_filter_creator(call: CallbackQuery, state: FSMContext):
    await state.update_data(pending_filter='creator_user_id')
    await state.set_state(ApplicationsStates.waiting_for_filter_selection)
    try:
        await call.message.edit_text("Yaratuvchi user ID ni kiriting (raqam):")
    except TelegramBadRequest:
        await call.message.answer("Yaratuvchi user ID ni kiriting (raqam):")
    await call.answer()

@router.callback_query(F.data.regexp(r"^app_saff_filter_type$"))
async def cb_filter_type(call: CallbackQuery, state: FSMContext):
    await state.update_data(pending_filter='type_of_zayavka')
    await state.set_state(ApplicationsStates.waiting_for_filter_selection)
    try:
        await call.message.edit_text("Turini kiriting (connection yoki technician):")
    except TelegramBadRequest:
        await call.message.answer("Turini kiriting (connection yoki technician):")
    await call.answer()

@router.callback_query(F.data.regexp(r"^app_(connection|technician|saff)_filter_date$"))
async def cb_filter_date(call: CallbackQuery, state: FSMContext):
    await state.update_data(pending_filter='date_range')
    await state.set_state(ApplicationsStates.waiting_for_filter_selection)
    try:
        await call.message.edit_text("Sana oralig'ini kiriting: YYYY-MM-DD to YYYY-MM-DD")
    except TelegramBadRequest:
        await call.message.answer("Sana oralig'ini kiriting: YYYY-MM-DD to YYYY-MM-DD")
    await call.answer()

@router.callback_query(F.data.regexp(r"^app_(connection|technician|saff)_filter_clear$"))
async def cb_filter_clear(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    app_type = data.get('app_type')
    await state.update_data(filters={})
    try:
        await call.message.edit_text("Filtrlar tozalandi.")
    except TelegramBadRequest:
        await call.message.answer("Filtrlar tozalandi.")
    if app_type == 'connection':
        result = await get_connection_orders_list(page=1)
    elif app_type == 'technician':
        result = await get_technician_orders_list(page=1)
    else:
        result = await get_saff_orders_list(page=1)
    await _edit_list(call, app_type, result, 'list')
    await call.answer()

@router.message(ApplicationsStates.waiting_for_filter_selection)
async def on_filter_value(message: Message, state: FSMContext):
    data = await state.get_data()
    app_type = data.get('app_type')
    pending = data.get('pending_filter')
    filters = data.get('filters', {})
    text = message.text.strip()

    if pending == 'date_range':
        try:
            parts = [p.strip() for p in text.split('to')]
            if len(parts) >= 2:
                date_from = datetime.strptime(parts[0], "%Y-%m-%d")
                date_to = datetime.strptime(parts[1], "%Y-%m-%d")
                filters['date_from'] = date_from
                filters['date_to'] = date_to
        except Exception:
            await message.answer("Sana formati noto'g'ri. Masalan: 2025-01-01 to 2025-01-31")
            return
    elif pending == 'creator_user_id':
        try:
            filters['creator_user_id'] = int(text)
        except ValueError:
            await message.answer("Raqam kiriting.")
            return
    else:
        filters[pending] = text

    await state.update_data(filters=filters)

    if app_type == 'connection':
        result = await filter_connection_orders(
            status=filters.get('status'),
            region=filters.get('region'),
            date_from=filters.get('date_from'),
            date_to=filters.get('date_to'),
            page=1
        )
    elif app_type == 'technician':
        result = await filter_technician_orders(
            status=filters.get('status'),
            technician_id=filters.get('technician_id'),
            date_from=filters.get('date_from'),
            date_to=filters.get('date_to'),
            page=1
        )
    else:
        result = await filter_saff_orders(
            status=filters.get('status'),
            creator_user_id=filters.get('creator_user_id'),
            type_of_zayavka=filters.get('type_of_zayavka'),
            date_from=filters.get('date_from'),
            date_to=filters.get('date_to'),
            page=1
        )

    await _send_list(message, app_type, result, 'filter')
