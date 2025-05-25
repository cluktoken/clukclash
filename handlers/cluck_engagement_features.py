from telegram import Update
from telegram.ext import ContextTypes
from db.database import get_inventory, add_to_inventory
import random
import sqlite3
from collections import Counter

DB_PATH = "/data/crypto_game.db"

# 🎨 Crafting system: combine 3 items into one rare item
CRAFTING_RECIPES = {
    ("Feather Scrap 🪶", "Rusty Beak 🦴", "Shiny Pebble 💎"): "Feather Wand 🪄",
    ("Mystery Egg 🥚", "Corn Nugget 🌽", "Crypto Yolk 🥏"): "Omega Omelette 🍳",
}

def remove_items(user_id, items):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for item in items:
        c.execute("DELETE FROM inventory WHERE user_id = ? AND item = ? LIMIT 1", (user_id, item))
    conn.commit()
    conn.close()

async def craft(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    inv = get_inventory(user_id)
    inv_count = Counter(inv)

    for ingredients, result in CRAFTING_RECIPES.items():
        if all(inv_count[i] >= 1 for i in ingredients):
            remove_items(user_id, ingredients)
            add_to_inventory(user_id, result)
            await update.message.reply_text(f"🛠️ Crafted: *{result}* from {', '.join(ingredients)}", parse_mode="Markdown")
            return

    await update.message.reply_text("❌ You don't have the right items to craft anything.")

# 🎯 Missions system
MISSIONS = [
    ("Collect 5 Common Items", lambda inv: sum(1 for i in inv if determine_rarity(i) == "common") >= 5),
    ("Own an Epic Item", lambda inv: any(determine_rarity(i) == "epic" for i in inv)),
    ("Have 10 total items", lambda inv: len(inv) >= 10),
]

async def mission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    inv = get_inventory(user_id)
    response = "🎯 <b>Active Missions</b>\n\n"
    for text, checker in MISSIONS:
        status = "✅" if checker(inv) else "❌"
        response += f"{status} {text}\n"
    await update.message.reply_text(response, parse_mode="HTML")

# 🛒 Marketplace: preview tradable items
MARKET_ITEMS = {
    "Silver Nest 🪺": 75,
    "Crypto Yolk 🥏": 50,
    "Elite Badge 🎖️": 200
}

async def pet_marketplace(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = "<b>🛍️ Cluck Marketplace</b>\n\n"
    for item, price in MARKET_ITEMS.items():
        response += f"• {item} — {price} $BITS\n"
    response += "\n*Trading not implemented yet – coming soon!*"
    await update.message.reply_text(response, parse_mode="HTML")