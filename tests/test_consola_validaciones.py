from app.main import registrar_cliente, registrar_veterinario
from app.repository import ClienteRepository, VeterinarioRepository
from app.services import ClienteService, VeterinarioService


def _simular_inputs(monkeypatch, valores):
    entradas = iter(valores)
    monkeypatch.setattr("builtins.input", lambda _mensaje: next(entradas))


def test_registrar_cliente_repite_campos_invalidos_en_consola(
    monkeypatch, capsys
):
    servicio = ClienteService(ClienteRepository())
    _simular_inputs(
        monkeypatch,
        [
            "fdsf",
            "12345678",
            "54345",
            "Juan Perez",
            "gdfgfd",
            "987654321",
            "gfdfg",
            "juan@mail.com",
        ],
    )

    registrar_cliente(servicio)

    salida = capsys.readouterr().out
    assert "El DNI del cliente solo debe contener numeros." in salida
    assert "El nombre del cliente solo debe contener letras y espacios." in salida
    assert "El telefono del cliente solo debe contener numeros." in salida
    assert "El correo del cliente no tiene un formato valido." in salida
    assert len(servicio.listar()) == 1
    assert servicio.listar()[0].nombre == "Juan Perez"


def test_registrar_veterinario_repite_campos_invalidos_en_consola(
    monkeypatch, capsys
):
    servicio = VeterinarioService(VeterinarioRepository())
    _simular_inputs(
        monkeypatch,
        [
            "123",
            "VET001",
            "Dr.",
            "Dr. Perez",
            "Ojo",
            "Cardiologia",
        ],
    )

    registrar_veterinario(servicio)

    salida = capsys.readouterr().out
    assert "El ID del veterinario debe tener letras seguidas de 3 a 6 numeros." in salida
    assert "El nombre del veterinario debe tener mas de 2 letras." in salida
    assert "La especialidad del veterinario debe tener mas de 3 letras." in salida
    assert len(servicio.listar()) == 1
    assert servicio.listar()[0].especialidad == "Cardiologia"
