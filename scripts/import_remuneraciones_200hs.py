import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "auditoria.db"
CSV_PATH = BASE_DIR / "data" / "raw" / "remuneraciones_200hs.csv"

# AJUSTE SI EL CSV ES POSICIONAL (sin encabezados de meses)
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

def get_or_create_categoria(sector, nombre):
    codigo = int(nombre) if nombre.strip().isdigit() else None

    cur.execute(
        "SELECT id FROM categorias WHERE sector=? AND nombre=?",
        (sector, nombre)
    )
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute(
        "INSERT INTO categorias (sector, nombre, codigo) VALUES (?, ?, ?)",
        (sector, nombre, codigo)
    )
    return cur.lastrowid

with open(CSV_PATH, encoding="latin-1") as f:
    rows = list(csv.reader(f, delimiter=';'))

sector_actual = None
insertados = 0

def periodos_por_posicion(n):
    anio, mes = START_ANIO, START_MES
    resultado = []
    for _ in range(n):
        resultado.append((anio, mes))
        mes += 1
        if mes > 12:
            mes = 1
            anio += 1
    return resultado

for row in rows:
    if not row or not row[0].strip():
        continue

    # Detectar encabezado de sector (sin valores a la derecha)
    if all(not c.strip() for c in row[1:]):
        sector_actual = row[0].strip()
        continue

    # Ignorar filas antes del primer sector válido
    if not sector_actual:
        continue

    # Fila de categoría con valores
    categoria = row[0].strip()
    categoria_id = get_or_create_categoria(sector_actual, categoria)

    valores = [c for c in row[1:] if c.strip()]
    periodos = periodos_por_posicion(len(valores))

    for (anio, mes), val in zip(periodos, valores):
        try:
            monto = float(val.replace('.', '').replace(',', '.'))
        except ValueError:
            continue

        periodo_id = get_or_create_periodo(anio, mes)

        # Desactivar registro vigente anterior
        cur.execute(
            """
            UPDATE remuneraciones_200hs
            SET vigente = 0
            WHERE categoria_id = ? AND periodo_id = ?
            """,
            (categoria_id, periodo_id)
        )

        cur.execute(
            """
            INSERT INTO remuneraciones_200hs
            (categoria_id, periodo_id, monto, vigente)
            VALUES (?, ?, ?, 1)
            """,
            (categoria_id, periodo_id, monto)
        )

        insertados += 1

conn.commit()
conn.close()

print("Remuneraciones 200 hs importadas:", insertados)