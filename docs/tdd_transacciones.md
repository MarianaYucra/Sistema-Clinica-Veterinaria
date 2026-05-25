# TDD - Transacciones

## Objetivo

Agregar la logica de pagos para una atencion veterinaria, manteniendo las funciones simples y probables desde `main.py`.

## Fase 1: Calculo de subtotal

RED:
Se empezo con pruebas para comprobar que el sistema pueda sumar los precios de los servicios realizados en una atencion.

Casos definidos:
- Un solo servicio debe devolver su mismo precio.
- Varios servicios deben devolver la suma total.
- Una lista vacia no debe aceptarse como pago valido.

GREEN:
Se uso `calcular_subtotal(precios)` para validar la lista recibida y sumar sus valores.

Codigo trabajado:
- `calcular_subtotal(precios)`

REFACTOR:
La funcion se mantuvo separada porque luego se reutiliza en el calculo del total y en la aplicacion de descuentos.

## Fase 2: Validacion de precios

RED:
Se agregaron pruebas para evitar pagos con servicios de precio cero o negativo.

Casos definidos:
- Un servicio con precio cero debe rechazarse.
- Un servicio con precio negativo debe rechazarse.

GREEN:
Se uso la validacion existente dentro de `calcular_subtotal(precios)` para lanzar `ValueError` cuando algun precio no sea mayor a cero.

Codigo trabajado:
- `calcular_subtotal(precios)`

REFACTOR:
La validacion quedo en la misma funcion porque el subtotal es el primer punto donde se revisan los precios del pago.
