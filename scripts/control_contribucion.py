from db import obtener_contribucion


def corresponde_contribucion(h, g):
    """
    h: valor tipo H12 (ej: porcentaje)
    g: valor tipo G12
    Devuelve True si corresponde aplicar contribución
    """
    return (h < 0.02) != (g < 1)


def calcular_contribucion(valor_h, valor_g, anio, mes):
    """
    Reemplazo directo de la fórmula de Excel
    """
    if not corresponde_contribucion(valor_h, valor_g):
        return 0

    contribucion = obtener_contribucion(anio, mes)

    if contribucion is None:
        return "SIN CONTRIBUCION DEFINIDA"

    return contribucion


# --- PRUEBA MANUAL ---
if __name__ == "__main__":
    valor_h = 0.03
    valor_g = 0
    anio = 2016
    mes = 5

    resultado = calcular_contribucion(valor_h, valor_g, anio, mes)
    print("Resultado:", resultado)
