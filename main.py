import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

TOKEN = "70217016:AAHgqbjLDHmcYvVXow7fxHJ7-ZzobNKA15Y"
CHANNEL_USERNAME = "@Alpha_252627"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Kanala agza bolmak", url=f"https://t.me/Alpha_252627")],
    ])
    await message.answer(
        "Salam! 👋 @Teeehnoo_bot-a hoş geldiňiz. Bu TikTok wideo ýükleýän bot.\n\n"
        "Boti ulanmagy dowam etmek üçin ilki bilen aşakdaky kanalymyza agza boluň!",
        reply_markup=markup
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "ℹ️ **Kömek:**\n\n"
        "Bota islendik TikTok wideo salgysyny (linkini) iberiň, mende size suw belgisiz görnüşini ýükläp bereyin!"
    )

@dp.message()
async def handle_message(message: types.Message):
    text = message.text
    if text and ("tiktok.com" in text or "vm.tiktok.com" in text):
        waiting_msg = await message.answer("⏳ Wideo ýüklenilýär, biraz garaşyň...")
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.mp4',
            'quiet': True
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)
                video_url = info.get('url', None)
                
            if video_url:
                await message.answer_video(video_url, caption="✅ TikTok wideo üstünlikli ýükl edildi!\n📢 Biziň kanal: @Alpha_252627")
                await waiting_msg.delete()
            else:
                await waiting_msg.edit_text("❌ Wideo tapylmady, linki barlaň.")
        except Exception as e:
            await waiting_msg.edit_text(f"❌ Ýüklemekde ýalňyşlyk ýüze çykdy: {e}")
    else:
        await message.answer("⚠️ Diňe TikTok wideo salgylaryny iberip bilersiňiz!")

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
