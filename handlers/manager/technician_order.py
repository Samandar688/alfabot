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
from keyboards.manager_buttons import (
    get_manager_main_menu,
    get_client_regions_keyboard,          # Region tanlash
    confirmation_keyboard_tech_service,   # confirm/resend (tech service)
)

# === States ===
from states.manager_states import SaffTechnicianOrderStates

# === DB ===
from database.manager_connection_queries import (
    find_user_by_phone,   # user lookup
    saff_orders_technician_create,        # texnik xizmat arizasi yaratish
)
from database.client_queries import ensure_user

# === Role filter ===
from filters.role_filter import RoleFilter

logger = logging.getLogger(__name__)

router = Router()
router.message.filter(RoleFilter("manager"))
router.callback_query.filter(RoleFilter("manager"))

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

# Region code -> numeric id mapping (saff_orders.region INTEGER)
REGION_CODE_TO_ID = {
    "toshkent_city": 1, "toshkent_region": 2, "andijon": 3, "fergana": 4, "namangan": 5,
    "sirdaryo": 6, "jizzax": 7, "samarkand": 8, "bukhara": 9, "navoi": 10,
    "kashkadarya": 11, "surkhandarya": 12, "khorezm": 13, "karakalpakstan": 14,
}

def map_region_code_to_id(region_code: str | None) -> int | None:
    if not region_code:
        return None
    return REGION_CODE_TO_ID.get(region_code)

# 🔙 Telefon bosqichiga qaytish uchun inline klaviatura
def back_to_phone_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Orqaga", callback_data="op_tservice_back_to_phone")]]
    )

# ======================= ENTRY (reply button) =======================
UZ_ENTRY_TEXT = "🔧 Texnik xizmat yaratish"
RU_ENTRY_TEXT = "🛠 Создать заявку на техобслуживание"

@router.message(F.text.in_([UZ_ENTRY_TEXT, RU_ENTRY_TEXT]))
async def op_start_text(msg: Message, state: FSMContext):
    await state.clear()
    await state.set_state(SaffTechnicianOrderStates.waiting_client_phone)
    await msg.answer(
        "📞 Mijoz telefon raqamini kiriting (masalan, +998901234567):",
        reply_markup=ReplyKeyboardRemove()
    )

# ======================= STEP 1: phone lookup =======================
@router.message(StateFilter(SaffTechnicianOrderStates.waiting_client_phone))
async def op_get_phone(msg: Message, state: FSMContext):
    phone_n = normalize_phone(msg.text)
    if not phone_n:
        return await msg.answer(
            "❗️ Noto'g'ri format. Masalan: +998901234567",
            reply_markup=back_to_phone_kb()
        )

    user = await find_user_by_phone(phone_n)
    if not user:
        return await msg.answer(
            "❌ Bu raqam bo'yicha foydalanuvchi topilmadi. To'g'ri raqam yuboring.",
            reply_markup=back_to_phone_kb()
        )

    await state.update_data(acting_client=user)
    # Topildi — Davom etish + Orqaga yonma-yon
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Davom etish ▶️", callback_data="op_tservice_continue"),
        InlineKeyboardButton(text="🔙 Orqaga",       callback_data="op_tservice_back_to_phone"),
    ]])
    text = (
        "👤 Mijoz topildi:\n"
        f"• ID: <b>{user.get('id','')}</b>\n"
        f"• F.I.Sh: <b>{user.get('full_name','')}</b>\n"
        f"• Tel: <b>{user.get('phone','')}</b>\n\n"
        "Davom etish yoki orqaga qaytishni tanlang."
    )
    await msg.answer(text, parse_mode="HTML", reply_markup=kb)

# 🔙 Har qayerdan telefon bosqichiga qaytarish
@router.callback_query(F.data == "op_tservice_back_to_phone")
async def tservice_back_to_phone(cq: CallbackQuery, state: FSMContext):
    await cq.answer("Telefon bosqichiga qaytdik")
    try:
        await cq.message.edit_reply_markup()
    except Exception:
        pass
    await state.clear()
    await state.set_state(SaffTechnicianOrderStates.waiting_client_phone)
    await cq.message.answer(
        "📞 Mijoz telefon raqamini kiriting (masalan, +998901234567):",
        reply_markup=ReplyKeyboardRemove()
    )

# ======================= STEP 2: region =======================
@router.callback_query(StateFilter(SaffTechnicianOrderStates.waiting_client_phone), F.data == "op_tservice_continue")
async def op_after_confirm_user(cq: CallbackQuery, state: FSMContext):
    await cq.message.edit_reply_markup()
    await cq.message.answer("🌍 Regionni tanlang:", reply_markup=get_client_regions_keyboard())
    await state.set_state(SaffTechnicianOrderStates.selecting_region)
    await cq.answer()

