import sqlite3

DB_PATH = "/data/crypto_game.db"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

try:
    c.execute("ALTER TABLE users ADD COLUMN pet_xp INTEGER DEFAULT 0;")
except:
    print("pet_xp already exists")

try:
    c.execute("ALTER TABLE users ADD COLUMN pet_name TEXT;")
except:
    print("pet_name already exists")

try:
    c.execute("ALTER TABLE users ADD COLUMN pet_skin TEXT;")
except:
    print("pet_skin already exists")

conn.commit()
conn.close()
print("✅ Pet migration complete.")
