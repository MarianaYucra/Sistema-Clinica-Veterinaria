from typing import Dict, List, Optional

from app.models import (
    Cita,
    Cliente,
    Mascota,
    RegistroClinico,
    Veterinario,
)


class ClienteRepository:
    def __init__(self):
        self._storage: Dict[str, Cliente] = {}

    def guardar(self, cliente: Cliente) -> None:
        self._storage[cliente.id_cliente] = cliente

    def buscar(self, id_cliente: str) -> Optional[Cliente]:
        return self._storage.get(id_cliente)

    def buscar_por_nombre(self, nombre: str) -> Optional[Cliente]:
        nombre_normalizado = nombre.strip().lower()
        for cliente in self._storage.values():
            if cliente.nombre.lower() == nombre_normalizado:
                return cliente
        return None

    def buscar_por_email(self, email: str) -> Optional[Cliente]:
        email_normalizado = email.strip().lower()
        for cliente in self._storage.values():
            if cliente.email.lower() == email_normalizado:
                return cliente
        return None

    def listar(self) -> List[Cliente]:
        return list(self._storage.values())

    def existe(self, id_cliente: str) -> bool:
        return id_cliente in self._storage


class VeterinarioRepository:
    def __init__(self):
        self._storage: Dict[str, Veterinario] = {}

    def guardar(self, veterinario: Veterinario) -> None:
        self._storage[veterinario.id_veterinario] = veterinario

    def buscar(self, id_veterinario: str) -> Optional[Veterinario]:
        return self._storage.get(id_veterinario)

    def buscar_por_nombre(self, nombre: str) -> Optional[Veterinario]:
        nombre_normalizado = nombre.strip().lower()
        for veterinario in self._storage.values():
            if veterinario.nombre.lower() == nombre_normalizado:
                return veterinario
        return None

    def buscar_por_especialidad(self, especialidad: str) -> Optional[Veterinario]:
        especialidad_normalizada = especialidad.strip().lower()
        for veterinario in self._storage.values():
            if veterinario.especialidad.lower() == especialidad_normalizada:
                return veterinario
        return None

    def listar(self) -> List[Veterinario]:
        return list(self._storage.values())

    def existe(self, id_veterinario: str) -> bool:
        return id_veterinario in self._storage


class MascotaRepository:
    def __init__(self):
        self._storage: Dict[int, Mascota] = {}
        self._next_id: int = 1

    def guardar(self, mascota: Mascota) -> Mascota:
        if mascota.id_mascota == 0:
            mascota.id_mascota = self._next_id
            self._next_id += 1
        self._storage[mascota.id_mascota] = mascota
        return mascota

    def buscar(self, id_mascota: int) -> Optional[Mascota]:
        return self._storage.get(id_mascota)

    def listar(self) -> List[Mascota]:
        return list(self._storage.values())

    def listar_por_cliente(self, id_cliente: str) -> List[Mascota]:
        return [m for m in self._storage.values() if m.id_cliente == id_cliente]

    def existe(self, id_mascota: int) -> bool:
        return id_mascota in self._storage


class CitaRepository:
    def __init__(self):
        self._storage: Dict[int, Cita] = {}
        self._next_id: int = 1

    def guardar(self, cita: Cita) -> Cita:
        if cita.id_cita == 0:
            cita.id_cita = self._next_id
            self._next_id += 1
        self._storage[cita.id_cita] = cita
        return cita

    def buscar(self, id_cita: int) -> Optional[Cita]:
        return self._storage.get(id_cita)

    def listar(self) -> List[Cita]:
        return list(self._storage.values())

    def buscar_por_veterinario_fecha_hora(
        self, id_veterinario: str, fecha: str, hora: str
    ) -> Optional[Cita]:
        for cita in self._storage.values():
            if (
                cita.id_veterinario == id_veterinario
                and cita.fecha == fecha
                and cita.hora == hora
                and cita.estado == "Programada"
            ):
                return cita
        return None


class RegistroClinicoRepository:
    def __init__(self):
        self._storage: Dict[int, RegistroClinico] = {}
        self._next_id: int = 1

    def guardar(self, registro: RegistroClinico) -> RegistroClinico:
        if registro.id_registro == 0:
            registro.id_registro = self._next_id
            self._next_id += 1
        self._storage[registro.id_registro] = registro
        return registro

    def buscar(self, id_registro: int) -> Optional[RegistroClinico]:
        return self._storage.get(id_registro)

    def listar_por_mascota(self, id_mascota: int) -> List[RegistroClinico]:
        return sorted(
            [r for r in self._storage.values() if r.id_mascota == id_mascota],
            key=lambda r: r.fecha,
        )
