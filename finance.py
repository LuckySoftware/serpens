"""
finance.py
Módulo con funciones financieras:
- Valor Presente Neto (VAN)
- Margen de Contribución
- Punto de Equilibrio
"""

from typing import List


def calcular_van(flujos: List[float], tasa_descuento: float, inversion_inicial: float) -> float:
    """
    Calcula el Valor Actual Neto (VAN).

    :param flujos: Lista de flujos de caja por período (sin incluir inversión inicial)
    :param tasa_descuento: Tasa de descuento anual (en %)
    :param inversion_inicial: Monto de inversión inicial
    :return: Valor Presente Neto
    """
    r = tasa_descuento / 100
    van = sum(flujo / ((1 + r) ** (i + 1)) for i, flujo in enumerate(flujos)) - inversion_inicial
    return round(van, 2)


def margen_contribucion_unitario(precio_venta: float, costo_variable: float) -> float:
    """Calcula el margen de contribución unitario."""
    return round(precio_venta - costo_variable, 2)


def margen_contribucion_porcentual(precio_venta: float, costo_variable: float) -> float:
    """Calcula el margen de contribución porcentual."""
    return round((margen_contribucion_unitario(precio_venta, costo_variable) / precio_venta) * 100, 2)


def punto_equilibrio_unidades(costos_fijos: float, precio_venta: float, costo_variable: float) -> float:
    """Calcula el punto de equilibrio en unidades."""
    margen_unitario = margen_contribucion_unitario(precio_venta, costo_variable)
    if margen_unitario <= 0:
        raise ValueError("El margen de contribución debe ser mayor que cero.")
    return round(costos_fijos / margen_unitario, 2)
