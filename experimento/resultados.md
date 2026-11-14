# Resultados del experimento de replicación y tolerancia a fallos

## Objetivo e hipótesis

Comprobar si un archivo con política `001` permanece legible al detener un servidor de volúmenes y si puede asignarse un archivo de una colección nueva con esa misma política durante la caída. La hipótesis de trabajo es que una copia superviviente permite leer el archivo previo, mientras que crear una nueva distribución de dos copias requiere dos servidores disponibles.

## Entorno observado

| Dato | Valor registrado |
|---|---|
| Fecha | 14 de noviembre de 2026 |
| Zona de las marcas del script | UTC−05:00, America/Guayaquil |
| Equipo | `DESKTOP-GTVSQ58` |
| Usuario del sistema | `User Program` |
| Sistema | Windows 11, compilación 26200 |
| Docker Desktop / Engine / Compose | 4.89.0 / 29.7.2 / v5.5.0 |
| Python | 3.14.7 |
| SeaweedFS comprobado dentro del contenedor | `version 30GB 3.85 7d7e06681 linux amd64` |
| Digest de imagen | `sha256:d67f9b5586f73b6623c143489849c958ae0ec36a698bf4243a19df07cfa28c22` |
| Servicios | Un Master, dos servidores de volúmenes, un Filer y un servidor S3 |
| Ubicación lógica | `dc1/rack1`, todos los contenedores en una computadora |
| Persistencia | Volúmenes Docker separados; metadatos del Filer en LevelDB2 |
| Política | `001`, dos copias totales; lectura directa con `-readMode=local` |

La cadena `30GB` forma parte de la salida de versión del binario. El límite configurado para los volúmenes de este laboratorio es 32 MB; no se interpreta esa cadena como tamaño efectivo de los volúmenes.

## Registro principal

[Salida completa de la ejecución final](../evidencias/experimento_20261114T161123023940.log), iniciada a las 16:11:23 y finalizada a las 16:11:44. El archivo conserva los comandos, respuestas y logs de los servicios. Los logs internos de los contenedores usan UTC y muestran horas cinco horas mayores que las del script.

Datos de la ejecución final:

```text
Identificador inicial: 13,087a06cd52
Identificador después de recuperar el nodo: 15,0b14fdee68
Tamaño del contenido: 112 bytes
SHA-256 esperado:
25b33ad8de4b41cbce48721b1cfdcbe99f376a95fbcefa389a7b00a8731f310e
Bucket: ta-ind-01-20261114t161123023940
```

## Observaciones

| Etapa | Resultado real | Comprobación |
|---|---|---|
| Dos servidores activos | Asignación HTTP 200 y carga HTTP 201 | El Master informó dos ubicaciones; las lecturas locales de ambos servidores devolvieron HTTP 200 y el mismo SHA-256 |
| Acceso S3 y Filer | Creación, escritura y lecturas HTTP 200 | El objeto leído por ambos servicios coincidió con el contenido original |
| `volume1` detenido | Estado `Exited (137)` tras `stop -t 5` | El Master informó una sola ubicación; lectura directa en `volume2` y lectura S3 del objeto previo con HTTP 200 |
| Nueva colección durante la caída | HTTP 406, aproximadamente 10,0494 segundos | Respuesta: `failed to find writable volumes ... replication:001 ... No writable volumes` |
| Capacidad durante la caída | 50 cupos libres en el servidor superviviente | `/dir/status` informó `Max:64`, `Volumes:14`, `Free:50`; el rechazo no ocurrió por agotamiento de esos cupos |
| Reinicio de `volume1` | El Master volvió a informar dos ubicaciones | Ambas copias anteriores conservaron el SHA-256 esperado |
| Nueva escritura después del reinicio | Asignación HTTP 200 y carga HTTP 201 | El archivo nuevo pudo leerse localmente en ambos servidores con el mismo SHA-256 |

