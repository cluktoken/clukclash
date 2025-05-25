from telegram import Update
from telegram.ext import ContextTypes
from db.database import get_inventory, add_to_inventory
import random

async def reroll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    inventory = get_inventory(user_id)

    if not inventory:
        await update.message.reply_text("🎒 You have no items to reroll.")
        return

    old_item = random.choice(inventory)
    all_possible = [
        "Mystery Egg 🥚", "Golden Feather ✨", "Corn Nugget 🌽", "Rusty Beak 🦴", "Shiny Pebble 💎",
        "Ancient Scroll 📜", "Worm Jerky 🪱", "Degen Dice 🎲", "Silver Nest 🪺", "Trader Hat 🎩",
        "Cluck Coin 🐔", "Mini Moon Rock 🌕", "Feather Cape 🦚", "Crypto Yolk 🥏", "Elite Badge 🎖️"
    ]

    new_item = random.choice([item for item in all_possible if item != old_item])
    add_to_inventory(user_id, new_item)

    await update.message.reply_text(
        f"🔄 You rerolled *{old_item}* and got *{new_item}*!",
        parse_mode="Markdown"
    )