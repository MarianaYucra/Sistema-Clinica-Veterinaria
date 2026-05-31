# pyrefly: ignore [missing-import]
import pytest

from app.repository import (
    CitaRepository,
    ClienteRepository,
    MascotaRepository,
    RegistroClinicoRepository,
    VeterinarioRepository,
)
from app.services import (
    AtencionService,
    CitaService,
    ClienteService,
    MascotaService,
    VeterinarioService,
)


@pytest.fixture
def cliente_repo():
    return ClienteRepository()


@pytest.fixture
def veterinario_repo():
    return VeterinarioRepository()


@pytest.fixture
def mascota_repo():
    return MascotaRepository()


@pytest.fixture
def cita_repo():
    return CitaRepository()


@pytest.fixture
def registro_repo():
    return RegistroClinicoRepository()


@pytest.fixture
def cliente_svc(cliente_repo):
    return ClienteService(cliente_repo)


@pytest.fixture
def veterinario_svc(veterinario_repo):
    return VeterinarioService(veterinario_repo)


@pytest.fixture
def mascota_svc(mascota_repo, cliente_repo):
    return MascotaService(mascota_repo, cliente_repo)


@pytest.fixture
def cita_svc(cita_repo, mascota_repo, veterinario_repo):
    return CitaService(cita_repo, mascota_repo, veterinario_repo)


@pytest.fixture
def atencion_svc(cita_repo, registro_repo):
    return AtencionService(cita_repo, registro_repo)


# ============================================================
# RPT-LC: Listar Clientes
# ============================================================


class TestListarClientes:
    def test_rpt_lc_01_listar_sin_registros(self, cliente_svc):
        resultado = cliente_svc.listar()

        assert resultado == []

    def test_rpt_lc_02_listar_con_un_registro(self, cliente_svc):
        cliente_svc.registrar("12345678", "Ana Lopez", "5550001", "ana@mail.com")

        resultado = cliente_svc.listar()

        assert len(resultado) == 1
        assert resultado[0].id_cliente == "12345678"

    def test_rpt_lc_03_listar_con_multiples_registros(self, cliente_svc):
        cliente_svc.registrar("12345678", "Ana Lopez", "5550001", "ana@mail.com")
        cliente_svc.registrar("87654321", "Carlos Ruiz", "5550002", "carlos@mail.com")
        cliente_svc.registrar("11223344", "Maria Torres", "5550003", "maria@mail.com")

        resultado = cliente_svc.listar()

        assert len(resultado) == 3

    def test_rpt_lc_04_verificar_integridad_datos(self, cliente_svc):
        cliente_svc.registrar("12345678", "Ana Lopez", "5550001", "ana@mail.com")

        resultado = cliente_svc.listar()

        cliente = resultado[0]
        assert cliente.nombre == "Ana Lopez"
        assert cliente.telefono == "5550001"
        assert cliente.email == "ana@mail.com"


# ============================================================
# RPT-LV: Listar Veterinarios
# ============================================================


class TestListarVeterinarios:
    def test_rpt_lv_01_listar_sin_registros(self, veterinario_svc):
        resultado = veterinario_svc.listar()

        assert resultado == []

    def test_rpt_lv_02_listar_con_un_registro(self, veterinario_svc):
        veterinario_svc.registrar("V001", "Dra. García", "Cirugía")

        resultado = veterinario_svc.listar()

        assert len(resultado) == 1
        assert resultado[0].id_veterinario == "V001"

    def test_rpt_lv_03_listar_con_multiples_registros(self, veterinario_svc):
        veterinario_svc.registrar("V001", "Dra. García", "Cirugía")
        veterinario_svc.registrar("V002", "Dr. Mendoza", "Dermatología")
        veterinario_svc.registrar("V003", "Dra. Ríos", "Cardiología")

        resultado = veterinario_svc.listar()

        assert len(resultado) == 3

    def test_rpt_lv_04_verificar_integridad_datos(self, veterinario_svc):
        veterinario_svc.registrar("V001", "Dra. García", "Cirugía")

        resultado = veterinario_svc.listar()

        vet = resultado[0]
        assert vet.nombre == "Dra. García"
        assert vet.especialidad == "Cirugía"


# ============================================================
# RPT-LM: Listar Mascotas
# ============================================================


