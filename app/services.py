import re
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

EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)
CODIGO_VETERINARIO_REGEX = re.compile(r"^[A-Za-z]{1,5}[0-9]{3,6}$")


def _texto_obligatorio(valor, campo: str) -> str:
    if valor is None:
        raise ValueError(f"{campo} no puede estar vacio.")
    texto = str(valor).strip()
    if not texto:
        raise ValueError(f"{campo} no puede estar vacio.")
    return texto


def _validar_solo_letras_espacios(valor: str, campo: str) -> None:
    if not all(caracter.isalpha() or caracter.isspace() for caracter in valor):
        raise ValueError(f"{campo} solo debe contener letras y espacios.")


def _validar_nombre_veterinario(valor: str) -> None:
    caracteres_validos = (
        caracter.isalpha() or caracter.isspace() or caracter == "."
        for caracter in valor
    )
    if not all(caracteres_validos):
        raise ValueError(
            "El nombre del veterinario solo debe contener letras, espacios y puntos."
        )
    if not any(caracter.isalpha() for caracter in valor):
        raise ValueError("El nombre del veterinario debe contener letras.")


class ClienteService:
    def __init__(self, repo: ClienteRepository):
        self._repo = repo

    def registrar(
        self, id_cliente: str, nombre: str, telefono: str, email: str
    ) -> Cliente:
        id_cliente = _texto_obligatorio(id_cliente, "El DNI del cliente")
        nombre = _texto_obligatorio(nombre, "El nombre del cliente")
        telefono = _texto_obligatorio(telefono, "El telefono del cliente")
        email = _texto_obligatorio(email, "El correo del cliente")

        if not id_cliente.isdigit():
            raise ValueError("El DNI del cliente solo debe contener numeros.")
        if not 8 <= len(id_cliente) <= 12:
            raise ValueError("El DNI del cliente debe tener entre 8 y 12 digitos.")
        if self._repo.existe(id_cliente):
            raise ValueError(
                f"Ya existe un cliente con ID '{id_cliente}'."
            )
        _validar_solo_letras_espacios(nombre, "El nombre del cliente")

        if not telefono.isdigit():
            raise ValueError("El telefono del cliente solo debe contener numeros.")
        if not 7 <= len(telefono) <= 15:
            raise ValueError(
                "El telefono del cliente debe tener entre 7 y 15 digitos."
            )

        if not EMAIL_REGEX.fullmatch(email):
            raise ValueError("El correo del cliente no tiene un formato valido.")
        if any(
            cliente.email.lower() == email.lower()
            for cliente in self._repo.listar()
        ):
            raise ValueError(
                f"Ya existe un cliente con correo '{email}'."
            )

        cliente = Cliente(
            id_cliente=id_cliente,
            nombre=nombre,
            telefono=telefono,
            email=email,
        )
        self._repo.guardar(cliente)
        return cliente

    def buscar(self, criterio: str) -> Cliente:
        criterio = _texto_obligatorio(criterio, "El dato de busqueda del cliente")
        cliente = self._repo.buscar(criterio)
        if cliente is None and EMAIL_REGEX.fullmatch(criterio):
            cliente = self._repo.buscar_por_email(criterio)
        if cliente is None:
            cliente = self._repo.buscar_por_nombre(criterio)
        if cliente is None:
            raise ValueError(
                f"No se encontro un cliente con el dato '{criterio}'."
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
        id_veterinario = _texto_obligatorio(
            id_veterinario, "El ID del veterinario"
        ).upper()
        nombre = _texto_obligatorio(nombre, "El nombre del veterinario")
        especialidad = _texto_obligatorio(
            especialidad, "La especialidad del veterinario"
        )

        if not CODIGO_VETERINARIO_REGEX.fullmatch(id_veterinario):
            raise ValueError(
                "El ID del veterinario debe tener letras seguidas de 3 a 6 numeros."
            )
        if self._repo.existe(id_veterinario):
            raise ValueError(
                f"Ya existe un veterinario con ID '{id_veterinario}'."
            )
        _validar_nombre_veterinario(nombre)
        _validar_solo_letras_espacios(
            especialidad, "La especialidad del veterinario"
        )

        veterinario = Veterinario(
            id_veterinario=id_veterinario,
            nombre=nombre,
            especialidad=especialidad,
        )
        self._repo.guardar(veterinario)
        return veterinario

    def buscar(self, criterio: str) -> Veterinario:
        criterio = _texto_obligatorio(
            criterio, "El dato de busqueda del veterinario"
        )
        veterinario = self._repo.buscar(criterio.upper())
        if veterinario is None:
            veterinario = self._repo.buscar_por_nombre(criterio)
        if veterinario is None:
            veterinario = self._repo.buscar_por_especialidad(criterio)
        if veterinario is None:
            raise ValueError(
                f"No se encontro un veterinario con el dato '{criterio}'."
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
