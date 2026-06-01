import datetime
from app.repository import (
    CitaRepository,
    ClienteRepository,
    MascotaRepository,
    RegistroClinicoRepository,
    VeterinarioRepository,
    obtener_ruta_base_datos,
)
from app.services import (
    AtencionService,
    CitaService,
    ClienteService,
    MascotaService,
    VeterinarioService,
    validar_dni_cliente,
    validar_email_cliente,
    validar_especialidad_veterinario,
    validar_id_veterinario,
    validar_nombre_cliente,
    validar_nombre_veterinario,
    validar_telefono_cliente,
)

SEPARADOR = "=" * 50


def mostrar_menu():
    print(f"\n{SEPARADOR}")
    print("   SISTEMA DE GESTIÓN - CLÍNICA VETERINARIA")
    print(SEPARADOR)
    print("  1. Registrar Cliente")
    print("  2. Buscar Cliente")
    print("  3. Listar Clientes")
    print("  4. Registrar Veterinario")
    print("  5. Buscar Veterinario")
    print("  6. Listar Veterinarios")
    print("  7. Registrar Mascota")
    print("  8. Buscar Mascota")
    print("  9. Listar Mascotas")
    print(" 10. Agendar Cita")
    print(" 11. Listar Citas")
    print(" 12. Registrar Atención (Completar Cita)")
    print(" 13. Ver Historial Clínico de Mascota")
    print("  0. Salir")
    print(SEPARADOR)


