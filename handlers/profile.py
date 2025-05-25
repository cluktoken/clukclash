from telegram import Update
from telegram.ext import ContextTypes
from db.database import get_xp, get_user_portfolio, get_inventory
import sqlite3

DB_PATH = "/data/crypto_game.db"

def get_user_meta(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username, title, skin FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row if row else ("unknown", "", "")

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    xp, level = get_xp(user_id)
    bits, cash = get_user_portfolio(user_id)
    inventory = get_inventory(user_id)
    username, title, skin = get_user_meta(user_id)

    xp_bar = "🟩" * (xp // 10) + "⬜" * (10 - xp // 10)
    title_text = f"🏷️ *Title:* `{title}`\n" if title else ""
    skin_text = f"🎨 *Skin:* `{skin}`\n" if skin else ""

    reply = (
        f"👤 *Profile of {username}*"
        f"🎖️ *Level:* {level}"
        f"⚡ *XP:* `{xp}/100` {xp_bar}"
        f"💰 *BITS:* `{bits}` | 💵 *Cash:* `${cash:.2f}`"
        f"🎒 *Items Collected:* {len(inventory)}"
        f"{title_text}{skin_text}"
        f"🌟 Keep tapping and upgrading!"
    )

    await update.message.reply_text(reply, parse_mode="MarkdownV2")
