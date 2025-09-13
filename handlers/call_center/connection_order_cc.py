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
from keyboards.call_center_buttons import (
    get_call_center_main_keyboard,
    zayavka_type_keyboard,                # connection type (b2c/b2b)
    get_client_regions_keyboard,          # region selector
    confirmation_keyboard,                # confirm/resend with confirm_zayavka_call_center
    get_operator_tariff_selection_keyboard,  # NEW: operator-only tariff keyboard (op_tariff_*)
)

# === States ===
from states.call_center_states import SaffConnectionOrderStates

# === DB functions ===
from database.call_center_operator_queries import (
    find_user_by_phone,
    saff_orders_create,
    get_or_create_tarif_by_code,
)
from database.client_queries import ensure_user

# === Role filter ===
from filters.role_filter import RoleFilter

logger = logging.getLogger(__name__)

router = Router()
router.message.filter(RoleFilter("callcenter_operator"))
router.callback_query.filter(RoleFilter("callcenter_operator"))

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

def strip_op_prefix_to_tariff(code: str | None) -> str | None:
    """
    op_tariff_xxx -> tariff_xxx  (we persist normalized code to state/DB helpers)
    """
    if not code:
        return None
    return "tariff_" + code[len("op_tariff_"):] if code.startswith("op_tariff_") else code

# Region code -> numeric id mapping expected by DB (saff_orders.region INTEGER)
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
    if not region_code:
        return None
    return REGION_CODE_TO_ID.get(region_code)

# ======================= ENTRY (reply buttons) =======================
UZ_ENTRY_TEXT = "🔌 Ulanish arizasi yaratish"
RU_ENTRY_TEXT = "🔌 Создать заявку на подключение"  # optional RU support

@router.message(F.text.in_([UZ_ENTRY_TEXT, RU_ENTRY_TEXT]))
async def op_start_text(msg: Message, state: FSMContext):
    """
    Operator starts connection request creation via reply-button.
    """
    await state.clear()
    await state.set_state(SaffConnectionOrderStates.waiting_client_phone)
    await msg.answer(
        "📞 Mijoz telefon raqamini kiriting (masalan, +998901234567):",
        reply_markup=ReplyKeyboardRemove(),
    )

# ======================= STEP 1: phone lookup =======================
@router.message(StateFilter(SaffConnectionOrderStates.waiting_client_phone))
async def op_get_phone(msg: Message, state: FSMContext):
    phone_n = normalize_phone(msg.text)
    if not phone_n:
        return await msg.answer("❗️ Noto'g'ri format. Masalan: +998901234567")

    user = await find_user_by_phone(phone_n)
    if not user:
        return await msg.answer("❌ Bu raqam bo'yicha foydalanuvchi topilmadi. To'g'ri raqam yuboring.")

    await state.update_data(acting_client=user)  # store client dict

    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Davom etish ▶️", callback_data="op_conn_continue")]]
    )
    text = (
        "👤 Mijoz topildi:\n"
        f"• ID: <b>{user.get('id','')}</b>\n"
        f"• F.I.Sh: <b>{user.get('full_name','')}</b>\n"
        f"• Tel: <b>{user.get('phone','')}</b>\n\n"
        "Davom etish uchun tugmani bosing."
    )
    await msg.answer(text, parse_mode="HTML", reply_markup=kb)

# ======================= STEP 2: region =======================
@router.callback_query(StateFilter(SaffConnectionOrderStates.waiting_client_phone), F.data == "op_conn_continue")
async def op_after_confirm_user(cq: CallbackQuery, state: FSMContext):
    await cq.message.edit_reply_markup()
    await cq.message.answer("🌍 Regionni tanlang:", reply_markup=get_client_regions_keyboard())
    await state.set_state(SaffConnectionOrderStates.selecting_region)
    await cq.answer()

