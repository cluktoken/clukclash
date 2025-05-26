# npc_interaction.py

from telegram import Update
from telegram.ext import ContextTypes
from db.database import add_tokens
import random

NPC_QUOTES = [
    "👀 ClucksterBot: 'You again? Don't lose all your BITS!'",
    "🧙‍♂️ MysticCluck: 'One day you’ll hatch into greatness… maybe.'",
    "🦹 Rogue Rooster: *steals* 10 $BITS! 🏃💨",
    "🎁 FarmerCluck: 'Take this gift, kid.' (+10 BITS)"
]

async def npc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    choice = random.choice(NPC_QUOTES)

    if "steals" in choice:
        add_tokens(user_id, "BITS", -10)
    elif "gift" in choice:
        add_tokens(user_id, "BITS", 10)

    await update.message.reply_text(choice, parse_mode="Markdown")
