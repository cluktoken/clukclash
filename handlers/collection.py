from telegram import Update
from telegram.ext import ContextTypes
from db.database import get_inventory

async def collection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    inventory = get_inventory(user_id)

    if not inventory:
        await update.message.reply_text("📦 Your collection is empty. Time to loot!")
        return

    reply = "📚 <b>Your Collection:</b>\n\n"
    unique_items = sorted(set(inventory))
    for item in unique_items:
        count = inventory.count(item)
        reply += f"• {item} x{count}\n"

    await update.message.reply_text(reply, parse_mode="HTML")
