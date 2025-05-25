from datetime import datetime
import sqlite3
DB_PATH = "/data/crypto_game.db"

def can_earn_xp(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.utcnow()
    c.execute("SELECT last_tap FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    if not row or not row[0]:
        c.execute("UPDATE users SET last_tap = ? WHERE id = ?", (now.isoformat(), user_id))
        conn.commit()
        conn.close()
        return True
    last = datetime.fromisoformat(row[0])
    diff = (now - last).total_seconds()
    conn.close()
    return diff > 30  # 30s cooldown