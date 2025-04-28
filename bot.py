
import os
import subprocess
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

# تثبيت المتطلبات تلقائيًا
try:
    import yt_dlp
except ImportError:
    os.system('pip install yt-dlp')

try:
    import pyrogram
except ImportError:
    os.system('pip install pyrogram tgcrypto')

# بيانات البوت
api_id = 20132946
api_hash = "35292231aa5077cc01bd269ba11a593a"
bot_token = "8145879704:AAFL1s5R5vANDfQPdnXTLkqCuI4yBO75mCc"

app = Client("youtube_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "أهلاً بيك!\n\nابعت رابط يوتيوب، واختار الجودة اللي تحبها لتحميل الفيديو أو الصوت.",
    )

@app.on_message(filters.text & filters.private)
async def handle_url(client, message):
    url = message.text.strip()
    if not ("youtu.be" in url or "youtube.com" in url):
        await message.reply("من فضلك ابعت رابط يوتيوب صحيح.")
        return

    await message.reply(
        "اختار الجودة اللي تحبها:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("1080p", callback_data=f"1080p|{url}")],
            [InlineKeyboardButton("720p", callback_data=f"720p|{url}")],
            [InlineKeyboardButton("360p", callback_data=f"360p|{url}")],
            [InlineKeyboardButton("صوت MP3", callback_data=f"audio|{url}")],
        ])
    )

@app.on_callback_query()
async def download_video(client, callback_query):
    choice, url = callback_query.data.split("|")
    await callback_query.message.edit_text("جاري التحميل...")

    if choice == "audio":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "downloaded.%(ext)s",
            "postprocessors": [
                {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"},
            ],
        }
    else:
        ydl_opts = {
            "format": f"bestvideo[height<={choice[:-1]}]+bestaudio/best",
            "outtmpl": "downloaded.%(ext)s",
            "merge_output_format": "mp4"
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if choice == "audio":
                filename = filename.rsplit(".", 1)[0] + ".mp3"

        if choice == "audio":
            await callback_query.message.reply_audio(filename, caption="اتفضل الصوت!")
        else:
            await callback_query.message.reply_video(filename, caption="اتفضل الفيديو!")

        os.remove(filename)

    except Exception as e:
        await callback_query.message.edit_text(f"حصل خطأ: {e}")

app.run()
