from telegram import Update
from telegram.ext import ContextTypes
from db.database import add_tokens, get_xp, level_up, get_inventory, add_to_inventory, update_xp
import random

async def tap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.first_name or "Player"

    # Emoji animation options
    animations = ["💥", "🔥", "💨", "💸", "🐔", "🥚", "✨", "🌽", "🔔"]
    emoji = random.choice(animations)

    # Fetch user level and XP (or default)
    xp, level = get_xp(user_id)
    base_reward = random.randint(8, 15)
    bonus = level * 2
    reward = base_reward + bonus

    # Add BITS reward
    add_tokens(user_id, "BITS", reward)

    # Gain XP
    xp_gain = random.randint(3, 7)
    new_xp = xp + xp_gain

    # Auto level-up if XP threshold met
    level_up_text = ""
    if new_xp >= 100:
        new_level = level_up(user_id)
        level_up_text = f"\n🎉 *LEVEL UP!* You are now Level {new_level}!"
    else:
        update_xp(user_id, new_xp)

    # Random loot drop chance
    loot_text = ""
    if random.random() < 0.12:
        loot_pool = [
            "Mystery Egg 🥚", "Golden Feather ✨", "Corn Nugget 🌽", "Rusty Beak 🦴", "Shiny Pebble 💎",
            "Ancient Scroll 📜", "Worm Jerky 🪱", "Degen Dice 🎲", "Solana Chip 💠", "Silver Nest 🪺",
            "Cluck Coin 🐔", "Trader Hat 🎩", "Egg of Insight 🧠", "Crypto Yolk 🥏", "Mini Moon Rock 🌕",
            "Chicken Boots 👢", "Feather Cape 🦚", "Cluck Whistle 📯", "Pocket Rug 🔴", "Tiny Backpack 🎒",
            "Golden Corn 🌽✨", "Giga Feather 🪶", "Zap Seed ⚡", "Lunar Lantern 🏮", "Robo Egg 🤖",
            "Treasure Map 🗺️", "Greedy Goblet 🏆", "Dusty Ledger 📖", "Hacker Feather 🧬", "Vanity Mirror 🪞",
            "Elite Badge 🎖️"
        ]
        loot_item = random.choice(loot_pool)
        add_to_inventory(user_id, loot_item)
        loot_text = f"\n🎁 BONUS DROP: You found a *{loot_item}*!"

    # Build reply message
    reply = (
        f"{emoji} *You tapped and earned* `{reward}` $BITS!\n"
        f"🔋 +{xp_gain} XP"
        f"{level_up_text}"
        f"{loot_text}"
    )

    await update.message.reply_text(reply, parse_mode="Markdown")
