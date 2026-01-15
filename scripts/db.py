import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "auditoria.db"


def obtener_contribucion(anio, mes):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT c.monto
        FROM contribucion_empresarial c
        JOIN periodos p ON p.id = c.periodo_id
        WHERE p.anio = ?
          AND p.mes = ?
          AND c.vigente = 1
    """, (anio, mes))

    row = cur.fetchone()
    conn.close()

    return row[0] if row else None
