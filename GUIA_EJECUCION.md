
# Guía de Ejecución: Sistema Clínica Veterinaria (CLI)

Este documento describe los pasos necesarios para descargar, ejecutar y administrar el Sistema de Clínica Veterinaria en un entorno local mediante Docker.

## 1. Requisitos Previos

Antes de comenzar, asegúrese de cumplir con los siguientes requisitos:

* Tener instalado **Docker Desktop** (Windows o macOS) o **Docker Engine** (Linux).
* Verificar que Docker se encuentre en ejecución.

## 2. Descargar y Ejecutar el Sistema (Primer Uso)

La imagen Docker es pública, por lo que no es necesario crear una cuenta ni iniciar sesión en Docker Hub.

Abra una terminal y ejecute el siguiente comando:

```bash
docker run -it --name clinica-veterinaria -v clinica_vol:/sistema/data jorghee/clinica-veterinaria-cli:latest
```

### 2.1. Descripción del comando

| Parámetro                                | Descripción                                                                 |
| ---------------------------------------- | --------------------------------------------------------------------------- |
| `docker run`                             | Crea e inicia un nuevo contenedor.                                          |
| `-it`                                    | Habilita el modo interactivo para utilizar la aplicación desde la terminal. |
| `--name clinica-veterinaria`             | Asigna un nombre identificador al contenedor.                               |
| `-v clinica_vol:/sistema/data`           | Monta un volumen persistente para almacenar los datos del sistema.          |
| `jorghee/clinica-veterinaria-cli:latest` | Imagen Docker del sistema.                                                  |

> **Importante**
>
> Los clientes, mascotas, citas y demás registros almacenados en el sistema permanecerán guardados incluso si se cierra la aplicación o se apaga el equipo, gracias al volumen persistente `clinica_vol`.

## 3. Verificar el Funcionamiento

Una vez iniciado el sistema:

1. Espere a que aparezca el **Menú Principal**.
2. Seleccione la opción `1` para registrar un cliente de prueba.
3. Complete los datos solicitados.
4. Seleccione la opción `0` para salir de la aplicación.
5. Vuelva a ingresar al sistema siguiendo las instrucciones de la sección 4.
6. Seleccione la opción `3` (**Listar Clientes**).

Si el cliente registrado aparece en pantalla, la persistencia de datos está funcionando correctamente.

## 4. Reanudar el Sistema

Si salió de la aplicación mediante la opción `0` o cerró la terminal, no debe volver a ejecutar el comando de la sección 2, ya que el contenedor ya existe.

Para reanudar el sistema utilice:

```bash
docker start -i clinica-veterinaria
```

Este comando iniciará nuevamente el contenedor existente y mostrará la aplicación en modo interactivo.

## 5. Reiniciar el Entorno de Pruebas

Si desea eliminar completamente los datos almacenados y comenzar desde cero, ejecute los siguientes comandos:

```bash
docker rm -f clinica-veterinaria
docker volume rm clinica_vol
```

### 5.1. Advertencia

La eliminación del volumen `clinica_vol` es irreversible.

Todos los registros almacenados (clientes, mascotas, citas y tratamientos) serán eliminados permanentemente.
