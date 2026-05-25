import pytest


def _registrar_cliente_valido(cliente_repo, svc_cliente):
    svc_cliente.registrar("CLI001", "Ana López", "987654321", "ana@mail.com")


# ────────────────────────────── registrar ───────────────────────────────


def test_registrar_mascota_exitoso(cliente_entorno, mascota_entorno):
    cliente_repo, svc_cliente = cliente_entorno
    _registrar_cliente_valido(cliente_repo, svc_cliente)

    _, _, svc = mascota_entorno
    m = svc.registrar("Firulais", "Canino", "Labrador", 3, 12.5, "CLI001")

    assert m.nombre == "Firulais"
    assert m.edad == 3
    assert m.peso == 12.5
    assert m.id_mascota > 0


@pytest.mark.parametrize(
    "nombre, motivo",
    [
        ("", "nombre vacío"),
        ("   ", "nombre con espacios"),
    ],
)
def test_registrar_mascota_nombre_invalido_pe(
    cliente_entorno, mascota_entorno, nombre, motivo
):
    cliente_repo, svc_cliente = cliente_entorno
    _registrar_cliente_valido(cliente_repo, svc_cliente)

    _, _, svc = mascota_entorno
    with pytest.raises(ValueError):
        svc.registrar(nombre, "Canino", "Labrador", 3, 12.5, "CLI001")


def test_registrar_mascota_nombre_none(cliente_entorno, mascota_entorno):
    cliente_repo, svc_cliente = cliente_entorno
    _registrar_cliente_valido(cliente_repo, svc_cliente)

    _, _, svc = mascota_entorno
    with pytest.raises(ValueError):
        svc.registrar(None, "Canino", "Labrador", 3, 12.5, "CLI001")


def test_registrar_mascota_nombre_int(cliente_entorno, mascota_entorno):
    cliente_repo, svc_cliente = cliente_entorno
    _registrar_cliente_valido(cliente_repo, svc_cliente)

    _, _, svc = mascota_entorno
    with pytest.raises(AttributeError):
        svc.registrar(123, "Canino", "Labrador", 3, 12.5, "CLI001")


@pytest.mark.parametrize("edad", [-1])
def test_registrar_mascota_edad_invalida_bva(
    cliente_entorno, mascota_entorno, edad
):
    cliente_repo, svc_cliente = cliente_entorno
    _registrar_cliente_valido(cliente_repo, svc_cliente)

    _, _, svc = mascota_entorno
    with pytest.raises(ValueError):
        svc.registrar("Firulais", "Canino", "Labrador", edad, 12.5, "CLI001")


@pytest.mark.parametrize("edad", [0, 1])
def test_registrar_mascota_edad_valida_bva(
    cliente_entorno, mascota_entorno, edad
):
    cliente_repo, svc_cliente = cliente_entorno
    _registrar_cliente_valido(cliente_repo, svc_cliente)

    _, _, svc = mascota_entorno
    svc.registrar("Firulais", "Canino", "Labrador", edad, 12.5, "CLI001")


def test_registrar_mascota_edad_none(cliente_entorno, mascota_entorno):
    cliente_repo, svc_cliente = cliente_entorno
    _registrar_cliente_valido(cliente_repo, svc_cliente)

    _, _, svc = mascota_entorno
    with pytest.raises(TypeError):
        svc.registrar("Firulais", "Canino", "Labrador", None, 12.5, "CLI001")


def test_registrar_mascota_edad_str(cliente_entorno, mascota_entorno):
    cliente_repo, svc_cliente = cliente_entorno
    _registrar_cliente_valido(cliente_repo, svc_cliente)

    _, _, svc = mascota_entorno
    with pytest.raises(TypeError):
        svc.registrar("Firulais", "Canino", "Labrador", "5", 12.5, "CLI001")


@pytest.mark.parametrize("peso", [-1, -0.1, 0])
def test_registrar_mascota_peso_invalido_bva(
    cliente_entorno, mascota_entorno, peso
):
    cliente_repo, svc_cliente = cliente_entorno
    _registrar_cliente_valido(cliente_repo, svc_cliente)

    _, _, svc = mascota_entorno
    with pytest.raises(ValueError):
        svc.registrar("Firulais", "Canino", "Labrador", 3, peso, "CLI001")


