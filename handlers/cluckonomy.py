from telegram import Update
from telegram.ext import ContextTypes
import sqlite3
from utils.price_simulator import get_price

DB_PATH = "/data/crypto_game.db"

async def cluckonomy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT COUNT(*), SUM(bits), AVG(level), SUM(pet_xp) FROM users")
    users, total_bits, avg_level, total_pet_xp = c.fetchone()

    avg_bits = total_bits / users if users else 0

    c.execute("SELECT username, bits FROM users ORDER BY bits DESC LIMIT 1")
    top_user, top_bits = c.fetchone()

    c.execute("SELECT COUNT(*) FROM inventory")
    total_items = c.fetchone()[0]

    conn.close()

    bits_price = get_price("BITS")

    await update.message.reply_text(
        f"📊 *Cluckonomy Dashboard:*
"
        f"👥 *Players:* {users}
"
        f"💰 *Total $BITS:* {int(total_bits)}
"
        f"💹 *$BITS Price:* `${bits_price:.2f}`
"
        f"🧮 *Avg $BITS/Player:* {int(avg_bits)}
"
        f"🥇 *Top Holder:* `{top_user}` – {top_bits} BITS
"
        f"📦 *Total Loot Items:* {total_items}
"
        f"🐣 *Avg Player Level:* {avg_level:.1f}
"
        f"🐔 *Total Pet XP:* {total_pet_xp}",
        parse_mode="Markdown"
    )
