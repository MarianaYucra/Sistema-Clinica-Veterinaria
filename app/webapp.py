import os

from flask import Flask, flash, redirect, render_template, url_for

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


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")

cliente_repo = ClienteRepository()
veterinario_repo = VeterinarioRepository()
mascota_repo = MascotaRepository()
cita_repo = CitaRepository()
registro_repo = RegistroClinicoRepository()

cliente_service = ClienteService(cliente_repo)
veterinario_service = VeterinarioService(veterinario_repo)
mascota_service = MascotaService(mascota_repo, cliente_repo)
cita_service = CitaService(cita_repo, mascota_repo, veterinario_repo)
atencion_service = AtencionService(cita_repo, registro_repo)


@app.route("/")
def dashboard():
    clientes = cliente_service.listar()
    veterinarios = veterinario_service.listar()
    mascotas = mascota_service.listar()
    citas = cita_service.listar()
    citas_programadas = [
        cita for cita in citas if cita.estado == "Programada"
    ]

    stats = {
        "clientes": len(clientes),
        "veterinarios": len(veterinarios),
        "mascotas": len(mascotas),
        "citas": len(citas),
    }

    return render_template(
        "dashboard.html",
        stats=stats,
        citas_programadas=citas_programadas,
    )


def _placeholder():
    flash("Modulo pendiente de implementar en la siguiente parte.", "info")
    return redirect(url_for("dashboard"))


@app.route("/clientes")
def listar_clientes():
    return _placeholder()


@app.route("/clientes/nuevo")
def nuevo_cliente():
    return _placeholder()


@app.route("/veterinarios")
def listar_veterinarios():
    return _placeholder()


@app.route("/veterinarios/nuevo")
def nuevo_veterinario():
    return _placeholder()


@app.route("/mascotas")
def listar_mascotas():
    return _placeholder()


@app.route("/mascotas/nueva")
def nueva_mascota():
    return _placeholder()


@app.route("/citas")
def listar_citas():
    return _placeholder()


@app.route("/citas/nueva")
def nueva_cita():
    return _placeholder()


@app.route("/citas/<int:id_cita>/atencion")
def atender_cita(id_cita):
    return _placeholder()


@app.route("/transacciones/pago")
def pago():
    return _placeholder()


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
