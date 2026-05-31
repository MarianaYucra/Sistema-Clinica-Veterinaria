import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import List, Optional

from app.models import (
    Cita,
    Cliente,
    Mascota,
    RegistroClinico,
    Veterinario,
)

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "clinica.db"


def obtener_ruta_base_datos() -> str:
    return str(DEFAULT_DB_PATH)


class SQLiteRepository:
    def __init__(self, db_path: str = ":memory:"):
        self._db_path = db_path
        self._conexion_memoria = (
            sqlite3.connect(self._db_path) if self._db_path == ":memory:" else None
        )
        if self._conexion_memoria is not None:
            self._conexion_memoria.execute("PRAGMA foreign_keys = ON")
        self._inicializar_base_datos()

    @contextmanager
    def _conectar(self):
        if self._conexion_memoria is not None:
            try:
                yield self._conexion_memoria
                self._conexion_memoria.commit()
            except Exception:
                self._conexion_memoria.rollback()
                raise
            return

        if self._db_path != ":memory:":
            Path(self._db_path).parent.mkdir(parents=True, exist_ok=True)
        conexion = sqlite3.connect(self._db_path)
        conexion.execute("PRAGMA foreign_keys = ON")
        try:
            yield conexion
            conexion.commit()
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    def _inicializar_base_datos(self):
        with self._conectar() as conexion:
            conexion.executescript(
                """
                CREATE TABLE IF NOT EXISTS clientes (
                    id_cliente TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                );

                CREATE TABLE IF NOT EXISTS veterinarios (
                    id_veterinario TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    especialidad TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS mascotas (
                    id_mascota INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    especie TEXT NOT NULL,
                    raza TEXT NOT NULL,
                    edad INTEGER NOT NULL,
                    peso REAL NOT NULL,
                    id_cliente TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS citas (
                    id_cita INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL,
                    hora TEXT NOT NULL,
                    id_mascota INTEGER NOT NULL,
                    id_veterinario TEXT NOT NULL,
                    motivo TEXT NOT NULL,
                    estado TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS registros_clinicos (
                    id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_cita INTEGER NOT NULL,
                    id_mascota INTEGER NOT NULL,
                    fecha TEXT NOT NULL,
                    diagnostico TEXT NOT NULL,
                    tratamiento TEXT NOT NULL,
                    observaciones TEXT NOT NULL
                );
                """
            )


def _cliente_desde_fila(fila) -> Optional[Cliente]:
    if fila is None:
        return None
    return Cliente(
        id_cliente=fila[0],
        nombre=fila[1],
        telefono=fila[2],
        email=fila[3],
    )


def _veterinario_desde_fila(fila) -> Optional[Veterinario]:
    if fila is None:
        return None
    return Veterinario(
        id_veterinario=fila[0],
        nombre=fila[1],
        especialidad=fila[2],
    )


def _mascota_desde_fila(fila) -> Optional[Mascota]:
    if fila is None:
        return None
    return Mascota(
        id_mascota=fila[0],
        nombre=fila[1],
        especie=fila[2],
        raza=fila[3],
        edad=fila[4],
        peso=fila[5],
        id_cliente=fila[6],
    )


def _cita_desde_fila(fila) -> Optional[Cita]:
    if fila is None:
        return None
    return Cita(
        id_cita=fila[0],
        fecha=fila[1],
        hora=fila[2],
        id_mascota=fila[3],
        id_veterinario=fila[4],
        motivo=fila[5],
        estado=fila[6],
    )


def _registro_desde_fila(fila) -> Optional[RegistroClinico]:
    if fila is None:
        return None
    return RegistroClinico(
        id_registro=fila[0],
        id_cita=fila[1],
        id_mascota=fila[2],
        fecha=fila[3],
        diagnostico=fila[4],
        tratamiento=fila[5],
        observaciones=fila[6],
    )


class ClienteRepository(SQLiteRepository):
    def guardar(self, cliente: Cliente) -> None:
        with self._conectar() as conexion:
            conexion.execute(
                """
                INSERT INTO clientes (id_cliente, nombre, telefono, email)
                VALUES (?, ?, ?, ?)
                """,
                (
                    cliente.id_cliente,
                    cliente.nombre,
                    cliente.telefono,
                    cliente.email,
                ),
            )

    def buscar(self, id_cliente: str) -> Optional[Cliente]:
        with self._conectar() as conexion:
            fila = conexion.execute(
                """
                SELECT id_cliente, nombre, telefono, email
                FROM clientes
                WHERE id_cliente = ?
                """,
                (id_cliente,),
            ).fetchone()
        return _cliente_desde_fila(fila)

    def buscar_por_nombre(self, nombre: str) -> Optional[Cliente]:
        with self._conectar() as conexion:
            fila = conexion.execute(
                """
                SELECT id_cliente, nombre, telefono, email
                FROM clientes
                WHERE LOWER(nombre) = LOWER(?)
                """,
                (nombre.strip(),),
            ).fetchone()
        return _cliente_desde_fila(fila)

    def buscar_por_email(self, email: str) -> Optional[Cliente]:
        with self._conectar() as conexion:
            fila = conexion.execute(
                """
                SELECT id_cliente, nombre, telefono, email
                FROM clientes
                WHERE LOWER(email) = LOWER(?)
                """,
                (email.strip(),),
            ).fetchone()
        return _cliente_desde_fila(fila)

    def listar(self) -> List[Cliente]:
        with self._conectar() as conexion:
            filas = conexion.execute(
                """
                SELECT id_cliente, nombre, telefono, email
                FROM clientes
                ORDER BY rowid
                """
            ).fetchall()
        return [_cliente_desde_fila(fila) for fila in filas]

    def existe(self, id_cliente: str) -> bool:
        with self._conectar() as conexion:
            fila = conexion.execute(
                "SELECT 1 FROM clientes WHERE id_cliente = ?",
                (id_cliente,),
            ).fetchone()
        return fila is not None


