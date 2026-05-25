# pyrefly: ignore [missing-import]
import pytest

from app.main import aplicar_descuento, calcular_subtotal, calcular_total


# PE - Subtotal

class TestSubtotal:
    @pytest.mark.parametrize(
        "precios, esperado",
        [
            ([50], 50),
            ([50, 30, 20], 100),
        ],
    )
    def test_calcular_subtotal_con_servicios_validos(self, precios, esperado):
        assert calcular_subtotal(precios) == esperado

    def test_calcular_subtotal_sin_servicios_lanza_error(self):
        with pytest.raises(ValueError):
            calcular_subtotal([])


# PE - Precios invalidos

class TestPreciosInvalidos:
    @pytest.mark.parametrize(
        "precios",
        [
            ([50, 0]),
            ([50, -10]),
        ],
    )
    def test_calcular_subtotal_con_precio_no_valido_lanza_error(self, precios):
        with pytest.raises(ValueError):
            calcular_subtotal(precios)


# AVL - Descuentos

class TestDescuentos:
    @pytest.mark.parametrize(
        "subtotal, descuento, esperado",
        [
            (100, 0, 0),
            (100, 100, 100),
        ],
    )
    def test_aplicar_descuento_con_limites_validos(
        self, subtotal, descuento, esperado
    ):
        assert aplicar_descuento(subtotal, descuento) == esperado

    @pytest.mark.parametrize("descuento", [-1, 101])
    def test_aplicar_descuento_fuera_de_rango_lanza_error(
        self, descuento
    ):
        with pytest.raises(ValueError):
            aplicar_descuento(100, descuento)


# PE - Pago total

class TestPagoTotal:
    def test_calcular_total_sin_descuento(self):
        assert calcular_total([50, 30]) == 80

    def test_calcular_total_con_descuento_valido(self):
        assert calcular_total([100, 50], 10) == 135


# AVL - Precios

class TestLimitesPrecios:
    def test_calcular_subtotal_con_precio_minimo_valido(self):
        assert calcular_subtotal([0.01]) == 0.01

    def test_calcular_subtotal_con_precio_limite_invalido_cero(self):
        with pytest.raises(ValueError):
            calcular_subtotal([0])
