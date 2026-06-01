import datetime
import pytest
from app.repository import (
    CitaRepository,
    ClienteRepository,
    MascotaRepository,
    VeterinarioRepository,
)
from app.services import (
    CitaService,
    ClienteService,
    MascotaService,
    VeterinarioService,
)

FUTURO_STR = (datetime.date.today() + datetime.timedelta(days=5)).isoformat()

@pytest.fixture
def clean_repos():
    return {
        "cliente": ClienteRepository(),
        "veterinario": VeterinarioRepository(),
        "mascota": MascotaRepository(),
        "cita": CitaRepository(),
    }

@pytest.fixture
def setup_services(clean_repos):
    repos = clean_repos
    cli_svc = ClienteService(repos["cliente"])
    vet_svc = VeterinarioService(repos["veterinario"])
    mas_svc = MascotaService(repos["mascota"], repos["cliente"])
    cit_svc = CitaService(repos["cita"], repos["mascota"], repos["veterinario"])
    
    # Register default valid entities for reference
    cli_svc.registrar("12345678", "Juan Perez", "987654321", "juan@mail.com")
    vet_svc.registrar("VET123", "Dr. Lopez", "General")
    mas_svc.registrar("Firulais", "Canino", "Labrador", 3, 15.2, "12345678")
    
    return mas_svc, cit_svc

# --- Mascota Validation Tests ---

def test_registrar_mascota_nombre_con_caracteres_invalidos(setup_services):
    mas_svc, _ = setup_services
    with pytest.raises(ValueError, match="El nombre de la mascota solo puede contener"):
        mas_svc.registrar("Firulais!", "Canino", "Labrador", 3, 15.2, "12345678")

def test_registrar_mascota_nombre_demasiado_corto(setup_services):
    mas_svc, _ = setup_services
    with pytest.raises(ValueError, match="El nombre de la mascota debe tener al menos"):
        mas_svc.registrar("A", "Canino", "Labrador", 3, 15.2, "12345678")

def test_registrar_mascota_especie_vacia(setup_services):
    mas_svc, _ = setup_services
    with pytest.raises(ValueError, match="La especie de la mascota no puede estar vacía"):
        mas_svc.registrar("Firulais", "", "Labrador", 3, 15.2, "12345678")

def test_registrar_mascota_especie_corta(setup_services):
    mas_svc, _ = setup_services
    with pytest.raises(ValueError, match="La especie de la mascota debe tener al menos"):
        mas_svc.registrar("Firulais", "C", "Labrador", 3, 15.2, "12345678")

def test_registrar_mascota_especie_con_numeros(setup_services):
    mas_svc, _ = setup_services
    with pytest.raises(ValueError, match="La especie de la mascota solo debe contener"):
        mas_svc.registrar("Firulais", "Canino123", "Labrador", 3, 15.2, "12345678")

def test_registrar_mascota_raza_vacia(setup_services):
    mas_svc, _ = setup_services
    with pytest.raises(ValueError, match="La raza de la mascota no puede estar vacía"):
        mas_svc.registrar("Firulais", "Canino", "", 3, 15.2, "12345678")

def test_registrar_mascota_raza_corta(setup_services):
    mas_svc, _ = setup_services
    with pytest.raises(ValueError, match="La raza de la mascota debe tener al menos"):
        mas_svc.registrar("Firulais", "Canino", "L", 3, 15.2, "12345678")

def test_registrar_mascota_raza_con_simbolos(setup_services):
    mas_svc, _ = setup_services
    with pytest.raises(ValueError, match="La raza de la mascota solo debe contener"):
        mas_svc.registrar("Firulais", "Canino", "Labrador!", 3, 15.2, "12345678")

def test_registrar_mascota_edad_no_realista(setup_services):
    mas_svc, _ = setup_services
    with pytest.raises(ValueError, match="La edad de la mascota no es realista"):
        mas_svc.registrar("Firulais", "Canino", "Labrador", 200, 15.2, "12345678")

