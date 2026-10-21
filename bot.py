import os
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

# 1. الإعدادات والمتغيرات
TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", "8443"))
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")

# المعرف الخاص بك كأدمن (تم تغييره لـ lo683_3)
ADMIN_USERNAME = "lo683_3"

app = Flask(__name__)
telegram_app = None

# قائمة بحفظ أيدي المستخدمين للوحة التحكم والإذاعة
user_ids = set()

# -------------------- الأوامر والوظائف --------------------

# أمر /start للمستخدمين
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_ids.add(user.id)
    
    # الأزرار التفاعلية الرئيسية للمستخدم
    keyboard = [
        [
            InlineKeyboardButton("📢 القناة الرسمية", url="https://t.me/telegram"),
            InlineKeyboardButton("💬 التواصل مع الأدمن", url=f"https://t.me/{ADMIN_USERNAME}")
        ],
        [
            InlineKeyboardButton("ℹ️ حول البوت", callback_data="about_bot")
        ]
    ]
