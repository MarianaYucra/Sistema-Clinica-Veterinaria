import os

from flask import Flask, flash, redirect, render_template, request, url_for

from app.main import aplicar_descuento, calcular_subtotal, calcular_total
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


def _form_int(nombre_campo, mensaje_error):
    try:
        return int(request.form.get(nombre_campo, "0"))
    except ValueError as exc:
        raise ValueError(mensaje_error) from exc


def _form_float(nombre_campo, mensaje_error):
    try:
        return float(request.form.get(nombre_campo, "0"))
    except ValueError as exc:
        raise ValueError(mensaje_error) from exc


def _parse_precios(texto):
    try:
        return [
            float(valor.strip())
            for valor in texto.replace(",", "\n").splitlines()
            if valor.strip()
        ]
    except ValueError as exc:
        raise ValueError("Ingrese precios validos.") from exc


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
    q = request.args.get("q", "").strip()
    veterinarios = veterinario_service.listar()

    if q:
        q_lower = q.lower()
        veterinarios = [
            veterinario
            for veterinario in veterinarios
            if q_lower in veterinario.id_veterinario.lower()
            or q_lower in veterinario.nombre.lower()
            or q_lower in veterinario.especialidad.lower()
        ]

    return render_template(
        "veterinarios/lista.html",
        veterinarios=veterinarios,
        q=q,
    )


@app.route("/veterinarios/nuevo", methods=["GET", "POST"])
def nuevo_veterinario():
    if request.method == "POST":
        try:
            veterinario = veterinario_service.registrar(
                request.form.get("id_veterinario", ""),
                request.form.get("nombre", ""),
                request.form.get("especialidad", ""),
            )
            flash(
                f"Veterinario '{veterinario.nombre}' registrado correctamente.",
                "success",
            )
            return redirect(
                url_for(
                    "detalle_veterinario",
                    id_veterinario=veterinario.id_veterinario,
                )
            )
        except ValueError as exc:
            flash(str(exc), "error")

    return render_template("veterinarios/formulario.html")


@app.route("/veterinarios/<id_veterinario>")
def detalle_veterinario(id_veterinario):
    try:
        veterinario = veterinario_service.buscar(id_veterinario)
    except ValueError as exc:
        flash(str(exc), "error")
        return redirect(url_for("listar_veterinarios"))

    citas = [
        cita
        for cita in cita_service.listar()
        if cita.id_veterinario == id_veterinario
    ]

    return render_template(
        "veterinarios/detalle.html",
        veterinario=veterinario,
        citas=citas,
    )


@app.route("/mascotas")
def listar_mascotas():
    q = request.args.get("q", "").strip()
    mascotas = mascota_service.listar()
    clientes = {cliente.id_cliente: cliente for cliente in cliente_service.listar()}

    if q:
        q_lower = q.lower()
        mascotas = [
            mascota
            for mascota in mascotas
            if q_lower in mascota.nombre.lower()
            or q_lower in mascota.especie.lower()
            or q_lower in mascota.raza.lower()
            or q_lower in mascota.id_cliente.lower()
        ]

    return render_template(
        "mascotas/lista.html",
        mascotas=mascotas,
        clientes=clientes,
        q=q,
    )


@app.route("/mascotas/nueva", methods=["GET", "POST"])
def nueva_mascota():
    clientes = cliente_service.listar()

    if request.method == "POST":
        try:
            edad = _form_int("edad", "La edad debe ser un numero entero.")
            peso = _form_float("peso", "El peso debe ser un numero valido.")
            mascota = mascota_service.registrar(
                request.form.get("nombre", ""),
                request.form.get("especie", ""),
                request.form.get("raza", ""),
                edad,
                peso,
                request.form.get("id_cliente", ""),
            )
            flash(f"Mascota '{mascota.nombre}' registrada correctamente.", "success")
            return redirect(
                url_for("detalle_mascota", id_mascota=mascota.id_mascota)
            )
        except ValueError as exc:
            flash(str(exc), "error")

    return render_template(
        "mascotas/formulario.html",
        clientes=clientes,
        selected_cliente=request.args.get("id_cliente", ""),
    )


