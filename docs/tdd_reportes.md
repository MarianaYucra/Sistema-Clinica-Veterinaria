## Módulo de Reportes

### Funciones bajo prueba

El módulo de Reportes cubre las siguientes funciones de consulta/lectura:

| # | Función | Servicio |
|---|---|---|---|
| R1 | Listar clientes | `ClienteService.listar()` |
| R2 | Listar veterinarios | `VeterinarioService.listar()` |
| R3 | Listar mascotas | `MascotaService.listar()` |
| R4 | Listar citas | `CitaService.listar()` |
| R5 | Obtener historial clínico | `AtencionService.obtener_historial(id_mascota)` |


### R1–R4: Listar Entidades (Clientes, Veterinarios, Mascotas, Citas)

Las funciones `listar()` de los 4 servicios comparten el mismo comportamiento: retornan una lista con todos los elementos registrados en memoria. La variable de entrada relevante es la **cantidad de elementos registrados (N)**.

#### 1. Partición de Equivalencia (PE)

##### Objetivo
Dividir la cantidad de elementos registrados en clases donde el comportamiento del listado sea equivalente.

##### Paso 1: Identificar Clases de Equivalencia

| Clase | Condición | Comportamiento esperado |
|---|---|---|
| **Clase válida 1 (vacía)** | N = 0 | Retorna lista vacía `[]` |
| **Clase válida 2 (un elemento)** | N = 1 | Retorna lista con exactamente 1 elemento |
| **Clase válida 3 (múltiples elementos)** | N > 1 | Retorna lista con todos los N elementos registrados |

> [!NOTE]
> No existen clases inválidas para las funciones `listar()` ya que no reciben parámetros de entrada del usuario. Toda entrada es implícita (el estado del repositorio en memoria).

##### Paso 2: Seleccionar Valores Representativos

| Clase | Valor de prueba (N) | Resultado esperado |
|---|---|---|
| Vacía | 0 registros | `[]` (lista vacía) |
| Un elemento | 1 registro | Lista con 1 elemento |
| Múltiples | 3 registros | Lista con 3 elementos |

##### Paso 3: Interpretación

- El valor `0` representa el estado inicial del sistema sin datos.
- El valor `1` representa el caso mínimo con un solo registro.
- El valor `3` representa cualquier cantidad mayor a 1, verificando que el sistema devuelve todos los elementos sin omisiones.

#### 2. Análisis de Valores Límite (AVL)

##### Objetivo
Probar los extremos de la cantidad de elementos registrados, ya que los errores suelen manifestarse en los bordes (lista vacía vs. primer elemento).

##### Paso 1: Identificar Límites

- **Límite inferior**: 0 (sin elementos registrados)
- **Límite operativo mínimo**: 1 (primer elemento)

##### Paso 2: Probar Valores Cercanos a los Límites

| Entrada (N) | Tipo | Resultado esperado |
|---|---|---|
| 0 | Límite inferior (sin registros) | Lista vacía `[]` |
| 1 | Límite inferior + 1 (primer registro) | Lista con 1 elemento |
| 2 | Límite inferior + 2 (segundo registro) | Lista con 2 elementos |


#### 3. Casos de Prueba — Listar Clientes

| ID | Caso de prueba | Técnica | Precondición | Acción | Resultado esperado |
|---|---|---|---|---|---|
| RPT-LC-01 | Listar clientes sin registros | PE (clase vacía) | No hay clientes registrados | Llamar `ClienteService.listar()` | Retorna `[]` |
| RPT-LC-02 | Listar clientes con 1 registro | PE (un elemento) / AVL (límite inferior + 1) | Se registra 1 cliente con ID `"C001"` | Llamar `ClienteService.listar()` | Retorna lista con 1 cliente: `id_cliente="C001"` |
| RPT-LC-03 | Listar clientes con múltiples registros | PE (múltiples) | Se registran 3 clientes: `"C001"`, `"C002"`, `"C003"` | Llamar `ClienteService.listar()` | Retorna lista con 3 clientes |
| RPT-LC-04 | Verificar que listar no altera los datos | PE (integridad) | Se registra 1 cliente con nombre `"Ana López"` | Llamar `listar()` y verificar el nombre del primer elemento | El nombre es exactamente `"Ana López"` |


#### 4. Casos de Prueba — Listar Veterinarios

