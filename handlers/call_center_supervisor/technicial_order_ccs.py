# handlers/call_center/technician_order_cc.py

import re
import logging
from aiogram import Router, F
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardRemove,
)
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

# === Keyboards ===
from keyboards.call_center_supervisor_buttons import (
    get_call_center_supervisor_main_menu,
    get_client_regions_keyboard,
    confirmation_keyboard_tech_service,
)

# === States ===
from states.call_center_states import SaffTechnicianOrderStates

# === DB ===
from database.call_center_operator_queries import find_user_by_phone
from database.client_queries import ensure_user
from database.call_center_supervisor_queries import saff_orders_technician_create

# === Role filter ===
from filters.role_filter import RoleFilter

logger = logging.getLogger(__name__)

router = Router()
router.message.filter(RoleFilter("callcenter_supervisor"))
router.callback_query.filter(RoleFilter("callcenter_supervisor"))

# ----------------------- helpers -----------------------
PHONE_RE = re.compile(r"^\+?998\s?\d{2}\s?\d{3}\s?\d{2}\s?\d{2}$|^\+?998\d{9}$|^\d{9,12}$")

def normalize_phone(phone_raw: str) -> str | None:
    phone_raw = (phone_raw or "").strip()
    if not PHONE_RE.match(phone_raw):
        return None
    digits = re.sub(r"\D", "", phone_raw)
    if digits.startswith("998") and len(digits) == 12:
        return "+" + digits
    if len(digits) == 9:
        return "+998" + digits
    return phone_raw if phone_raw.startswith("+") else ("+" + digits if digits else None)

REGION_CODE_TO_ID = {
    "toshkent_city": 1, "toshkent_region": 2, "andijon": 3, "fergana": 4, "namangan": 5,
    "sirdaryo": 6, "jizzax": 7, "samarkand": 8, "bukhara": 9, "navoi": 10,
    "kashkadarya": 11, "surkhandarya": 12, "khorezm": 13, "karakalpakstan": 14,
}

def map_region_code_to_id(region_code: str | None) -> int | None:
    if not region_code:
        return None
    return REGION_CODE_TO_ID.get(region_code)

# ======================= ENTRY =======================
ENTRY_TEXTS = {
    "uz": "🔧 Texnik xizmat yaratish",
    "ru": "🛠 Создать заявку на техобслуживание",
}

@router.message(F.text.in_([ENTRY_TEXTS["uz"], ENTRY_TEXTS["ru"]]))
async def op_start_text(msg: Message, state: FSMContext):
    lang = "uz" if msg.text == ENTRY_TEXTS["uz"] else "ru"
    await state.clear()
    await state.update_data(lang=lang)
    text = (
        "📞 Mijoz telefon raqamini kiriting (masalan, +998901234567):"
        if lang == "uz"
        else "📞 Введите номер клиента (например, +998901234567):"
    )
    await state.set_state(SaffTechnicianOrderStates.waiting_client_phone)
    await msg.answer(text, reply_markup=ReplyKeyboardRemove())

# ======================= STEP 1: phone lookup =======================
@router.message(StateFilter(SaffTechnicianOrderStates.waiting_client_phone))
async def op_get_phone(msg: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    phone_n = normalize_phone(msg.text)
    if not phone_n:
        return await msg.answer(
            "❗️ Noto'g'ri format. Masalan: +998901234567"
            if lang == "uz"
            else "❗️ Неверный формат. Например: +998901234567"
        )

    user = await find_user_by_phone(phone_n)
    if not user:
        return await msg.answer(
            "❌ Bu raqam bo'yicha foydalanuvchi topilmadi."
            if lang == "uz"
            else "❌ Пользователь с таким номером не найден."
        )

    await state.update_data(acting_client=user)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Davom etish" if lang == "uz" else "▶️ Продолжить", callback_data="op_tservice_continue")]
    ])
    text = (
        "👤 Mijoz topildi:\n"
        f"• ID: <b>{user.get('id','')}</b>\n"
        f"• F.I.Sh: <b>{user.get('full_name','')}</b>\n"
        f"• Tel: <b>{user.get('phone','')}</b>\n\n"
        "Davom etish uchun tugmani bosing."
        if lang == "uz"
        else
        "👤 Клиент найден:\n"
        f"• ID: <b>{user.get('id','')}</b>\n"
        f"• Ф.И.О: <b>{user.get('full_name','')}</b>\n"
        f"• Тел: <b>{user.get('phone','')}</b>\n\n"
        "Нажмите кнопку, чтобы продолжить."
    )
    await msg.answer(text, parse_mode="HTML", reply_markup=kb)

