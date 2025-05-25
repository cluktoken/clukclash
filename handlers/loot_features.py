import random
import sqlite3
from collections import Counter
from telegram import Update
from telegram.ext import ContextTypes
from db.database import add_to_inventory, get_inventory, add_tokens, update_xp, get_xp

DB_PATH = "/data/crypto_game.db"

RARITY_LOOT = {
    "common": ["Mystery Egg 🥚", "Rusty Beak 🦴", "Corn Nugget 🌽", "Shiny Pebble 💎", "Feather Scrap 🪶"],
    "rare": ["Golden Feather ✨", "Worm Jerky 🪱", "Trader Hat 🎩", "Mini Moon Rock 🌕", "Crypto Yolk 🥏"],
    "epic": ["Ancient Scroll 📜", "Silver Nest 🪺", "Egg of Insight 🧠", "Robo Egg 🤖", "Greedy Goblet 🏆"],
    "legendary": ["Giga Feather 🪶", "Zap Seed ⚡", "Lunar Lantern 🏮", "Vanity Mirror 🪞", "Elite Badge 🎖️"]
}

RELICS = ["Cluck Relic 💎🐔"]  # ultra rare

RARITY_CHANCES = [
    ("relic", 0.001),
    ("legendary", 0.01),
    ("epic", 0.04),
    ("rare", 0.15),
    ("common", 0.799)
]

LOOT_PRICES = {
    "common": 10,
    "rare": 25,
    "epic": 60,
    "legendary": 150,
    "relic": 500
}

# Drop system with relics
def drop_loot(user_id):
    roll = random.random()
    for rarity, chance in RARITY_CHANCES:
        if roll < chance:
            if rarity == "relic":
                item = random.choice(RELICS)
            else:
                item = random.choice(RARITY_LOOT[rarity])
            add_to_inventory(user_id, item)
            return f"🎁 You found a {rarity.upper()} item: *{item}*!"
        roll -= chance
    return ""

def determine_rarity(item_name):
    if item_name in RELICS:
        return "relic"
    for rarity, items in RARITY_LOOT.items():
        if item_name in items:
            return rarity
    return "common"

def clear_inventory(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM inventory WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

async def open_loot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    inventory = get_inventory(user_id)

    if not inventory:
        await update.message.reply_text("🎒 Your inventory is empty.")
        return

    used_item = random.choice(inventory)
    rarity = determine_rarity(used_item)
    effect = ""

    if "XP" in used_item or "Scroll" in used_item or used_item == "Egg of Insight 🧠":
        effect = "+10 XP!"
        xp, _ = get_xp(user_id)
        update_xp(user_id, xp + 10)
    elif "Corn" in used_item or "Nugget" in used_item:
        effect = "+20 BITS!"
        add_tokens(user_id, "BITS", 20)
    elif used_item in RELICS:
        effect = "🔓 You unlocked the hidden /clucklair!"

    await update.message.reply_text(
        f"🪙 You opened *{used_item}*...
{effect or 'It shimmered, but nothing happened.'}",
        parse_mode="Markdown"
    )

async def sell_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    inventory = get_inventory(user_id)

    if not inventory:
        await update.message.reply_text("🎒 You have no items to sell.")
        return

    count = Counter(determine_rarity(item) for item in inventory)
    total = sum(LOOT_PRICES.get(rarity, 5) * qty for rarity, qty in count.items())
    add_tokens(user_id, "BITS", total)
    clear_inventory(user_id)

    breakdown = "\n".join([f"• {qty} {rarity.capitalize()}" for rarity, qty in count.items()])
    await update.message.reply_text(
        f"🧾 Sold:
{breakdown}

💰 Total earned: `{total}` $BITS",
        parse_mode="Markdown"
    )

async def reroll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    inventory = get_inventory(user_id)

    if not inventory:
        await update.message.reply_text("🌀 You need at least 1 item to reroll.")
        return

    lost = random.choice(inventory)
    rarity = determine_rarity(lost)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM inventory WHERE user_id = ? AND item = ? LIMIT 1", (user_id, lost))
    conn.commit()
    conn.close()

    new_msg = drop_loot(user_id)
    await update.message.reply_text(f"♻️ You rerolled *{lost}*...
{new_msg}", parse_mode="Markdown")

async def collection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    inventory = set(get_inventory(user_id))
    all_items = set(sum(RARITY_LOOT.values(), []) + RELICS)
    owned = len(inventory)
    total = len(all_items)

    await update.message.reply_text(
        f"📦 Collection Progress: `{owned}` / `{total}` unique items found!",
        parse_mode="Markdown"
    )
