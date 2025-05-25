from telegram import Update
from telegram.ext import ContextTypes
import sqlite3
DB_PATH = "/data/crypto_game.db"

async def set_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /title <your title>")
        return
    title = " ".join(context.args)[:32]
    user_id = update.effective_user.id
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET title = ? WHERE id = ?", (title, user_id))
    conn.commit()
    conn.close()
    await update.message.reply_text(f"🏷️ Title set to: *{title}*", parse_mode="Markdown")