from telegram import Update
from telegram.ext import ContextTypes
from db.database import add_tokens

async def passive_income(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    add_tokens(user_id, "BITS", 5)
    await update.message.reply_text("🛌 You earned 5 passive $BITS while idling!")