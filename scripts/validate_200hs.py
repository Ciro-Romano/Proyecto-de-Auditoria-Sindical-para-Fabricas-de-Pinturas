import sqlite3

conn = sqlite3.connect("data/auditoria.db")
cur = conn.cursor()

cur.execute("""
SELECT 
    p.anio,
    p.mes,
    cg.sector,
    cg.nombre,
    rh.monto
FROM remuneraciones_200hs rh
JOIN categorias cg ON cg.id = rh.categoria_id
JOIN periodos p ON p.id = rh.periodo_id
WHERE cg.nombre = '12'
  AND cg.sector LIKE '%OPER%'
  AND rh.vigente = 1
ORDER BY p.anio, p.mes
LIMIT 5;
""")

rows = cur.fetchall()

for r in rows:
    print(r)

conn.close()
