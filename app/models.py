from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Cliente:
    id_cliente: str
    nombre: str
    telefono: str
    email: str


@dataclass
class Veterinario:
    id_veterinario: str
    nombre: str
    especialidad: str


@dataclass
class Mascota:
    id_mascota: int
    nombre: str
    especie: str
    raza: str
    edad: int
    peso: float
    id_cliente: str


@dataclass
class Cita:
    id_cita: int
    fecha: str
    hora: str
    id_mascota: int
    id_veterinario: str
    motivo: str
    estado: str = "Programada"


@dataclass
class RegistroClinico:
    id_registro: int
    id_cita: int
    id_mascota: int
    fecha: str
    diagnostico: str
    tratamiento: str
    observaciones: str
