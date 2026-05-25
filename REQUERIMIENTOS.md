# REQUIREMENTS — Sistema de Gestión de Clínica Veterinaria

## Descripción general
MVP (Producto Mínimo Viable) de un sistema web para clínica veterinaria desarrollado en Python y Flask. El sistema permite registrar clientes (dueños) y mascotas (pacientes), gestionar el ciclo completo de una cita médica (programada → en atención → finalizada) y generar recetas médicas/comprobantes automáticos en formato PDF con impuestos y un código QR único de validación.

---

## Requisitos Funcionales

### RF-01 — Gestión de Clientes (Dueños)
* El sistema debe permitir registrar un cliente con: DNI, nombre, apellido, teléfono y email.
* El DNI debe ser una cadena válida (no vacía, no nula, ni compuesta solo por espacios).
* El email debe ser un correo válido y contener obligatoriamente el carácter `@`.
* No se permiten dos clientes con el mismo número de DNI en el sistema.
* El sistema debe permitir buscar y recuperar los datos de un cliente mediante su DNI.

### RF-02 — Gestión de Mascotas (Pacientes)
* El sistema debe permitir registrar mascotas asociadas a un cliente con: ID de mascota, nombre, especie (ej. CANINO, FELINO), edad y peso.
* La edad de la mascota debe ser un número entero mayor o igual a cero ($\ge 0$).
* El peso de la mascota en kilogramos debe ser un valor estrictamente positivo ($> 0$).
* Cada mascota tendrá un identificador único. El sistema debe permitir listar todas las mascotas de un cliente específico.

### RF-03 — Gestión de Citas Médicas
* El sistema debe permitir crear una cita médica vinculando a un cliente, una mascota y un veterinario disponible, asignando fecha y hora.
* La fecha de la cita debe ser programada para el día actual o una fecha futura.
* Una cita puede crearse inicialmente en estado: `PROGRAMADA`.
* El sistema calcula automáticamente el costo base de la consulta médica según la especialidad del veterinario asignado.
* Una cita puede ser cancelada; al hacerlo, el estado de la cita cambia a `CANCELADA` y se libera el horario del veterinario.

### RF-04 — Inicio de Atención (Check-in de Cita)
* El sistema debe permitir iniciar la consulta médica únicamente si la cita está en estado `PROGRAMADA`.
* Al iniciar la atención, el estado de la cita pasa a `EN_ATENCION`.
* No se puede iniciar la atención de una cita que ya fue cancelada, finalizada o que ya se encuentra activa.

### RF-05 — Cierre de Consulta y Facturación
* El sistema debe permitir finalizar la consulta de una cita que se encuentre en estado `EN_ATENCION`.
* Al finalizar la atención, el estado de la cita pasa a `FINALIZADA`.
* El sistema genera automáticamente un reporte/receta médica en formato PDF que incluye un código QR único con los datos del paciente.
* Al mismo tiempo, se genera un comprobante electrónico con un número correlativo, subtotal, impuesto (IGV 18%) y el costo total a pagar.
* No se puede emitir el PDF ni el comprobante de pago de una cita que no haya concluido con éxito (`FINALIZADA`).

---


## Reglas de Negocio

| ID Regla | Descripción de la Regla |
| :--- | :--- |
| **RN-01** | El DNI del cliente debe ser obligatorio, no nulo y no vacío. |
| **RN-02** | El formato de email del cliente debe contener obligatoriamente el carácter `@`. |
| **RN-03** | La edad de la mascota debe ser un valor numérico entero $\ge 0$. |
| **RN-04** | El peso de la mascota debe ser un valor de punto flotante $> 0.0$. |
| **RN-05** | La fecha de una nueva cita programada debe ser $\ge$ a la fecha actual. |
| **RN-06** | Una cita solo puede iniciar atención si su estado actual es `PROGRAMADA`. |
| **RN-07** | Una consulta solo puede finalizarse si su estado actual es `EN_ATENCION`. |
| **RN-08** | El reporte médico digital (PDF) solo se emite sobre citas en estado `FINALIZADA`. |
| **RN-09** | La tasa fija del Impuesto General a las Ventas (IGV) es igual al 18% del subtotal. |
| **RN-10** | El Costo Total de la atención es equivalente a: $\text{Subtotal} + \text{IGV}$. |

---

## Casos de Prueba — Técnicas de Caja Negra

### 1. Partición de Equivalencia (PE)
Divide los datos de entrada en clases equivalentes válidas e inválidas para el entorno de pruebas (`test_clientes.py`):

| Campo / Flujo | Clase Válida | Clase Inválida |
| :--- | :--- | :--- |
| **DNI Cliente** | Cadena de texto con caracteres válidos | Objeto nulo (`None`), cadena vacía (`""`), solo espacios (`"   "`) |
| **Email** | Cadena que incluye el carácter `@` | Cadena sin `@`, texto vacío, nulo |
| **Edad Mascota** | Número entero $\ge 0$ | Números negativos (ej. `-1`, `-5`) |
| **Peso Mascota** | Número decimal (float) $> 0.0$ | Valor igual a `0.0`, valores negativos |
| **Estado para Inicio** | Cita en estado `PROGRAMADA` | Estados `EN_ATENCION`, `CANCELADA`, `FINALIZADA` |
| **Estado para Cierre** | Cita en estado `EN_ATENCION` | Estados `PROGRAMADA`, `CANCELADA`, `FINALIZADA` |