@router.callback_query(F.data.startswith("region_"), StateFilter(SaffTechnicianOrderStates.selecting_region))
async def op_select_region(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()
    region_code = callback.data.replace("region_", "", 1)
    await state.update_data(selected_region=region_code)

    # STEP 3: description
    await callback.message.answer("📝 Muammoni qisqacha ta'riflab bering (description):")
    await state.set_state(SaffTechnicianOrderStates.problem_description)

# ======================= STEP 3: description =======================
@router.message(StateFilter(SaffTechnicianOrderStates.problem_description))
async def op_get_description(msg: Message, state: FSMContext):
    desc = (msg.text or "").strip()
    if not desc or len(desc) < 5:
        return await msg.answer("❗️ Iltimos, muammoni aniqroq yozing (kamida 5 belgi).")
    await state.update_data(description=desc)

    # Next: address
    await msg.answer("🏠 Manzilingizni kiriting:")
    await state.set_state(SaffTechnicianOrderStates.entering_address)

# ======================= STEP 4: address =======================
@router.message(StateFilter(SaffTechnicianOrderStates.entering_address))
async def op_get_address(msg: Message, state: FSMContext):
    address = (msg.text or "").strip()
    if not address:
        return await msg.answer("❗️ Iltimos, manzilni kiriting.")
    await state.update_data(address=address)
    await op_show_summary(msg, state)

# ======================= STEP 5: summary =======================
async def op_show_summary(target, state: FSMContext):
    data = await state.get_data()
    region = data.get("selected_region", "-")
    address = data.get("address", "-")
    description = data.get("description", "-")

    text = (
        f"🗺️ <b>Hudud:</b> {region}\n"
        f"🛠 <b>Xizmat turi:</b> Texnik xizmat\n"
        f"📝 <b>Ta'rif:</b> {description}\n"
        f"🏠 <b>Manzil:</b> {address}\n\n"
        "Ma'lumotlar to‘g‘rimi?"
    )

    kb = confirmation_keyboard_tech_service()
    if hasattr(target, "answer"):
        await target.answer(text, parse_mode="HTML", reply_markup=kb)
    else:
        await target.message.answer(text, parse_mode="HTML", reply_markup=kb)

    await state.set_state(SaffTechnicianOrderStates.confirming_connection)

# ======================= STEP 6: confirm / resend =======================
@router.callback_query(
    F.data == "confirm_zayavka_call_center_tech_service",
    StateFilter(SaffTechnicianOrderStates.confirming_connection)
)
async def op_confirm(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_reply_markup()
        data = await state.get_data()

        acting_client = data.get("acting_client")
        if not acting_client:
            return await callback.answer("Mijoz tanlanmagan", show_alert=True)

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

        await callback.message.answer(
            (
                "✅ <b>Texnik xizmat arizasi yaratildi</b>\n\n"
                f"🆔 Ariza raqami: <code>{request_id}</code>\n"
                f"📍 Region: {region_code.replace('_', ' ').title()}\n"
                f"📞 Tel: {acting_client.get('phone','-')}\n"
                f"🏠 Manzil: {data.get('address','-')}\n"
                f"📝 Muammo: {description or '-'}\n"
            ),
            reply_markup=get_manager_main_menu(),
            parse_mode="HTML",
        )
        await state.clear()
    except Exception as e:
        logger.exception("Operator technical confirm error: %s", e)
        await callback.answer("Xatolik yuz berdi", show_alert=True)

@router.callback_query(
    F.data == "resend_zayavka_call_center_tech_service",
    StateFilter(SaffTechnicianOrderStates.confirming_connection)
)
async def op_resend(callback: CallbackQuery, state: FSMContext):
    """
    Qayta yuborish: jarayonni REGION tanlashdan qayta boshlaydi.
    Telefon bo'yicha acting_client saqlanib qoladi.
    """
    await callback.answer("🔄 Qaytadan boshladik")
    try:
        await callback.message.edit_reply_markup()
    except Exception:
        pass

    data = await state.get_data()
    acting_client = data.get("acting_client")
    await state.clear()
    if acting_client:
        await state.update_data(acting_client=acting_client)

    await state.set_state(SaffTechnicianOrderStates.selecting_region)
    await callback.message.answer("🌍 Regionni tanlang:", reply_markup=get_client_regions_keyboard())
