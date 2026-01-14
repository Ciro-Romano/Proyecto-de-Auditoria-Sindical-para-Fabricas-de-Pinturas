import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "auditoria.db"
CSV_PATH = BASE_DIR / "data" / "raw" / "contribucion_empresarial.csv"

# PERIODO INICIAL
START_ANIO = 2015
START_MES = 1  # enero

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

def get_or_create_periodo(anio, mes):
    cur.execute(
        "SELECT id FROM periodos WHERE anio=? AND mes=?",
        (anio, mes)
    )
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute(
        "INSERT INTO periodos (anio, mes) VALUES (?, ?)",
        (anio, mes)
    )
    return cur.lastrowid

with open(CSV_PATH, encoding="latin-1") as f:
    reader = csv.reader(f, delimiter=';')
    rows = list(reader)

# Buscar la primera fila que tenga números reales
valores = None
for row in rows:
    if any(c.strip().replace('.', '').replace(',', '').isdigit() for c in row):
        valores = row
        break

if not valores:
    print("No se encontraron valores numéricos.")
    exit()

anio = START_ANIO
mes = START_MES
insertados = 0

for val in valores:
    if not val.strip():
        continue

    try:
        monto = float(val.replace('.', '').replace(',', '.'))
    except ValueError:
        continue

    periodo_id = get_or_create_periodo(anio, mes)

    # desactivar valor anterior
    cur.execute(
        "UPDATE contribucion_empresarial SET vigente=0 WHERE periodo_id=?",
        (periodo_id,)
    )

    cur.execute(
        """
        INSERT INTO contribucion_empresarial
        (periodo_id, monto, vigente)
        VALUES (?, ?, 1)
        """,
        (periodo_id, monto)
    )

    insertados += 1

    # avanzar mes
    mes += 1
    if mes > 12:
        mes = 1
        anio += 1

conn.commit()
conn.close()

print("Contribuciones importadas:", insertados)
