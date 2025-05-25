from telegram import Update
from telegram.ext import ContextTypes
import sqlite3
DB_PATH = "/data/crypto_game.db"

async def set_skin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /skin <style_name>")
        return
    style = context.args[0]
    user_id = update.effective_user.id
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET skin = ? WHERE id = ?", (style, user_id))
    conn.commit()
    conn.close()
    await update.message.reply_text(f"🎨 Cluk skin set to: {style}")