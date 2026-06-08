# REQUERIMIENTOS FUNCIONALES DEL SISTEMA DE CLÍNICA VETERINARIA

### Módulo 1: Gestión de Clientes

| N° | Nombre | Descripción | Prioridad | Actor |
| :--- | :--- | :--- | :--- | :--- |
| **RF-01** | Validación de ID de Cliente | El sistema debe rechazar el registro si la Cédula/DNI no está compuesta exclusivamente por caracteres numéricos o si su longitud no se encuentra entre 8 y 12 dígitos. | Alta | Recepcionista / Administrador |
| **RF-02** | Validación de Duplicidad de ID | El sistema debe verificar en el repositorio que la Cédula/DNI ingresada sea única. Si ya existe, la operación debe ser rechazada. | Alta | Recepcionista / Administrador |
| **RF-03** | Validación de Nombre de Cliente | El sistema debe rechazar el registro si el nombre contiene caracteres distintos a letras y espacios, o si su longitud es inferior a 2 caracteres alfabéticos. | Alta | Recepcionista / Administrador |
| **RF-04** | Validación de Teléfono | El sistema debe rechazar el registro si el número telefónico contiene caracteres no numéricos o si su longitud está fuera del rango de 7 a 15 dígitos. | Media | Recepcionista / Administrador |
| **RF-05** | Validación de Formato de Email | El sistema debe validar que el correo electrónico cumpla con una estructura de formato válida (usuario@dominio.extensión). | Media | Recepcionista / Administrador |
| **RF-06** | Validación de Duplicidad de Email | El sistema debe rechazar el registro si el correo electrónico ingresado (ignorando mayúsculas/minúsculas) ya se encuentra asociado a otro cliente en la base de datos. | Alta | Recepcionista / Administrador |
| **RF-07** | Búsqueda Multicriterio de Cliente | El sistema debe permitir la consulta de un cliente utilizando como criterio de búsqueda su ID, su Nombre exacto o su Email exacto. Si no existe coincidencia, debe emitir un error controlado. | Media | Recepcionista / Administrador |

### Módulo 2: Gestión de Veterinarios

| N° | Nombre | Descripción | Prioridad | Actor |
| :--- | :--- | :--- | :--- | :--- |
| **RF-08** | Validación de ID de Veterinario | El sistema debe rechazar el registro si el ID no cumple con el formato requerido: de 1 a 5 letras opcionales, seguidas estrictamente por 3 a 6 dígitos numéricos. | Alta | Administrador |
| **RF-09** | Validación de Duplicidad de ID | El sistema debe garantizar que el ID del veterinario (normalizado a mayúsculas) no exista previamente en la base de datos. | Alta | Administrador |
| **RF-10** | Validación de Nombre | El sistema debe rechazar el registro si el nombre no contiene al menos 2 caracteres alfabéticos o si incluye caracteres especiales no permitidos (solo letras y espacios). | Alta | Administrador |
| **RF-11** | Validación de Especialidad | El sistema debe rechazar el registro si la especialidad médica contiene números/símbolos o posee menos de 3 caracteres alfabéticos. | Media | Administrador |
| **RF-12** | Búsqueda Multicriterio | El sistema debe permitir localizar veterinarios ingresando su ID (búsqueda exacta), Nombre (búsqueda exacta) o Especialidad (búsqueda parcial/coincidencias múltiples). | Media | Recepcionista / Administrador |

### Módulo 3: Gestión de Mascotas

| N° | Nombre | Descripción | Prioridad | Actor |
| :--- | :--- | :--- | :--- | :--- |
| **RF-13** | Validación de Nombre | El sistema debe rechazar el registro si el nombre contiene menos de 2 caracteres o incluye caracteres fuera del conjunto de letras y espacios. | Alta | Recepcionista |
| **RF-14** | Validación de Especie | El sistema debe rechazar el registro si la especie contiene menos de 2 caracteres o incluye caracteres fuera del conjunto de letras y espacios. | Alta | Recepcionista |
| **RF-15** | Validación de Raza | El sistema debe rechazar el registro si la raza contiene menos de 3 caracteres o incluye caracteres fuera del conjunto de letras y espacios. | Media | Recepcionista |
| **RF-16** | Rango de Edad | El sistema debe rechazar el registro si la edad ingresada no es un valor entero o si se encuentra fuera del rango realista permitido (0 a 35 años). | Alta | Recepcionista |
| **RF-17** | Rango de Peso | El sistema debe rechazar el registro si el peso no es un valor numérico o si se encuentra fuera del rango realista permitido (mayor a 0.01 y hasta 200 kg). | Alta | Recepcionista |
| **RF-18** | Verificación de Relación Dueño-Mascota | El sistema debe verificar que el ID del cliente (dueño) ingresado exista en la base de datos antes de permitir el registro de la mascota. | Alta | Recepcionista |

### Módulo 4: Agenda de Citas Médicas

