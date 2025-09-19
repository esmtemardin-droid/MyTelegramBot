# bot.py
import os
import asyncio
from aiohttp import web
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

# ======= تنظیمات =======
TOKEN = "8473648131:AAGnEuohCll0ge3IZ2jNyWVZwVU8rUpop7E"  # ← اینجا توکن رباتت رو بذار
PORT = int(os.environ.get("PORT", 5000))  # Render به طور خودکار پورت می‌ده

# ======= فرمان /start =======
async def start(update: Update, context):
    await update.message.reply_text("ربات من آنلاین است 😎")

# ======= ساخت ربات =======
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

# ======= Web Server ساده برای Render =======
async def handle(request):
    return web.Response(text="Bot is running!")

web_app = web.Application()
web_app.add_routes([web.get('/', handle)])

async def start_webserver():
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"Web server running on port {PORT}")

# ======= اجرای همزمان ربات و Web Server =======
async def main():
    await start_webserver()
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
