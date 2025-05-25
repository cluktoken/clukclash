import random
from db.database import add_to_inventory, get_inventory, add_tokens

# Rarity-based loot pool
RARITY_LOOT = {
    "common": [
        "Mystery Egg 🥚", "Rusty Beak 🦴", "Corn Nugget 🌽", "Shiny Pebble 💎", "Feather Scrap 🪶"
    ],
    "rare": [
        "Golden Feather ✨", "Worm Jerky 🪱", "Trader Hat 🎩", "Mini Moon Rock 🌕", "Crypto Yolk 🥏"
    ],
    "epic": [
        "Ancient Scroll 📜", "Silver Nest 🪺", "Egg of Insight 🧠", "Robo Egg 🤖", "Greedy Goblet 🏆"
    ],
    "legendary": [
        "Giga Feather 🪶", "Zap Seed ⚡", "Lunar Lantern 🏮", "Vanity Mirror 🪞", "Elite Badge 🎖️"
    ]
}

RARITY_CHANCES = [
    ("legendary", 0.01),
    ("epic", 0.05),
    ("rare", 0.15),
    ("common", 0.79)
]

def drop_loot(user_id):
    roll = random.random()
    for rarity, chance in RARITY_CHANCES:
        if roll < chance:
            item = random.choice(RARITY_LOOT[rarity])
            add_to_inventory(user_id, item)
            return f"🎁 You found a {rarity.upper()} item: *{item}*!"
        roll -= chance
    return ""


# /open command - simulates using a loot item
from telegram import Update
from telegram.ext import ContextTypes

async def open_loot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    inventory = get_inventory(user_id)

    if not inventory:
        await update.message.reply_text("🎒 Your inventory is empty.")
        return

    used_item = random.choice(inventory)
    effect = random.choice([
        "You gained 20 BITS!",
        "It was a dud! Nothing happened.",
        "You found a bonus XP scroll!",
        "You earned 5 bonus XP!"
    ])

    await update.message.reply_text(
        f"🪙 You opened *{used_item}*...\n{effect}",
        parse_mode="Markdown"
    )


# /sellall command - converts all loot into BITS
LOOT_PRICES = {
    "common": 10,
    "rare": 25,
    "epic": 60,
    "legendary": 150
}

def determine_rarity(item_name):
    for rarity, items in RARITY_LOOT.items():
        if item_name in items:
            return rarity
    return "common"

async def sell_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    inventory = get_inventory(user_id)

    if not inventory:
        await update.message.reply_text("🎒 You have no items to sell.")
        return

    total = 0
    for item in inventory:
        rarity = determine_rarity(item)
        total += LOOT_PRICES.get(rarity, 5)

    add_tokens(user_id, "BITS", total)
    await update.message.reply_text(
        f"💰 You sold your loot for `{total}` $BITS!",
        parse_mode="Markdown"
    )
