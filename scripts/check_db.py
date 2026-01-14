import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "auditoria.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

tables = cur.execute("""
SELECT name FROM sqlite_master
WHERE type='table'
ORDER BY name;
""").fetchall()

print("Tablas creadas:")
for t in tables:
    print("-", t[0])

conn.close()
