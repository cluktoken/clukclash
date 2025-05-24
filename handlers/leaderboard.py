from telegram import Update
from telegram.ext import ContextTypes
from db.database import get_leaderboard

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    leaders = get_leaderboard()
    message = "🏆 Top Players:\n"
    for idx, (user, value) in enumerate(leaders):
        message += f"{idx+1}. {user}: ${value:.2f}\n"
    await update.message.reply_text(message)