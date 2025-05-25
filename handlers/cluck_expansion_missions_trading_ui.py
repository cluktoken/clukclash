from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from db.database import get_inventory, add_to_inventory, add_tokens
import random
import sqlite3
import datetime

DB_PATH = "/data/crypto_game.db"

DAILY_MISSIONS = [
    ("Tap 5 times today", "tap_5"),
    ("Open 2 loot crates", "open_2"),
    ("Feed your pet", "feed_1")
]

# simulate a user mission state in a real app you'd store per-user data
USER_MISSIONS = {}

async def daily_missions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in USER_MISSIONS:
        USER_MISSIONS[user_id] = {code: False for _, code in DAILY_MISSIONS}

    reply = "📆 <b>Daily Missions</b>\n\n"
    for text, code in DAILY_MISSIONS:
        status = "✅" if USER_MISSIONS[user_id].get(code) else "⬜"
        reply += f"{status} {text}\n"

    await update.message.reply_text(reply, parse_mode="HTML")

# 🧪 Crafting UI (inline menu)
async def craft_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("🪄 Feather Wand", callback_data="craft_wand")],
        [InlineKeyboardButton("🍳 Omega Omelette", callback_data="craft_omelette")]
    ]
    markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("🔧 Choose a recipe to craft:", reply_markup=markup)

async def handle_craft_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    inv = get_inventory(user_id)
    await query.answer()

    recipes = {
        "craft_wand": (["Feather Scrap 🪶", "Rusty Beak 🦴", "Shiny Pebble 💎"], "Feather Wand 🪄"),
        "craft_omelette": (["Mystery Egg 🥚", "Corn Nugget 🌽", "Crypto Yolk 🥏"], "Omega Omelette 🍳")
    }

    if query.data not in recipes:
        return

    required, result = recipes[query.data]
    if all(inv.count(i) >= 1 for i in required):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        for item in required:
            c.execute("DELETE FROM inventory WHERE user_id = ? AND item = ? LIMIT 1", (user_id, item))
        conn.commit()
        conn.close()

        add_to_inventory(user_id, result)
        await query.edit_message_text(f"✅ Crafted: {result} from {', '.join(required)}")
    else:
        await query.edit_message_text("❌ You don't have all the required ingredients.")

# 🧑‍🤝‍🧑 Trading stub
async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤝 Player-to-player trading is coming soon! You'll be able to send and receive loot securely via the bot.")
