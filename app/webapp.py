import os

from flask import Flask, flash, redirect, render_template, request, url_for

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
    q = request.args.get("q", "").strip()
    clientes = cliente_service.listar()

    if q:
        q_lower = q.lower()
        clientes = [
            cliente
            for cliente in clientes
            if q_lower in cliente.id_cliente.lower()
            or q_lower in cliente.nombre.lower()
        ]

    return render_template(
        "clientes/lista.html",
        clientes=clientes,
        q=q,
    )


@app.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():
    if request.method == "POST":
        try:
            cliente = cliente_service.registrar(
                request.form.get("id_cliente", ""),
                request.form.get("nombre", ""),
                request.form.get("telefono", ""),
                request.form.get("email", ""),
            )
            flash(f"Cliente '{cliente.nombre}' registrado correctamente.", "success")
            return redirect(
                url_for("detalle_cliente", id_cliente=cliente.id_cliente)
            )
        except ValueError as exc:
            flash(str(exc), "error")

    return render_template("clientes/formulario.html")


@app.route("/clientes/<id_cliente>")
def detalle_cliente(id_cliente):
    try:
        cliente = cliente_service.buscar(id_cliente)
    except ValueError as exc:
        flash(str(exc), "error")
        return redirect(url_for("listar_clientes"))

    mascotas = [
        mascota
        for mascota in mascota_service.listar()
        if mascota.id_cliente == id_cliente
    ]

    return render_template(
        "clientes/detalle.html",
        cliente=cliente,
        mascotas=mascotas,
    )


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


@app.route("/mascotas/<int:id_mascota>")
def detalle_mascota(id_mascota):
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
