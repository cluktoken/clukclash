import sqlite3
from utils.price_simulator import get_price
from datetime import datetime, timedelta


DB_PATH = "db/crypto_game.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, bits INTEGER DEFAULT 0, cash REAL DEFAULT 1000)")
    conn.commit()
    conn.close()

def add_user(user_id, username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    conn.close()

def add_tokens(user_id, token, amount):
    if token != "BITS":
        return
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET bits = bits + ? WHERE id = ?", (amount, user_id))
    conn.commit()
    conn.close()

def trade_token(user_id, token, amount, action):
    price = get_price(token)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT bits, cash FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    bits, cash = row
    total_cost = amount * price
    if action == "buy":
        if cash >= total_cost:
            c.execute("UPDATE users SET bits = bits + ?, cash = cash - ? WHERE id = ?", (amount, total_cost, user_id))
            conn.commit()
            msg = f"✅ Bought {amount} $BITS for ${total_cost:.2f}"
        else:
            msg = "❌ Not enough $CASH."
    else:
        if bits >= amount:
            c.execute("UPDATE users SET bits = bits - ?, cash = cash + ? WHERE id = ?", (amount, total_cost, user_id))
            conn.commit()
            msg = f"✅ Sold {amount} $BITS for ${total_cost:.2f}"
        else:
            msg = "❌ Not enough $BITS."
    conn.close()
    return msg

def get_all_prices():
    return {"BITS": get_price("BITS"), "MOON": get_price("MOON")}

def get_leaderboard():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username, bits * ? + cash as net FROM users ORDER BY net DESC LIMIT 5", (get_price("BITS"),))
    result = c.fetchall()
    conn.close()
    return result

def get_user_portfolio(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT bits, cash FROM users WHERE id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            bits INTEGER DEFAULT 0,
            cash REAL DEFAULT 1000,
            last_daily TEXT
        )
    """)
    conn.commit()
    conn.close()

def give_daily_bonus(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT last_daily FROM users WHERE id = ?", (user_id,))
    result = c.fetchone()

    now = datetime.utcnow()
    if result and result[0]:
        last_claim = datetime.fromisoformat(result[0])
        if now - last_claim < timedelta(hours=24):
            next_claim = last_claim + timedelta(hours=24)
            wait_time = (next_claim - now).seconds // 3600
            return f"⏳ You've already claimed your daily reward. Try again in ~{wait_time}h."

    # reward
    reward = 25
    c.execute("UPDATE users SET bits = bits + ?, last_daily = ? WHERE id = ?", (reward, now.isoformat(), user_id))
    conn.commit()
    conn.close()
    return f"🎁 You claimed your daily bonus: {reward} $BITS!"
