import pytest


def test_registrar_veterinario_exitoso(veterinario_entorno):
    repo, svc = veterinario_entorno
    vet = svc.registrar("VET001", "Dr. Perez", "Cardiologia")

    assert vet.id_veterinario == "VET001"
    assert vet.nombre == "Dr. Perez"
    assert vet.especialidad == "Cardiologia"
    assert repo.existe("VET001") is True


@pytest.mark.parametrize(
    "id_vet, nombre, especialidad",
    [
        ("", "Dr. Perez", "Cardiologia"),
        ("   ", "Dr. Perez", "Cardiologia"),
        ("123", "Dr. Perez", "Cardiologia"),
        ("VET", "Dr. Perez", "Cardiologia"),
        ("VET01", "Dr. Perez", "Cardiologia"),
        ("VET-001", "Dr. Perez", "Cardiologia"),
        ("VET001", "", "Cardiologia"),
        ("VET001", "   ", "Cardiologia"),
        ("VET001", "Dr.", "Cardiologia"),
        ("VET001", "Dr. Perez 123", "Cardiologia"),
        ("VET001", "Dr. @Perez", "Cardiologia"),
        ("VET001", "Dr. Perez", ""),
        ("VET001", "Dr. Perez", "   "),
        ("VET001", "Dr. Perez", "Ojo"),
        ("VET001", "Dr. Perez", "Cardiologia 123"),
        ("VET001", "Dr. Perez", "Cardiologia!"),
    ],
)
def test_registrar_veterinario_cadenas_invalidas_pe(
    veterinario_entorno, id_vet, nombre, especialidad
):
    _, svc = veterinario_entorno
    with pytest.raises(ValueError):
        svc.registrar(id_vet, nombre, especialidad)


@pytest.mark.parametrize(
    "id_vet, nombre, especialidad",
    [
        (None, "Dr. Perez", "Cardiologia"),
        ("VET001", None, "Cardiologia"),
        ("VET001", "Dr. Perez", None),
        (123, "Dr. Perez", "Cardiologia"),
        ("VET001", 123, "Cardiologia"),
        ("VET001", "Dr. Perez", 456),
    ],
)
def test_registrar_veterinario_tipos_invalidos(
    veterinario_entorno, id_vet, nombre, especialidad
):
    _, svc = veterinario_entorno
    with pytest.raises(ValueError):
        svc.registrar(id_vet, nombre, especialidad)


def test_registrar_veterinario_normaliza_id(veterinario_entorno):
    _, svc = veterinario_entorno
    vet = svc.registrar("vet001", "Dra. Gomez", "Dermatologia")

    assert vet.id_veterinario == "VET001"


def test_registrar_veterinario_duplicado_bva(veterinario_entorno):
    _, svc = veterinario_entorno
    svc.registrar("VET001", "Dr. Perez", "Cardiologia")

    with pytest.raises(ValueError, match="Ya existe un veterinario"):
        svc.registrar("vet001", "Dr. Gomez", "Dermatologia")


def test_buscar_veterinario_existente(veterinario_entorno):
    _, svc = veterinario_entorno
    svc.registrar("VET001", "Dr. Perez", "Cardiologia")

    assert svc.buscar("VET001").nombre == "Dr. Perez"
    assert svc.buscar("vet001").nombre == "Dr. Perez"
    assert svc.buscar("Dr. Perez").id_veterinario == "VET001"


def test_buscar_veterinario_por_especialidad_devuelve_coincidencias(
    veterinario_entorno,
):
    _, svc = veterinario_entorno
    svc.registrar("VET001", "Dr. Perez", "Cardiologia")
    svc.registrar("VET002", "Dra. Gomez", "Cardiologia")
    svc.registrar("VET003", "Dr. Ruiz", "Dermatologia")

    resultado = svc.buscar("cardio")

    assert [vet.id_veterinario for vet in resultado] == ["VET001", "VET002"]


def test_buscar_veterinario_no_existente(veterinario_entorno):
    _, svc = veterinario_entorno
    with pytest.raises(ValueError, match="No se encontro un veterinario"):
        svc.buscar("VET999")


@pytest.mark.parametrize("criterio", [None, "", "   "])
def test_buscar_veterinario_criterio_invalido(veterinario_entorno, criterio):
    _, svc = veterinario_entorno
    with pytest.raises(ValueError):
        svc.buscar(criterio)


def test_listar_veterinarios_sin_datos(veterinario_entorno):
    _, svc = veterinario_entorno
    assert svc.listar() == []


def test_listar_veterinarios_con_datos(veterinario_entorno):
    _, svc = veterinario_entorno
    svc.registrar("VET001", "Dr. Perez", "Cardiologia")
    svc.registrar("VET002", "Dra. Gomez", "Dermatologia")

    resultado = svc.listar()
    assert len(resultado) == 2
    assert resultado[0].id_veterinario == "VET001"
    assert resultado[1].id_veterinario == "VET002"
