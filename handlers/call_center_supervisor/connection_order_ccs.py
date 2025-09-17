# handlers/call_center/connection_order_cc.py

from datetime import datetime
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
    zayavka_type_keyboard,                # connection type (b2c/b2b)
    get_client_regions_keyboard,          # region selector
    confirmation_keyboard,                # confirm/resend with confirm_zayavka_call_center
    get_operator_tariff_selection_keyboard,  # NEW: operator-only tariff keyboard (op_tariff_*)
)

# === States ===
from states.call_center_states import SaffConnectionOrderStates

# === DB functions ===
from database.call_center_supervisor_queries import (
    find_user_by_phone,
    saff_orders_create,
    get_or_create_tarif_by_code,
)
from database.client_queries import ensure_user

# === Role filter ===
from filters.role_filter import RoleFilter

logger = logging.getLogger(__name__)

router = Router()
router.message.filter(RoleFilter("callcenter_supervisor"))
router.callback_query.filter(RoleFilter("callcenter_supervisor"))

# ----------------------- helpers -----------------------
PHONE_RE = re.compile(r"^\+998\d{9}$")  # aniqroq variant

def normalize_phone(phone_raw: str) -> str | None:
    phone_raw = (phone_raw or "").strip()
    digits = re.sub(r"\D", "", phone_raw)
    if digits.startswith("998") and len(digits) == 12:
        return "+" + digits
    if len(digits) == 9:
        return "+998" + digits
    return phone_raw if phone_raw.startswith("+998") and len(digits) == 12 else None

def strip_op_prefix_to_tariff(code: str | None) -> str | None:
    return "tariff_" + code[len("op_tariff_"):] if code and code.startswith("op_tariff_") else code

REGION_CODE_TO_ID: dict[str, int] = {
    "toshkent_city": 1,
    "toshkent_region": 2,
    "andijon": 3,
    "fergana": 4,
    "namangan": 5,
    "sirdaryo": 6,
    "jizzax": 7,
    "samarkand": 8,
    "bukhara": 9,
    "navoi": 10,
    "kashkadarya": 11,
    "surkhandarya": 12,
    "khorezm": 13,
    "karakalpakstan": 14,
}

def map_region_code_to_id(region_code: str | None) -> int | None:
    return REGION_CODE_TO_ID.get(region_code) if region_code else None

# ======================= ENTRY =======================
UZ_ENTRY_TEXT = "🔌 Ulanish arizasi yaratish"
RU_ENTRY_TEXT = "🔌 Создать заявку на подключение"

@router.message(F.text.in_([UZ_ENTRY_TEXT, RU_ENTRY_TEXT]))
async def op_start_text(msg: Message, state: FSMContext):
    await state.clear()
    lang = "uz" if msg.text == UZ_ENTRY_TEXT else "ru"
    await state.update_data(lang=lang)
    text = (
        "📞 Mijoz telefon raqamini kiriting (masalan, +998901234567):"
        if lang == "uz" else
        "📞 Введите номер телефона клиента (например, +998901234567):"
    )
    await state.set_state(SaffConnectionOrderStates.waiting_client_phone)
    await msg.answer(text, reply_markup=ReplyKeyboardRemove())

# ======================= STEP 1: phone lookup =======================
@router.message(StateFilter(SaffConnectionOrderStates.waiting_client_phone))
async def op_get_phone(msg: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    phone_n = normalize_phone(msg.text)
    if not phone_n:
        return await msg.answer("❗️ Noto'g'ri format. Masalan: +998901234567" if lang == "uz"
                                else "❗️ Неверный формат. Например: +998901234567")

    user = await find_user_by_phone(phone_n)
    if not user:
        return await msg.answer("❌ Bu raqam bo'yicha foydalanuvchi topilmadi." if lang == "uz"
                                else "❌ Пользователь с таким номером не найден.")

    await state.update_data(acting_client=user)
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
            text="Davom etish ▶️" if lang == "uz" else "Продолжить ▶️",
            callback_data="op_conn_continue"
        )]]
    )
    text = (
        "👤 Mijoz topildi:\n"
        f"• ID: <b>{user.get('id','')}</b>\n"
        f"• F.I.Sh: <b>{user.get('full_name','')}</b>\n"
        f"• Tel: <b>{user.get('phone','')}</b>\n\n"
        "Davom etish uchun tugmani bosing."
        if lang == "uz" else
        "👤 Клиент найден:\n"
        f"• ID: <b>{user.get('id','')}</b>\n"
        f"• ФИО: <b>{user.get('full_name','')}</b>\n"
        f"• Тел: <b>{user.get('phone','')}</b>\n\n"
        "Нажмите кнопку, чтобы продолжить."
    )
    await msg.answer(text, parse_mode="HTML", reply_markup=kb)

