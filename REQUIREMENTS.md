**REQUERIMIENTOS FUNCIONALES DEL SISTEMA DE CLINICA VETERINARIA**

| Requerimiento funcional N°: RF-01 | Nombre: Validación de ID de Cliente |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Recepcionista / Administrador | |
| Descripción: El sistema debe impedir el registro de un cliente si el ID de cliente (Cédula/DNI) está vacío o contiene solo espacios en blanco. | |

| Requerimiento funcional N°: RF-02 | Nombre: Validación de Duplicidad de Cliente |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Recepcionista / Administrador | |
| Descripción: El sistema debe validar que el ID del cliente no exista en el repositorio antes de proceder con el registro. | |

| Requerimiento funcional N°: RF-03 | Nombre: Validación de Nombre de Cliente |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Recepcionista / Administrador | |
| Descripción: El sistema debe impedir el registro de un cliente si el nombre está vacío o contiene solo espacios en blanco. | |

| Requerimiento funcional N°: RF-04 | Nombre: Persistencia de Cliente |
| :--- | :--- |
| Tipo: Registro / Proceso | Prioridad: Alta |
| Actor: Recepcionista / Administrador | |
| Descripción: El sistema debe almacenar el ID, nombre, teléfono y correo electrónico del cliente en el repositorio, eliminando los espacios en blanco sobrantes (trimming). | |

| Requerimiento funcional N°: RF-05 | Nombre: Búsqueda de Cliente por ID |
| :--- | :--- |
| Tipo: Consulta | Prioridad: Alta |
| Actor: Recepcionista / Administrador | |
| Descripción: El sistema debe permitir la consulta y visualización de un cliente específico mediante la introducción de su ID único. | |

| Requerimiento funcional N°: RF-06 | Nombre: Control de Ausencia en Búsqueda de Cliente |
| :--- | :--- |
| Tipo: Validación / Excepción | Prioridad: Alta |
| Actor: Recepcionista / Administrador | |
| Descripción: El sistema debe lanzar un mensaje de error controlado si el ID de cliente buscado no existe en los registros. | |

| Requerimiento funcional N°: RF-07 | Nombre: Listar Clientes |
| :--- | :--- |
| Tipo: Consulta / Reporte | Prioridad: Alta |
| Actor: Recepcionista / Administrador | |
| Descripción: El sistema debe recuperar y mostrar en pantalla un listado general de todos los registros de clientes almacenados. | |

| Requerimiento funcional N°: RF-08 | Nombre: Validación de ID de Veterinario |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Administrador | |
| Descripción: El sistema debe impedir el registro de un veterinario si su ID está vacío o contiene solo espacios en blanco. | |

| Requerimiento funcional N°: RF-09 | Nombre: Validación de Duplicidad de Veterinario |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Administrador | |
| Descripción: El sistema debe validar que el ID del veterinario sea único en el sistema antes de permitir que sea guardado. | |

| Requerimiento funcional N°: RF-10 | Nombre: Validación de Nombre de Veterinario |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Administrador | |
| Descripción: El sistema debe rechazar el registro de un veterinario si el campo del nombre no es proporcionado o viene vacío. | |

| Requerimiento funcional N°: RF-11 | Nombre: Persistencia de Veterinario |
| :--- | :--- |
| Tipo: Registro / Proceso | Prioridad: Alta |
| Actor: Administrador | |
| Descripción: El sistema debe almacenar el ID, nombre y especialidad del veterinario, limpiando los espacios en blanco sobrantes. | |

| Requerimiento funcional N°: RF-12 | Nombre: Búsqueda de Veterinario |
| :--- | :--- |
| Tipo: Consulta | Prioridad: Alta |
| Actor: Administrador / Recepcionista | |
| Descripción: El sistema debe permitir localizar y mostrar los datos de un veterinario ingresando su ID único. | |

| Requerimiento funcional N°: RF-013 | Nombre: Listar Veterinarios |
| :--- | :--- |
| Tipo: Consulta / Reporte | Prioridad: Alta |
| Actor: Administrador / Recepcionista | |
| Descripción: El sistema debe retornar y desplegar la lista completa de todos los veterinarios médicos registrados en la clínica. | |

| Requerimiento funcional N°: RF-14 | Nombre: Validación de Nombre de Mascota |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Recepcionista | |
| Descripción: El sistema debe rechazar el registro de la mascota si el nombre está vacío o contiene únicamente espacios en blanco. | |

| Requerimiento funcional N°: RF-15 | Nombre: Validación de Existencia de Dueño |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Recepcionista | |
| Descripción: El sistema debe verificar que el ID del cliente (dueño) ingresado exista en el repositorio de clientes antes de permitir registrar la mascota. | |

| Requerimiento funcional N°: RF-16 | Nombre: Validación de Edad de Mascota |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Recepcionista | |
| Descripción: El sistema debe impedir el registro si el valor numérico de la edad de la mascota es inferior a 0. | |

