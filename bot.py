import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# التوكن من BotFather والمتغيرات البيئية
TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", "8443"))
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")

app = Flask(__name__)
telegram_app = None

# رسالة عند إرسال /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! بوت @WindowsApp_bot يعمل الآن بنجاح 24/7 🚀")

async def init_bot():
    global telegram_app
    telegram_app = ApplicationBuilder().token(TOKEN).build()
    telegram_app.add_handler(CommandHandler("start", start))
    await telegram_app.initialize()
    
    # ربط الـ Webhook مع سيرفر Render
    if RENDER_EXTERNAL_URL:
        webhook_url = f"{RENDER_EXTERNAL_URL}/{TOKEN}"
        await telegram_app.bot.set_webhook(url=webhook_url)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    if telegram_app:
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        asyncio.run(telegram_app.process_update(update))
    return "OK", 200

@app.route("/")
def index():
    return "Bot @WindowsApp_bot is active!", 200

if __name__ == "__main__":
    asyncio.run(init_bot())
    app.run(host="0.0.0.0", port=PORT)
