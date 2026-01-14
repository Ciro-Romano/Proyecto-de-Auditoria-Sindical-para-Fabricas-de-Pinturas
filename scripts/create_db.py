import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "auditoria.db"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"

# Crear carpeta data si no existe
DB_PATH.parent.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    schema_sql = f.read()

cur.executescript(schema_sql)

conn.commit()
conn.close()

print("Base de datos creada correctamente.")