class TestListarMascotas:
    def test_rpt_lm_01_listar_sin_registros(self, mascota_svc):
        resultado = mascota_svc.listar()

        assert resultado == []

    def test_rpt_lm_02_listar_con_un_registro(self, cliente_svc, mascota_svc):
        cliente_svc.registrar("12345678", "Ana Lopez", "5550001", "ana@mail.com")
        mascota_svc.registrar("Fido", "Perro", "Labrador", 3, 25.0, "12345678")

        resultado = mascota_svc.listar()

        assert len(resultado) == 1

    def test_rpt_lm_03_listar_con_multiples_registros(
        self, cliente_svc, mascota_svc
    ):
        cliente_svc.registrar("12345678", "Ana Lopez", "5550001", "ana@mail.com")
        mascota_svc.registrar("Fido", "Perro", "Labrador", 3, 25.0, "12345678")
        mascota_svc.registrar("Misu", "Gato", "Siames", 2, 4.5, "12345678")
        mascota_svc.registrar("Rocky", "Perro", "Bulldog", 5, 18.0, "12345678")

        resultado = mascota_svc.listar()

        assert len(resultado) == 3

    def test_rpt_lm_04_verificar_vinculacion_cliente(
        self, cliente_svc, mascota_svc
    ):
        cliente_svc.registrar("12345678", "Ana Lopez", "5550001", "ana@mail.com")
        mascota_svc.registrar("Fido", "Perro", "Labrador", 3, 25.0, "12345678")

        resultado = mascota_svc.listar()

        assert resultado[0].id_cliente == "12345678"


# ============================================================
# RPT-LCI: Listar Citas
# ============================================================


class TestListarCitas:
    @pytest.fixture(autouse=True)
    def _setup_entidades(self, cliente_svc, veterinario_svc, mascota_svc):
        cliente_svc.registrar("12345678", "Ana Lopez", "5550001", "ana@mail.com")
        veterinario_svc.registrar("V001", "Dra. García", "Cirugía")
        mascota_svc.registrar("Fido", "Perro", "Labrador", 3, 25.0, "12345678")

    def test_rpt_lci_01_listar_sin_registros(self, cita_svc):
        resultado = cita_svc.listar()

        assert resultado == []

    def test_rpt_lci_02_listar_con_un_registro(self, cita_svc):
        cita_svc.agendar("2026-06-01", "10:00", 1, "V001", "Vacunación")

        resultado = cita_svc.listar()

        assert len(resultado) == 1
        assert resultado[0].estado == "Programada"

    def test_rpt_lci_03_listar_con_multiples_registros(
        self, cita_svc, veterinario_svc
    ):
        veterinario_svc.registrar("V002", "Dr. Mendoza", "Dermatología")
        veterinario_svc.registrar("V003", "Dra. Ríos", "Cardiología")
        cita_svc.agendar("2026-06-01", "10:00", 1, "V001", "Vacunación")
        cita_svc.agendar("2026-06-01", "11:00", 1, "V002", "Control")
        cita_svc.agendar("2026-06-02", "09:00", 1, "V003", "Revisión")

        resultado = cita_svc.listar()

        assert len(resultado) == 3

    def test_rpt_lci_04_listar_refleja_cambio_estado(
        self, cita_svc, atencion_svc
    ):
        cita_svc.agendar("2026-06-01", "10:00", 1, "V001", "Vacunación")
        atencion_svc.registrar_atencion(1, "Sano", "Vacuna antirrábica", "")

        resultado = cita_svc.listar()

        assert resultado[0].estado == "Completada"


# ============================================================
# RPT-HC: Historial Clínico
# ============================================================