# ======================= STEP 2: region =======================
@router.callback_query(StateFilter(SaffTechnicianOrderStates.waiting_client_phone), F.data == "op_tservice_continue")
async def op_after_confirm_user(cq: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    await cq.message.edit_reply_markup()
    await cq.message.answer(
        "🌍 Regionni tanlang:" if lang == "uz" else "🌍 Выберите регион:",
        reply_markup=get_client_regions_keyboard()
    )
    await state.set_state(SaffTechnicianOrderStates.selecting_region)
    await cq.answer()

@router.callback_query(F.data.startswith("region_"), StateFilter(SaffTechnicianOrderStates.selecting_region))
async def op_select_region(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    await callback.answer()
    await callback.message.edit_reply_markup()
    region_code = callback.data.replace("region_", "", 1)
    await state.update_data(selected_region=region_code)

    await callback.message.answer(
        "📝 Muammoni qisqacha ta'riflab bering:" if lang == "uz" else "📝 Опишите проблему:"
    )
    await state.set_state(SaffTechnicianOrderStates.problem_description)

# ======================= STEP 3: description =======================
@router.message(StateFilter(SaffTechnicianOrderStates.problem_description))
async def op_get_description(msg: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    desc = (msg.text or "").strip()
    if not desc or len(desc) < 5:
        return await msg.answer(
            "❗️ Iltimos, muammoni aniqroq yozing (kamida 5 belgi)."
            if lang == "uz"
            else "❗️ Пожалуйста, опишите проблему подробнее (минимум 5 символов)."
        )
    await state.update_data(description=desc)

    await msg.answer("🏠 Manzilingizni kiriting:" if lang == "uz" else "🏠 Введите адрес:")
    await state.set_state(SaffTechnicianOrderStates.entering_address)

# ======================= STEP 4: address =======================
@router.message(StateFilter(SaffTechnicianOrderStates.entering_address))
async def op_get_address(msg: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    address = (msg.text or "").strip()
    if not address:
        return await msg.answer(
            "❗️ Iltimos, manzilni kiriting." if lang == "uz" else "❗️ Пожалуйста, введите адрес."
        )
    await state.update_data(address=address)
    await op_show_summary(msg, state)

# ======================= STEP 5: summary =======================
async def op_show_summary(target, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    region = data.get("selected_region", "-")
    address = data.get("address", "-")
    description = data.get("description", "-")

    text = (
        f"🗺️ <b>Hudud:</b> {region}\n"
        f"🛠 <b>Xizmat turi:</b> Texnik xizmat\n"
        f"📝 <b>Ta'rif:</b> {description}\n"
        f"🏠 <b>Manzil:</b> {address}\n\n"
        "Ma'lumotlar to‘g‘rimi?"
        if lang == "uz"
        else
        f"🗺️ <b>Регион:</b> {region}\n"
        f"🛠 <b>Тип услуги:</b> Техническое обслуживание\n"
        f"📝 <b>Описание:</b> {description}\n"
        f"🏠 <b>Адрес:</b> {address}\n\n"
        "Данные верны?"
    )

    kb = confirmation_keyboard_tech_service()
    if hasattr(target, "answer"):
        await target.answer(text, parse_mode="HTML", reply_markup=kb)
    else:
        await target.message.answer(text, parse_mode="HTML", reply_markup=kb)

    await state.set_state(SaffTechnicianOrderStates.confirming_connection)

# ======================= STEP 6: confirm =======================
@router.callback_query(F.data == "confirm_zayavka_call_center_tech_service", StateFilter(SaffTechnicianOrderStates.confirming_connection))
async def op_confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    try:
        await callback.message.edit_reply_markup()

        acting_client = data.get("acting_client")
        if not acting_client:
            return await callback.answer(
                "Mijoz tanlanmagan" if lang == "uz" else "Клиент не выбран",
                show_alert=True
            )

        client_user_id = acting_client["id"]
        user_row = await ensure_user(callback.from_user.id, callback.from_user.full_name, callback.from_user.username)
        user_id = user_row["id"]

        region_code = (data.get("selected_region") or "toshkent_city").lower()
        region_id = map_region_code_to_id(region_code)
        if region_id is None:
            raise ValueError(f"Unknown region code: {region_code}")

        description = data.get("description", "") or ""

        request_id = await saff_orders_technician_create(
            user_id=user_id,
            phone=acting_client.get("phone"),
            abonent_id=str(client_user_id),
            region=region_id,
            address=data.get("address", "Kiritilmagan"),
            description=description,
        )

        text = (
            "✅ <b>Texnik xizmat arizasi yaratildi</b>\n\n"
            f"🆔 Ariza raqami: <code>{request_id}</code>\n"
            f"📍 Region: {region_code.replace('_', ' ').title()}\n"
            f"📞 Tel: {acting_client.get('phone','-')}\n"
            f"🏠 Manzil: {data.get('address','-')}\n"
            f"📝 Muammo: {description or '-'}\n"
            if lang == "uz"
            else
            "✅ <b>Заявка на техобслуживание создана</b>\n\n"
            f"🆔 Номер заявки: <code>{request_id}</code>\n"
            f"📍 Регион: {region_code.replace('_', ' ').title()}\n"
            f"📞 Тел: {acting_client.get('phone','-')}\n"
            f"🏠 Адрес: {data.get('address','-')}\n"
            f"📝 Проблема: {description or '-'}\n"
        )

        await callback.message.answer(
            text,
            reply_markup=get_call_center_supervisor_main_menu(),
            parse_mode="HTML",
        )
        await state.clear()

    except Exception as e:
        logger.exception("Operator technical confirm error: %s", e)
        await callback.answer(
            "Xatolik yuz berdi" if lang == "uz" else "Произошла ошибка",
            show_alert=True
        )

# ======================= STEP 7: resend =======================
@router.callback_query(F.data == "resend_zayavka_call_center_tech_service", StateFilter(SaffTechnicianOrderStates.confirming_connection))
async def op_resend(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    await callback.answer(
        "🔄 Ma'lumotlar qayta ko‘rsatildi." if lang == "uz" else "🔄 Данные показаны снова."
    )
    await op_show_summary(callback, state)
