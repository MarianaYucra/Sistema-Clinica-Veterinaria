import pytest


# ────────────────────────────── registrar ───────────────────────────────


def test_registrar_veterinario_exitoso(veterinario_entorno):
    repo, svc = veterinario_entorno
    vet = svc.registrar("VET001", "Dr. Pérez", "Cardiología")

    assert vet.id_veterinario == "VET001"
    assert vet.nombre == "Dr. Pérez"
    assert vet.especialidad == "Cardiología"
    assert repo.existe("VET001") is True


@pytest.mark.parametrize(
    "id_vet, nombre, motivo",
    [
        ("", "Dr. Pérez", "ID vacío"),
        ("   ", "Dr. Pérez", "ID con espacios"),
        ("VET001", "", "nombre vacío"),
        ("VET001", "   ", "nombre con espacios"),
    ],
)
def test_registrar_veterinario_cadenas_invalidas_pe(
    veterinario_entorno, id_vet, nombre, motivo
):
    _, svc = veterinario_entorno
    with pytest.raises(ValueError):
        svc.registrar(id_vet, nombre, "Cardiología")


def test_registrar_veterinario_id_none(veterinario_entorno):
    _, svc = veterinario_entorno
    with pytest.raises(ValueError):
        svc.registrar(None, "Dr. Pérez", "Cardiología")


def test_registrar_veterinario_nombre_none(veterinario_entorno):
    _, svc = veterinario_entorno
    with pytest.raises(ValueError):
        svc.registrar("VET001", None, "Cardiología")


def test_registrar_veterinario_id_int(veterinario_entorno):
    _, svc = veterinario_entorno
    with pytest.raises(AttributeError):
        svc.registrar(123, "Dr. Pérez", "Cardiología")


def test_registrar_veterinario_nombre_int(veterinario_entorno):
    _, svc = veterinario_entorno
    with pytest.raises(AttributeError):
        svc.registrar("VET001", 123, "Cardiología")


def test_registrar_veterinario_especialidad_none(veterinario_entorno):
    _, svc = veterinario_entorno
    with pytest.raises(AttributeError):
        svc.registrar("VET001", "Dr. Pérez", None)


def test_registrar_veterinario_especialidad_int(veterinario_entorno):
    _, svc = veterinario_entorno
    with pytest.raises(AttributeError):
        svc.registrar("VET001", "Dr. Pérez", 456)


def test_registrar_veterinario_duplicado_bva(veterinario_entorno):
    _, svc = veterinario_entorno
    svc.registrar("VET001", "Dr. Pérez", "Cardiología")
    with pytest.raises(ValueError, match="Ya existe un veterinario"):
        svc.registrar("VET001", "Dr. Gómez", "Dermatología")


# ──────────────────────────────── buscar ────────────────────────────────


def test_buscar_veterinario_existente(veterinario_entorno):
    _, svc = veterinario_entorno
    svc.registrar("VET001", "Dr. Pérez", "Cardiología")

    vet = svc.buscar("VET001")
    assert vet.nombre == "Dr. Pérez"


def test_buscar_veterinario_no_existente(veterinario_entorno):
    _, svc = veterinario_entorno
    with pytest.raises(ValueError, match="No se encontró un veterinario"):
        svc.buscar("VET999")


def test_buscar_veterinario_none(veterinario_entorno):
    _, svc = veterinario_entorno
    with pytest.raises(ValueError):
        svc.buscar(None)


def test_buscar_veterinario_vacio(veterinario_entorno):
    _, svc = veterinario_entorno
    with pytest.raises(ValueError):
        svc.buscar("")


# ──────────────────────────────── listar ────────────────────────────────


def test_listar_veterinarios_sin_datos(veterinario_entorno):
    _, svc = veterinario_entorno
    assert svc.listar() == []


def test_listar_veterinarios_con_datos(veterinario_entorno):
    _, svc = veterinario_entorno
    svc.registrar("VET001", "Dr. Pérez", "Cardiología")
    svc.registrar("VET002", "Dra. Gómez", "Dermatología")

    resultado = svc.listar()
    assert len(resultado) == 2
    assert resultado[0].id_veterinario == "VET001"
    assert resultado[1].id_veterinario == "VET002"