El resultado principal es que la disponibilidad observada depende de la operación: leer un objeto ya replicado siguió funcionando, mientras que asignar un archivo de una colección nueva con dos copias fue rechazado con un solo servidor disponible. Tras recuperar el servidor, la nueva asignación y la escritura funcionaron.

## Problemas encontrados y correcciones

1. **Parámetro de arranque:** la primera configuración usó `-master` en los servidores de volúmenes. SeaweedFS 3.85 respondió `flag provided but not defined: -master`. Se corrigió a `-mserver=master:9333`; el Filer sí utiliza `-master`.
2. **Cupos insuficientes:** en la [primera ejecución registrada](../evidencias/experimento_20261114T160821039874.log), con ocho cupos por servidor, las colecciones consumieron los cupos debido al crecimiento predeterminado. La asignación posterior al reinicio devolvió HTTP 406 y el script terminó con error. Por tanto, esa ejecución no demuestra que recuperar el nodo sea insuficiente: había una limitación de capacidad que confundía el resultado.
3. **Ajuste del laboratorio:** se configuró `master.toml` para crear un volumen lógico por colección y se aumentó el límite a 64 por servidor. La [segunda ejecución](../evidencias/experimento_20261114T161012710281.log) completó la secuencia de caída y recuperación.
4. **Lectura estrictamente local:** para evitar que la lectura directa de un servidor pudiera reenviarse a otra réplica, se añadió `-readMode=local` y se realizó la ejecución final enlazada arriba. El script también comprueba servicios y capacidad antes de empezar.

Se conservaron los tres registros, incluido el fallido. No se eliminó ni editó el contenido de esos registros para convertir un fallo en un resultado satisfactorio.

## Interpretación y límites

- La réplica permitió mantener el acceso a los datos previos en el fallo probado. Eso no equivale a disponibilidad total de todas las operaciones.
- El ensayo de creación durante la caída es una **asignación de una colección nueva**. No se probó una actualización concurrente del mismo objeto ni se demostró que toda escritura posible tenga exactamente el mismo comportamiento.
- La comparación SHA-256 comprueba igualdad de los contenidos leídos. No mide por sí sola linealizabilidad, consistencia bajo concurrencia o durabilidad ante pérdida de energía.
- Se detuvo un proceso/contenedor. No se provocó una partición de red; estos resultados no bastan para clasificar globalmente el sistema como CP o AP ni para demostrar PACELC.
- Se reinició el mismo contenedor con sus datos persistentes. No se borró un disco ni se sustituyó una réplica vacía: no se demostró reconstrucción automática desde cero.
- No se ejecutó `volume.fix.replication`; no se atribuye la recuperación observada a ese comando.
- El Master y el Filer son únicos y comparten computadora con los servidores. No se probó su caída ni la caída del equipo anfitrión.
- Se usó un contenido de 112 bytes y pocas operaciones. Las duraciones registradas son observaciones de esta ejecución, no un benchmark de rendimiento ni una comparación experimental con MinIO.
- La versión estudiada es 3.85. No se generalizan estos resultados a todas las versiones de SeaweedFS.
- La ejecución registrada del script se realizó mediante asistencia automatizada. Posteriormente se incorporaron cuatro capturas de consultas manuales desde PowerShell: servicios y versión, lectura de ambas réplicas, detención con lectura superviviente y recuperación. El rechazo de nueva asignación está documentado en el registro, no en esas capturas.

## Estado al finalizar

Al terminar el script quedaron cinco servicios activos y los datos de prueba conservados. Las capturas posteriores se guardaron como `evidencias/captura_01.png` a `captura_04.png`, sin modificar sus imágenes. Las capturas 2 a 4 muestran fecha y hora en el encabezado HTTP `Date`, además del usuario y equipo en el contenido. La captura 1 muestra el estado de los cinco servicios, la versión y las salidas de `Get-Date`, `whoami` y `hostname`, con fecha local 14 de noviembre de 2026 a las 16:25:54. Se tomó después de la recuperación: su numeración organiza los temas y no representa el orden cronológico de las tomas.