# ======================= STEP 2: region =======================
@router.callback_query(StateFilter(SaffConnectionOrderStates.waiting_client_phone), F.data == "op_conn_continue")
async def op_after_confirm_user(cq: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    await cq.message.edit_reply_markup()
    text = "🌍 Regionni tanlang:" if lang == "uz" else "🌍 Выберите регион:"
    await cq.message.answer(text, reply_markup=get_client_regions_keyboard())
    await state.set_state(SaffConnectionOrderStates.selecting_region)
    await cq.answer()

@router.callback_query(F.data.startswith("region_"), StateFilter(SaffConnectionOrderStates.selecting_region))
async def op_select_region(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    await callback.answer()
    await callback.message.edit_reply_markup()

    region_code = callback.data.replace("region_", "", 1)
    await state.update_data(selected_region=region_code)

    text = "🔌 Ulanish turini tanlang:" if lang == "uz" else "🔌 Выберите тип подключения:"
    await callback.message.answer(text, reply_markup=zayavka_type_keyboard())
    await state.set_state(SaffConnectionOrderStates.selecting_connection_type)

# ======================= STEP 3: connection type =======================
@router.callback_query(F.data.startswith("zayavka_type_"), StateFilter(SaffConnectionOrderStates.selecting_connection_type))
async def op_select_connection_type(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    await callback.answer()
    await callback.message.edit_reply_markup()

    connection_type = callback.data.split("_")[-1]
    await state.update_data(connection_type=connection_type)

    text = "📋 <b>Tariflardan birini tanlang:</b>" if lang == "uz" else "📋 <b>Выберите один из тарифов:</b>"
    await callback.message.answer(text, reply_markup=get_operator_tariff_selection_keyboard(), parse_mode="HTML")
    await state.set_state(SaffConnectionOrderStates.selecting_tariff)

# ======================= STEP 4: tariff =======================
@router.callback_query(StateFilter(SaffConnectionOrderStates.selecting_tariff), F.data.startswith("op_tariff_"))
async def op_select_tariff(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    await callback.answer()
    await callback.message.edit_reply_markup()

    normalized_code = strip_op_prefix_to_tariff(callback.data)
    await state.update_data(selected_tariff=normalized_code)

    text = "🏠 Manzilingizni kiriting:" if lang == "uz" else "🏠 Введите ваш адрес:"
    await callback.message.answer(text)
    await state.set_state(SaffConnectionOrderStates.entering_address)

# ======================= STEP 5: address =======================
@router.message(StateFilter(SaffConnectionOrderStates.entering_address))
async def op_get_address(msg: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    address = (msg.text or "").strip()
    if not address:
        return await msg.answer("❗️ Iltimos, manzilni kiriting." if lang == "uz" else "❗️ Пожалуйста, введите адрес.")
    await state.update_data(address=address)
    await op_show_summary(msg, state)

# ======================= STEP 6: summary =======================
async def op_show_summary(target, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    region = data.get("selected_region", "-")
    ctype = (data.get("connection_type") or "b2c").upper()
    code_to_name = {
        "tariff_xammasi_birga_4": "Hammasi birga 4",
        "tariff_xammasi_birga_3_plus": "Hammasi birga 3+",
        "tariff_xammasi_birga_3": "Hammasi birga 3",
        "tariff_xammasi_birga_2": "Hammasi birga 2",
    }
    tariff_code = data.get("selected_tariff")
    tariff_display = code_to_name.get(tariff_code, tariff_code or "-")
    address = data.get("address", "-")

    text = (
        f"🗺️ <b>Hudud:</b> {region}\n"
        f"🔌 <b>Ulanish turi:</b> {ctype}\n"
        f"💳 <b>Tarif:</b> {tariff_display}\n"
        f"🏠 <b>Manzil:</b> {address}\n\n"
        "Ma'lumotlar to‘g‘rimi?"
        if lang == "uz" else
        f"🗺️ <b>Регион:</b> {region}\n"
        f"🔌 <b>Тип подключения:</b> {ctype}\n"
        f"💳 <b>Тариф:</b> {tariff_display}\n"
        f"🏠 <b>Адрес:</b> {address}\n\n"
        "Данные верны?"
    )

    if hasattr(target, "answer"):
        await target.answer(text, parse_mode="HTML", reply_markup=confirmation_keyboard())
    else:
        await target.message.answer(text, parse_mode="HTML", reply_markup=confirmation_keyboard())

    await state.set_state(SaffConnectionOrderStates.confirming_connection)

# ======================= STEP 7: confirm =======================
@router.callback_query(F.data == "confirm_zayavka_call_center", StateFilter(SaffConnectionOrderStates.confirming_connection))
async def op_confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    try:
        await callback.message.edit_reply_markup()
        acting_client = data.get("acting_client")
        if not acting_client:
            return await callback.answer("Mijoz tanlanmagan" if lang == "uz" else "Клиент не выбран", show_alert=True)

        client_user_id = acting_client["id"]
        user_row = await ensure_user(callback.from_user.id, callback.from_user.full_name, callback.from_user.username)
        user_id = user_row["id"]

        region_code = (data.get("selected_region") or "toshkent_city").lower()
        tariff_code = data.get("selected_tariff")
        tarif_id = await get_or_create_tarif_by_code(tariff_code) if tariff_code else None

        region_id = map_region_code_to_id(region_code)
        if region_id is None:
            raise ValueError(f"Unknown region code: {region_code}")

        request_id = await saff_orders_create(
            user_id=user_id,
            phone=acting_client.get("phone"),
            abonent_id=str(client_user_id),
            region=region_id,
            address=data.get("address", "Kiritilmagan"),
            tarif_id=tarif_id,
        )

        text = (
            "✅ <b>Ariza yaratildi (mijoz nomidan)</b>\n\n"
            f"🆔 Ariza raqami: <code>{request_id}</code>\n"
            f"📍 Region: {region_code.replace('_', ' ').title()}\n"
            f"💳 Tarif: {tariff_code or '-'}\n"
            f"📞 Tel: {acting_client.get('phone','-')}\n"
            f"🏠 Manzil: {data.get('address','-')}\n"
            if lang == "uz" else
            "✅ <b>Заявка создана (от имени клиента)</b>\n\n"
            f"🆔 Номер заявки: <code>{request_id}</code>\n"
            f"📍 Регион: {region_code.replace('_', ' ').title()}\n"
            f"💳 Тариф: {tariff_code or '-'}\n"
            f"📞 Тел: {acting_client.get('phone','-')}\n"
            f"🏠 Адрес: {data.get('address','-')}\n"
        )

        await callback.message.answer(text, reply_markup=get_call_center_supervisor_main_menu(), parse_mode="HTML")
        await state.clear()
    except Exception as e:
        logger.exception("Operator confirm error: %s", e)
        await callback.answer("Xatolik yuz berdi" if lang == "uz" else "Произошла ошибка", show_alert=True)

@router.callback_query(F.data == "resend_zayavka_call_center", StateFilter(SaffConnectionOrderStates.confirming_connection))
async def op_resend(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    await callback.answer("🔄 Ma'lumotlar qayta ko‘rsatildi." if lang == "uz" else "🔄 Данные показаны повторно.")
    await op_show_summary(callback, state)