def test_registrar_mascota_peso_no_realista(setup_services):
    mas_svc, _ = setup_services
    with pytest.raises(ValueError, match="El peso de la mascota no es realista"):
        mas_svc.registrar("Firulais", "Canino", "Labrador", 3, 1500.0, "12345678")

def test_registrar_mascota_id_cliente_no_string(setup_services):
    mas_svc, _ = setup_services
    with pytest.raises(ValueError, match="El ID del cliente debe ser una cadena de texto"):
        mas_svc.registrar("Firulais", "Canino", "Labrador", 3, 15.2, 12345678)

# --- Cita Validation Tests ---

def test_agendar_cita_fecha_tipo_invalido(setup_services):
    _, cit_svc = setup_services
    with pytest.raises(ValueError, match="La fecha debe ser una cadena de texto"):
        cit_svc.agendar(123, "10:00", 1, "VET123", "Control")

def test_agendar_cita_hora_tipo_invalido(setup_services):
    _, cit_svc = setup_services
    with pytest.raises(ValueError, match="La hora debe ser una cadena de texto"):
        cit_svc.agendar(FUTURO_STR, 1000, 1, "VET123", "Control")

def test_agendar_cita_id_mascota_tipo_invalido(setup_services):
    _, cit_svc = setup_services
    with pytest.raises(ValueError, match="El ID de la mascota debe ser un número entero"):
        cit_svc.agendar(FUTURO_STR, "10:00", "1", "VET123", "Control")

def test_agendar_cita_id_veterinario_tipo_invalido(setup_services):
    _, cit_svc = setup_services
    with pytest.raises(ValueError, match="El ID del veterinario debe ser una cadena de texto"):
        cit_svc.agendar(FUTURO_STR, "10:00", 1, 123, "Control")

def test_agendar_cita_motivo_tipo_invalido(setup_services):
    _, cit_svc = setup_services
    with pytest.raises(ValueError, match="El motivo debe ser una cadena de texto"):
        cit_svc.agendar(FUTURO_STR, "10:00", 1, "VET123", 123)

def test_agendar_cita_fecha_formato_invalido(setup_services):
    _, cit_svc = setup_services
    with pytest.raises(ValueError, match="La fecha debe tener el formato YYYY-MM-DD"):
        cit_svc.agendar("05/06/2026", "10:00", 1, "VET123", "Control")

def test_agendar_cita_fecha_calendario_invalido(setup_services):
    _, cit_svc = setup_services
    with pytest.raises(ValueError, match="La fecha debe tener el formato YYYY-MM-DD"):
        cit_svc.agendar("2026-02-30", "10:00", 1, "VET123", "Control")

def test_agendar_cita_hora_formato_invalido(setup_services):
    _, cit_svc = setup_services
    with pytest.raises(ValueError, match="La hora debe tener el formato HH:MM"):
        cit_svc.agendar(FUTURO_STR, "10:00 AM", 1, "VET123", "Control")

def test_agendar_cita_hora_invalida(setup_services):
    _, cit_svc = setup_services
    with pytest.raises(ValueError, match="La hora debe tener el formato HH:MM"):
        cit_svc.agendar(FUTURO_STR, "25:00", 1, "VET123", "Control")

def test_agendar_cita_motivo_corto(setup_services):
    _, cit_svc = setup_services
    with pytest.raises(ValueError, match="El motivo de la cita debe tener al menos 3 caracteres"):
        cit_svc.agendar(FUTURO_STR, "10:00", 1, "VET123", "Co")

def test_agendar_cita_fecha_en_el_pasado(setup_services):
    _, cit_svc = setup_services
    ayer = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    with pytest.raises(ValueError, match="La fecha de la cita no puede estar en el pasado"):
        cit_svc.agendar(ayer, "10:00", 1, "VET123", "Control")
