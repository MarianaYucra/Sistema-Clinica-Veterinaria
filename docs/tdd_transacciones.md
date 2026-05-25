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

## Fase 3: Descuentos

RED:
Se agregaron pruebas para revisar los limites permitidos del descuento.

Casos definidos:
- Descuento de 0% debe generar monto descontado 0.
- Descuento de 100% debe descontar todo el subtotal.
- Descuento menor a 0% debe rechazarse.
- Descuento mayor a 100% debe rechazarse.

GREEN:
Se uso `validar_descuento(descuento)` desde `aplicar_descuento(subtotal, descuento)` para aceptar solo valores entre 0 y 100.

Codigo trabajado:
- `validar_descuento(descuento)`
- `aplicar_descuento(subtotal, descuento)`

REFACTOR:
La validacion del descuento quedo separada para que no se repita si luego se usa en otra parte del flujo de pagos.

## Fase 4: Total del pago

RED:
Se agregaron pruebas para comprobar el total final del pago con y sin descuento.

Casos definidos:
- Si no se envia descuento, el sistema debe usar 0%.
- Si se envia un descuento valido, debe restarse del subtotal.

GREEN:
Se uso `calcular_total(precios, descuento=0)` combinando el subtotal y el monto descontado.

Codigo trabajado:
- `calcular_total(precios, descuento)`
- `calcular_subtotal(precios)`
- `aplicar_descuento(subtotal, descuento)`

REFACTOR:
El descuento quedo con valor por defecto 0 para representar pagos normales sin promocion.
