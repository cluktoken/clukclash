from telegram import Update
from telegram.ext import ContextTypes
from db.database import get_user_portfolio, get_price

async def portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    portfolio = get_user_portfolio(user_id)
    
    if portfolio is None:
        await update.message.reply_text("❌ You don't have a portfolio yet. Try /start.")
        return

    bits, cash = portfolio
    price = get_price("BITS")
    total = bits * price + cash

    message = (
        f"💼 Your Portfolio:\n"
        f"🪙 $BITS: {bits}\n"
        f"💵 $CASH: ${cash:.2f}\n"
        f"📈 Net Worth: ${total:.2f}"
    )
    await update.message.reply_text(message)