@pytest.mark.parametrize("peso", [0.1, 1])
def test_registrar_mascota_peso_valido_bva(
    cliente_entorno, mascota_entorno, peso
):
    cliente_repo, svc_cliente = cliente_entorno
    _registrar_cliente_valido(cliente_repo, svc_cliente)

    _, _, svc = mascota_entorno
    svc.registrar("Firulais", "Canino", "Labrador", 3, peso, "CLI001")


def test_registrar_mascota_peso_none(cliente_entorno, mascota_entorno):
    cliente_repo, svc_cliente = cliente_entorno
    _registrar_cliente_valido(cliente_repo, svc_cliente)

    _, _, svc = mascota_entorno
    with pytest.raises(TypeError):
        svc.registrar("Firulais", "Canino", "Labrador", 3, None, "CLI001")


def test_registrar_mascota_peso_str(cliente_entorno, mascota_entorno):
    cliente_repo, svc_cliente = cliente_entorno
    _registrar_cliente_valido(cliente_repo, svc_cliente)

    _, _, svc = mascota_entorno
    with pytest.raises(TypeError):
        svc.registrar("Firulais", "Canino", "Labrador", 3, "2.5", "CLI001")


def test_registrar_mascota_id_cliente_inexistente(mascota_entorno):
    _, _, svc = mascota_entorno
    with pytest.raises(ValueError, match="No existe un cliente"):
        svc.registrar("Firulais", "Canino", "Labrador", 3, 12.5, "CLI999")


def test_registrar_mascota_id_cliente_none(mascota_entorno):
    _, _, svc = mascota_entorno
    with pytest.raises(ValueError):
        svc.registrar("Firulais", "Canino", "Labrador", 3, 12.5, None)


def test_registrar_mascota_id_cliente_vacio(mascota_entorno):
    _, _, svc = mascota_entorno
    with pytest.raises(ValueError):
        svc.registrar("Firulais", "Canino", "Labrador", 3, 12.5, "")


def test_registrar_mascota_especie_none(cliente_entorno, mascota_entorno):
    cliente_repo, svc_cliente = cliente_entorno
    _registrar_cliente_valido(cliente_repo, svc_cliente)

    _, _, svc = mascota_entorno
    with pytest.raises(AttributeError):
        svc.registrar("Firulais", None, "Labrador", 3, 12.5, "CLI001")


def test_registrar_mascota_especie_int(cliente_entorno, mascota_entorno):
    cliente_repo, svc_cliente = cliente_entorno
    _registrar_cliente_valido(cliente_repo, svc_cliente)

    _, _, svc = mascota_entorno
    with pytest.raises(AttributeError):
        svc.registrar("Firulais", 456, "Labrador", 3, 12.5, "CLI001")


# ──────────────────────────────── buscar ────────────────────────────────


def test_buscar_mascota_existente(cliente_entorno, mascota_entorno):
    cliente_repo, svc_cliente = cliente_entorno
    _registrar_cliente_valido(cliente_repo, svc_cliente)

    _, _, svc = mascota_entorno
    m = svc.registrar("Firulais", "Canino", "Labrador", 3, 12.5, "CLI001")

    resultado = svc.buscar(m.id_mascota)
    assert resultado.nombre == "Firulais"


def test_buscar_mascota_no_existente(mascota_entorno):
    _, _, svc = mascota_entorno
    with pytest.raises(ValueError, match="No se encontró una mascota"):
        svc.buscar(999)


def test_buscar_mascota_none(mascota_entorno):
    _, _, svc = mascota_entorno
    with pytest.raises(ValueError):
        svc.buscar(None)


def test_buscar_mascota_negativo(mascota_entorno):
    _, _, svc = mascota_entorno
    with pytest.raises(ValueError):
        svc.buscar(-1)


def test_buscar_mascota_cero(mascota_entorno):
    _, _, svc = mascota_entorno
    with pytest.raises(ValueError):
        svc.buscar(0)


# ──────────────────────────────── listar ────────────────────────────────


def test_listar_mascotas_sin_datos(mascota_entorno):
    _, _, svc = mascota_entorno
    assert svc.listar() == []


def test_listar_mascotas_con_datos(cliente_entorno, mascota_entorno):
    cliente_repo, svc_cliente = cliente_entorno
    _registrar_cliente_valido(cliente_repo, svc_cliente)

    _, _, svc = mascota_entorno
    svc.registrar("Firulais", "Canino", "Labrador", 3, 12.5, "CLI001")
    svc.registrar("Misi", "Felino", "Siamés", 5, 4.2, "CLI001")

    resultado = svc.listar()
    assert len(resultado) == 2
