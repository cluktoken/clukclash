from telegram import Update
from telegram.ext import ContextTypes
from db.database import get_xp, level_up

async def levelup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    xp, level = get_xp(user_id)
    if xp < 100:
        await update.message.reply_text("🔒 You need at least 100 XP to level up!")
        return

    new_level = level_up(user_id)
    await update.message.reply_text(f"🎉 Level up! You are now Level {new_level}!")