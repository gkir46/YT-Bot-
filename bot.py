
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import yt_dlp
import os

# إعدادات البوت
api_id = 123456  # اكتب ال API ID بتاعك
api_hash = "abc123abc123abc123abc123abc123ab"  # اكتب ال API Hash بتاعك
bot_token = "YOUR_BOT_TOKEN"  # اكتب توكن البوت بتاعك

app = Client("youtube_downloader_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.private & filters.text)
async def ask_download_type(client, message):
    url = message.text.strip()
    if "youtube.com" not in url and "youtu.be" not in url:
        await message.reply("ارسللي رابط يوتيوب صحيح.")
        return

    await message.reply(
        "تحب تحمل ايه؟",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("فيديو", callback_data=f"video|{url}")],
            [InlineKeyboardButton("صوت", callback_data=f"audio|{url}")]
        ])
    )

@app.on_callback_query()
async def callback_handler(client, callback_query: CallbackQuery):
    data = callback_query.data
    choice, url = data.split("|")
    await callback_query.message.edit_text("جاري التحميل... استنى شوية.")

    try:
        if choice == "video":
            ydl_opts = {'format': 'best', 'outtmpl': 'downloaded.%(ext)s'}
        else:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloaded.%(ext)s',
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if choice == "audio":
                filename = filename.rsplit(".", 1)[0] + ".mp3"

        if choice == "video":
            await callback_query.message.reply_video(filename, caption="اتفضل الفيديو!")
        else:
            await callback_query.message.reply_audio(filename, caption="اتفضل الصوت!")

        os.remove(filename)

    except Exception as e:
        await callback_query.message.edit_text(f"حصل خطأ: {str(e)}")

app.run()
