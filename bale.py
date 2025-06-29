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
    """
    اگر پیام حاوی 'dl' ریپلای به یک پیام دیگر بود و آن پیامْ مدیا داشت،
    مدیا را دانلود و سپس در Saved Messages آپلود می‌کنیم.
    """
    # مطمئن شویم کاربر واقعاً ریپلای کرده است
    if not event.is_reply:
        return

    reply_msg = await event.get_reply_message()

    # فقط وقتی مدیا وجود دارد
    if not reply_msg.media:
        await event.reply("❌ این پیام هیچ مدیایی ندارد.")
        return

    # دانلود در یک فولدر موقت (Telethon خودش فولدر downloads می‌سازد)
    temp_path = await reply_msg.download_media()
    try:
        # ارسال به «پیام‌های ذخیره شده»
        await client.send_file(
            "me",                # معادل Saved Messages
            temp_path,
            caption=f"📥 ذخیره‌شده از {event.chat.title or 'PM'}\n🆔 {reply_msg.id}"
        )
    finally:
        # پاک‌سازی فایل موقتی
        try:
            os.remove(temp_path)
        except OSError:
            pass


async def main():
    print(">>> کلاینت آماده است؛ Ctrl+C برای خروج")
    await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        asyncio.run(main())
