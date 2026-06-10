# Reporte de condiciones de entrada

Este reporte describe las condiciones de entrada que acepta actualmente el backend para los registros de clientes, veterinarios, mascotas y citas. Las reglas salen de `backend/app/services/validation.py` y `backend/app/services/clinic.py`.

## Reglas generales

- Los campos de texto obligatorios no pueden ser `null`, cadena vacía ni solo espacios.
- Los espacios al inicio y al final se eliminan antes de validar.
- Cuando un campo tiene longitud máxima, se valida después de eliminar espacios externos.
- La API espera cuerpos JSON.
- Las validaciones de existencia y unicidad se realizan contra la base de datos.

## Registro de clientes

Endpoint: `POST /api/clientes`

Campos esperados:

| Campo | Tipo esperado | Condiciones admitidas | Ejemplos válidos | Ejemplos inválidos |
|---|---:|---|---|---|
| `id_cliente` | Texto numérico | Obligatorio. Solo dígitos. Entre 8 y 12 caracteres. Debe ser único. | `"12345678"`, `"001234567890"` | `"1234567"`, `"1234567890123"`, `"1234ABCD"`, `"1234 5678"`, `""` |
| `nombre` | Texto | Obligatorio. Máximo 120 caracteres. Solo letras y espacios. Debe tener al menos 2 letras. | `"Ana Torres"`, `"Jose Luis"` | `"A"`, `"Ana2"`, `"Ana-Torres"`, `"Ana."`, `""` |
| `telefono` | Texto numérico | Obligatorio. Solo dígitos. Entre 7 y 15 caracteres. No acepta espacios, guiones ni prefijo `+`. No está limitado solo a Perú. | `"987654321"`, `"1234567"`, `"51987654321"` | `"987 654 321"`, `"+51987654321"`, `"987-654-321"`, `"123456"`, `"telefono"` |
| `email` | Texto | Obligatorio. Máximo 160 caracteres. Debe cumplir formato básico `usuario@dominio.ext`. Debe ser único sin distinguir mayúsculas/minúsculas. | `"ana@mail.com"`, `"user.name+tag@example.org"` | `"ana@mail"`, `"ana.com"`, `"ana@.com"`, `"ana mail@example.com"`, `""` |

Ejemplo JSON válido:

```json
{
  "id_cliente": "12345678",
  "nombre": "Ana Torres",
  "telefono": "987654321",
  "email": "ana.torres@example.com"
}
```

## Registro de veterinarios

Endpoint: `POST /api/veterinarios`

Campos esperados:

| Campo | Tipo esperado | Condiciones admitidas | Ejemplos válidos | Ejemplos inválidos |
|---|---:|---|---|---|
| `id_veterinario` | Texto alfanumérico | Obligatorio. Máximo 11 caracteres. Debe tener de 1 a 5 letras seguidas por 3 a 6 números. Se convierte a mayúsculas antes de guardar. Debe ser único. | `"VET001"`, `"vet123"`, `"CARD123456"` | `"001VET"`, `"VET12"`, `"VETERI123"`, `"VET-001"`, `"VET001A"` |
| `nombre` | Texto | Obligatorio. Máximo 120 caracteres. Acepta letras, espacios y puntos. | `"Dr. Luis Perez"`, `"Maria Torres"` | `"Dr. Luis 2"`, `"Luis-Perez"`, `"Luis@"`, `""` |
| `especialidad` | Texto | Obligatorio. Máximo 120 caracteres. Solo letras y espacios. Debe tener al menos 3 letras. | `"Cirugia"`, `"Medicina interna"` | `"OR"`, `"Cirugia 2"`, `"Medicina-interna"`, `"Dermatologia."`, `""` |

Ejemplo JSON válido:

```json
{
  "id_veterinario": "vet001",
  "nombre": "Dr. Luis Perez",
  "especialidad": "Cirugia"
}
```

Nota: aunque el ejemplo usa minúsculas en `id_veterinario`, el backend lo normaliza a mayúsculas y lo guarda como `"VET001"`.

## Registro de mascotas

Endpoint: `POST /api/mascotas`

Campos esperados:

