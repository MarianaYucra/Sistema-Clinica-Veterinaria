import pytest


def test_registrar_cliente_exitoso(cliente_entorno):
    """Prueba que un cliente valido se registre correctamente."""
    repo, svc = cliente_entorno
    cliente = svc.registrar(
        "12345678", "Juan Perez", "987654321", "juan@mail.com"
    )

    assert cliente.id_cliente == "12345678"
    assert cliente.nombre == "Juan Perez"
    assert cliente.telefono == "987654321"
    assert cliente.email == "juan@mail.com"
    assert repo.existe("12345678") is True


@pytest.mark.parametrize(
    "id_cli, nombre, telefono, email",
    [
        ("", "Juan Perez", "987654321", "juan@mail.com"),
        ("   ", "Juan Perez", "987654321", "juan@mail.com"),
        ("1234567", "Juan Perez", "987654321", "juan@mail.com"),
        ("1234567A", "Juan Perez", "987654321", "juan@mail.com"),
        ("12345678", "", "987654321", "juan@mail.com"),
        ("12345678", "   ", "987654321", "juan@mail.com"),
        ("12345678", "Juan 123", "987654321", "juan@mail.com"),
        ("12345678", "Juan Perez", "", "juan@mail.com"),
        ("12345678", "Juan Perez", "987ABC321", "juan@mail.com"),
        ("12345678", "Juan Perez", "123456", "juan@mail.com"),
        ("12345678", "Juan Perez", "987654321", ""),
        ("12345678", "Juan Perez", "987654321", "correo"),
        ("12345678", "Juan Perez", "987654321", "juan@"),
    ],
)
def test_registrar_cliente_invalidos_pe(
    cliente_entorno, id_cli, nombre, telefono, email
):
    _, svc = cliente_entorno
    with pytest.raises(ValueError):
        svc.registrar(id_cli, nombre, telefono, email)


def test_registrar_cliente_duplicado_avl(cliente_entorno):
    _, svc = cliente_entorno
    svc.registrar("12345678", "Juan Perez", "987654321", "juan@mail.com")

    with pytest.raises(ValueError, match="Ya existe un cliente"):
        svc.registrar("12345678", "Pedro Ruiz", "987654322", "pedro@mail.com")


def test_registrar_cliente_correo_duplicado(cliente_entorno):
    _, svc = cliente_entorno
    svc.registrar("12345678", "Juan Perez", "987654321", "juan@mail.com")

    with pytest.raises(ValueError, match="Ya existe un cliente"):
        svc.registrar("87654321", "Pedro Ruiz", "987654322", "JUAN@mail.com")


def test_buscar_cliente_existente_y_no_existente(cliente_entorno):
    _, svc = cliente_entorno
    svc.registrar("12345678", "Juan Perez", "987654321", "juan@mail.com")

    assert svc.buscar("12345678").nombre == "Juan Perez"
    assert svc.buscar("Juan Perez").id_cliente == "12345678"
    assert svc.buscar("JUAN@mail.com").id_cliente == "12345678"
    with pytest.raises(ValueError, match="No se encontro un cliente"):
        svc.buscar("99999999")


@pytest.mark.parametrize("criterio", ["", "   ", "ABC12345"])
def test_buscar_cliente_criterio_invalido(cliente_entorno, criterio):
    _, svc = cliente_entorno
    with pytest.raises(ValueError):
        svc.buscar(criterio)


def test_listar_clientes(cliente_entorno):
    _, svc = cliente_entorno
    assert len(svc.listar()) == 0

    svc.registrar("12345678", "Juan Perez", "987654321", "juan@mail.com")

    assert len(svc.listar()) == 1
