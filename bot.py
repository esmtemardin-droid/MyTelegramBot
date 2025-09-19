from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import random, requests

# لیست جوک‌ها
jokes = [
    "می‌دونی چرا کتاب ریاضی همیشه غمگینه؟ چون پر از مسئله‌ست! 📚😂",
    "یه مورچه میره کافی‌شاپ، میگن چی می‌خوری؟ میگه یه دونه شکر لطفاً 🐜☕",
    "می‌دونی چرا کامپیوتر همیشه خسته‌س؟ چون همیشه بایت بایت کار می‌کنه 💻😅"
]

# لیست جملات انگیزشی
quotes = [
    "هیچوقت برای شروع دیر نیست 💪",
    "موفقیت از دل تلاش‌های کوچیک ساخته میشه 🚀",
    "وقتی همه میگن نمیشه، یعنی وقتشه که تو ثابت کنی میشه ✨"
]

# API عکس گربه
def get_cat_photo():
    url = "https://api.thecatapi.com/v1/images/search"
    r = requests.get(url).json()
    return r[0]["url"]

# آب‌وهوا
def get_weather(city="Tehran"):
    API_KEY = "8fd93f050ee4bd20ea08b71ff6abb994"  # باید API Key رایگان از openweathermap.org بگیری
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=fa"
    data = requests.get(url).json()
    if data.get("main"):
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"🌤 وضعیت هوا در {city}:\n{desc}, دما: {temp}°C"
    return "❌ نتونستم وضعیت هوا رو بیارم!"

# شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("😂 جوک", callback_data="joke"),
         InlineKeyboardButton("✨ انگیزشی", callback_data="quote")],
        [InlineKeyboardButton("🐱 عکس گربه", callback_data="cat"),
         InlineKeyboardButton("🎶 موزیک", callback_data="music")],
        [InlineKeyboardButton("🎲 بازی تاس", callback_data="dice"),
         InlineKeyboardButton("✂️ سنگ-کاغذ-قیچی", callback_data="rps")],
        [InlineKeyboardButton("🌤 وضعیت هوا", callback_data="weather")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("سلام! 👋 انتخاب کن:", reply_markup=reply_markup)

# هندلر دکمه‌ها
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "joke":
        await query.message.reply_text(random.choice(jokes))
    elif query.data == "quote":
        await query.message.reply_text(random.choice(quotes))
    elif query.data == "cat":
        await query.message.reply_photo(get_cat_photo())
    elif query.data == "music":
        await query.message.reply_audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    elif query.data == "dice":
        dice = random.randint(1, 6)
        await query.message.reply_text(f"🎲 عدد تاس: {dice}")
    elif query.data == "rps":
        choice = random.choice(["✊ سنگ", "✋ کاغذ", "✌ قیچی"])
        await query.message.reply_text(f"انتخاب من: {choice}")
    elif query.data == "weather":
        await query.message.reply_text(get_weather("Tehran"))

def main():
    TOKEN = "8473648131:AAGnEuohCll0ge3IZ2jNyWVZwVU8rUpop7E"  # توکن ربات خودت

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == "__main__":
    main()
