from telegram import Update
from telegram.ext import ContextTypes
from db.database import add_tokens

async def tap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    add_tokens(user_id, "BITS", 10)
    await update.message.reply_text("🪙 You tapped and earned 10 $BITS!")