@app.route("/mascotas/<int:id_mascota>")
def detalle_mascota(id_mascota):
    try:
        mascota = mascota_service.buscar(id_mascota)
        cliente = cliente_service.buscar(mascota.id_cliente)
    except ValueError as exc:
        flash(str(exc), "error")
        return redirect(url_for("listar_mascotas"))

    citas = [
        cita for cita in cita_service.listar() if cita.id_mascota == id_mascota
    ]
    historial = atencion_service.obtener_historial(id_mascota)

    return render_template(
        "mascotas/detalle.html",
        mascota=mascota,
        cliente=cliente,
        citas=citas,
        historial=historial,
    )


@app.route("/citas")
def listar_citas():
    citas = cita_service.listar()
    mascotas = {
        mascota.id_mascota: mascota for mascota in mascota_service.listar()
    }
    veterinarios = {
        veterinario.id_veterinario: veterinario
        for veterinario in veterinario_service.listar()
    }

    return render_template(
        "citas/lista.html",
        citas=citas,
        mascotas=mascotas,
        veterinarios=veterinarios,
    )


@app.route("/citas/nueva", methods=["GET", "POST"])
def nueva_cita():
    mascotas = mascota_service.listar()
    veterinarios = veterinario_service.listar()

    if request.method == "POST":
        try:
            id_mascota = _form_int(
                "id_mascota",
                "Seleccione una mascota valida.",
            )
            cita = cita_service.agendar(
                request.form.get("fecha", ""),
                request.form.get("hora", ""),
                id_mascota,
                request.form.get("id_veterinario", ""),
                request.form.get("motivo", ""),
            )
            flash(f"Cita #{cita.id_cita} agendada correctamente.", "success")
            return redirect(url_for("listar_citas"))
        except ValueError as exc:
            flash(str(exc), "error")

    return render_template(
        "citas/formulario.html",
        mascotas=mascotas,
        veterinarios=veterinarios,
    )


@app.route("/citas/<int:id_cita>/atencion", methods=["GET", "POST"])
def atender_cita(id_cita):
    try:
        cita = cita_service.buscar(id_cita)
        mascota = mascota_service.buscar(cita.id_mascota)
        veterinario = veterinario_service.buscar(cita.id_veterinario)
    except ValueError as exc:
        flash(str(exc), "error")
        return redirect(url_for("listar_citas"))

    if request.method == "POST":
        try:
            atencion_service.registrar_atencion(
                id_cita,
                request.form.get("diagnostico", ""),
                request.form.get("tratamiento", ""),
                request.form.get("observaciones", ""),
            )
            flash(f"Atencion de la cita #{id_cita} registrada.", "success")
            return redirect(
                url_for("detalle_mascota", id_mascota=cita.id_mascota)
            )
        except ValueError as exc:
            flash(str(exc), "error")

    return render_template(
        "citas/atencion.html",
        cita=cita,
        mascota=mascota,
        veterinario=veterinario,
    )


@app.route("/transacciones/pago", methods=["GET", "POST"])
def pago():
    resultado = None

    if request.method == "POST":
        try:
            precios_texto = request.form.get("precios", "")
            precios = _parse_precios(precios_texto)
            descuento = _form_float(
                "descuento",
                "El descuento debe ser un numero valido.",
            )

            subtotal = calcular_subtotal(precios)
            monto_descuento = aplicar_descuento(subtotal, descuento)
            total = calcular_total(precios, descuento)

            resultado = {
                "subtotal": subtotal,
                "descuento": descuento,
                "monto_descuento": monto_descuento,
                "total": total,
            }
        except ValueError as exc:
            flash(str(exc), "error")

    return render_template(
        "transacciones/pago.html",
        resultado=resultado,
    )


if __name__ == "__main__":
    app.run(
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True,
        use_reloader=False,
    )
