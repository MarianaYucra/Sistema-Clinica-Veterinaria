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
def cliente_entorno():
    repo = ClienteRepository()
    svc = ClienteService(repo)
    return repo, svc


@pytest.fixture
def veterinario_entorno():
    repo = VeterinarioRepository()
    svc = VeterinarioService(repo)
    return repo, svc


@pytest.fixture
def mascota_entorno(cliente_entorno):
    cliente_repo, _ = cliente_entorno
    repo = MascotaRepository()
    svc = MascotaService(repo, cliente_repo)
    return repo, cliente_repo, svc


@pytest.fixture
def cita_entorno(mascota_entorno, veterinario_entorno):
    mascota_repo, cliente_repo, _ = mascota_entorno
    vet_repo, _ = veterinario_entorno
    repo = CitaRepository()
    svc = CitaService(repo, mascota_repo, vet_repo)
    return repo, mascota_repo, vet_repo, svc


@pytest.fixture
def atencion_entorno(cita_entorno):
    cita_repo, _, _, _ = cita_entorno
    reg_repo = RegistroClinicoRepository()
    svc = AtencionService(cita_repo, reg_repo)
    return cita_repo, reg_repo, svc