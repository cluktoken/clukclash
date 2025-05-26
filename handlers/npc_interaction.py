
import random
from telegram import Update
from telegram.ext import ContextTypes

NPC_QUOTES = [
    "😈 Cluckles: 'Back again? Don’t think I won’t steal your loot!'",
    "😇 Chickette: 'You're doing great! Here’s a little something 🪙'",
    "😎 Roostro: 'I heard you lost a battle... try again, weakling.'",
    "🧙 Clucklor: 'Mystery surrounds you. Check your inventory... or don’t.'"
]

REWARDS = [
    ("BITS", 20),
    ("BITS", -10),
    ("item", "Rusty Beak 🦴"),
    ("nothing", None)
]

async def npc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    npc_quote = random.choice(NPC_QUOTES)
    reward_type, reward_value = random.choice(REWARDS)

    reply = npc_quote + "\n"

    if reward_type == "BITS":
        from db.database import add_tokens
        add_tokens(user_id, "BITS", reward_value)
        if reward_value > 0:
            reply += f"🎁 You gained {reward_value} $BITS!"
        else:
            reply += f"💨 Oh no! You lost {-reward_value} $BITS!"
    elif reward_type == "item":
        from db.database import add_to_inventory
        add_to_inventory(user_id, reward_value)
        reply += f"📦 You received an item: {reward_value}"
    else:
        reply += "🐔 The NPC vanished in a puff of feathers..."

    await update.message.reply_text(reply)