| Campo | Tipo esperado | Condiciones admitidas | Ejemplos válidos | Ejemplos inválidos |
|---|---:|---|---|---|
| `nombre` | Texto | Obligatorio. Máximo 80 caracteres. Mínimo 2 caracteres. Solo letras ASCII, números, espacios, puntos y guiones. | `"Firulais"`, `"K-9"`, `"Luna 2"`, `"Draco."` | `"Ñato"`, `"Mía"`, `"A"`, `"Luna@"`, `""` |
| `especie` | Texto | Obligatorio. Máximo 80 caracteres. Solo letras y espacios. Debe tener al menos 2 letras. | `"Perro"`, `"Gato"`, `"Ave domestica"` | `"P"`, `"Perro2"`, `"Ave-domestica"`, `"Gato."`, `""` |
| `raza` | Texto | Obligatorio. Máximo 80 caracteres. Solo letras y espacios. Debe tener al menos 2 letras. | `"Labrador"`, `"Mestizo"`, `"Pastor Aleman"` | `"X"`, `"Pastor-Aleman"`, `"Mestizo2"`, `"Raza."`, `""` |
| `edad` | Número entero | Obligatorio. Entero entre 0 y 150. No acepta booleanos. | `0`, `3`, `15`, `"7"` | `-1`, `151`, `true`, `"tres"`, `3.5` |
| `peso` | Número | Obligatorio. Mayor a 0 y menor o igual a 1000. No acepta booleanos. | `0.5`, `12`, `32.75`, `"8.4"` | `0`, `-2`, `1000.1`, `true`, `"pesado"` |
| `id_cliente` | Texto numérico | Obligatorio. Mismas reglas de DNI de cliente: solo dígitos, entre 8 y 12 caracteres. El cliente debe existir en base de datos. | `"12345678"` | `"1234567"`, `"1234ABCD"`, `"1234 5678"`, `"99999999"` si no existe |

Ejemplo JSON válido:

```json
{
  "nombre": "Luna",
  "especie": "Perro",
  "raza": "Mestizo",
  "edad": 4,
  "peso": 12.5,
  "id_cliente": "12345678"
}
```

Notas:

- `edad` y `peso` pueden llegar como número JSON o como texto numérico; el backend los convierte.
- El nombre de mascota usa una expresión regular ASCII, por eso nombres con tildes o `ñ` no son admitidos actualmente.

## Registro de citas

Endpoint: `POST /api/citas`

Campos esperados:

| Campo | Tipo esperado | Condiciones admitidas | Ejemplos válidos | Ejemplos inválidos |
|---|---:|---|---|---|
| `fecha` | Texto fecha | Obligatorio. Formato `YYYY-MM-DD`. Debe ser una fecha real. No puede estar en el pasado respecto a la fecha del servidor. | `"2099-06-10"`, `"2099-12-31"` | `"10/06/2026"`, `"2026-02-30"`, fecha anterior al día actual, `""` |
| `hora` | Texto hora | Obligatorio. Formato `HH:MM` en 24 horas. Debe ser una hora real. | `"09:00"`, `"13:30"`, `"23:59"` | `"9:00"`, `"24:00"`, `"13:60"`, `"1 PM"`, `""` |
| `id_mascota` | Número entero | Obligatorio. Entero mayor a 0. No acepta booleanos. La mascota debe existir en base de datos. | `1`, `25`, `"3"` | `0`, `-1`, `true`, `"abc"`, `9999` si no existe |
| `id_veterinario` | Texto alfanumérico | Obligatorio. Mismas reglas del ID de veterinario. Se convierte a mayúsculas. El veterinario debe existir en base de datos. | `"VET001"`, `"vet123"` | `"VET12"`, `"001VET"`, `"VET-001"`, `"NOEXISTE999"` si no existe |
| `motivo` | Texto | Obligatorio. Máximo 240 caracteres. No puede estar vacío. | `"Consulta general"`, `"Vacunacion anual"` | `""`, `"   "`, texto de más de 240 caracteres |

Reglas adicionales:

- No se permite agendar una cita para un veterinario que ya tiene una cita `Programada` en la misma fecha y hora.
- Al crearse, la cita queda con estado `"Programada"`.

Ejemplo JSON válido:

```json
{
  "fecha": "2099-06-10",
  "hora": "10:30",
  "id_mascota": 1,
  "id_veterinario": "VET001",
  "motivo": "Consulta general"
}
```

## Casos de prueba sugeridos

| Módulo | Caso válido mínimo | Caso inválido recomendado |
|---|---|---|
| Clientes | DNI de 8 dígitos, teléfono de 7 dígitos, email válido | Teléfono con espacios o guiones |
| Veterinarios | ID con letras y 3 números | ID con números antes de letras |
| Mascotas | Edad `0`, peso `0.5`, cliente existente | Mascota con cliente inexistente |
| Citas | Fecha de hoy o futura, hora `HH:MM`, mascota y veterinario existentes | Fecha pasada o conflicto de horario |
