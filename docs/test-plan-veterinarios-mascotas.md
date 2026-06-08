# Plan de Pruebas — VeterinarioService & MascotaService

Técnicas: **Partición de Equivalencia (PE)** y **Análisis de Valores Límite (AVL / BVA)**.

---

## `VeterinarioService`

### `registrar(id_veterinador, nombre, especialidad)`

#### Campo `id_veterinario` — PE (cadena)

| Partición | Rango / Clase | Límite (Frontera) | Valor AVL | Tipo | Resultado Esperado |
|-----------|---------------|-------------------|-----------|------|-------------------|
| P1 | Vacío (Inválido) | — | `""` | PE Inválida | `ValueError` |
| P2 | Solo espacios (Inválido) | — | `"   "` | PE Inválida | `ValueError` |
| P3 | `None` (Inválido) | — | `None` | Robustez | `ValueError` |
| P4 | Tipo incorrecto (Inválido) | — | `123` | Robustez | `AttributeError` |
| P5 | No vacío (Válido) | — | `"VET001"` | PE Válida | Éxito |

#### Campo `nombre` — PE (cadena)

| Partición | Rango / Clase | Límite (Frontera) | Valor AVL | Tipo | Resultado Esperado |
|-----------|---------------|-------------------|-----------|------|-------------------|
| P1 | Vacío (Inválido) | — | `""` | PE Inválida | `ValueError` |
| P2 | Solo espacios (Inválido) | — | `"   "` | PE Inválida | `ValueError` |
| P3 | `None` (Inválido) | — | `None` | Robustez | `ValueError` |
| P4 | Tipo incorrecto (Inválido) | — | `123` | Robustez | `AttributeError` |
| P5 | No vacío (Válido) | — | `"Dr. Pérez"` | PE Válida | Éxito |

#### Campo `especialidad` — PE y Robustez (sin validación)

| Partición | Rango / Clase | Límite (Frontera) | Valor AVL | Tipo | Resultado Esperado |
|-----------|---------------|-------------------|-----------|------|-------------------|
| P1 | Vacío (Válido) | — | `""` | PE — Aceptado | Éxito |
| P2 | No vacío (Válido) | — | `"Cardiología"` | PE Válida | Éxito |
| P3 | `None` (Inválido) | — | `None` | Robustez | `AttributeError` (no validado) |
| P4 | Tipo incorrecto (Inválido) | — | `456` | Robustez | `AttributeError` (no validado) |

#### Duplicado `id_veterinario` — BVA

| Partición | Rango / Clase | Límite (Frontera) | Valor AVL | Tipo | Resultado Esperado |
|-----------|---------------|-------------------|-----------|------|-------------------|
| P1 | No registrado (Válido) | — | `"VET001"` | 1<sup>a</sup> vez | Éxito |
| P2 | Ya registrado (Inválido) | — | `"VET001"` | Duplicado | `ValueError` |

---

### `buscar(id_veterinario)`

| Partición | Rango / Clase | Límite (Frontera) | Valor AVL | Tipo | Resultado Esperado |
|-----------|---------------|-------------------|-----------|------|-------------------|
| P1 | ID existente (Válido) | — | `"VET001"` | PE Válida | `Veterinario` |
| P2 | ID no existente (Inválido) | — | `"VET999"` | PE Inválida | `ValueError` |
| P3 | `None` (Inválido) | — | `None` | Robustez | `ValueError` |
| P4 | Cadena vacía (Inválido) | — | `""` | Robustez | `ValueError` |

---

### `listar()`

| Partición | Rango / Clase | Límite (Frontera) | Valor AVL | Tipo | Resultado Esperado |
|-----------|---------------|-------------------|-----------|------|-------------------|
| P1 | Sin datos (Válido) | — | — | PE | `[]` (lista vacía) |
| P2 | Con 1 veterinario (Válido) | — | — | PE | `[Veterinario]` (1 elemento) |

---

## `MascotaService`

### `registrar(nombre, especie, raza, edad, peso, id_cliente)`

#### Campo `nombre` — PE y Robustez (cadena)

