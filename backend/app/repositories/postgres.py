from typing import Optional

from app.domain.models import Cita, Cliente, Mascota, RegistroClinico, Veterinario
from app.infrastructure.database import get_connection


def _cliente(row: Optional[dict]) -> Optional[Cliente]:
    return Cliente(**row) if row else None


def _veterinario(row: Optional[dict]) -> Optional[Veterinario]:
    return Veterinario(**row) if row else None


def _mascota(row: Optional[dict]) -> Optional[Mascota]:
    if not row:
        return None
    row["peso"] = float(row["peso"])
    return Mascota(**row)


def _cita(row: Optional[dict]) -> Optional[Cita]:
    if not row:
        return None
    row["fecha"] = row["fecha"].isoformat()
    row["hora"] = row["hora"].strftime("%H:%M")
    return Cita(**row)


def _registro(row: Optional[dict]) -> Optional[RegistroClinico]:
    if not row:
        return None
    row["fecha"] = row["fecha"].isoformat()
    return RegistroClinico(**row)


class ClienteRepository:
    def guardar(self, cliente: Cliente) -> Cliente:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO clientes (id_cliente, nombre, telefono, email)
                VALUES (%s, %s, %s, %s)
                """,
                (cliente.id_cliente, cliente.nombre, cliente.telefono, cliente.email),
            )
        return cliente

    def buscar(self, id_cliente: str) -> Optional[Cliente]:
        with get_connection() as connection:
            row = connection.execute(
                "SELECT * FROM clientes WHERE id_cliente = %s",
                (id_cliente,),
            ).fetchone()
        return _cliente(row)

    def buscar_por_email(self, email: str) -> Optional[Cliente]:
        with get_connection() as connection:
            row = connection.execute(
                "SELECT * FROM clientes WHERE LOWER(email) = LOWER(%s)",
                (email,),
            ).fetchone()
        return _cliente(row)

    def buscar_por_nombre(self, nombre: str) -> Optional[Cliente]:
        with get_connection() as connection:
            row = connection.execute(
                "SELECT * FROM clientes WHERE LOWER(nombre) = LOWER(%s)",
                (nombre,),
            ).fetchone()
        return _cliente(row)

    def listar(self) -> list[Cliente]:
        with get_connection() as connection:
            rows = connection.execute(
                "SELECT * FROM clientes ORDER BY nombre"
            ).fetchall()
        return [_cliente(row) for row in rows]

    def existe(self, id_cliente: str) -> bool:
        return self.buscar(id_cliente) is not None


class VeterinarioRepository:
    def guardar(self, veterinario: Veterinario) -> Veterinario:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO veterinarios (id_veterinario, nombre, especialidad)
                VALUES (%s, %s, %s)
                """,
                (
                    veterinario.id_veterinario,
                    veterinario.nombre,
                    veterinario.especialidad,
                ),
            )
        return veterinario

    def buscar(self, id_veterinario: str) -> Optional[Veterinario]:
        with get_connection() as connection:
            row = connection.execute(
                "SELECT * FROM veterinarios WHERE id_veterinario = %s",
                (id_veterinario,),
            ).fetchone()
        return _veterinario(row)

    def buscar_por_nombre(self, nombre: str) -> Optional[Veterinario]:
        with get_connection() as connection:
            row = connection.execute(
                "SELECT * FROM veterinarios WHERE LOWER(nombre) = LOWER(%s)",
                (nombre,),
            ).fetchone()
        return _veterinario(row)

    def buscar_por_especialidad(self, especialidad: str) -> list[Veterinario]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT * FROM veterinarios
                WHERE especialidad ILIKE %s
                ORDER BY nombre
                """,
                (f"%{especialidad}%",),
            ).fetchall()
        return [_veterinario(row) for row in rows]

    def listar(self) -> list[Veterinario]:
        with get_connection() as connection:
            rows = connection.execute(
                "SELECT * FROM veterinarios ORDER BY nombre"
            ).fetchall()
        return [_veterinario(row) for row in rows]

    def existe(self, id_veterinario: str) -> bool:
        return self.buscar(id_veterinario) is not None


class MascotaRepository:
    def guardar(self, mascota: Mascota) -> Mascota:
        with get_connection() as connection:
            row = connection.execute(
                """
                INSERT INTO mascotas (nombre, especie, raza, edad, peso, id_cliente)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING *
                """,
                (
                    mascota.nombre,
                    mascota.especie,
                    mascota.raza,
                    mascota.edad,
                    mascota.peso,
                    mascota.id_cliente,
                ),
            ).fetchone()
        return _mascota(row)

    def buscar(self, id_mascota: int) -> Optional[Mascota]:
        with get_connection() as connection:
            row = connection.execute(
                "SELECT * FROM mascotas WHERE id_mascota = %s",
                (id_mascota,),
            ).fetchone()
        return _mascota(row)

    def listar(self) -> list[Mascota]:
        with get_connection() as connection:
            rows = connection.execute(
                "SELECT * FROM mascotas ORDER BY nombre"
            ).fetchall()
        return [_mascota(row) for row in rows]

    def listar_por_cliente(self, id_cliente: str) -> list[Mascota]:
        with get_connection() as connection:
            rows = connection.execute(
                "SELECT * FROM mascotas WHERE id_cliente = %s ORDER BY nombre",
                (id_cliente,),
            ).fetchall()
        return [_mascota(row) for row in rows]

    def existe(self, id_mascota: int) -> bool:
        return self.buscar(id_mascota) is not None


class CitaRepository:
    def guardar(self, cita: Cita) -> Cita:
        with get_connection() as connection:
            row = connection.execute(
                """
                INSERT INTO citas
                    (fecha, hora, id_mascota, id_veterinario, motivo, estado)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING *
                """,
                (
                    cita.fecha,
                    cita.hora,
                    cita.id_mascota,
                    cita.id_veterinario,
                    cita.motivo,
                    cita.estado,
                ),
            ).fetchone()
        return _cita(row)

    def buscar(self, id_cita: int) -> Optional[Cita]:
        with get_connection() as connection:
            row = connection.execute(
                "SELECT * FROM citas WHERE id_cita = %s",
                (id_cita,),
            ).fetchone()
        return _cita(row)

    def buscar_por_veterinario_fecha_hora(
        self, id_veterinario: str, fecha: str, hora: str
    ) -> Optional[Cita]:
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT * FROM citas
                WHERE id_veterinario = %s
                  AND fecha = %s
                  AND hora = %s
                  AND estado = 'Programada'
                """,
                (id_veterinario, fecha, hora),
            ).fetchone()
        return _cita(row)

    def listar(self) -> list[Cita]:
        with get_connection() as connection:
            rows = connection.execute(
                "SELECT * FROM citas ORDER BY fecha, hora"
            ).fetchall()
        return [_cita(row) for row in rows]

    def actualizar_estado(self, id_cita: int, estado: str) -> None:
        with get_connection() as connection:
            connection.execute(
                "UPDATE citas SET estado = %s WHERE id_cita = %s",
                (estado, id_cita),
            )


class RegistroClinicoRepository:
    def guardar(self, registro: RegistroClinico) -> RegistroClinico:
        with get_connection() as connection:
            row = connection.execute(
                """
                INSERT INTO registros_clinicos
                    (id_cita, id_mascota, fecha, diagnostico, tratamiento, observaciones)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING *
                """,
                (
                    registro.id_cita,
                    registro.id_mascota,
                    registro.fecha,
                    registro.diagnostico,
                    registro.tratamiento,
                    registro.observaciones,
                ),
            ).fetchone()
        return _registro(row)

    def listar_por_mascota(self, id_mascota: int) -> list[RegistroClinico]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT * FROM registros_clinicos
                WHERE id_mascota = %s
                ORDER BY fecha DESC, id_registro DESC
                """,
                (id_mascota,),
            ).fetchall()
        return [_registro(row) for row in rows]
