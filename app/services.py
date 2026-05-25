from typing import List

from app.models import (
    Cita,
    Cliente,
    Mascota,
    RegistroClinico,
    Veterinario,
)
from app.repository import (
    CitaRepository,
    ClienteRepository,
    MascotaRepository,
    RegistroClinicoRepository,
    VeterinarioRepository,
)


class ClienteService:
    def __init__(self, repo: ClienteRepository):
        self._repo = repo

    def registrar(
        self, id_cliente: str, nombre: str, telefono: str, email: str
    ) -> Cliente:
        if not id_cliente or not id_cliente.strip():
            raise ValueError("El ID del cliente no puede estar vacío.")
        if self._repo.existe(id_cliente):
            raise ValueError(
                f"Ya existe un cliente con ID '{id_cliente}'."
            )
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del cliente no puede estar vacío.")
        cliente = Cliente(
            id_cliente=id_cliente.strip(),
            nombre=nombre.strip(),
            telefono=telefono.strip(),
            email=email.strip(),
        )
        self._repo.guardar(cliente)
        return cliente

    def buscar(self, id_cliente: str) -> Cliente:
        cliente = self._repo.buscar(id_cliente)
        if cliente is None:
            raise ValueError(
                f"No se encontró un cliente con ID '{id_cliente}'."
            )
        return cliente

    def listar(self) -> List[Cliente]:
        return self._repo.listar()


class VeterinarioService:
    def __init__(self, repo: VeterinarioRepository):
        self._repo = repo

    def registrar(
        self, id_veterinario: str, nombre: str, especialidad: str
    ) -> Veterinario:
        if not id_veterinario or not id_veterinario.strip():
            raise ValueError("El ID del veterinario no puede estar vacío.")
        if self._repo.existe(id_veterinario):
            raise ValueError(
                f"Ya existe un veterinario con ID '{id_veterinario}'."
            )
        if not nombre or not nombre.strip():
            raise ValueError(
                "El nombre del veterinario no puede estar vacío."
            )
        veterinario = Veterinario(
            id_veterinario=id_veterinario.strip(),
            nombre=nombre.strip(),
            especialidad=especialidad.strip(),
        )
        self._repo.guardar(veterinario)
        return veterinario

    def buscar(self, id_veterinario: str) -> Veterinario:
        veterinario = self._repo.buscar(id_veterinario)
        if veterinario is None:
            raise ValueError(
                f"No se encontró un veterinario con ID '{id_veterinario}'."
            )
        return veterinario

    def listar(self) -> List[Veterinario]:
        return self._repo.listar()


class MascotaService:
    def __init__(
        self, repo: MascotaRepository, cliente_repo: ClienteRepository
    ):
        self._repo = repo
        self._cliente_repo = cliente_repo

    def registrar(
        self,
        nombre: str,
        especie: str,
        raza: str,
        edad: int,
        peso: float,
        id_cliente: str,
    ) -> Mascota:
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la mascota no puede estar vacío.")
        if not self._cliente_repo.existe(id_cliente):
            raise ValueError(
                f"No existe un cliente con ID '{id_cliente}'. "
                "Registre al cliente primero."
            )
        if edad < 0:
            raise ValueError("La edad no puede ser negativa.")
        if peso <= 0:
            raise ValueError("El peso debe ser mayor a cero.")
        mascota = Mascota(
            id_mascota=0,
            nombre=nombre.strip(),
            especie=especie.strip(),
            raza=raza.strip(),
            edad=edad,
            peso=peso,
            id_cliente=id_cliente,
        )
        return self._repo.guardar(mascota)

    def buscar(self, id_mascota: int) -> Mascota:
        mascota = self._repo.buscar(id_mascota)
        if mascota is None:
            raise ValueError(
                f"No se encontró una mascota con ID '{id_mascota}'."
            )
        return mascota

    def listar(self) -> List[Mascota]:
        return self._repo.listar()


class CitaService:
    def __init__(
        self,
        repo: CitaRepository,
        mascota_repo: MascotaRepository,
        veterinario_repo: VeterinarioRepository,
    ):
        self._repo = repo
        self._mascota_repo = mascota_repo
        self._veterinario_repo = veterinario_repo

    def agendar(
        self,
        fecha: str,
        hora: str,
        id_mascota: int,
        id_veterinario: str,
        motivo: str,
    ) -> Cita:
        if not fecha or not fecha.strip():
            raise ValueError("La fecha no puede estar vacía.")
        if not hora or not hora.strip():
            raise ValueError("La hora no puede estar vacía.")
        if not self._mascota_repo.existe(id_mascota):
            raise ValueError(
                f"No existe una mascota con ID '{id_mascota}'."
            )
        if not self._veterinario_repo.existe(id_veterinario):
            raise ValueError(
                f"No existe un veterinario con ID '{id_veterinario}'."
            )
        if not motivo or not motivo.strip():
            raise ValueError("El motivo de la cita no puede estar vacío.")
        conflicto = self._repo.buscar_por_veterinario_fecha_hora(
            id_veterinario, fecha.strip(), hora.strip()
        )
        if conflicto is not None:
            raise ValueError(
                f"El veterinario '{id_veterinario}' ya tiene una cita "
                f"programada el {fecha} a las {hora}."
            )
        cita = Cita(
            id_cita=0,
            fecha=fecha.strip(),
            hora=hora.strip(),
            id_mascota=id_mascota,
            id_veterinario=id_veterinario,
            motivo=motivo.strip(),
        )
        return self._repo.guardar(cita)

    def buscar(self, id_cita: int) -> Cita:
        cita = self._repo.buscar(id_cita)
        if cita is None:
            raise ValueError(
                f"No se encontró una cita con ID '{id_cita}'."
            )
        return cita

    def listar(self) -> List[Cita]:
        return self._repo.listar()


class AtencionService:
    def __init__(
        self, cita_repo: CitaRepository, registro_repo: RegistroClinicoRepository
    ):
        self._cita_repo = cita_repo
        self._registro_repo = registro_repo

    def registrar_atencion(
        self,
        id_cita: int,
        diagnostico: str,
        tratamiento: str,
        observaciones: str,
    ) -> RegistroClinico:
        cita = self._cita_repo.buscar(id_cita)
        if cita is None:
            raise ValueError(
                f"No se encontró una cita con ID '{id_cita}'."
            )
        if cita.estado != "Programada":
            raise ValueError(
                f"La cita '{id_cita}' no está en estado 'Programada' "
                f"(estado actual: '{cita.estado}')."
            )
        if not diagnostico or not diagnostico.strip():
            raise ValueError("El diagnóstico no puede estar vacío.")
        if not tratamiento or not tratamiento.strip():
            raise ValueError("El tratamiento no puede estar vacío.")

        cita.estado = "Completada"

        registro = RegistroClinico(
            id_registro=0,
            id_cita=id_cita,
            id_mascota=cita.id_mascota,
            fecha=cita.fecha,
            diagnostico=diagnostico.strip(),
            tratamiento=tratamiento.strip(),
            observaciones=observaciones.strip() if observaciones else "",
        )
        return self._registro_repo.guardar(registro)

    def obtener_historial(self, id_mascota: int) -> List[RegistroClinico]:
        return self._registro_repo.listar_por_mascota(id_mascota)
