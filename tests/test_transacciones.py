import pytest

from app.main import calcular_subtotal


# PE - Subtotal

def test_calcular_subtotal_con_un_servicio_valido():
    assert calcular_subtotal([50]) == 50


def test_calcular_subtotal_con_varios_servicios_validos():
    assert calcular_subtotal([50, 30, 20]) == 100


def test_calcular_subtotal_sin_servicios_lanza_error():
    with pytest.raises(ValueError):
        calcular_subtotal([])


# PE - Precios invalidos

def test_calcular_subtotal_con_precio_cero_lanza_error():
    with pytest.raises(ValueError):
        calcular_subtotal([50, 0])


def test_calcular_subtotal_con_precio_negativo_lanza_error():
    with pytest.raises(ValueError):
        calcular_subtotal([50, -10])
