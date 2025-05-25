import random
import sqlite3
from telegram import Update
from telegram.ext import ContextTypes
from db.database import get_user_portfolio, add_tokens

DB_PATH = "/data/crypto_game.db"

PET_STAGES = [
    (0, "🥚", "Cluck Egg"),
    (100, "🐣", "Tiny Clucker"),
    (300, "🐔", "Big Cluck"),
    (600, "🐲", "Cluckzilla")
]

PET_SKINS = [
    "Rainbow Feather 🌈", "Knight Armor 🛡️", "Laser Eyes 🔥",
    "Wizard Hat 🧙", "Tuxedo 🎩", "Cyber Wings 🦾", "Dragon Claws 🐉"
]

BATTLE_REWARDS = {"win": 40, "lose": 15}


def get_pet_stage(xp):
    stage = PET_STAGES[0]
    for threshold, emoji, name in PET_STAGES:
        if xp >= threshold:
            stage = (threshold, emoji, name)
    return stage


def get_pet_data(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT pet_xp, pet_name, pet_skin FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row if row else (0, None, None)


def update_pet_xp(user_id, amount):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET pet_xp = pet_xp + ? WHERE id = ?", (amount, user_id))
    conn.commit()
    conn.close()


def set_pet_name(user_id, name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET pet_name = ? WHERE id = ?", (name, user_id))
    conn.commit()
    conn.close()


def set_pet_skin(user_id, skin):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET pet_skin = ? WHERE id = ?", (skin, user_id))
    conn.commit()
    conn.close()


async def pet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    xp, name, skin = get_pet_data(user_id)
    _, emoji, stage_name = get_pet_stage(xp)
    name_text = f"Name: <b>{name}</b>\n" if name else ""
    skin_text = f"Style: <i>{skin}</i>\n" if skin else ""
    reply = (
        f"{emoji} <b>Your Pet Status</b>\n\n"
        f"{name_text}{skin_text}"
        f"Stage: <b>{stage_name}</b>\n"
        f"XP: <code>{xp}</code>/600\n\n"
        f"Use /feed to evolve, /namepet to name it, /dresspet to style it!"
    )
    await update.message.reply_text(reply, parse_mode="HTML")


async def feed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bits, _ = get_user_portfolio(user_id)
    if bits < 50:
        await update.message.reply_text("🚫 You need at least 50 $BITS to feed your pet.")
        return
    add_tokens(user_id, "BITS", -50)
    xp_gain = random.randint(20, 40)
    update_pet_xp(user_id, xp_gain)
    await update.message.reply_text(f"🍗 You fed your pet and gained {xp_gain} XP!")


async def namepet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text("Usage: /namepet <new_name>")
        return
    new_name = " ".join(context.args)
    set_pet_name(user_id, new_name)
    await update.message.reply_text(f"✅ Your pet is now named <b>{new_name}</b>!", parse_mode="HTML")


async def dresspet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    new_skin = random.choice(PET_SKINS)
    set_pet_skin(user_id, new_skin)
    await update.message.reply_text(f"🎨 Your pet put on: <b>{new_skin}</b>", parse_mode="HTML")


async def pet_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /petbattle <user_id>")
        return
    try:
        challenger_id = update.effective_user.id
        opponent_id = int(context.args[0])
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT pet_xp, pet_name FROM users WHERE id = ?", (challenger_id,))
        xp1, name1 = c.fetchone()
        c.execute("SELECT pet_xp, pet_name FROM users WHERE id = ?", (opponent_id,))
        xp2, name2 = c.fetchone()
        conn.close()

        _, emoji1, stage1 = get_pet_stage(xp1)
        _, emoji2, stage2 = get_pet_stage(xp2)
        p1 = xp1 // 10 + random.randint(0, 20)
        p2 = xp2 // 10 + random.randint(0, 20)

        winner = challenger_id if p1 > p2 else opponent_id
        reward = BATTLE_REWARDS["win"] if winner == challenger_id else BATTLE_REWARDS["lose"]
        add_tokens(challenger_id, "BITS", reward)

        result = (
            f"{emoji1} {name1 or 'Pet1'} ({p1}) VS {emoji2} {name2 or 'Pet2'} ({p2})\n\n"
            f"🏆 {'You win!' if winner == challenger_id else 'You lose!'} +{reward} $BITS"
        )
        await update.message.reply_text(result, parse_mode="HTML")
    except Exception as e:
        await update.message.reply_text(f"❌ Battle error: {str(e)}")


async def pet_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username, pet_xp FROM users ORDER BY pet_xp DESC LIMIT 5")
    top = c.fetchall()
    conn.close()
    reply = "🐔 <b>Top 5 Cluck Pets</b>\n\n"
    for i, (name, xp) in enumerate(top, 1):
        _, emoji, stage = get_pet_stage(xp)
        reply += f"{i}. {emoji} {name} — {stage} ({xp} XP)\n"
    await update.message.reply_text(reply, parse_mode="HTML")


async def pet_marketplace(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = (
        "🛍️ <b>Pet Skin Marketplace</b>\n\n"
        "Use /dresspet to randomly unlock a style.\n"
        "No trades available yet. Stay tuned for peer-to-peer pet trading!"
    )
    await update.message.reply_text(reply, parse_mode="HTML")


async def pet_fusion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    xp, name, _ = get_pet_data(user_id)
    if xp < 400:
        await update.message.reply_text("❌ You need at least 400 XP to fuse your pet!")
        return
    add_tokens(user_id, "BITS", -100)
    update_pet_xp(user_id, -200)
    new_skin = "Fusion Core 🧬"
    set_pet_skin(user_id, new_skin)
    await update.message.reply_text(f"🧬 Fusion complete! Your pet now glows with a <b>{new_skin}</b>.", parse_mode="HTML")
