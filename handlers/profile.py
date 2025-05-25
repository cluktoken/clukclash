from telegram import Update
from telegram.ext import ContextTypes
from db.database import get_xp, get_user_portfolio, get_inventory
import sqlite3
import random

DB_PATH = "/data/crypto_game.db"

def get_user_meta(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username, title, skin FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row if row else ("unknown", "", "")

def generate_badges(level, inventory_count):
    badges = []
    if level >= 10:
        badges.append("🏅")
    if inventory_count >= 5:
        badges.append("🎖️")
    if random.random() < 0.1:
        badges.append("✨")
    return " ".join(badges) or "—"

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    xp, level = get_xp(user_id)
    bits, cash = get_user_portfolio(user_id)
    inventory = get_inventory(user_id)
    username, title, skin = get_user_meta(user_id)
    badges = generate_badges(level, len(inventory))

    xp_bar = "🟩" * (xp // 10) + "⬜" * (10 - xp // 10)
    percent = f"{xp}%"

reply = (
    f"👤 <b>Profile of {username}</b>\n\n"
    f"🎖️ <b>Level:</b> {level}    <b>XP:</b> {xp}/100 ({percent})\n"
    f"{xp_bar}\n\n"
    f"💰 <b>BITS:</b> {bits}    💵 <b>Cash:</b> ${cash:.2f}\n"
    f"🎒 <b>Items:</b> {len(inventory)}\n"
    f"🏅 <b>Badges:</b> {badges}\n\n"
    f"🏷️ <b>Title:</b> {title or 'None'}\n"
    f"🎨 <b>Skin:</b> {skin or 'Default'}\n\n"
    f"🌟 <i>Keep tapping, trading, and collecting to rise in the ranks!</i>"
    )
await update.message.reply_text(reply, parse_mode="HTML")
