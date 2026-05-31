# Sistema Clinica Veterinaria

Sistema de gestion para una clinica veterinaria. El proyecto conserva una interfaz de consola y agrega una aplicacion web con Flask.

En la ejecucion por consola, los datos se almacenan en una base de datos SQLite local en `data/clinica.db`. El archivo se crea automaticamente al iniciar el sistema.

## Funcionalidades

- Dashboard con estadisticas generales.
- Gestion de clientes.
- Gestion de veterinarios.
- Gestion de mascotas asociadas a clientes.
- Agenda de citas.
- Registro de atencion medica e historial clinico.
- Calculadora de pagos con subtotal, descuento y total.

## Requisitos

- Python 3.10 o superior.
- pip.

## Instalacion

En Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

En Linux o macOS:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Ejecutar Aplicacion Web

Desde la raiz del proyecto:

```powershell
python -m app.webapp
```

Luego abre:

```text
http://127.0.0.1:5000/
```

## Ejecutar Modo Consola

Desde la raiz del proyecto:

```powershell
python -m app.main
```

## Ejecutar Pruebas

```powershell
python -m pytest -q
```

Con cobertura:

```powershell
coverage run -m pytest
coverage report
```

## Docker

Construir imagen:

```powershell
docker build -t clinica-veterinaria .
```

Ejecutar contenedor:

```powershell
docker run --rm -p 5000:5000 clinica-veterinaria
```

La aplicacion quedara disponible en:

```text
http://127.0.0.1:5000/
```

## Estructura Principal

```text
app/
├── main.py          # Interfaz de consola
├── webapp.py        # Aplicacion web Flask
├── models.py        # Entidades
├── repository.py    # Repositorios en memoria
├── services.py      # Logica de negocio
├── templates/       # Vistas Jinja2
└── static/          # CSS y JavaScript
```
