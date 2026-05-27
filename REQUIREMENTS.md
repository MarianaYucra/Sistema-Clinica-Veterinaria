# REQUIREMENTS

Guía de instalación detallada para desplegar el proyecto en Linux, Windows y macOS.

---

## Dependencias

| Herramienta | Versión mínima |  
|-------------|---------------|
| Python      | 3.10+         |
| Pytest      | 8.0.0+        |
| Coverage.py | latest        |

> No se requieren dependencias adicionales más allá de la biblioteca estándar de Python.

---

## Linux

### 1. Instalar Python 3.10+

```bash
# Ubuntu / Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv -y

# Fedora
sudo dnf install python3 python3-pip -y

# Arch Linux
sudo pacman -S python python-pip
```

Verifica:

```bash
python3 --version
```

### 2. Clonar el repositorio

```bash
git clone https://github.com/MarianaYucra/Sistema-Clinica-Veterinaria.git
cd Sistema-Clinica-Veterinaria
```

### 3. Crear y activar el entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install pytest coverage
```

### 5. Ejecutar el sistema

```bash
python3 app/main.py
```

### 6. Ejecutar las pruebas

```bash
pytest -v
```

---

## Windows

### 1. Instalar Python 3.10+

Descarga el instalador desde [https://www.python.org/downloads/](https://www.python.org/downloads/).

> **Importante:** Durante la instalación marca **"Add Python to PATH"** antes de continuar.

Verifica desde PowerShell:

```powershell
python --version
```

### 2. Instalar Git (si no lo tienes)

Descárgalo desde [https://git-scm.com/](https://git-scm.com/) e instálalo con las opciones por defecto.

### 3. Clonar el repositorio

```powershell
git clone https://github.com/MarianaYucra/Sistema-Clinica-Veterinaria.git
cd Sistema-Clinica-Veterinaria
```

### 4. Crear y activar el entorno virtual

```powershell
python -m venv venv
venv\Scripts\activate
```

> Si ves un error de permisos, ejecuta primero:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

### 5. Instalar dependencias

```powershell
pip install pytest coverage
```

### 6. Ejecutar el sistema

```powershell
python app/main.py
```

### 7. Ejecutar las pruebas

```powershell
pytest -v
```

---

## macOS

### 1. Instalar Python 3.10+

```bash
# Instalar Homebrew (si no lo tienes)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python
brew install python
```

Verifica:

```bash
python3 --version
```

### 2. Clonar el repositorio

```bash
git clone https://github.com/MarianaYucra/Sistema-Clinica-Veterinaria.git
cd Sistema-Clinica-Veterinaria
```

### 3. Crear y activar el entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install pytest coverage
```

### 5. Ejecutar el sistema

```bash
python3 app/main.py
```

### 6. Ejecutar las pruebas

```bash
pytest -v
```

---

## Notas generales

- Usa siempre un **entorno virtual** para aislar las dependencias del proyecto.
- Para desactivar el entorno virtual en cualquier sistema:
  ```bash
  deactivate
  ```
- Si `pytest` no se reconoce como comando, prueba:
  ```bash
  python -m pytest -v
  ```
- Para medir cobertura de pruebas:
  ```bash
  coverage run -m pytest
  coverage report
  ```