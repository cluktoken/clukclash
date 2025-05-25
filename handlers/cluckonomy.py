from telegram import Update
from telegram.ext import ContextTypes
import sqlite3
DB_PATH = "/data/crypto_game.db"

async def cluckonomy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*), SUM(bits) FROM users")
    users, total_bits = c.fetchone()
    conn.close()
    await update.message.reply_text(
        f"📊 *Cluckonomy Stats:*"
        f"• Players: {users}"
        f"• Total $BITS in circulation: {int(total_bits)}",
        parse_mode="Markdown"
    )
