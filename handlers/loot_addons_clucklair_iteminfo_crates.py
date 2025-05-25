from telegram import Update
from telegram.ext import ContextTypes
from db.database import get_inventory, get_xp
import random

RARITY_INFO = {
    "common": "📦 Basic and easy to find. Great for beginners.",
    "rare": "🔹 Less common. May offer small bonuses.",
    "epic": "💎 Powerful loot with cool effects.",
    "legendary": "🔥 Extremely rare with big impact.",
    "relic": "👑 Ultra rare. Grants access to hidden areas."
}

ITEM_DESCRIPTIONS = {
    "Mystery Egg 🥚": "A mysterious egg. Who knows what’s inside?",
    "Golden Feather ✨": "Grants shimmer to your pet.",
    "Corn Nugget 🌽": "A crunchy snack worth some BITS.",
    "Ancient Scroll 📜": "Gives +10 XP when opened.",
    "Cluck Relic 💎🐔": "The rarest artifact. Grants access to /clucklair."
}

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


async def iteminfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❓ Usage: /iteminfo <item name>")
        return

    item = " ".join(context.args)
    desc = ITEM_DESCRIPTIONS.get(item, "No special information found.")
    rarity = determine_rarity(item)
    rarity_desc = RARITY_INFO.get(rarity, "")

    await update.message.reply_text(
        f"🔍 *Item:* {item}\n"
        f"⭐ *Rarity:* {rarity.title()}\n"
        f"ℹ️ {desc}\n\n"
        f"{rarity_desc}",
        parse_mode="Markdown"
    )

async def clucklair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    inventory = get_inventory(user_id)
    if "Cluck Relic 💎🐔" in inventory:
        await update.message.reply_text(
            "🏛️ Welcome to the secret Cluck Lair! Here you can access exclusive relic upgrades and ancient clucker wisdom. 🧙‍♂️🐔"
        )
    else:
        await update.message.reply_text("🚫 You need a Cluck Relic 💎🐔 to enter the /clucklair.")

async def open_common(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    item = random.choice(RARITY_LOOT["common"])
    add_to_inventory(user_id, item)
    await update.message.reply_text(f"📦 You opened a Common Cluck Crate! 🎁 Loot: *{item}*", parse_mode="Markdown")

async def open_epic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    item = random.choice(RARITY_LOOT["epic"])
    add_to_inventory(user_id, item)
    await update.message.reply_text(f"🚀 You opened an Epic Crate! 🎁 Loot: *{item}*", parse_mode="Markdown")