| ID | Caso de prueba | Técnica | Precondición | Acción | Resultado esperado |
|---|---|---|---|---|---|
| RPT-LV-01 | Listar veterinarios sin registros | PE (clase vacía) | No hay veterinarios registrados | Llamar `VeterinarioService.listar()` | Retorna `[]` |
| RPT-LV-02 | Listar veterinarios con 1 registro | PE (un elemento) / AVL (límite inferior + 1) | Se registra 1 veterinario con ID `"V001"` | Llamar `VeterinarioService.listar()` | Retorna lista con 1 veterinario: `id_veterinario="V001"` |
| RPT-LV-03 | Listar veterinarios con múltiples registros | PE (múltiples) | Se registran 3 veterinarios: `"V001"`, `"V002"`, `"V003"` | Llamar `VeterinarioService.listar()` | Retorna lista con 3 veterinarios |
| RPT-LV-04 | Verificar integridad de datos en listado | PE (integridad) | Se registra veterinario `"V001"` con especialidad `"Cirugía"` | Llamar `listar()` y verificar la especialidad | La especialidad es exactamente `"Cirugía"` |


#### 5. Casos de Prueba — Listar Mascotas

| ID | Caso de prueba | Técnica | Precondición | Acción | Resultado esperado |
|---|---|---|---|---|---|
| RPT-LM-01 | Listar mascotas sin registros | PE (clase vacía) | No hay mascotas registradas | Llamar `MascotaService.listar()` | Retorna `[]` |
| RPT-LM-02 | Listar mascotas con 1 registro | PE (un elemento) / AVL (límite inferior + 1) | Se registra cliente `"C001"` y 1 mascota vinculada | Llamar `MascotaService.listar()` | Retorna lista con 1 mascota |
| RPT-LM-03 | Listar mascotas con múltiples registros | PE (múltiples) | Se registra cliente `"C001"` y 3 mascotas vinculadas | Llamar `MascotaService.listar()` | Retorna lista con 3 mascotas |
| RPT-LM-04 | Verificar vinculación cliente-mascota en listado | PE (integridad referencial) | Se registra cliente `"C001"` y mascota con `id_cliente="C001"` | Llamar `listar()` y verificar `id_cliente` de la mascota | `id_cliente` es `"C001"` |


#### 6. Casos de Prueba — Listar Citas

| ID | Caso de prueba | Técnica | Precondición | Acción | Resultado esperado |
|---|---|---|---|---|---|
| RPT-LCI-01 | Listar citas sin registros | PE (clase vacía) | No hay citas registradas | Llamar `CitaService.listar()` | Retorna `[]` |
| RPT-LCI-02 | Listar citas con 1 registro | PE (un elemento) / AVL (límite inferior + 1) | Se agenda 1 cita con entidades válidas | Llamar `CitaService.listar()` | Retorna lista con 1 cita en estado `"Programada"` |
| RPT-LCI-03 | Listar citas con múltiples registros | PE (múltiples) | Se agendan 3 citas en horarios distintos | Llamar `CitaService.listar()` | Retorna lista con 3 citas |
| RPT-LCI-04 | Listar citas refleja cambio de estado | PE (estado) | Se agenda 1 cita y luego se atiende | Llamar `listar()` | La cita aparece con estado `"Completada"` |


### R5: Obtener Historial Clínico de Mascota

Esta función recibe un parámetro de entrada (`id_mascota: int`) y retorna la lista de registros clínicos asociados ordenados cronológicamente. Es la función más rica del módulo para aplicar PE y AVL.

#### 1. Partición de Equivalencia (PE)

##### Objetivo
Dividir los datos de entrada (`id_mascota`) y la cantidad de registros clínicos en clases con comportamiento equivalente.

##### Paso 1: Identificar Clases de Equivalencia

**Variable 1: `id_mascota` (entrada)**

| Clase | Condición | Comportamiento esperado |
|---|---|---|
| **Válida** | `id_mascota` corresponde a una mascota existente | Retorna la lista de registros (puede ser vacía) |
| **Inválida** | `id_mascota` no corresponde a ninguna mascota registrada | Retorna lista vacía `[]` |

**Variable 2: Cantidad de registros clínicos de la mascota (N)**

| Clase | Condición | Comportamiento esperado |
|---|---|---|
| **Válida 1 (sin historial)** | N = 0 | Retorna `[]` |
| **Válida 2 (un registro)** | N = 1 | Retorna lista con 1 `RegistroClinico` |
| **Válida 3 (múltiples registros)** | N > 1 | Retorna lista con N registros, ordenados cronológicamente por fecha |

##### Paso 2: Seleccionar Valores Representativos

| Clase | Valor de prueba | Resultado esperado |
|---|---|---|
| ID válido, sin historial | `id_mascota=1`, 0 atenciones | `[]` |
| ID válido, un registro | `id_mascota=1`, 1 atención registrada | Lista con 1 `RegistroClinico` |
| ID válido, múltiples registros | `id_mascota=1`, 3 atenciones registradas | Lista con 3 registros ordenados por fecha |
| ID inválido (inexistente) | `id_mascota=999` (no existe) | `[]` |

