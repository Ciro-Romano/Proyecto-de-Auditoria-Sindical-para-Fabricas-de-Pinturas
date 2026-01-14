import csv
import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "auditoria.db"
CSV_PATH = BASE_DIR / "data" / "raw" / "vencimientos.csv"

mes_map = {
    'ene':1,'feb':2,'mar':3,'abr':4,'may':5,'jun':6,
    'jul':7,'ago':8,'sep':9,'sept':9,'oct':10,'nov':11,'dic':12
}

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

def get_or_create_periodo(anio, mes):
    cur.execute(
        "SELECT id FROM periodos WHERE anio=? AND mes=?",
        (anio, mes)
    )
    r = cur.fetchone()
    if r:
        return r[0]
    cur.execute(
        "INSERT INTO periodos (anio, mes) VALUES (?,?)",
        (anio, mes)
    )
    return cur.lastrowid

with open(CSV_PATH, encoding="latin-1") as f:
    rows = list(csv.reader(f, delimiter=';'))

insertados = 0

for row in rows[1:]:  # saltar encabezado
    if not row or not row[0].strip():
        continue

    periodo_txt = row[0].strip().lower()

    # aceptar solo formato tipo ene-15
    if '-' not in periodo_txt:
        continue

    partes = periodo_txt.split('-')
    if len(partes) != 2:
        continue

    mes_txt, anio_txt = partes

    if mes_txt not in mes_map:
        continue

    try:
        anio = 2000 + int(anio_txt)
        mes = mes_map[mes_txt]
    except ValueError:
        continue

    periodo_id = get_or_create_periodo(anio, mes)

    for i, fecha_txt in enumerate(row[1:]):
        if not fecha_txt.strip():
            continue

        try:
            fecha = datetime.strptime(fecha_txt.strip(), "%d/%m/%Y").date()
        except ValueError:
            continue

        digito = i  # columnas 0 a 9

        # desactivar vencimiento anterior
        cur.execute("""
            UPDATE vencimientos
            SET vigente=0
            WHERE periodo_id=? AND digito_cuit=?
        """, (periodo_id, digito))

        cur.execute("""
            INSERT INTO vencimientos
            (periodo_id, digito_cuit, fecha_vencimiento, vigente)
            VALUES (?,?,?,1)
        """, (periodo_id, digito, fecha))

        insertados += 1

conn.commit()
conn.close()

print("Vencimientos importados:", insertados)
