from telegram import Update
from telegram.ext import ContextTypes
from db.database import get_all_prices

async def market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prices = get_all_prices()
    message = "📈 Current Market Prices:\n"
    for token, price in prices.items():
        message += f"{token}: ${price:.2f}\n"
    await update.message.reply_text(message)