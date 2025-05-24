from telegram import Update
from telegram.ext import ContextTypes
from db.database import add_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or "Anonymous"
    add_user(user_id, username)
    await update.message.reply_text("👋 Welcome to Crypto Clash! Use /tap to earn tokens and /market to see prices.")