@router.callback_query(F.data.startswith("region_"), StateFilter(SaffConnectionOrderStates.selecting_region))
async def op_select_region(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()

    region_code = callback.data.replace("region_", "", 1)   # e.g. toshkent_city
    await state.update_data(selected_region=region_code)

    await callback.message.answer("🔌 Ulanish turini tanlang:", reply_markup=zayavka_type_keyboard())
    await state.set_state(SaffConnectionOrderStates.selecting_connection_type)

# ======================= STEP 3: connection type =======================
@router.callback_query(F.data.startswith("zayavka_type_"), StateFilter(SaffConnectionOrderStates.selecting_connection_type))
async def op_select_connection_type(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()

    connection_type = callback.data.split("_")[-1]  # 'b2c' or 'b2b'
    await state.update_data(connection_type=connection_type)

    await callback.message.answer(
        "📋 <b>Tariflardan birini tanlang:</b>",
        reply_markup=get_operator_tariff_selection_keyboard(),  # operator-only keyboard
        parse_mode="HTML",
    )
    await state.set_state(SaffConnectionOrderStates.selecting_tariff)

# ======================= STEP 4: tariff (OP-ONLY callbacks) =======================
@router.callback_query(
    StateFilter(SaffConnectionOrderStates.selecting_tariff),
    F.data.startswith("op_tariff_")
)
async def op_select_tariff(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()

    # Example in: op_tariff_xammasi_birga_3_plus  ->  out: tariff_xammasi_birga_3_plus
    normalized_code = strip_op_prefix_to_tariff(callback.data)
    await state.update_data(selected_tariff=normalized_code)

    await callback.message.answer("🏠 Manzilingizni kiriting:")
    await state.set_state(SaffConnectionOrderStates.entering_address)

# ======================= STEP 5: address =======================
@router.message(StateFilter(SaffConnectionOrderStates.entering_address))
async def op_get_address(msg: Message, state: FSMContext):
    address = (msg.text or "").strip()
    if not address:
        return await msg.answer("❗️ Iltimos, manzilni kiriting.")
    await state.update_data(address=address)
    await op_show_summary(msg, state)  # direct summary

# ======================= STEP 6: summary =======================
async def op_show_summary(target, state: FSMContext):
    data = await state.get_data()
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
    )

    if hasattr(target, "answer"):
        await target.answer(text, parse_mode="HTML", reply_markup=confirmation_keyboard())
    else:
        await target.message.answer(text, parse_mode="HTML", reply_markup=confirmation_keyboard())

    await state.set_state(SaffConnectionOrderStates.confirming_connection)

# ======================= STEP 7: confirm / resend =======================
@router.callback_query(F.data == "confirm_zayavka_call_center", StateFilter(SaffConnectionOrderStates.confirming_connection))
async def op_confirm(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_reply_markup()
        data = await state.get_data()

        acting_client = data.get("acting_client")  # dict from phone lookup
        if not acting_client:
            return await callback.answer("Mijoz tanlanmagan", show_alert=True)

        client_user_id = acting_client["id"]
        user_row = await ensure_user(callback.from_user.id, callback.from_user.full_name, callback.from_user.username)
        user_id = user_row["id"]
        region_code = (data.get("selected_region") or "toshkent_city").lower()
        tariff_code = data.get("selected_tariff")  # already normalized: tariff_xammasi_birga_*
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

        await callback.message.answer(
            (
                "✅ <b>Ariza yaratildi (mijoz nomidan)</b>\n\n"
                f"🆔 Ariza raqami: <code>{request_id}</code>\n"
                f"📍 Region: {region_code.replace('_', ' ').title()}\n"
                f"💳 Tarif: {tariff_code or '-'}\n"
                f"📞 Tel: {acting_client.get('phone','-')}\n"
                f"🏠 Manzil: {data.get('address','-')}\n"
            ),
            reply_markup=get_call_center_main_keyboard(),
            parse_mode="HTML",
        )
        await state.clear()
    except Exception as e:
        logger.exception("Operator confirm error: %s", e)
        await callback.answer("Xatolik yuz berdi", show_alert=True)

@router.callback_query(F.data == "resend_zayavka_call_center", StateFilter(SaffConnectionOrderStates.confirming_connection))
async def op_resend(callback: CallbackQuery, state: FSMContext):
    await callback.answer("🔄 Ma'lumotlar qayta ko‘rsatildi.")
    await op_show_summary(callback, state)
