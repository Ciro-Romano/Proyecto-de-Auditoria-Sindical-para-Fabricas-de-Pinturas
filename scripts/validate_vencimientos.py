import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "auditoria.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
SELECT 
    p.anio,
    p.mes,
    v.digito_cuit,
    v.fecha_vencimiento
FROM vencimientos v
JOIN periodos p ON p.id = v.periodo_id
WHERE v.vigente = 1
ORDER BY p.anio, p.mes, v.digito_cuit
LIMIT 20;
""")

rows = cur.fetchall()

print("Año | Mes | Dígito | Fecha vencimiento")
print("---------------------------------------")

for anio, mes, digito, fecha in rows:
    print(f"{anio} | {mes:02d} | {digito} | {fecha}")

conn.close()