| Requerimiento funcional N°: RF-17 | Nombre: Validación de Peso de Mascota |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Recepcionista | |
| Descripción: El sistema debe obligar a que el peso decimal de la mascota sea estrictamente mayor a 0 kg. | |

| Requerimiento funcional N°: RF-19 | Nombre: Búsqueda de Mascota |
| :--- | :--- |
| Tipo: Consulta | Prioridad: Alta |
| Actor: Recepcionista / Veterinario | |
| Descripción: El sistema debe recuperar y mostrar todos los datos de una mascota introduciendo su ID entero único. | |

| Requerimiento funcional N°: RF-21 | Nombre: Validación de Fecha de Cita |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Recepcionista | |
| Descripción: El sistema debe exigir una fecha obligatoria (no vacía) para poder agendar una cita médica. | |

| Requerimiento funcional N°: RF-22 | Nombre: Validación de Hora de Cita |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Recepcionista | |
| Descripción: El sistema debe exigir una hora obligatoria (no vacía) para poder procesar la agenda de una cita médica. | |

| Requerimiento funcional N°: RF-23 | Nombre: Validación de Mascota Existente en Cita |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Recepcionista | |
| Descripción: El sistema debe verificar en el repositorio que la mascota exista a través de su ID antes de asignarle una nueva cita. | |

| Requerimiento funcional N°: RF-24 | Nombre: Validación de Veterinario Existente en Cita |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Recepcionista | |
| Descripción: El sistema debe verificar en el repositorio que el veterinario exista a través de su ID antes de asignarle una nueva cita. | |

| Requerimiento funcional N°: RF-25 | Nombre: Validación de Motivo de Cita |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Recepcionista | |
| Descripción: El sistema debe rechazar el agendamiento si el campo de motivo de consulta médica está vacío. | |

| Requerimiento funcional N°: RF-26 | Nombre: Validación de Concurrencia de Agenda Médica |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Recepcionista / Administrador | |
| Descripción: El sistema debe comprobar que el veterinario seleccionado no posea ya otra cita en estado "Programada" asignada exactamente en la misma fecha y hora solicitada. | |

| Requerimiento funcional N°: RF-27 | Nombre: Asignación de Estado Inicial a Cita |
| :--- | :--- |
| Tipo: Proceso / Automatización | Prioridad: Alta |
| Actor: Sistema | |
| Descripción: El sistema debe asignar por defecto el estado "Programada" a cualquier cita médica que sea generada desde cero. | |

| Requerimiento funcional N°: RF-28 | Nombre: Asignación de ID Autonumérico a Cita |
| :--- | :--- |
| Tipo: Proceso / Automatización | Prioridad: Alta |
| Actor: Sistema | |
| Descripción: El sistema debe generar e indexar automáticamente un ID numérico secuencial e incremental a cada nueva cita aprobada. | |

| Requerimiento funcional N°: RF-29 | Nombre: Listar Citas Medicas |
| :--- | :--- |
| Tipo: Consulta | Prioridad: Alta |
| Actor: Recepcionista / Veterinario | |
| Descripción: El sistema debe mostrar todas las citas registradas en la aplicación reflejando claramente sus datos principales y su estado actual. | |

| Requerimiento funcional N°: RF-30 | Nombre: Verificación de Existencia de Cita para Atención |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Veterinario | |
| Descripción: El sistema debe comprobar que el ID de la cita médica exista en la base de datos antes de permitir al médico abrir el módulo de atención. | |

| Requerimiento funcional N°: RF-31 | Nombre: Verificación de Estado Vigente de la Cita |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Veterinario | |
| Descripción: El sistema debe validar que la cita a atender esté estrictamente en estado "Programada". Si se encuentra en otro estado, debe rechazar la transacción. | |

| Requerimiento funcional N°: RF-32 | Nombre: Validación de Campo Diagnóstico |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Veterinario | |
| Descripción: El sistema debe obligar a que el texto ingresado en el campo "Diagnóstico" no se encuentre vacío o rellenado solo de espacios. | |

| Requerimiento funcional N°: RF-33 | Nombre: Validación de Campo Tratamiento |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Veterinario | |
| Descripción: El sistema debe obligar a que el texto ingresado en el campo "Tratamiento" sea mandatorio y contenga caracteres válidos. | |

| Requerimiento funcional N°: RF-34 | Nombre: Transición Automatizada de Estado de Cita |
| :--- | :--- |
| Tipo: Proceso / Automatización | Prioridad: Alta |
| Actor: Sistema | |
| Descripción: El sistema debe cambiar automáticamente el estado de la cita original de "Programada" a "Completada" al guardar con éxito la atención veterinaria. | |