##### Paso 3: Interpretación

- El `id_mascota=1` con 0 registros verifica que el sistema maneja correctamente una mascota sin historial.
- El `id_mascota=1` con 1 registro verifica el caso mínimo funcional.
- El `id_mascota=1` con 3 registros verifica la acumulación y el ordenamiento cronológico.
- El `id_mascota=999` verifica que el sistema no falla ante un ID sin registros asociados.

#### 2. Análisis de Valores Límite (AVL)

##### Objetivo
Probar los extremos de la cantidad de registros clínicos y los valores límite del `id_mascota`.

##### Paso 1: Identificar Límites

- **Cantidad de registros**: límite inferior = 0, primer registro = 1
- **`id_mascota`**: límite inferior del auto-incremento = 1

##### Paso 2: Probar Valores Cercanos a los Límites

**Límites de cantidad de registros:**

| Entrada | Tipo | Resultado esperado |
|---|---|---|
| Mascota con 0 registros | Límite inferior | `[]` |
| Mascota con 1 registro | Límite inferior + 1 | Lista con 1 registro |
| Mascota con 2 registros | Límite inferior + 2 | Lista con 2 registros ordenados por fecha |

**Límites de `id_mascota`:**

| Entrada | Tipo | Resultado esperado |
|---|---|---|
| `id_mascota = 0` | Límite inferior - 1 (ID no generado) | `[]` (no existe mascota con ID 0) |
| `id_mascota = 1` | Límite inferior (primer ID auto-generado) | Retorna registros de la mascota 1 |
| `id_mascota = 2` | Límite inferior + 1 (segundo ID auto-generado) | Retorna registros de la mascota 2 |
| `id_mascota = -1` | Valor negativo (fuera de rango) | `[]` (no existe mascota con ID negativo) |


#### 3. Casos de Prueba — Historial Clínico

| ID | Caso de prueba | Técnica | Precondición | Acción | Resultado esperado |
|---|---|---|---|---|---|
| RPT-HC-01 | Historial de mascota sin atenciones | PE (sin historial) / AVL (0 registros) | Mascota `id=1` registrada, sin citas atendidas | Llamar `obtener_historial(1)` | Retorna `[]` |
| RPT-HC-02 | Historial de mascota con 1 atención | PE (un registro) / AVL (1 registro) | Mascota `id=1` con 1 cita atendida (fecha `"2026-06-01"`) | Llamar `obtener_historial(1)` | Retorna lista con 1 `RegistroClinico` con fecha `"2026-06-01"` |
| RPT-HC-03 | Historial de mascota con múltiples atenciones | PE (múltiples) | Mascota `id=1` con 3 citas atendidas en fechas: `"2026-01-15"`, `"2026-06-01"`, `"2026-03-10"` | Llamar `obtener_historial(1)` | Retorna 3 registros ordenados: `"2026-01-15"`, `"2026-03-10"`, `"2026-06-01"` |
| RPT-HC-04 | Historial con ID de mascota inexistente | PE (ID inválido) | No existe mascota con `id=999` | Llamar `obtener_historial(999)` | Retorna `[]` |
| RPT-HC-05 | Historial con ID de mascota = 0 | AVL (límite inferior - 1) | No existe mascota con `id=0` | Llamar `obtener_historial(0)` | Retorna `[]` |
| RPT-HC-06 | Historial con ID de mascota negativo | AVL (fuera de rango) | No existe mascota con `id=-1` | Llamar `obtener_historial(-1)` | Retorna `[]` |
| RPT-HC-07 | Historial con primer ID auto-generado | AVL (límite inferior) | Mascota `id=1` (primera registrada) con 1 atención | Llamar `obtener_historial(1)` | Retorna lista con 1 registro |
| RPT-HC-08 | Historial con segundo ID auto-generado | AVL (límite inferior + 1) | Mascota `id=2` (segunda registrada) con 1 atención | Llamar `obtener_historial(2)` | Retorna lista con 1 registro |
| RPT-HC-09 | Verificar aislamiento entre mascotas | PE (filtrado) | Mascota `id=1` con 2 atenciones, mascota `id=2` con 1 atención | Llamar `obtener_historial(1)` | Retorna exactamente 2 registros (no incluye registros de mascota 2) |
| RPT-HC-10 | Verificar contenido del registro clínico | PE (integridad) | Mascota `id=1` atendida con diagnóstico `"Dermatitis"`, tratamiento `"Crema tópica"`, observaciones `"Revisión en 15 días"` | Llamar `obtener_historial(1)` y verificar campos del registro | `diagnostico="Dermatitis"`, `tratamiento="Crema tópica"`, `observaciones="Revisión en 15 días"` |

