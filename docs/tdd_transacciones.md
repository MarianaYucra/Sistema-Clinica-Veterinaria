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
