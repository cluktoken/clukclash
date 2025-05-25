from telegram import Update
from telegram.ext import ContextTypes
from db.database import get_xp, get_user_portfolio, get_inventory

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    xp, level = get_xp(user_id)
    bits, cash = get_user_portfolio(user_id)
    inventory = get_inventory(user_id)
    await update.message.reply_text(
        f"👤 *Your Profile:*"
        f"Level: {level} | XP: {xp}/100"
        f"💰 BITS: {bits} | Cash: ${cash:.2f}"
        f"🎒 Items: {len(inventory)}",
        parse_mode="Markdown"
    )