| Requerimiento funcional N°: RF-35 | Nombre: Persistencia de Registro Clínico |
| :--- | :--- |
| Tipo: Registro / Proceso | Prioridad: Alta |
| Actor: Veterinario | |
| Descripción: El sistema debe salvar un nuevo nodo de historial clínico heredando la fecha y el ID de mascota de la cita procesada, sumándole un ID único autoincremental de registro clínico. | |

| Requerimiento funcional N°: RF-36 | Nombre: Consulta de Historial Clínico |
| :--- | :--- |
| Tipo: Consulta | Prioridad: Alta |
| Actor: Veterinario | |
| Descripción: El sistema debe permitir la extracción integral de los registros clínicos históricos asociados a una mascota ingresando su ID de paciente. | |

| Requerimiento funcional N°: RF-37 | Nombre: Ordenamiento de Historial Clínico |
| :--- | :--- |
| Tipo: Proceso / Datos | Prioridad: Alta |
| Actor: Sistema | |
| Descripción: El sistema debe estructurar y ordenar cronológicamente de forma ascendente (por su fecha) todos los registros clínicos recuperados de una mascota. | |

| Requerimiento funcional N°: RF-38 | Nombre: Validación de Nombre de Servicio Cobrado |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Recepcionista | |
| Descripción: El sistema debe rechazar el procesamiento del cobro si el nombre del servicio facturado se envía en blanco. | |

| Requerimiento funcional N°: RF-39 | Nombre: Validación de Rango de Precio Unitario |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Recepcionista | |
| Descripción: El sistema debe emitir un error y detener el cálculo matemático de caja si algún precio unitario digitado es igual o menor a 0. | |

| Requerimiento funcional N°: RF-40 | Nombre: Cálculo Automatizado de Subtotal |
| :--- | :--- |
| Tipo: Proceso | Prioridad: Alta |
| Actor: Sistema | |
| Descripción: El sistema debe sumar de manera íntegra y precisa los precios de todos los servicios ingresados para obtener el subtotal bruto. | |

| Requerimiento funcional N°: RF-41 | Nombre: Validación del Rango Porcentual de Descuento |
| :--- | :--- |
| Tipo: Validación | Prioridad: Alta |
| Actor: Recepcionista | |
| Descripción: El sistema debe validar aritméticamente que el porcentaje de descuento capturado se mantenga estrictamente entre los valores numéricos de 0 y 100. | |

| Requerimiento funcional N°: RF-42 | Nombre: Cálculo de Deducción por Descuento |
| :--- | :--- |
| Tipo: Proceso / Cálculo | Prioridad: Alta |
| Actor: Sistema | |
| Descripción: El sistema debe calcular el monto monetario a deducir aplicando la fórmula matemática de porcentaje sobre el subtotal bruto del pago actual. | |

| Requerimiento funcional N°: RF-43 | Nombre: Cálculo de Total Neto a Pagar |
| :--- | :--- |
| Tipo: Proceso / Cálculo | Prioridad: Alta |
| Actor: Sistema | |
| Descripción: El sistema debe restar el monto calculado por concepto de descuento al subtotal bruto para renderizar e imprimir en pantalla el total neto final a pagar por el cliente. | |

| Requerimiento funcional N°: RF-44 | Nombre: Despliegue de Menú de Opciones Principal |
| :--- | :--- |
| Tipo: InteRF-az de usuario | Prioridad: Alta |
| Actor: Sistema | |
| Descripción: El sistema debe renderizar mediante caracteres estándar un menú interactivo en la consola con 14 comandos lógicos ejecutables (opciones del 0 al 13). | |

| Requerimiento funcional N°: RF-45 | Nombre: Captura y Validación de Datos Tipo Entero |
| :--- | :--- |
| Tipo: Validación / InteRF-az | Prioridad: Alta |
| Actor: Sistema | |
| Descripción: El sistema debe atrapar las excepciones de entrada de datos (ValueError) cuando se solicita un dato entero (IDs numéricos, opciones del menú) y solicitar la re-introducción del dato hasta recibir un formato numérico válido. | |

| Requerimiento funcional N°: RF-46 | Nombre: Captura y Validación de Datos Tipo Flotante |
| :--- | :--- |
| Tipo: Validación / InteRF-az | Prioridad: Alta |
| Actor: Sistema | |
| Descripción: El sistema debe verificar de forma activa que los valores de entrada designados como decimales (pesos, precios) contengan una estructura numérica válida antes de enviarla a las capas del servicio. | |

| Requerimiento funcional N°: RF-47 | Nombre: Manejo Seguro de Interrupción por Teclado |
| :--- | :--- |
| Tipo: Excepción / Control | Prioridad: Alta |
| Actor: Sistema | |
| Descripción: El sistema debe capturar el evento nativo KeyboardInterrupt (Ctrl+C) gatillado por el usuario con el fin de abortar de forma limpia el flujo actual o salir del sistema sin corromper la memoria volátil de la aplicación. | |
