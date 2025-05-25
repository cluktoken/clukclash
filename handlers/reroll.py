from telegram import Update
from telegram.ext import ContextTypes

async def reroll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎲 Reroll feature coming soon!")
