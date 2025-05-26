from telegram import Update
from telegram.ext import ContextTypes
import random
from db.database import add_tokens  # Optional if your NPCs give/take bits

async def npc_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    npc_actions = [
        ("😏 *Rival Cluck*: Heard you missed a tap streak again... pathetic.", 0),
        ("🧙 *Wise Cluck*: Here’s some advice — and 10 free $BITS.", +10),
        ("🦹 *Thief Cluck*: Oops, I may have 'borrowed' 5 $BITS. 💸", -5),
        ("👻 *Ghost Cluck*: You’ll never hatch the golden egg. Or will you?", 0),
        ("🎩 *Investor Cluck*: I’ll match your hustle. +15 $BITS for style.", +15)
    ]

    message, bits = random.choice(npc_actions)

    # Apply BITS reward or penalty if needed
    if bits != 0:
        add_tokens(user_id, "BITS", bits)

    await update.message.reply_text(message, parse_mode="Markdown")