class VeterinarioRepository(SQLiteRepository):
    def guardar(self, veterinario: Veterinario) -> None:
        with self._conectar() as conexion:
            conexion.execute(
                """
                INSERT INTO veterinarios (id_veterinario, nombre, especialidad)
                VALUES (?, ?, ?)
                """,
                (
                    veterinario.id_veterinario,
                    veterinario.nombre,
                    veterinario.especialidad,
                ),
            )

    def buscar(self, id_veterinario: str) -> Optional[Veterinario]:
        with self._conectar() as conexion:
            fila = conexion.execute(
                """
                SELECT id_veterinario, nombre, especialidad
                FROM veterinarios
                WHERE id_veterinario = ?
                """,
                (id_veterinario,),
            ).fetchone()
        return _veterinario_desde_fila(fila)

    def buscar_por_nombre(self, nombre: str) -> Optional[Veterinario]:
        with self._conectar() as conexion:
            fila = conexion.execute(
                """
                SELECT id_veterinario, nombre, especialidad
                FROM veterinarios
                WHERE LOWER(nombre) = LOWER(?)
                """,
                (nombre.strip(),),
            ).fetchone()
        return _veterinario_desde_fila(fila)

    def buscar_por_especialidad(self, especialidad: str) -> List[Veterinario]:
        with self._conectar() as conexion:
            filas = conexion.execute(
                """
                SELECT id_veterinario, nombre, especialidad
                FROM veterinarios
                WHERE LOWER(especialidad) LIKE LOWER(?)
                ORDER BY rowid
                """,
                (f"%{especialidad.strip()}%",),
            ).fetchall()
        return [_veterinario_desde_fila(fila) for fila in filas]

    def listar(self) -> List[Veterinario]:
        with self._conectar() as conexion:
            filas = conexion.execute(
                """
                SELECT id_veterinario, nombre, especialidad
                FROM veterinarios
                ORDER BY rowid
                """
            ).fetchall()
        return [_veterinario_desde_fila(fila) for fila in filas]

    def existe(self, id_veterinario: str) -> bool:
        with self._conectar() as conexion:
            fila = conexion.execute(
                "SELECT 1 FROM veterinarios WHERE id_veterinario = ?",
                (id_veterinario,),
            ).fetchone()
        return fila is not None