| Partición | Rango / Clase | Límite (Frontera) | Valor AVL | Tipo | Resultado Esperado |
|-----------|---------------|-------------------|-----------|------|-------------------|
| P1 | Vacío (Inválido) | — | `""` | PE Inválida | `ValueError` |
| P2 | Solo espacios (Inválido) | — | `"   "` | PE Inválida | `ValueError` |
| P3 | `None` (Inválido) | — | `None` | Robustez | `ValueError` |
| P4 | Tipo incorrecto (Inválido) | — | `123` | Robustez | `AttributeError` |
| P5 | No vacío (Válido) | — | `"Firulais"` | PE Válida | Éxito |

#### Campo `edad` — BVA y Robustez (entero)

| Partición | Rango / Clase | Límite (Frontera) | Valor AVL | Tipo | Resultado Esperado |
|-----------|---------------|-------------------|-----------|------|-------------------|
| P1 | `< 0` (Inválida) | 0 | `-1` | BVA — Frontera - 1 | `ValueError` |
| P2 | `>= 0` (Válida) | 0 | `0` | BVA — Frontera | Éxito |
| | | 0 | `1` | BVA — Frontera + 1 | Éxito |
| P3 | `None` (Inválido) | — | `None` | Robustez | `TypeError` (no manejado) |
| P4 | Tipo str (Inválido) | — | `"5"` | Robustez | `TypeError` (no manejado) |

#### Campo `peso` — BVA y Robustez (float)

| Partición | Rango / Clase | Límite (Frontera) | Valor AVL | Tipo | Resultado Esperado |
|-----------|---------------|-------------------|-----------|------|-------------------|
| P1 | `<= 0` (Inválida) | 0 | `-1` | BVA — Frontera - 1 | `ValueError` |
| | | 0 | `-0.1` | BVA — Frontera - ε | `ValueError` |
| | | 0 | `0` | BVA — Frontera | `ValueError` |
| P2 | `> 0` (Válida) | 0 | `0.1` | BVA — Frontera + ε | Éxito |
| | | 0 | `1` | BVA — Frontera + 1 | Éxito |
| P3 | `None` (Inválido) | — | `None` | Robustez | `TypeError` (no manejado) |
| P4 | Tipo str (Inválido) | — | `"2.5"` | Robustez | `TypeError` (no manejado) |

#### Campo `id_cliente` — PE y Robustez

| Partición | Rango / Clase | Límite (Frontera) | Valor AVL | Tipo | Resultado Esperado |
|-----------|---------------|-------------------|-----------|------|-------------------|
| P1 | Cliente no registrado (Inválido) | — | `"CLI999"` | PE Inválida | `ValueError` |
| P2 | `None` (Inválido) | — | `None` | Robustez | `ValueError` |
| P3 | Vacío (Inválido) | — | `""` | Robustez | `ValueError` |

#### Campos `especie`, `raza` — PE y Robustez (no validados)

| Partición | Rango / Clase | Límite (Frontera) | Valor AVL | Tipo | Resultado Esperado |
|-----------|---------------|-------------------|-----------|------|-------------------|
| P1 | Vacío (Válido) | — | `""` | PE — Aceptado | Éxito |
| P2 | No vacío (Válido) | — | `"Canino"` / `"Labrador"` | PE Válida | Éxito |
| P3 | `None` (Inválido) | — | `None` | Robustez | `AttributeError` (no validado) |
| P4 | Tipo incorrecto (Inválido) | — | `456` | Robustez | `AttributeError` (no validado) |

---

### `buscar(id_mascota)`

| Partición | Rango / Clase | Límite (Frontera) | Valor AVL | Tipo | Resultado Esperado |
|-----------|---------------|-------------------|-----------|------|-------------------|
| P1 | ID existente (Válido) | — | `1` (el que asigne repo) | PE Válida | `Mascota` |
| P2 | ID no existente (Inválido) | — | `999` | PE Inválida | `ValueError` |
| P3 | `None` (Inválido) | — | `None` | Robustez | `ValueError` |
| P4 | ID negativo (Inválido) | — | `-1` | Robustez | `ValueError` |
| P5 | ID cero (Inválido) | — | `0` | Robustez | `ValueError` |

---

### `listar()`

