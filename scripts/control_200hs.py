import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "auditoria.db"

def obtener_valor_200hs(categoria, anio, mes):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT rh.monto
        FROM remuneraciones_200hs rh
        JOIN categorias c ON c.id = rh.categoria_id
        JOIN periodos p ON p.id = rh.periodo_id
        WHERE c.nombre = ?
          AND p.anio = ?
          AND p.mes = ?
          AND rh.vigente = 1
    """, (categoria, anio, mes))

    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def controlar(valor_declarado, categoria, anio, mes):
    if valor_declarado is None:
        return None

    valor_oficial = obtener_valor_200hs(categoria, anio, mes)

    if valor_oficial is None:
        return "SIN PARAMETRO"

    if valor_declarado < valor_oficial:
        return "MENOR AL MINIMO"

    return "OK"

# ---- PRUEBA ----
categoria = "12"
anio = 2016
mes = 3
valor_declarado = 8000  # ejemplo

resultado = controlar(valor_declarado, categoria, anio, mes)
print("Resultado del control:", resultado)
