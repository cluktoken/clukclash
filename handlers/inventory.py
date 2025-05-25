from telegram import Update
from telegram.ext import ContextTypes
from db.database import get_inventory

async def inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    items = get_inventory(user_id)
    if not items:
        await update.message.reply_text("🎒 Your inventory is empty.")
        return

    reply = "🎒 *Your Inventory:*
"
    for item in items:
        reply += f"• {item}\n"
    await update.message.reply_text(reply, parse_mode="Markdown")