| Partición | Rango / Clase | Límite (Frontera) | Valor AVL | Tipo | Resultado Esperado |
|-----------|---------------|-------------------|-----------|------|-------------------|
| P1 | Sin datos (Válido) | — | — | PE | `[]` (lista vacía) |
| P2 | Con 1 mascota (Válido) | — | — | PE | `[Mascota]` (1 elemento) |

---

## Resumen de pruebas por archivo

### `test_veterinarios.py` — 17 casos

| # | Método | Técnica | Descripción |
|---|--------|---------|-------------|
| 1 | `registrar` | PE | `id_veterinario` vacío → `ValueError` |
| 2 | `registrar` | PE | `id_veterinario` solo espacios → `ValueError` |
| 3 | `registrar` | Robustez | `id_veterinario=None` → `ValueError` |
| 4 | `registrar` | Robustez | `id_veterinario=123` (int) → `AttributeError` |
| 5 | `registrar` | PE | `nombre` vacío → `ValueError` |
| 6 | `registrar` | PE | `nombre` solo espacios → `ValueError` |
| 7 | `registrar` | Robustez | `nombre=None` → `ValueError` |
| 8 | `registrar` | Robustez | `nombre=123` (int) → `AttributeError` |
| 9 | `registrar` | Robustez | `especialidad=None` → `AttributeError` (no validado) |
| 10 | `registrar` | Robustez | `especialidad=456` (int) → `AttributeError` (no validado) |
| 11 | `registrar` | PE | Todo válido → Éxito |
| 12 | `registrar` | BVA | `id_veterinario` duplicado → `ValueError` |
| 13 | `buscar` | PE | ID existente → retorna `Veterinario` |
| 14 | `buscar` | PE | ID no existente → `ValueError` |
| 15 | `buscar` | Robustez | `None` → `ValueError` |
| 16 | `buscar` | Robustez | `""` → `ValueError` |
| 17 | `listar` | PE | Sin datos → `[]`, con datos → `[Veterinario]` |

### `test_mascotas.py` — 28 casos

| # | Método | Técnica | Descripción |
|---|--------|---------|-------------|
| 1 | `registrar` | PE | `nombre` vacío → `ValueError` |
| 2 | `registrar` | PE | `nombre` solo espacios → `ValueError` |
| 3 | `registrar` | Robustez | `nombre=None` → `ValueError` |
| 4 | `registrar` | Robustez | `nombre=123` (int) → `AttributeError` |
| 5 | `registrar` | BVA | `edad = -1` → `ValueError` |
| 6 | `registrar` | BVA | `edad = 0` → Éxito |
| 7 | `registrar` | BVA | `edad = 1` → Éxito |
| 8 | `registrar` | Robustez | `edad=None` → `TypeError` (no manejado) |
| 9 | `registrar` | Robustez | `edad="5"` (str) → `TypeError` (no manejado) |
| 10 | `registrar` | BVA | `peso = -1` → `ValueError` |
| 11 | `registrar` | BVA | `peso = -0.1` → `ValueError` |
| 12 | `registrar` | BVA | `peso = 0` → `ValueError` |
| 13 | `registrar` | BVA | `peso = 0.1` → Éxito |
| 14 | `registrar` | BVA | `peso = 1` → Éxito |
| 15 | `registrar` | Robustez | `peso=None` → `TypeError` (no manejado) |
| 16 | `registrar` | Robustez | `peso="2.5"` (str) → `TypeError` (no manejado) |
| 17 | `registrar` | PE | `id_cliente` no existe → `ValueError` |
| 18 | `registrar` | Robustez | `id_cliente=None` → `ValueError` |
| 19 | `registrar` | Robustez | `id_cliente=""` → `ValueError` |
| 20 | `registrar` | Robustez | `especie=None` → `AttributeError` (no validado) |
| 21 | `registrar` | Robustez | `especie=456` (int) → `AttributeError` (no validado) |
| 22 | `registrar` | PE | Todo válido → Éxito |
| 23 | `buscar` | PE | ID existente → retorna `Mascota` |
| 24 | `buscar` | PE | ID no existente → `ValueError` |
| 25 | `buscar` | Robustez | `None` → `ValueError` |
| 26 | `buscar` | Robustez | `-1` → `ValueError` |
| 27 | `buscar` | Robustez | `0` → `ValueError` |
| 28 | `listar` | PE | Sin datos → `[]`, con datos → `[Mascota]` |
