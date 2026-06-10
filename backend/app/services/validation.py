import datetime as dt
import re
from typing import Any

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
VET_ID_RE = re.compile(r"^[A-Za-z]{1,5}[0-9]{3,6}$")
PET_NAME_RE = re.compile(r"^[A-Za-z0-9 .-]+$")


def required_text(value: Any, field: str, max_length: int = 240) -> str:
    if value is None:
        raise ValueError(f"{field} es obligatorio.")
    text = str(value).strip()
    if not text:
        raise ValueError(f"{field} es obligatorio.")
    if len(text) > max_length:
        raise ValueError(f"{field} no debe superar {max_length} caracteres.")
    return text


def letters_spaces(value: str, field: str, min_letters: int = 2) -> str:
    if not all(char.isalpha() or char.isspace() for char in value):
        raise ValueError(f"{field} solo debe contener letras y espacios.")
    if sum(char.isalpha() for char in value) < min_letters:
        raise ValueError(f"{field} debe tener al menos {min_letters} letras.")
    return value


def dni(value: Any) -> str:
    text = required_text(value, "El DNI del cliente", 12)
    if not text.isdigit() or not 8 <= len(text) <= 12:
        raise ValueError("El DNI del cliente debe tener entre 8 y 12 numeros.")
    return text


def email(value: Any) -> str:
    text = required_text(value, "El correo del cliente", 160)
    if not EMAIL_RE.fullmatch(text):
        raise ValueError("El correo del cliente no tiene un formato valido.")
    return text


def phone(value: Any) -> str:
    text = required_text(value, "El telefono del cliente", 15)
    if not text.isdigit() or not 7 <= len(text) <= 15:
        raise ValueError("El telefono del cliente debe tener entre 7 y 15 numeros.")
    return text


def veterinarian_id(value: Any) -> str:
    text = required_text(value, "El ID del veterinario", 11).upper()
    if not VET_ID_RE.fullmatch(text):
        raise ValueError("El ID del veterinario debe tener letras y de 3 a 6 numeros.")
    return text


def positive_int(value: Any, field: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{field} debe ser un numero entero.")
    if isinstance(value, float) and not value.is_integer():
        raise ValueError(f"{field} debe ser un numero entero.")
    if isinstance(value, str) and not value.strip().isdigit():
        raise ValueError(f"{field} debe ser un numero entero.")
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} debe ser un numero entero.") from exc
    if number <= 0:
        raise ValueError(f"{field} debe ser mayor a cero.")
    return number


def age(value: Any) -> int:
    if isinstance(value, bool):
        raise ValueError("La edad debe ser un numero entero.")
    if isinstance(value, float) and not value.is_integer():
        raise ValueError("La edad debe ser un numero entero.")
    if isinstance(value, str) and not value.strip().isdigit():
        raise ValueError("La edad debe ser un numero entero.")
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("La edad debe ser un numero entero.") from exc
    if number < 0 or number > 150:
        raise ValueError("La edad debe estar entre 0 y 150.")
    return number


def weight(value: Any) -> float:
    if isinstance(value, bool):
        raise ValueError("El peso debe ser un numero.")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("El peso debe ser un numero.") from exc
    if number <= 0 or number > 1000:
        raise ValueError("El peso debe ser mayor a cero y menor o igual a 1000.")
    return number


def appointment_date(value: Any) -> str:
    text = required_text(value, "La fecha", 10)
    try:
        date = dt.datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError("La fecha debe tener formato YYYY-MM-DD.") from exc
    if date < dt.date.today():
        raise ValueError("La fecha de la cita no puede estar en el pasado.")
    return date.isoformat()


def appointment_time(value: Any) -> str:
    text = required_text(value, "La hora", 5)
    try:
        time = dt.datetime.strptime(text, "%H:%M").time()
    except ValueError as exc:
        raise ValueError("La hora debe tener formato HH:MM de 24 horas.") from exc
    return time.strftime("%H:%M")
