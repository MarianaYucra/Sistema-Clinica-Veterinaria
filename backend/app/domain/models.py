from dataclasses import asdict, dataclass


@dataclass
class Cliente:
    id_cliente: str
    nombre: str
    telefono: str
    email: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Veterinario:
    id_veterinario: str
    nombre: str
    especialidad: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Mascota:
    id_mascota: int
    nombre: str
    especie: str
    raza: str
    edad: int
    peso: float
    id_cliente: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Cita:
    id_cita: int
    fecha: str
    hora: str
    id_mascota: int
    id_veterinario: str
    motivo: str
    estado: str = "Programada"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RegistroClinico:
    id_registro: int
    id_cita: int
    id_mascota: int
    fecha: str
    diagnostico: str
    tratamiento: str
    observaciones: str

    def to_dict(self) -> dict:
        return asdict(self)
