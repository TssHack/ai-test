# save_media_to_savedmessages.py
import os
import asyncio
from telethon import TelegramClient, events

# ──────────── مشخصات حساب ────────────
api_id   = 18377832          # ← api_id خودتان
api_hash = "ed8556c450c6d0fd68912423325dd09c"   # ← api_hash خودتان
session_name = "my_session"  # نام فایل سشن (هر اسم دلخواه)

client = TelegramClient(session_name, api_id, api_hash)


@client.on(events.NewMessage(pattern=r'^dl$', incoming=True))
async def save_media(event):
    if not event.is_reply:
        await event.reply("❌ لطفاً روی یک پیام مدیادار ریپلای کنید.")
        return

    reply_msg = await event.get_reply_message()
    if not reply_msg.media:
        await event.reply("❌ این پیام هیچ مدیایی ندارد.")
        return

    temp_path = await reply_msg.download_media()
    try:
        await client.send_file(
            'me',
            temp_path,
            caption=f"📥 ذخیره‌شده از چت: {event.chat.title or 'Private Chat'}"
        )
        await event.reply("✅ مدیا در پیام‌های ذخیره‌شده ذخیره شد.")
    finally:
        try:
            os.remove(temp_path)
        except Exception:
            pass

# ───── اجرای اصلی ─────
print("✅ کلاینت آماده است؛ Ctrl+C برای خروج")
client.start()
client.run_until_disconnected()
