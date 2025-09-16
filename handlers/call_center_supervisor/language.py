from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database.models import User
from database.database import get_session

router = Router()

@router.message(F.text.in_(["🌐 Tilni o'zgartirish", "🌐 Изменить язык"]))
async def language_handler(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇿 O'zbek tili", callback_data="lang_uz")],
        [InlineKeyboardButton(text="🇷🇺 Русский язык", callback_data="lang_ru")]
    ])
    await message.answer("🌐 Tilni tanlang / Выберите язык:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("lang_"))
async def language_callback_handler(callback: CallbackQuery):
    language = callback.data.split("_")[1]
    user_id = callback.from_user.id
    
    try:
        async with get_session() as session:
            user = await session.get(User, user_id)
            if user:
                user.language = language
                await session.commit()
                
                if language == "uz":
                    text = "✅ Til muvaffaqiyatli o'zgartirildi!\n\n👤 Rol: Call Center Supervisor"
                else:
                    text = "✅ Язык успешно изменен!\n\n👤 Роль: Call Center Supervisor"
                
                await callback.message.delete()
                await callback.message.answer(text)
            else:
                await callback.message.edit_text("❌ Xatolik yuz berdi / Произошла ошибка")
    except Exception as e:
        await callback.message.edit_text("❌ Xatolik yuz berdi / Произошла ошибка")
    
    await callback.answer()
