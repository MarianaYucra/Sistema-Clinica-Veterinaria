import pytest


def test_registrar_cliente_exitoso(cliente_entorno):
    repo, svc = cliente_entorno
    cliente = svc.registrar("12345678", "Juan Perez", "987654321", "j@a.com")

    assert cliente.id_cliente == "12345678"
    assert cliente.nombre == "Juan Perez"
    assert repo.existe("12345678") is True


@pytest.mark.parametrize(
    "id_cli, nombre, motivo",
    [
        ("", "Juan", "ID vacío"),
        ("   ", "Juan", "ID con espacios"),
        ("123", "", "Nombre vacío"),
        ("123", "   ", "Nombre con espacios"),
    ],
)
def test_registrar_cliente_invalidos_pe(cliente_entorno, id_cli, nombre, motivo):
    _, svc = cliente_entorno
    with pytest.raises(ValueError):
        svc.registrar(id_cli, nombre, "987", "a@a.com")


def test_registrar_cliente_duplicado_avl(cliente_entorno):
    _, svc = cliente_entorno
    svc.registrar("123", "Juan", "987", "j@a.com")
    with pytest.raises(ValueError, match="Ya existe un cliente"):
        svc.registrar("123", "Pedro", "654", "p@a.com")


def test_buscar_cliente_existente_y_no_existente(cliente_entorno):
    _, svc = cliente_entorno
    svc.registrar("123", "Juan", "987", "j@a.com")

    assert svc.buscar("123").nombre == "Juan"
    with pytest.raises(ValueError, match="No se encontró un cliente"):
        svc.buscar("999")


def test_listar_clientes(cliente_entorno):
    _, svc = cliente_entorno
    assert len(svc.listar()) == 0
    svc.registrar("123", "Juan", "987", "j@a.com")
    assert len(svc.listar()) == 1