# Ejecución del experimento de SeaweedFS

Todos los comandos de esta guía se ejecutan desde la raíz del repositorio, en PowerShell. El experimento usa únicamente datos de prueba y deja los cinco servicios activos al finalizar.

## Requisitos y configuración

- Docker Desktop iniciado, con motor de contenedores Linux y Docker Compose.
- Python 3.10 o posterior; el script utiliza solo la biblioteca estándar. Versión comprobada: Python 3.14.7.
- Puertos locales libres: 9333, 8080, 8081, 8888 y 8333.
- Conexión a Internet para descargar la imagen en el primer arranque.
- Imagen: SeaweedFS 3.85, Linux amd64, fijada también por digest en `docker-compose.yml`. No se utiliza `latest`.
- Dos servidores en `dc1/rack1`, política `001`: original y una copia adicional. Cada servidor dispone de 64 cupos de volúmenes. `master.toml` reduce el crecimiento a un volumen lógico por colección, para no consumir los cupos con volúmenes vacíos.
- `-readMode=local` en ambos servidores: una lectura directa verifica los datos locales, sin reenviarse a otra réplica.
- Metadatos del Filer: LevelDB2 incorporado, persistido mediante el volumen Docker `filer-data`. No requiere instalar otra base de datos.
- El acceso S3 del laboratorio no tiene credenciales configuradas. Los puertos están publicados exclusivamente en `127.0.0.1`; esta configuración no es una propuesta de seguridad para producción.

## 1. Comprobar y arrancar

```powershell
docker version
docker compose version
docker compose -f experimento/docker-compose.yml config --quiet
docker compose -f experimento/docker-compose.yml up -d
docker compose -f experimento/docker-compose.yml ps -a
docker compose -f experimento/docker-compose.yml exec -T master weed version
```

`depends_on` ordena el arranque, pero no garantiza que un servicio esté listo. El script espera hasta 60 segundos por los servicios HTTP y comprueba que el Master registre dos servidores con cupos disponibles.

## 2. Ejecutar la prueba completa

```powershell
python experimento/ejecutar_prueba.py
```

El script imprime las salidas y crea un registro nuevo en `evidencias/experimento_FECHAHORA.log`, con fecha y hora UTC−05:00, usuario, equipo, versiones, solicitudes HTTP, estados, contenidos y hashes. La fecha y el nombre cambian en cada ejecución; no debe esperarse obtener los mismos identificadores de archivo.

Secuencia ejecutada:

1. Verificar versiones, configuración, servicios y capacidad.
2. Solicitar un identificador al Master usando `replication=001` y una colección nueva.
3. Subir un archivo de prueba por HTTP multipart al servidor asignado.
4. Consultar las dos ubicaciones del volumen y leer el archivo directamente en los puertos 8080 y 8081. Comparar cada SHA-256 con el original.
5. Crear un bucket S3 de prueba, escribir un objeto y comprobarlo mediante S3 y Filer.
6. Detener `volume1` y esperar a que el Master registre una ubicación del volumen.
7. Leer la copia superviviente y el objeto S3 previo; registrar la capacidad todavía disponible.
8. Intentar asignar un archivo de una colección nueva con `replication=001`. Registrar el rechazo HTTP.
9. Reiniciar `volume1`, esperar a recuperar las dos ubicaciones y comprobar los hashes.
10. Asignar y escribir otro archivo; comprobar las dos copias nuevas.

El script utiliza `finally` para reiniciar `volume1` si falla una comprobación durante la etapa de caída. Si se cierra abruptamente Python o Docker, comprobar el estado y ejecutar el comando de inicio indicado abajo.

## 3. Comandos y operaciones utilizados por el script

Estos comandos se ejecutaron durante la prueba; las salidas completas están en los registros:

```powershell
docker compose -f experimento/docker-compose.yml stop -t 5 volume1
docker compose -f experimento/docker-compose.yml start volume1
docker compose -f experimento/docker-compose.yml ps -a
docker compose -f experimento/docker-compose.yml logs --no-color --tail 35 master volume1 volume2 filer s3
```

`stop -t 5` envía la señal de detención y concede cinco segundos antes de forzar el cierre. En esta ejecución `volume1` terminó con código 137. Se trata de una detención de proceso/contenedor, no de una partición de red ni de una pérdida de disco.

Las operaciones HTTP se implementan en Python con `urllib.request`, no mediante un cliente S3 externo:

| Operación | Solicitud |
|---|---|
| Topología y cupos | `GET http://127.0.0.1:9333/dir/status` |
| Asignar con dos copias | `GET http://127.0.0.1:9333/dir/assign?replication=001&count=1&collection=COLECCION` |
| Localizar volumen | `GET http://127.0.0.1:9333/dir/lookup?volumeId=ID` |
| Subir archivo | `POST http://127.0.0.1:8080/FID` o puerto 8081, multipart |
| Leer copia local | `GET http://127.0.0.1:8080/FID` y `GET http://127.0.0.1:8081/FID` |
| Crear bucket | `PUT http://127.0.0.1:8333/BUCKET` |
| Escribir objeto S3 | `PUT http://127.0.0.1:8333/BUCKET/prueba.txt` |
| Leer objeto S3 | `GET http://127.0.0.1:8333/BUCKET/prueba.txt` |
| Leer mediante Filer | `GET http://127.0.0.1:8888/buckets/BUCKET/prueba.txt` |

`FID`, `ID`, `COLECCION` y `BUCKET` son valores obtenidos o generados en cada ejecución. El script convierte las direcciones internas `volume1:8080` y `volume2:8080` a los puertos locales correspondientes.

## 4. Consultar el entorno y detenerlo

Interfaces del laboratorio: [Master](http://127.0.0.1:9333), [Filer](http://127.0.0.1:8888) y [S3](http://127.0.0.1:8333). S3 devuelve una respuesta de API, no una consola gráfica de administración.

Comando disponible para detener el entorno conservando sus datos; no se ejecuta automáticamente al terminar:

```powershell
docker compose -f experimento/docker-compose.yml stop
```

Para volver a iniciarlo:

```powershell
docker compose -f experimento/docker-compose.yml up -d
```

No usar `down -v` salvo que se quiera eliminar deliberadamente todos los datos del laboratorio. Las ejecuciones conservan sus colecciones y consumen cupos; el script rechaza el inicio si no quedan suficientes. Un clon limpio puede tener distintos volúmenes y salidas, pero debe reproducir las comprobaciones funcionales.

## Fuentes técnicas de la configuración

- [Versión 3.85 del proyecto](https://github.com/seaweedfs/seaweedfs/releases/tag/3.85).
- [Parámetros del Filer en 3.85](https://github.com/seaweedfs/seaweedfs/blob/3.85/weed/command/filer.go).
- [Parámetros de servidores de volúmenes en 3.85](https://github.com/seaweedfs/seaweedfs/blob/3.85/weed/command/volume.go).
- [API REST de SeaweedFS](https://github.com/seaweedfs/seaweedfs/blob/master/REST_API.md), documentación actual; las solicitudes de esta guía se comprobaron contra el binario 3.85.

Se incorporaron cuatro capturas de consultas manuales desde PowerShell en `evidencias/captura_01.png` a `captura_04.png`, con identificación del entorno y fecha/hora. La primera se tomó después de recuperar el servidor y documenta el estado de los cinco servicios. Los registros automatizados se conservan por separado y no se presentan como capturas.
