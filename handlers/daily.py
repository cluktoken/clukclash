from telegram import Update
from telegram.ext import ContextTypes
from db.database import give_daily_bonus
from datetime import datetime, timedelta

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = give_daily_bonus(user_id)
    await update.message.reply_text(message)
