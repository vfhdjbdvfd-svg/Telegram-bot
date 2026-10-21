import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

# 1. إعداد سيرفر وهمي لإبقاء Render شغال
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot @WindowsApp_bot is Online 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. إعدادات البوت والبيانات
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 8247949817
ADMIN_USERNAME = "lo683_3"

user_ids = set()

def is_admin(user) -> bool:
    if user.id == ADMIN_ID or (user.username and user.username.lower() == ADMIN_USERNAME.lower()):
        return True
    return False

# الأوامر والردود
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_ids.add(user.id)
    
    keyboard = [
        [
            InlineKeyboardButton("📢 القناة الرسمية", url="https://t.me/telegram"),
            InlineKeyboardButton("💬 التواصل مع الأدمن", url=f"https://t.me/{ADMIN_USERNAME}")
        ],
        [
            InlineKeyboardButton("ℹ️ حول البوت", callback_data="about_bot")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"أهلاً بك يا **{user.first_name}** في بوت **@WindowsApp_bot** 🚀\n\nأنا أعمل الآن بنجاح 24/7!",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not is_admin(user):
        await update.message.reply_text("⚠️ عذراً! هذه اللوحة مخصصة للأدمن فقط.")
        return

    admin_keyboard = [
        [InlineKeyboardButton("📊 عدد المشتركين", callback_data="count_users")]
    ]
    reply_markup = InlineKeyboardMarkup(admin_keyboard)
    await update.message.reply_text("👑 **أهلاً بك في لوحة تحكم الأدمن:**", reply_markup=reply_markup, parse_mode="Markdown")

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "about_bot":
        await query.edit_message_text("🤖 بوت تطبيقات ويندوز يعمل على مدار الساعة.")
    elif query.data == "count_users" and is_admin(query.from_user):
        await query.edit_message_text(f"📊 إجمالي المشتركين: **{len(user_ids)}**", parse_mode="Markdown")

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user_ids.add(update.effective_user.id)

    if any(word in text for word in ["مرحبا", "هلا", "السلام عليكم"]):
        await update.message.reply_text("وعليكم السلام وأهلاً بك! كيف يمكنني مساعدتك؟")
    else:
        await update.message.reply_text("شكراً لتواصلك! تم استلام رسالتك.")

def main():
    # تشغيل السيرفر في مسار منفصل (Thread)
    threading.Thread(target=run_flask, daemon=True).start()

    # تشغيل البوت بنظام Polling
    telegram_app = ApplicationBuilder().token(TOKEN).build()

    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("admin", admin_panel))
    telegram_app.add_handler(CallbackQueryHandler(button_click))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    print("البوت يعمل الآن بنجاح...")
    telegram_app.run_polling()

if __name__ == "__main__":
    main()
