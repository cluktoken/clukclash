import sqlite3
from utils.price_simulator import get_price
from datetime import datetime, timedelta


DB_PATH = "/data/crypto_game.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, bits INTEGER DEFAULT 0, cash REAL DEFAULT 1000, xp INTEGER DEFAULT 0, level INTEGER DEFAULT 1, pet_xp INTEGER DEFAULT 0, pet_name TEXT, pet_skin TEXT, title TEXT, skin TEXT, last_tap TEXT, last_daily TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS inventory (user_id INTEGER, item TEXT)")
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
    if not row:
        conn.close()
        return "❌ User not found. Try using /start or /tap first."
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
            return f"⏳ Already claimed. Come back in ~{wait_time}h."

    reward = 25
    c.execute("UPDATE users SET bits = bits + ?, last_daily = ? WHERE id = ?", (reward, now.isoformat(), user_id))
    conn.commit()
    conn.close()
    return f"🎁 You claimed your daily bonus: {reward} $BITS!"

def get_xp(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT xp, level FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row if row else (0, 1)

def level_up(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET xp = xp - 100, level = level + 1 WHERE id = ?", (user_id,))
    conn.commit()
    c.execute("SELECT level FROM users WHERE id = ?", (user_id,))
    new_level = c.fetchone()[0]
    conn.close()
    return new_level

def get_inventory(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT item FROM inventory WHERE user_id = ?", (user_id,))
    items = [row[0] for row in c.fetchall()]
    conn.close()
    return items

def update_xp(user_id, new_xp):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET xp = ? WHERE id = ?", (new_xp, user_id))
    conn.commit()
    conn.close()

def add_to_inventory(user_id, item):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO inventory (user_id, item) VALUES (?, ?)", (user_id, item))
    conn.commit()
    conn.close()

def reset_daily(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET last_daily = NULL WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def upgrade_schema():
    conn = sqlite3.connect("/data/crypto_game.db")
    c = conn.cursor()

    try: c.execute("ALTER TABLE users ADD COLUMN title TEXT")
    except sqlite3.OperationalError: pass

    try: c.execute("ALTER TABLE users ADD COLUMN skin TEXT")
    except sqlite3.OperationalError: pass

    try: c.execute("ALTER TABLE users ADD COLUMN last_tap TEXT")
    except sqlite3.OperationalError: pass

    conn.commit()
    conn.close()


