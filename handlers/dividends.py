from telegram import Update
from telegram.ext import ContextTypes
from db.database import get_user_portfolio, add_tokens

async def dividends(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bits, _ = get_user_portfolio(user_id)
    reward = bits * 0.02  # 2% passive income
    add_tokens(user_id, "BITS", int(reward))
    await update.message.reply_text(f"💸 You received {int(reward)} $BITS in dividends!")