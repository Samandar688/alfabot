from aiogram import Router, F
from aiogram.types import Message, FSInputFile
import os

router = Router()

@router.message(F.text.in_(["📄 Bot qo'llanmasi", "📄Инструкция по использованию бота"]))
async def bot_guide_handler(message: Message):
    # Video faylni yuborish
    video_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "media", "uztelecom.MP4")
    
    if os.path.exists(video_path):
        video = FSInputFile(video_path)
        
        # Chiroyli matn va hashtag bilan
        caption = """🛜 **UZTELECOM RASMIY BOTI**

✨ *Bizning bot orqali siz quyidagi xizmatlardan foydalanishingiz mumkin:*

🔧 **Texnik xizmat** - Muammolaringizni tez hal qiling
📞 **Ulanish buyurtmasi** - Yangi ulanish uchun ariza bering  
📋 **Buyurtmalarim** - Barcha arizalaringizni kuzatib boring
👤 **Profil** - Shaxsiy ma'lumotlaringizni boshqaring
📞 **Aloqa** - Bizning xizmat markazimiz bilan bog'laning

💡 *Bot 24/7 ishlaydi va sizning barcha so'rovlaringizni tezkor qayta ishlaydi!*

🌟 **Bizning afzalliklarimiz:**
• Tezkor xizmat ko'rsatish
• Professional yondashuv  
• Sifatli texnik yordam
• Doimiy qo'llab-quvvatlash

#UzTelecom #RasmiyBot #TexnikXizmat #Ulanish #Buyurtma #OnlineXizmat #Toshkent """
        
        await message.answer_video(
            video=video,
            caption=caption,
            parse_mode="Markdown"
        )
    else:
        # Agar video topilmasa, faqat matn yuborish
        text = """🛜 **UZTELECOM RASMIY BOTI**

✨ *Bizning bot orqali siz quyidagi xizmatlardan foydalanishingiz mumkin:*

🔧 **Texnik xizmat** - Muammolaringizni tez hal qiling
📞 **Ulanish buyurtmasi** - Yangi ulanish uchun ariza bering  
📋 **Buyurtmalarim** - Barcha arizalaringizni kuzatib boring
👤 **Profil** - Shaxsiy ma'lumotlaringizni boshqaring
📞 **Aloqa** - Bizning xizmat markazimiz bilan bog'laning

💡 *Bot 24/7 ishlaydi va sizning barcha so'rovlaringizni tezkor qayta ishlaydi!*

🌟 **Bizning afzalliklarimiz:**
• Tezkor xizmat ko'rsatish
• Professional yondashuv  
• Sifatli texnik yordam
• Doimiy qo'llab-quvvatlash

#UzTelecom #RasmiyBot #TexnikXizmat #Ulanish #Buyurtma #OnlineXizmat #Toshkent """
        
        await message.answer(text, parse_mode="Markdown")
