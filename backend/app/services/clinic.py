from app.domain.models import Cita, Cliente, Mascota, RegistroClinico, Veterinario
from app.services import validation as v


class ClienteService:
    def __init__(self, repository):
        self.repository = repository

    def registrar(self, data: dict) -> Cliente:
        cliente = Cliente(
            id_cliente=v.dni(data.get("id_cliente")),
            nombre=v.letters_spaces(v.required_text(data.get("nombre"), "El nombre", 120), "El nombre"),
            telefono=v.phone(data.get("telefono")),
            email=v.email(data.get("email")),
        )
        if self.repository.existe(cliente.id_cliente):
            raise ValueError("Ya existe un cliente con ese DNI.")
        if self.repository.buscar_por_email(cliente.email):
            raise ValueError("Ya existe un cliente con ese correo.")
        return self.repository.guardar(cliente)

    def buscar(self, criterio: str) -> Cliente:
        criterio = v.required_text(criterio, "El criterio de busqueda", 160)
        cliente = self.repository.buscar(criterio)
        if cliente is None and v.EMAIL_RE.fullmatch(criterio):
            cliente = self.repository.buscar_por_email(criterio)
        if cliente is None:
            cliente = self.repository.buscar_por_nombre(criterio)
        if cliente is None:
            raise ValueError("No se encontro el cliente.")
        return cliente

    def listar(self) -> list[Cliente]:
        return self.repository.listar()


class VeterinarioService:
    def __init__(self, repository):
        self.repository = repository

    def registrar(self, data: dict) -> Veterinario:
        nombre = v.required_text(data.get("nombre"), "El nombre", 120)
        if not all(char.isalpha() or char.isspace() or char == "." for char in nombre):
            raise ValueError("El nombre solo debe contener letras, espacios y puntos.")
        veterinario = Veterinario(
            id_veterinario=v.veterinarian_id(data.get("id_veterinario")),
            nombre=nombre,
            especialidad=v.letters_spaces(
                v.required_text(data.get("especialidad"), "La especialidad", 120),
                "La especialidad",
                3,
            ),
        )
        if self.repository.existe(veterinario.id_veterinario):
            raise ValueError("Ya existe un veterinario con ese ID.")
        return self.repository.guardar(veterinario)

    def listar(self) -> list[Veterinario]:
        return self.repository.listar()


class MascotaService:
    def __init__(self, repository, cliente_repository):
        self.repository = repository
        self.cliente_repository = cliente_repository

    def registrar(self, data: dict) -> Mascota:
        nombre = v.required_text(data.get("nombre"), "El nombre de la mascota", 80)
        if not v.PET_NAME_RE.fullmatch(nombre) or len(nombre) < 2:
            raise ValueError("El nombre de la mascota tiene caracteres invalidos.")
        id_cliente = v.dni(data.get("id_cliente"))
        if not self.cliente_repository.existe(id_cliente):
            raise ValueError("El cliente indicado no existe.")
        mascota = Mascota(
            id_mascota=0,
            nombre=nombre,
            especie=v.letters_spaces(v.required_text(data.get("especie"), "La especie", 80), "La especie"),
            raza=v.letters_spaces(v.required_text(data.get("raza"), "La raza", 80), "La raza"),
            edad=v.age(data.get("edad")),
            peso=v.weight(data.get("peso")),
            id_cliente=id_cliente,
        )
        return self.repository.guardar(mascota)

    def listar(self) -> list[Mascota]:
        return self.repository.listar()

    def buscar(self, id_mascota) -> Mascota:
        mascota = self.repository.buscar(v.positive_int(id_mascota, "El ID de la mascota"))
        if mascota is None:
            raise ValueError("No se encontro la mascota.")
        return mascota


class CitaService:
    def __init__(self, repository, mascota_repository, veterinario_repository):
        self.repository = repository
        self.mascota_repository = mascota_repository
        self.veterinario_repository = veterinario_repository

    def agendar(self, data: dict) -> Cita:
        id_mascota = v.positive_int(data.get("id_mascota"), "El ID de la mascota")
        id_veterinario = v.veterinarian_id(data.get("id_veterinario"))
        fecha = v.appointment_date(data.get("fecha"))
        hora = v.appointment_time(data.get("hora"))
        if not self.mascota_repository.existe(id_mascota):
            raise ValueError("La mascota indicada no existe.")
        if not self.veterinario_repository.existe(id_veterinario):
            raise ValueError("El veterinario indicado no existe.")
        if self.repository.buscar_por_veterinario_fecha_hora(id_veterinario, fecha, hora):
            raise ValueError("El veterinario ya tiene una cita programada en ese horario.")
        cita = Cita(
            id_cita=0,
            fecha=fecha,
            hora=hora,
            id_mascota=id_mascota,
            id_veterinario=id_veterinario,
            motivo=v.required_text(data.get("motivo"), "El motivo", 240),
        )
        return self.repository.guardar(cita)

    def listar(self) -> list[Cita]:
        return self.repository.listar()

    def buscar(self, id_cita) -> Cita:
        cita = self.repository.buscar(v.positive_int(id_cita, "El ID de la cita"))
        if cita is None:
            raise ValueError("No se encontro la cita.")
        return cita


class AtencionService:
    def __init__(self, cita_repository, registro_repository):
        self.cita_repository = cita_repository
        self.registro_repository = registro_repository

    def registrar(self, id_cita, data: dict) -> RegistroClinico:
        cita = self.cita_repository.buscar(v.positive_int(id_cita, "El ID de la cita"))
        if cita is None:
            raise ValueError("No se encontro la cita.")
        if cita.estado != "Programada":
            raise ValueError("La cita ya fue completada.")
        registro = RegistroClinico(
            id_registro=0,
            id_cita=cita.id_cita,
            id_mascota=cita.id_mascota,
            fecha=cita.fecha,
            diagnostico=v.required_text(data.get("diagnostico"), "El diagnostico", 500),
            tratamiento=v.required_text(data.get("tratamiento"), "El tratamiento", 500),
            observaciones=str(data.get("observaciones") or "").strip()[:500],
        )
        self.cita_repository.actualizar_estado(cita.id_cita, "Completada")
        return self.registro_repository.guardar(registro)

    def historial(self, id_mascota) -> list[RegistroClinico]:
        return self.registro_repository.listar_por_mascota(
            v.positive_int(id_mascota, "El ID de la mascota")
        )
