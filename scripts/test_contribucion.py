import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "auditoria.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
SELECT p.anio, p.mes, c.monto
FROM contribucion_empresarial c
JOIN periodos p ON p.id = c.periodo_id
WHERE c.vigente = 1
ORDER BY p.anio, p.mes
LIMIT 5;
""")

for row in cur.fetchall():
    print(row)

conn.close()