def leer_entero(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: Ingrese un número entero válido.")


def leer_entero_positivo(mensaje: str) -> int:
    while True:
        valor = leer_entero(mensaje)
        if valor > 0:
            return valor
        print("Error: El número ingresado debe ser positivo y mayor a cero.")


def leer_flotante(mensaje: str) -> float:
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: Ingrese un número válido.")


def leer_campo_validado(mensaje: str, validador):
    while True:
        try:
            return validador(input(mensaje))
        except ValueError as e:
            print(str(e))


def leer_texto_mascota(mensaje: str, campo: str) -> str:
    while True:
        valor = input(mensaje).strip()

        if not valor:
            print(f"Error: {campo} no puede estar vacío.")
            continue

        if len(valor) < 2:
            print(f"Error: {campo} debe tener al menos 2 caracteres.")
            continue

        if not all(c.isalpha() or c.isspace() for c in valor):
            print(f"Error: {campo} solo puede contener letras y espacios.")
            continue

        return valor


def leer_entero_rango(mensaje: str, minimo: int, maximo: int) -> int:
    while True:
        try:
            valor = int(input(mensaje).strip())
        except ValueError:
            print("Error: Ingrese un número entero válido.")
            continue

        if valor < minimo:
            print(f"Error: El valor no puede ser menor que {minimo}.")
            continue

        if valor > maximo:
            print(f"Error: El valor no puede ser mayor que {maximo}.")
            continue

        return valor


def leer_flotante_rango(mensaje: str, minimo: float, maximo: float) -> float:
    while True:
        try:
            valor = float(input(mensaje).strip())
        except ValueError:
            print("Error: Ingrese un número válido.")
            continue

        if valor < minimo:
            print(f"Error: El valor debe ser mayor o igual que {minimo}.")
            continue

        if valor > maximo:
            print(f"Error: El valor no puede ser mayor que {maximo}.")
            continue

        return valor


def leer_id_cliente_mascota(mensaje: str, servicio: MascotaService) -> str:
    while True:
        id_cliente = input(mensaje).strip()

        if not id_cliente:
            print("Error: El ID del cliente no puede estar vacío.")
            continue

        if not servicio._cliente_repo.existe(id_cliente):
            print(
                f"Error: No existe un cliente con ID '{id_cliente}'. "
                "Registre al cliente primero."
            )
            continue

        return id_cliente

# Validaciones para citas


def leer_fecha_cita(mensaje: str) -> str:
    while True:
        fecha = input(mensaje).strip()

        if not fecha:
            print("Error: La fecha no puede estar vacía.")
            continue

        try:
            fecha_obj = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            print("Error: La fecha debe tener el formato YYYY-MM-DD y ser válida.")
            continue

        if fecha_obj < datetime.date.today():
            print("Error: La fecha de la cita no puede estar en el pasado.")
            continue

        return fecha


def leer_hora_cita(mensaje: str, fecha: str) -> str:
    while True:
        hora = input(mensaje).strip()

        if not hora:
            print("Error: La hora no puede estar vacía.")
            continue

        try:
            hora_obj = datetime.datetime.strptime(hora, "%H:%M").time()
        except ValueError:
            print("Error: La hora debe tener el formato HH:MM en formato de 24 horas.")
            continue

        fecha_obj = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
        hoy = datetime.date.today()
        hora_actual = datetime.datetime.now().time()

        if fecha_obj == hoy and hora_obj <= hora_actual:
            print("Error: La hora de la cita no puede estar en el pasado.")
            continue

        return hora


def leer_id_mascota_cita(mensaje: str, servicio: CitaService) -> int:
    while True:
        try:
            id_mascota = int(input(mensaje).strip())
        except ValueError:
            print("Error: El ID de la mascota debe ser un número entero.")
            continue

        if id_mascota <= 0:
            print("Error: El ID de la mascota debe ser mayor a cero.")
            continue

        if not servicio._mascota_repo.existe(id_mascota):
            print(f"Error: No existe una mascota con ID '{id_mascota}'.")
            continue

        return id_mascota


def leer_id_veterinario_cita(
    mensaje: str,
    servicio: CitaService,
    fecha: str,
    hora: str
) -> str:
    while True:
        id_veterinario = input(mensaje).strip().upper()

        if not id_veterinario:
            print("Error: El ID del veterinario no puede estar vacío.")
            continue

        if not servicio._veterinario_repo.existe(id_veterinario):
            print(f"Error: No existe un veterinario con ID '{
                  id_veterinario}'.")
            continue

        conflicto = servicio._repo.buscar_por_veterinario_fecha_hora(
            id_veterinario,
            fecha,
            hora
        )

        if conflicto is not None:
            print(
                f"Error: El veterinario '{id_veterinario}' ya tiene una cita "
                f"programada el {fecha} a las {hora}."
            )
            continue

        return id_veterinario


def leer_motivo_cita(mensaje: str) -> str:
    while True:
        motivo = input(mensaje).strip()

        if not motivo:
            print("Error: El motivo de la cita no puede estar vacío.")
            continue

        if len(motivo) < 3:
            print("Error: El motivo de la cita debe tener al menos 3 caracteres.")
            continue

        if len(motivo) > 120:
            print("Error: El motivo de la cita no puede superar los 120 caracteres.")
            continue

        return motivo

# Validaciones para busqueda de clientes y veterinarios


def validar_criterio_busqueda(valor: str) -> str:
    if valor is None or not valor.strip():
        raise ValueError("El dato de busqueda no puede estar vacio.")
    return valor.strip()


def validar_descuento(descuento: float):
    if descuento < 0 or descuento > 100:
        raise ValueError("El descuento debe estar entre 0 y 100.")


def calcular_subtotal(precios):
    if not precios:
        raise ValueError("Debe ingresar al menos un servicio.")
    if any(precio <= 0 for precio in precios):
        raise ValueError("Los precios deben ser mayores a cero.")
    return sum(precios)


def aplicar_descuento(subtotal: float, descuento: float = 0) -> float:
    validar_descuento(descuento)
    return subtotal * (descuento / 100)


def calcular_total(precios, descuento: float = 0) -> float:
    subtotal = calcular_subtotal(precios)
    monto_descuento = aplicar_descuento(subtotal, descuento)
    return subtotal - monto_descuento


def registrar_pago_atencion():
    print("\n--- Registrar Pago de Atencion ---")
    precios = []

    while True:
        servicio = input("Servicio realizado: ")
        if not servicio.strip():
            print("Error: El nombre del servicio no puede estar vacio.")
            continue

        precio = leer_flotante("Precio del servicio: ")
        precios.append(precio)

        continuar = input("Agregar otro servicio? (s/n): ")
        if continuar.strip().lower() != "s":
            break

    while True:
        descuento_texto = input("Descuento (%) [Enter si no hay]: ")
        try:
            descuento = 0 if not descuento_texto.strip() else float(descuento_texto)
            break
        except ValueError:
            print("Error: Ingrese un numero valido.")

    try:
        subtotal = calcular_subtotal(precios)
        monto_descuento = aplicar_descuento(subtotal, descuento)
        total = calcular_total(precios, descuento)
        print(f"Subtotal: S/ {subtotal:.2f}")
        print(f"Descuento: S/ {monto_descuento:.2f}")
        print(f"Total a pagar: S/ {total:.2f}")
        print("Pago registrado.")
    except ValueError as e:
        print(f"Error: {e}")


def registrar_cliente(servicio: ClienteService):
    print("\n--- Registrar Cliente ---")
    while True:
        id_cliente = leer_campo_validado("Cédula/DNI: ", validar_dni_cliente)
        nombre = leer_campo_validado("Nombre: ", validar_nombre_cliente)
        telefono = leer_campo_validado("Teléfono: ", validar_telefono_cliente)
        email = leer_campo_validado("Email: ", validar_email_cliente)
        try:
            cliente = servicio.registrar(id_cliente, nombre, telefono, email)
            print(f"Cliente '{cliente.nombre}' registrado exitosamente.")
            return
        except ValueError as e:
            print(str(e))
            print("Vuelva a ingresar los datos del cliente.")


def buscar_cliente(servicio: ClienteService):
    print("\n--- Buscar Cliente ---")
    criterio = leer_campo_validado(
        "DNI, nombre o email a buscar: ", validar_criterio_busqueda
    )
    try:
        c = servicio.buscar(criterio)
        print(f"  ID: {c.id_cliente}")
        print(f"  Nombre: {c.nombre}")
        print(f"  Teléfono: {c.telefono}")
        print(f"  Email: {c.email}")
    except ValueError as e:
        print(f"Error: {e}")


def listar_clientes(servicio: ClienteService):
    print("\n--- Lista de Clientes ---")
    clientes = servicio.listar()
    if not clientes:
        print("No hay clientes registrados.")
        return
    for c in clientes:
        print(f"  [{c.id_cliente}] {c.nombre} | Tel: {c.telefono} | {c.email}")


def registrar_veterinario(servicio: VeterinarioService):
    print("\n--- Registrar Veterinario ---")
    while True:
        id_vet = leer_campo_validado(
            "ID Veterinario: ", validar_id_veterinario)
        nombre = leer_campo_validado("Nombre: ", validar_nombre_veterinario)
        especialidad = leer_campo_validado(
            "Especialidad: ", validar_especialidad_veterinario
        )
        try:
            vet = servicio.registrar(id_vet, nombre, especialidad)
            print(f"Veterinario '{vet.nombre}' registrado exitosamente.")
            return
        except ValueError as e:
            print(str(e))
            print("Vuelva a ingresar los datos del veterinario.")


def buscar_veterinario(servicio: VeterinarioService):
    print("\n--- Buscar Veterinario ---")
    criterio = leer_campo_validado(
        "ID, nombre o especialidad a buscar: ", validar_criterio_busqueda
    )
    try:
        resultado = servicio.buscar(criterio)
        veterinarios = resultado if isinstance(
            resultado, list) else [resultado]
        for v in veterinarios:
            print(f"  ID: {v.id_veterinario}")
            print(f"  Nombre: {v.nombre}")
            print(f"  Especialidad: {v.especialidad}")
    except ValueError as e:
        print(str(e))


def listar_veterinarios(servicio: VeterinarioService):
    print("\n--- Lista de Veterinarios ---")
    vets = servicio.listar()
    if not vets:
        print("No hay veterinarios registrados.")
        return
    for v in vets:
        print(f"  [{v.id_veterinario}] {v.nombre} | {v.especialidad}")


def registrar_mascota(servicio: MascotaService):
    nombre = leer_texto_mascota(
        "Nombre: ",
        "El nombre de la mascota"
    )

    especie = leer_texto_mascota(
        "Especie: ",
        "La especie de la mascota"
    )

    raza = leer_texto_mascota(
        "Raza: ",
        "La raza de la mascota"
    )

    edad = leer_entero_rango(
        "Edad (años): ",
        minimo=0,
        maximo=35
    )

    peso = leer_flotante_rango(
        "Peso (kg): ",
        minimo=0.01,
        maximo=200
    )

    id_cliente = leer_id_cliente_mascota(
        "ID del Cliente (dueño): ",
        servicio
    )

    try:
        mascota = servicio.registrar(
            nombre,
            especie,
            raza,
            edad,
            peso,
            id_cliente
        )
        print(
            f"Mascota '{mascota.nombre}' registrada con "
            f"ID {mascota.id_mascota}."
        )

    except ValueError as e:
        print(f"Error: {e}")


def buscar_mascota(servicio: MascotaService):
    print("\n--- Buscar Mascota ---")
    id_mascota = leer_entero("ID Mascota a buscar: ")
    try:
        m = servicio.buscar(id_mascota)
        print(f"  ID: {m.id_mascota}")
        print(f"  Nombre: {m.nombre}")
        print(f"  Especie: {m.especie}")
        print(f"  Raza: {m.raza}")
        print(f"  Edad: {m.edad} años")
        print(f"  Peso: {m.peso} kg")
        print(f"  ID Cliente: {m.id_cliente}")
    except ValueError as e:
        print(f"Error: {e}")


def listar_mascotas(servicio: MascotaService):
    print("\n--- Lista de Mascotas ---")
    mascotas = servicio.listar()
    if not mascotas:
        print("No hay mascotas registradas.")
        return
    for m in mascotas:
        print(
            f"  [ID {m.id_mascota}] {m.nombre} | {m.especie} - {m.raza} | "
            f"Dueño: {m.id_cliente}"
        )


def agendar_cita(servicio: CitaService):
    print("\n--- Agendar Cita ---")

    fecha = leer_fecha_cita("Fecha (YYYY-MM-DD): ")

    hora = leer_hora_cita(
        "Hora (HH:MM): ",
        fecha
    )

    id_mascota = leer_id_mascota_cita(
        "ID Mascota: ",
        servicio
    )

    id_vet = leer_id_veterinario_cita(
        "ID Veterinario: ",
        servicio,
        fecha,
        hora
    )

    motivo = leer_motivo_cita("Motivo: ")

    try:
        cita = servicio.agendar(
            fecha,
            hora,
            id_mascota,
            id_vet,
            motivo
        )

        print(f"Cita agendada con ID {cita.id_cita}.")

    except ValueError as e:
        print(f"Error: {e}")


def listar_citas(servicio: CitaService):
    print("\n--- Lista de Citas ---")
    citas = servicio.listar()
    if not citas:
        print("No hay citas registradas.")
        return
    for c in citas:
        print(
            f"  [ID {c.id_cita}] {c.fecha} {c.hora} | "
            f"Mascota: {c.id_mascota} | Vet: {c.id_veterinario} | "
            f"Estado: {c.estado}"
        )

# Registrar atencion


def registrar_atencion(servicio: AtencionService):
    print("\n--- Registrar Atención ---")
    id_cita = leer_entero_positivo("ID Cita a atender: ")
    diagnostico = input("Diagnóstico: ")
    tratamiento = input("Tratamiento: ")
    observaciones = input("Observaciones (opcional): ")
    try:
        registro = servicio.registrar_atencion(
            id_cita, diagnostico, tratamiento, observaciones
        )
        print(
            f"Atención registrada (Registro #{registro.id_registro}). "
            f"Cita marcada como 'Completada'."
        )
        opcion_pago = input("Registrar pago de esta atencion? (s/n): ")
        if opcion_pago.strip().lower() == "s":
            registrar_pago_atencion()
    except ValueError as e:
        print(f"Error: {e}")


def leer_id_cita_atencion(mensaje: str, servicio: AtencionService) -> int:
    while True:
        try:
            id_cita = int(input(mensaje).strip())
        except ValueError:
            print("Error: El ID de la cita debe ser un número entero.")
            continue

        if id_cita <= 0:
            print("Error: El ID de la cita debe ser mayor a cero.")
            continue

        cita = servicio._cita_repo.buscar(id_cita)

        if cita is None:
            print(f"Error: No existe una cita con ID '{id_cita}'.")
            continue

        if cita.estado != "Programada":
            print(
                f"Error: La cita '{id_cita}' no está en estado 'Programada' "
                f"(estado actual: '{cita.estado}')."
            )
            continue

        return id_cita


def leer_texto_atencion(mensaje: str, campo: str) -> str:
    while True:
        valor = input(mensaje).strip()

        if not valor:
            print(f"Error: {campo} no puede estar vacío.")
            continue

        if len(valor) < 3:
            print(f"Error: {campo} debe tener al menos 3 caracteres.")
            continue

        if len(valor) > 200:
            print(f"Error: {campo} no puede superar los 200 caracteres.")
            continue

        return valor


def leer_observaciones_atencion(mensaje: str) -> str:
    while True:
        valor = input(mensaje).strip()

        if len(valor) > 250:
            print("Error: Las observaciones no pueden superar los 250 caracteres.")
            continue

        return valor


def ver_historial(
    atencion_servicio: AtencionService, mascota_servicio: MascotaService
):
    print("\n--- Historial Clínico ---")
    id_mascota = leer_entero("ID Mascota: ")
    try:
        mascota = mascota_servicio.buscar(id_mascota)
    except ValueError as e:
        print(f"Error: {e}")
        return

    registros = atencion_servicio.obtener_historial(id_mascota)
    if not registros:
        print(f"La mascota '{mascota.nombre}' no tiene registros clínicos.")
        return

    print(f"Historial de '{mascota.nombre}' ({len(registros)} registro(s)):\n")
    for r in registros:
        print(f"  Registro #{r.id_registro} | Fecha: {
              r.fecha} | Cita: {r.id_cita}")
        print(f"    Diagnóstico:   {r.diagnostico}")
        print(f"    Tratamiento:   {r.tratamiento}")
        print(f"    Observaciones: {r.observaciones}")
        print()


def main():
    db_path = obtener_ruta_base_datos()
    cliente_repo = ClienteRepository(db_path)
    veterinario_repo = VeterinarioRepository(db_path)
    mascota_repo = MascotaRepository(db_path)
    cita_repo = CitaRepository(db_path)
    registro_repo = RegistroClinicoRepository(db_path)

    cliente_svc = ClienteService(cliente_repo)
    veterinario_svc = VeterinarioService(veterinario_repo)
    mascota_svc = MascotaService(mascota_repo, cliente_repo)
    cita_svc = CitaService(cita_repo, mascota_repo, veterinario_repo)
    atencion_svc = AtencionService(cita_repo, registro_repo)

    acciones = {
        1: lambda: registrar_cliente(cliente_svc),
        2: lambda: buscar_cliente(cliente_svc),
        3: lambda: listar_clientes(cliente_svc),
        4: lambda: registrar_veterinario(veterinario_svc),
        5: lambda: buscar_veterinario(veterinario_svc),
        6: lambda: listar_veterinarios(veterinario_svc),
        7: lambda: registrar_mascota(mascota_svc),
        8: lambda: buscar_mascota(mascota_svc),
        9: lambda: listar_mascotas(mascota_svc),
        10: lambda: agendar_cita(cita_svc),
        11: lambda: listar_citas(cita_svc),
        12: lambda: registrar_atencion(atencion_svc),
        13: lambda: ver_historial(atencion_svc, mascota_svc),
    }

    while True:
        try:
            mostrar_menu()
            opcion = leer_entero("Seleccione una opción: ")

            if opcion == 0:
                print("¡Hasta luego!")
                break

            accion = acciones.get(opcion)
            if accion:
                try:
                    accion()
                except KeyboardInterrupt:
                    print("\n\n[Operación cancelada por el usuario]")
            else:
                print("Opción no válida. Intente de nuevo.")
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego!")
            break


if __name__ == "__main__":
    main()
