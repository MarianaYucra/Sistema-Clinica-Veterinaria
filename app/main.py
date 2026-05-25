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


def leer_flotante(mensaje: str) -> float:
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: Ingrese un número válido.")


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
    id_cliente = input("Cédula/DNI: ")
    nombre = input("Nombre: ")
    telefono = input("Teléfono: ")
    email = input("Email: ")
    try:
        cliente = servicio.registrar(id_cliente, nombre, telefono, email)
        print(f"Cliente '{cliente.nombre}' registrado exitosamente.")
    except ValueError as e:
        print(f"Error: {e}")


def buscar_cliente(servicio: ClienteService):
    print("\n--- Buscar Cliente ---")
    id_cliente = input("Cédula/DNI a buscar: ")
    try:
        c = servicio.buscar(id_cliente)
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
    id_vet = input("ID Veterinario: ")
    nombre = input("Nombre: ")
    especialidad = input("Especialidad: ")
    try:
        vet = servicio.registrar(id_vet, nombre, especialidad)
        print(f"Veterinario '{vet.nombre}' registrado exitosamente.")
    except ValueError as e:
        print(f"Error: {e}")


def buscar_veterinario(servicio: VeterinarioService):
    print("\n--- Buscar Veterinario ---")
    id_vet = input("ID Veterinario a buscar: ")
    try:
        v = servicio.buscar(id_vet)
        print(f"  ID: {v.id_veterinario}")
        print(f"  Nombre: {v.nombre}")
        print(f"  Especialidad: {v.especialidad}")
    except ValueError as e:
        print(f"Error: {e}")


def listar_veterinarios(servicio: VeterinarioService):
    print("\n--- Lista de Veterinarios ---")
    vets = servicio.listar()
    if not vets:
        print("No hay veterinarios registrados.")
        return
    for v in vets:
        print(f"  [{v.id_veterinario}] {v.nombre} | {v.especialidad}")


def registrar_mascota(servicio: MascotaService):
    print("\n--- Registrar Mascota ---")
    nombre = input("Nombre: ")
    especie = input("Especie: ")
    raza = input("Raza: ")
    edad = leer_entero("Edad (años): ")
    peso = leer_flotante("Peso (kg): ")
    id_cliente = input("ID del Cliente (dueño): ")
    try:
        mascota = servicio.registrar(nombre, especie, raza, edad, peso, id_cliente)
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
    fecha = input("Fecha (YYYY-MM-DD): ")
    hora = input("Hora (HH:MM): ")
    id_mascota = leer_entero("ID Mascota: ")
    id_vet = input("ID Veterinario: ")
    motivo = input("Motivo: ")
    try:
        cita = servicio.agendar(fecha, hora, id_mascota, id_vet, motivo)
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


def registrar_atencion(servicio: AtencionService):
    print("\n--- Registrar Atención ---")
    id_cita = leer_entero("ID Cita a atender: ")
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
        print(f"  Registro #{r.id_registro} | Fecha: {r.fecha} | Cita: {r.id_cita}")
        print(f"    Diagnóstico:   {r.diagnostico}")
        print(f"    Tratamiento:   {r.tratamiento}")
        print(f"    Observaciones: {r.observaciones}")
        print()


def main():
    cliente_repo = ClienteRepository()
    veterinario_repo = VeterinarioRepository()
    mascota_repo = MascotaRepository()
    cita_repo = CitaRepository()
    registro_repo = RegistroClinicoRepository()

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
        mostrar_menu()
        opcion = leer_entero("Seleccione una opción: ")

        if opcion == 0:
            print("¡Hasta luego!")
            break

        accion = acciones.get(opcion)
        if accion:
            accion()
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()
