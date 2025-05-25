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
        f"👤 <b>Profile of {username}</b><br><br>"
        f"🎖️ <b>Level:</b> {level} &nbsp;&nbsp; <b>XP:</b> {xp}/100 ({percent})<br>"
        f"{xp_bar}<br><br>"
        f"💰 <b>BITS:</b> {bits} &nbsp;&nbsp; 💵 <b>Cash:</b> ${cash:.2f}<br>"
        f"🎒 <b>Items:</b> {len(inventory)}<br>"
        f"🏅 <b>Badges:</b> {badges}<br><br>"
        f"🏷️ <b>Title:</b> {title or 'None'}<br>"
        f"🎨 <b>Skin:</b> {skin or 'Default'}<br><br>"
        f"🌟 <i>Keep tapping, trading, and collecting to rise in the ranks!</i>"
    )

    await update.message.reply_text(reply, parse_mode="HTML")