class TestHistorialClinico:
    @pytest.fixture(autouse=True)
    def _setup_entidades(
        self, cliente_svc, veterinario_svc, mascota_svc
    ):
        cliente_svc.registrar("12345678", "Ana Lopez", "5550001", "ana@mail.com")
        veterinario_svc.registrar("V001", "Dra. García", "Cirugía")

    def test_rpt_hc_01_historial_sin_atenciones(
        self, mascota_svc, atencion_svc
    ):
        mascota_svc.registrar("Fido", "Perro", "Labrador", 3, 25.0, "12345678")

        resultado = atencion_svc.obtener_historial(1)

        assert resultado == []

    def test_rpt_hc_02_historial_con_una_atencion(
        self, mascota_svc, cita_svc, atencion_svc
    ):
        mascota_svc.registrar("Fido", "Perro", "Labrador", 3, 25.0, "12345678")
        cita_svc.agendar("2026-06-01", "10:00", 1, "V001", "Vacunación")
        atencion_svc.registrar_atencion(1, "Sano", "Vacuna antirrábica", "")

        resultado = atencion_svc.obtener_historial(1)

        assert len(resultado) == 1
        assert resultado[0].fecha == "2026-06-01"

    def test_rpt_hc_03_historial_multiples_atenciones_ordenadas(
        self, mascota_svc, cita_svc, atencion_svc, veterinario_svc
    ):
        mascota_svc.registrar("Fido", "Perro", "Labrador", 3, 25.0, "12345678")
        veterinario_svc.registrar("V002", "Dr. Mendoza", "Dermatología")
        veterinario_svc.registrar("V003", "Dra. Ríos", "Cardiología")

        cita_svc.agendar("2026-06-01", "10:00", 1, "V001", "Vacunación")
        cita_svc.agendar("2026-01-15", "09:00", 1, "V002", "Control")
        cita_svc.agendar("2026-03-10", "14:00", 1, "V003", "Revisión")

        atencion_svc.registrar_atencion(1, "Sano", "Vacuna", "")
        atencion_svc.registrar_atencion(2, "Sobrepeso", "Dieta", "")
        atencion_svc.registrar_atencion(3, "Alergia", "Antihistamínico", "")

        resultado = atencion_svc.obtener_historial(1)

        assert len(resultado) == 3
        assert resultado[0].fecha == "2026-01-15"
        assert resultado[1].fecha == "2026-03-10"
        assert resultado[2].fecha == "2026-06-01"

    def test_rpt_hc_04_historial_id_inexistente(self, atencion_svc):
        resultado = atencion_svc.obtener_historial(999)

        assert resultado == []

    def test_rpt_hc_05_historial_id_cero(self, atencion_svc):
        resultado = atencion_svc.obtener_historial(0)

        assert resultado == []

    def test_rpt_hc_06_historial_id_negativo(self, atencion_svc):
        resultado = atencion_svc.obtener_historial(-1)

        assert resultado == []

    def test_rpt_hc_07_historial_primer_id_autogenerado(
        self, mascota_svc, cita_svc, atencion_svc
    ):
        mascota_svc.registrar("Fido", "Perro", "Labrador", 3, 25.0, "12345678")
        cita_svc.agendar("2026-06-01", "10:00", 1, "V001", "Vacunación")
        atencion_svc.registrar_atencion(1, "Sano", "Vacuna", "")

        resultado = atencion_svc.obtener_historial(1)

        assert len(resultado) == 1

    def test_rpt_hc_08_historial_segundo_id_autogenerado(
        self, mascota_svc, cita_svc, atencion_svc
    ):
        mascota_svc.registrar("Fido", "Perro", "Labrador", 3, 25.0, "12345678")
        mascota_svc.registrar("Misu", "Gato", "Siames", 2, 4.5, "12345678")
        cita_svc.agendar("2026-06-01", "10:00", 2, "V001", "Control")
        atencion_svc.registrar_atencion(1, "Sano", "Desparasitación", "")

        resultado = atencion_svc.obtener_historial(2)

        assert len(resultado) == 1

    def test_rpt_hc_09_historial_aislamiento_entre_mascotas(
        self, mascota_svc, cita_svc, atencion_svc, veterinario_svc
    ):
        veterinario_svc.registrar("V002", "Dr. Mendoza", "Dermatología")
        mascota_svc.registrar("Fido", "Perro", "Labrador", 3, 25.0, "12345678")
        mascota_svc.registrar("Misu", "Gato", "Siames", 2, 4.5, "12345678")

        cita_svc.agendar("2026-06-01", "10:00", 1, "V001", "Vacunación")
        cita_svc.agendar("2026-06-01", "11:00", 1, "V002", "Control")
        cita_svc.agendar("2026-06-02", "09:00", 2, "V001", "Revisión")

        atencion_svc.registrar_atencion(1, "Sano", "Vacuna", "")
        atencion_svc.registrar_atencion(2, "Leve", "Observación", "")
        atencion_svc.registrar_atencion(3, "Parásitos", "Desparasitante", "")

        resultado_fido = atencion_svc.obtener_historial(1)
        resultado_misu = atencion_svc.obtener_historial(2)

        assert len(resultado_fido) == 2
        assert len(resultado_misu) == 1

    def test_rpt_hc_10_verificar_contenido_registro(
        self, mascota_svc, cita_svc, atencion_svc
    ):
        mascota_svc.registrar("Fido", "Perro", "Labrador", 5, 25.0, "12345678")
        cita_svc.agendar("2026-06-01", "10:00", 1, "V001", "Revisión piel")
        atencion_svc.registrar_atencion(
            1, "Dermatitis", "Crema tópica", "Revisión en 15 días"
        )

        resultado = atencion_svc.obtener_historial(1)

        registro = resultado[0]
        assert registro.diagnostico == "Dermatitis"
        assert registro.tratamiento == "Crema tópica"
        assert registro.observaciones == "Revisión en 15 días"
        assert registro.id_mascota == 1
        assert registro.id_cita == 1