| N° | Nombre | Descripción | Prioridad | Actor |
| :--- | :--- | :--- | :--- | :--- |
| **RF-19** | Validación de Lógica de Fecha | El sistema debe exigir el formato de fecha YYYY-MM-DD, validar lógicamente el calendario (fechas reales) y rechazar agendamientos cuya fecha sea anterior al día actual. | Alta | Recepcionista |
| **RF-20** | Validación de Lógica de Hora | El sistema debe exigir el formato HH:MM (24h). Si la cita se agenda para el día actual, debe verificar que la hora propuesta sea posterior a la hora actual del reloj del sistema. | Alta | Recepcionista |
| **RF-21** | Integridad Referencial en Agenda | El sistema debe verificar que tanto el ID de la mascota (entero mayor a 0) como el ID del veterinario existan en sus respectivos repositorios antes de agendar la cita. | Alta | Recepcionista |
| **RF-22** | Longitud de Motivo de Cita | El sistema debe rechazar el agendamiento si el texto del motivo de la cita contiene menos de 3 o más de 120 caracteres. | Media | Recepcionista |
| **RF-23** | Prevención de Concurrencia Médica | El sistema debe rechazar la transacción si el veterinario seleccionado ya posee una cita en estado "Programada" para la misma fecha y hora solicitadas. | Alta | Recepcionista |
| **RF-24** | Estado e ID Automáticos | El sistema debe asignar el estado por defecto "Programada" y generar un ID numérico autoincremental de forma automática al confirmar una nueva cita. | Alta | Sistema |

### Módulo 5: Registro de Atenciones (Historial Clínico)

| N° | Nombre | Descripción | Prioridad | Actor |
| :--- | :--- | :--- | :--- | :--- |
| **RF-25** | Validación de Petición de Atención | El sistema debe exigir un ID de cita que sea un número entero mayor a cero, y verificar que dicha cita exista en la base de datos. | Alta | Veterinario |
| **RF-26** | Verificación de Estado Vigente | El sistema debe rechazar el intento de registrar una atención si la cita solicitada no se encuentra estrictamente en el estado "Programada". | Alta | Veterinario |
| **RF-27** | Reglas de Formato para Diagnóstico | El sistema debe rechazar la atención si el diagnóstico tiene menos de 5 o más de 200 caracteres, asegurando que contenga caracteres alfabéticos (no solo números/símbolos). | Alta | Veterinario |
| **RF-28** | Reglas de Formato para Tratamiento | El sistema debe rechazar la atención si el tratamiento tiene menos de 5 o más de 200 caracteres, asegurando que contenga caracteres alfabéticos. | Alta | Veterinario |
| **RF-29** | Límite de Longitud para Observaciones | El sistema debe permitir que el campo observaciones quede vacío, pero si se ingresan datos, la cadena no debe superar los 250 caracteres. | Media | Veterinario |
| **RF-30** | Transición y Herencia de Historial | Al guardar con éxito, el sistema debe cambiar la cita a "Completada" y generar el Registro Clínico heredando inmutablemente el ID de la mascota y la fecha de la cita original. | Alta | Sistema |
| **RF-31** | Recuperación Ordenada de Historial | El sistema debe retornar el historial completo de una mascota mediante su ID, ordenando los registros cronológicamente (ascendente) en base a la fecha de atención. | Alta | Veterinario / Recepcionista |

### Módulo 6: Calculadora de Pagos

| N° | Nombre | Descripción | Prioridad | Actor |
| :--- | :--- | :--- | :--- | :--- |
| **RF-32** | Validación de Captura de Servicios | El sistema debe requerir al menos un servicio facturado con nombre válido (no vacío) y su respectivo precio. | Alta | Recepcionista |
| **RF-33** | Reglas Numéricas de Precios | El sistema debe emitir un error y abortar el cálculo si se ingresa algún precio unitario que sea menor o igual a 0. | Alta | Recepcionista |
| **RF-34** | Límites Porcentuales de Descuento | El sistema debe procesar el porcentaje de descuento asegurándose de que su valor numérico se encuentre estrictamente entre 0 y 100. | Media | Recepcionista |
| **RF-35** | Cálculo Financiero Automatizado | El sistema debe sumar los precios válidos (subtotal), aplicar el porcentaje de descuento sobre este (monto deducido), y restar la deducción para retornar el total neto a pagar. | Alta | Sistema |

### Módulo 7: Interfaz y Estabilidad del Sistema

| N° | Nombre | Descripción | Prioridad | Actor |
| :--- | :--- | :--- | :--- | :--- |
| **RF-36** | Despliegue de Menú Interactivo | El sistema debe renderizar un menú en consola con opciones numéricas predefinidas del 0 al 13 que mapeen correctamente a cada funcionalidad del negocio. | Baja | Sistema |
| **RF-37** | Captura de Fallos de Tipo (Tipado) | El sistema debe atrapar excepciones cuando se ingrese texto en lugar de números (enteros o flotantes), evitando colapsos del programa y solicitando el reingreso del dato. | Alta | Sistema |
| **RF-38** | Manejo de Interrupciones (Fail-Safe) | El sistema debe interceptar comandos de cancelación (Ctrl+C / KeyboardInterrupt) para cancelar la operación de forma limpia, retornando al menú o saliendo sin corromper memoria. | Alta | Sistema |
