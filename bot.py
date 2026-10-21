import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

# الحصول على التوكن
TOKEN = os.environ.get("BOT_TOKEN")

# بيانات الأدمن
ADMIN_ID = 8247949817
ADMIN_USERNAME = "lo683_3"

user_ids = set()

def is_admin(user) -> bool:
    if user.id == ADMIN_ID or (user.username and user.username.lower() == ADMIN_USERNAME.lower()):
        return True
    return False

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
        f"أهلاً بك يا **{user.first_name}** في بوت **@WindowsApp_bot** 🚀\n\nأنا أعمل الآن بنجاح!",
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
        await query.edit_message_text("🤖 بوت يعمل 24/7 لخدمة تطبيقات ويندوز.")
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
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
