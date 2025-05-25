import random
from telegram import Update
from telegram.ext import ContextTypes
from db.database import get_all_prices

async def market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prices = get_all_prices()
    message = "📈 <b>Current Market Prices</b>\n\n"

    for token, price in prices.items():
        change = random.uniform(-7, 7)  # Simulate daily % change
        emoji = "📈" if change > 0 else "📉"
        trend = "🚀" if price > 2 else "😬" if price < 0.5 else "💠"
        message += f"{trend} <b>{token}</b>: ${price:.2f} ({emoji} {change:+.2f}%)\n"

    avg_price = sum(prices.values()) / len(prices)
    featured = random.choice(list(prices.keys()))

    message += f"\n🧮 <i>{len(prices)} tokens tracked</i>"
    message += f"\n🌐 <b>Avg Price:</b> ${avg_price:.2f}"
    message += f"\n🌟 <b>Featured Token:</b> {featured}"

    await update.message.reply_text(message, parse_mode="HTML")
