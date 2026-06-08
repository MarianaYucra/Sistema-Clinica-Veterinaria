from flask import Flask, jsonify, request
from psycopg import Error as DatabaseError

from app.infrastructure.database import initialize_database
from app.repositories.postgres import (
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


def _payload() -> dict:
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValueError("El cuerpo de la solicitud debe ser JSON.")
    return data


def _list(items) -> list[dict]:
    return [item.to_dict() for item in items]


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    cliente_repo = ClienteRepository()
    veterinario_repo = VeterinarioRepository()
    mascota_repo = MascotaRepository()
    cita_repo = CitaRepository()
    registro_repo = RegistroClinicoRepository()

    clientes = ClienteService(cliente_repo)
    veterinarios = VeterinarioService(veterinario_repo)
    mascotas = MascotaService(mascota_repo, cliente_repo)
    citas = CitaService(cita_repo, mascota_repo, veterinario_repo)
    atenciones = AtencionService(cita_repo, registro_repo)

    @app.after_request
    def add_cors_headers(response):
        origin = request.headers.get("Origin", "*")
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
        return response

    @app.before_request
    def handle_options():
        if request.method == "OPTIONS":
            return ("", 204)

    @app.errorhandler(ValueError)
    def validation_error(error):
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(DatabaseError)
    def database_error(error):
        return jsonify({"error": "Error de base de datos.", "detail": str(error)}), 500

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.post("/setup")
    def setup_database():
        initialize_database()
        return jsonify({"status": "database initialized"})

    @app.get("/api/dashboard")
    def dashboard():
        all_clientes = clientes.listar()
        all_veterinarios = veterinarios.listar()
        all_mascotas = mascotas.listar()
        all_citas = citas.listar()
        return jsonify(
            {
                "stats": {
                    "clientes": len(all_clientes),
                    "veterinarios": len(all_veterinarios),
                    "mascotas": len(all_mascotas),
                    "citas": len(all_citas),
                },
                "citas": _list(all_citas),
            }
        )

    @app.get("/api/clientes")
    def list_clientes():
        return jsonify(_list(clientes.listar()))

    @app.post("/api/clientes")
    def create_cliente():
        return jsonify(clientes.registrar(_payload()).to_dict()), 201

    @app.get("/api/veterinarios")
    def list_veterinarios():
        return jsonify(_list(veterinarios.listar()))

    @app.post("/api/veterinarios")
    def create_veterinario():
        return jsonify(veterinarios.registrar(_payload()).to_dict()), 201

    @app.get("/api/mascotas")
    def list_mascotas():
        return jsonify(_list(mascotas.listar()))

    @app.post("/api/mascotas")
    def create_mascota():
        return jsonify(mascotas.registrar(_payload()).to_dict()), 201

    @app.get("/api/citas")
    def list_citas():
        return jsonify(_list(citas.listar()))

    @app.post("/api/citas")
    def create_cita():
        return jsonify(citas.agendar(_payload()).to_dict()), 201

    @app.post("/api/citas/<int:id_cita>/atencion")
    def create_atencion(id_cita: int):
        return jsonify(atenciones.registrar(id_cita, _payload()).to_dict()), 201

    @app.get("/api/mascotas/<int:id_mascota>/historial")
    def get_historial(id_mascota: int):
        return jsonify(_list(atenciones.historial(id_mascota)))

    return app
