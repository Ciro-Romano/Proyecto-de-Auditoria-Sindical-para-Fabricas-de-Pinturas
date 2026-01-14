-- =========================
-- TABLA: periodos
-- =========================
-- Representa un mes/año (ene-15, feb-16, etc.)
CREATE TABLE periodos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    anio INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    UNIQUE (anio, mes)
);

-- =========================
-- TABLA: categorias
-- =========================
-- Categorías laborales (numéricas o textuales)
CREATE TABLE categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sector TEXT NOT NULL,
    nombre TEXT NOT NULL,
    codigo INTEGER,
    UNIQUE (sector, nombre)
);

-- =========================
-- TABLA: remuneraciones_200hs
-- =========================
-- Valores históricos de remuneración 200 hs
CREATE TABLE remuneraciones_200hs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria_id INTEGER NOT NULL,
    periodo_id INTEGER NOT NULL,
    monto REAL NOT NULL,
    vigente INTEGER NOT NULL DEFAULT 1,
    fecha_carga DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id),
    FOREIGN KEY (periodo_id) REFERENCES periodos(id),
    UNIQUE (categoria_id, periodo_id, vigente)
);

-- =========================
-- TABLA: contribucion_empresarial
-- =========================
-- Monto fijo por período
CREATE TABLE contribucion_empresarial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    periodo_id INTEGER NOT NULL,
    monto REAL NOT NULL,
    vigente INTEGER NOT NULL DEFAULT 1,
    fecha_carga DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (periodo_id) REFERENCES periodos(id),
    UNIQUE (periodo_id, vigente)
);

-- =========================
-- TABLA: vencimientos
-- =========================
-- Vencimientos por período y último dígito de CUIT
CREATE TABLE vencimientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    periodo_id INTEGER NOT NULL,
    digito_cuit INTEGER NOT NULL CHECK (digito_cuit BETWEEN 0 AND 9),
    fecha_vencimiento DATE NOT NULL,
    vigente INTEGER NOT NULL DEFAULT 1,
    fecha_carga DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (periodo_id) REFERENCES periodos(id),
    UNIQUE (periodo_id, digito_cuit, vigente)
);
