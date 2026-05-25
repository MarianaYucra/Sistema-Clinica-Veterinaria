# TDD - Transacciones

## Objetivo

Agregar logica de pagos para una atencion veterinaria dentro de `main.py`.

Funciones trabajadas:
- `calcular_subtotal(precios)`
- `validar_descuento(descuento)`
- `aplicar_descuento(subtotal, descuento)`
- `calcular_total(precios, descuento)`
- `registrar_pago_atencion()`

## Tecnicas usadas

Se usaron pruebas con `pytest`, clases para agrupar escenarios y parametrizacion para evitar repetir casos parecidos.

Las pruebas se separaron en casos PE y AVL:
- PE: particiones validas e invalidas.
- AVL: valores limite de descuentos y precios.

## Fase 1: Calculo de subtotal

RED:
Se definieron pruebas para comprobar que el sistema pueda sumar los precios de los servicios realizados.

Casos:
- Un servicio valido.
- Varios servicios validos.
- Lista vacia.

GREEN:
Se uso `calcular_subtotal(precios)` para sumar los valores y rechazar listas vacias.

REFACTOR:
Los casos validos se agruparon con `pytest.mark.parametrize` dentro de `TestSubtotal`.

## Fase 2: Validacion de precios

RED:
Se agregaron pruebas para rechazar precios que no representan un cobro valido.

Casos:
- Precio cero.
- Precio negativo.

GREEN:
Se mantuvo la validacion dentro de `calcular_subtotal(precios)`, exigiendo precios mayores a cero.

REFACTOR:
Los casos invalidos se agruparon con parametrizacion dentro de `TestPreciosInvalidos`.

## Fase 3: Descuentos

RED:
Se probaron los limites permitidos del descuento.

Casos:
- Descuento 0%.
- Descuento 100%.
- Descuento -1%.
- Descuento 101%.

GREEN:
Se uso `validar_descuento(descuento)` desde `aplicar_descuento(subtotal, descuento)`.

REFACTOR:
Los descuentos validos e invalidos se separaron en dos pruebas parametrizadas dentro de `TestDescuentos`.

## Fase 4: Total del pago

RED:
Se agregaron pruebas para calcular el pago final con y sin descuento.

Casos:
- Pago sin descuento.
- Pago con descuento valido.

GREEN:
Se uso `calcular_total(precios, descuento=0)`, combinando subtotal y descuento.

REFACTOR:
El descuento quedo con valor por defecto 0 para representar pagos normales.

## Fase 5: Limites de precios

RED:
Se agregaron pruebas para diferenciar el minimo valido del limite invalido.

Casos:
- Precio 0.01.
- Precio 0.

GREEN:
La validacion existente de precios mayores a cero cubrio ambos casos.

REFACTOR:
No se agrego otra funcion porque `calcular_subtotal(precios)` ya centraliza esa regla.
