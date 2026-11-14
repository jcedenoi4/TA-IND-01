# TA-IND-01 — Análisis crítico de SeaweedFS

Actividad académica individual de Sistemas Distribuidos, Unidad 1.

## Objetivo

Analizar críticamente la arquitectura de SeaweedFS, sus transparencias de distribución, sus decisiones relacionadas con CAP y PACELC, sus modelos de comunicación y su tolerancia a fallos, comparándolo con MinIO.

El análisis se apoya en fuentes contrastadas y un experimento reproducible. Las conclusiones se basan en la documentación consultada y los resultados registrados.

## Estado del proyecto

El informe académico está redactado y compilado, con seis artículos de 2025 y 2026 complementados con documentación oficial, tres imágenes de lectura subrayadas y un entorno SeaweedFS 3.85 ejecutado con Docker. La prueba de replicación y caída de un servidor tiene comandos, resultados y cuatro capturas con identificación del entorno y fecha. El esquema a mano, el diagrama digital y el enlace del video de sustentación están incorporados. La revisión final de los requisitos de entrega sigue pendiente.

La bibliografía del informe contiene nueve entradas: seis artículos, los recursos oficiales de SeaweedFS y MinIO y una referencia universitaria para CAP/PACELC. Las referencias de proyecto indican las versiones y secciones consultadas para localizar el respaldo técnico.

## Organización

```text
informe/             Informe LaTeX, bibliografía y PDF del borrador compilado.
figuras/             Foto del esquema a mano, diagrama PNG y editable de draw.io.
evidencias/          Cuatro capturas de ejecución y registros del experimento.
evidencias/fuentes/  Capturas de lectura subrayadas y artículos originales.
experimento/         Configuración reproducible, script, comandos y resultados.
BITACORA.md          Registro de las sesiones de trabajo.
```

## Compilación

Archivo principal: `informe/informe.tex`. Requiere una distribución LaTeX con `pdflatex`, Biber y los paquetes `babel` (español), `fontenc`, `inputenc`, `lmodern`, `geometry`, `graphicx`, `booktabs`, `tabularx`, `array`, `longtable`, `csquotes`, `microtype`, `hyperref`, `xurl`, `biblatex` y el estilo `biblatex-ieee`. `tabularx`, `array` y `longtable` pertenecen al conjunto de herramientas LaTeX de la distribución.

La bibliografía está configurada con BibLaTeX, Biber y estilo IEEE. Ejecutar desde `informe/`:

```text
pdflatex informe.tex
biber informe
pdflatex informe.tex
pdflatex informe.tex
```

Compilación comprobada el 14 de noviembre de 2026 con pdfTeX de MiKTeX 26.5 y Biber 2.22. La versión compacta tiene nueve páginas: carátula, cinco páginas de contenido, referencias y dos páginas de anexos. El diagrama digital se incluye en arquitectura y la fotografía del dibujo a mano en el Anexo A. La sección de arquitectura explica las diferencias entre las dos representaciones. Las capturas originales se conservan en el repositorio para consultarlas a tamaño completo.

## Evidencias y sustentación

Los PDF originales están en `evidencias/fuentes/documentos/`. Las tres imágenes de lectura subrayadas están en `evidencias/fuentes/` y se incluyen en el Anexo B.

Los dos ejemplos de mi entorno describen demoras durante la inscripción de materias en el SGA de la UTEQ y retrasos de recepción de mensajes en WhatsApp. Están incorporados al informe y distinguen las observaciones personales de las posibles explicaciones técnicas.

Arquitectura: `figuras/esquema_mano.jpg`, `figuras/arquitectura.png` y `figuras/arquitectura.drawio`. Las imágenes se incorporaron sin modificar sus contenidos.

## Experimento reproducible

Requiere Docker Desktop con contenedores Linux, Docker Compose y Python 3.10 o posterior. Desde la raíz del repositorio:

```powershell
docker compose -f experimento/docker-compose.yml up -d
python experimento/ejecutar_prueba.py
```

La prueba comprueba dos réplicas mediante SHA-256, detiene únicamente `volume1`, consulta el archivo superviviente, intenta una nueva asignación con dos copias y reinicia el servidor. Genera un registro nuevo en `evidencias/` y conserva los datos del laboratorio. Los puertos se publican solo en localhost y la imagen está fijada por versión y digest.

Procedimiento completo: [comandos](experimento/comandos.md). Observaciones, problemas encontrados y límites: [resultados](experimento/resultados.md). Las consultas manuales, la caída y la recuperación se documentan en las capturas; la nueva asignación rechazada está registrada en el log automatizado.

**Video de sustentación:** [Ver video](https://youtu.be/Bx9uwho5vcA).

## Entrega

Repositorio: https://github.com/jcedenoi4/TA-IND-01

Fecha límite: 15 de noviembre de 2026, 23:55 (America/Guayaquil).

En el SGA entregaré únicamente un PDF de una página con mis datos identificativos y la URL completa del repositorio en una sola línea. Publicaré el informe completo y sus archivos reproducibles en el repositorio público.
