import pytest
from finance import calcular_van, margen_contribucion_unitario, punto_equilibrio_unidades

def test_van():
    flujos = [2000, 3000, 4000]
    tasa = 10
    inversion = 7000
    assert round(calcular_van(flujos, tasa, inversion), 2) == pytest.approx(199.48, 0.1)

def test_margen():
    assert margen_contribucion_unitario(100, 60) == 40

def test_equilibrio():
    assert punto_equilibrio_unidades(10000, 100, 60) == 250