class MascotaRepository(SQLiteRepository):
    def guardar(self, mascota: Mascota) -> Mascota:
        with self._conectar() as conexion:
            if mascota.id_mascota == 0:
                cursor = conexion.execute(
                    """
                    INSERT INTO mascotas
                        (nombre, especie, raza, edad, peso, id_cliente)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        mascota.nombre,
                        mascota.especie,
                        mascota.raza,
                        mascota.edad,
                        mascota.peso,
                        mascota.id_cliente,
                    ),
                )
                mascota.id_mascota = cursor.lastrowid
            else:
                conexion.execute(
                    """
                    UPDATE mascotas
                    SET nombre = ?, especie = ?, raza = ?, edad = ?,
                        peso = ?, id_cliente = ?
                    WHERE id_mascota = ?
                    """,
                    (
                        mascota.nombre,
                        mascota.especie,
                        mascota.raza,
                        mascota.edad,
                        mascota.peso,
                        mascota.id_cliente,
                        mascota.id_mascota,
                    ),
                )
        return mascota

    def buscar(self, id_mascota: int) -> Optional[Mascota]:
        with self._conectar() as conexion:
            fila = conexion.execute(
                """
                SELECT id_mascota, nombre, especie, raza, edad, peso, id_cliente
                FROM mascotas
                WHERE id_mascota = ?
                """,
                (id_mascota,),
            ).fetchone()
        return _mascota_desde_fila(fila)

    def listar(self) -> List[Mascota]:
        with self._conectar() as conexion:
            filas = conexion.execute(
                """
                SELECT id_mascota, nombre, especie, raza, edad, peso, id_cliente
                FROM mascotas
                ORDER BY id_mascota
                """
            ).fetchall()
        return [_mascota_desde_fila(fila) for fila in filas]

    def listar_por_cliente(self, id_cliente: str) -> List[Mascota]:
        with self._conectar() as conexion:
            filas = conexion.execute(
                """
                SELECT id_mascota, nombre, especie, raza, edad, peso, id_cliente
                FROM mascotas
                WHERE id_cliente = ?
                ORDER BY id_mascota
                """,
                (id_cliente,),
            ).fetchall()
        return [_mascota_desde_fila(fila) for fila in filas]

    def existe(self, id_mascota: int) -> bool:
        with self._conectar() as conexion:
            fila = conexion.execute(
                "SELECT 1 FROM mascotas WHERE id_mascota = ?",
                (id_mascota,),
            ).fetchone()
        return fila is not None


class CitaRepository(SQLiteRepository):
    def guardar(self, cita: Cita) -> Cita:
        with self._conectar() as conexion:
            if cita.id_cita == 0:
                cursor = conexion.execute(
                    """
                    INSERT INTO citas
                        (fecha, hora, id_mascota, id_veterinario, motivo, estado)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        cita.fecha,
                        cita.hora,
                        cita.id_mascota,
                        cita.id_veterinario,
                        cita.motivo,
                        cita.estado,
                    ),
                )
                cita.id_cita = cursor.lastrowid
            else:
                conexion.execute(
                    """
                    UPDATE citas
                    SET fecha = ?, hora = ?, id_mascota = ?,
                        id_veterinario = ?, motivo = ?, estado = ?
                    WHERE id_cita = ?
                    """,
                    (
                        cita.fecha,
                        cita.hora,
                        cita.id_mascota,
                        cita.id_veterinario,
                        cita.motivo,
                        cita.estado,
                        cita.id_cita,
                    ),
                )
        return cita

    def actualizar_estado(self, id_cita: int, estado: str) -> None:
        with self._conectar() as conexion:
            conexion.execute(
                "UPDATE citas SET estado = ? WHERE id_cita = ?",
                (estado, id_cita),
            )

    def buscar(self, id_cita: int) -> Optional[Cita]:
        with self._conectar() as conexion:
            fila = conexion.execute(
                """
                SELECT id_cita, fecha, hora, id_mascota, id_veterinario,
                       motivo, estado
                FROM citas
                WHERE id_cita = ?
                """,
                (id_cita,),
            ).fetchone()
        return _cita_desde_fila(fila)

    def listar(self) -> List[Cita]:
        with self._conectar() as conexion:
            filas = conexion.execute(
                """
                SELECT id_cita, fecha, hora, id_mascota, id_veterinario,
                       motivo, estado
                FROM citas
                ORDER BY id_cita
                """
            ).fetchall()
        return [_cita_desde_fila(fila) for fila in filas]

    def buscar_por_veterinario_fecha_hora(
        self, id_veterinario: str, fecha: str, hora: str
    ) -> Optional[Cita]:
        with self._conectar() as conexion:
            fila = conexion.execute(
                """
                SELECT id_cita, fecha, hora, id_mascota, id_veterinario,
                       motivo, estado
                FROM citas
                WHERE id_veterinario = ?
                  AND fecha = ?
                  AND hora = ?
                  AND estado = 'Programada'
                """,
                (id_veterinario, fecha, hora),
            ).fetchone()
        return _cita_desde_fila(fila)


class RegistroClinicoRepository(SQLiteRepository):
    def guardar(self, registro: RegistroClinico) -> RegistroClinico:
        with self._conectar() as conexion:
            if registro.id_registro == 0:
                cursor = conexion.execute(
                    """
                    INSERT INTO registros_clinicos
                        (id_cita, id_mascota, fecha, diagnostico,
                         tratamiento, observaciones)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        registro.id_cita,
                        registro.id_mascota,
                        registro.fecha,
                        registro.diagnostico,
                        registro.tratamiento,
                        registro.observaciones,
                    ),
                )
                registro.id_registro = cursor.lastrowid
            else:
                conexion.execute(
                    """
                    UPDATE registros_clinicos
                    SET id_cita = ?, id_mascota = ?, fecha = ?,
                        diagnostico = ?, tratamiento = ?, observaciones = ?
                    WHERE id_registro = ?
                    """,
                    (
                        registro.id_cita,
                        registro.id_mascota,
                        registro.fecha,
                        registro.diagnostico,
                        registro.tratamiento,
                        registro.observaciones,
                        registro.id_registro,
                    ),
                )
        return registro

    def buscar(self, id_registro: int) -> Optional[RegistroClinico]:
        with self._conectar() as conexion:
            fila = conexion.execute(
                """
                SELECT id_registro, id_cita, id_mascota, fecha,
                       diagnostico, tratamiento, observaciones
                FROM registros_clinicos
                WHERE id_registro = ?
                """,
                (id_registro,),
            ).fetchone()
        return _registro_desde_fila(fila)

    def listar_por_mascota(self, id_mascota: int) -> List[RegistroClinico]:
        with self._conectar() as conexion:
            filas = conexion.execute(
                """
                SELECT id_registro, id_cita, id_mascota, fecha,
                       diagnostico, tratamiento, observaciones
                FROM registros_clinicos
                WHERE id_mascota = ?
                ORDER BY fecha
                """,
                (id_mascota,),
            ).fetchall()
        return [_registro_desde_fila(fila) for fila in filas]
