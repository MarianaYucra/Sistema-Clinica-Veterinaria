import pytest

from app.main import aplicar_descuento, calcular_subtotal


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


# AVL - Descuentos

def test_aplicar_descuento_con_cero_por_ciento():
    assert aplicar_descuento(100, 0) == 0


def test_aplicar_descuento_con_cien_por_ciento():
    assert aplicar_descuento(100, 100) == 100


def test_aplicar_descuento_menor_a_cero_lanza_error():
    with pytest.raises(ValueError):
        aplicar_descuento(100, -1)


def test_aplicar_descuento_mayor_a_cien_lanza_error():
    with pytest.raises(ValueError):
        aplicar_descuento(100, 101)
