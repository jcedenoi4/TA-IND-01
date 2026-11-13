# TA-IND-01 — Análisis crítico de SeaweedFS

Actividad académica individual de Sistemas Distribuidos, Unidad 1.

## Objetivo

Analizar críticamente la arquitectura de SeaweedFS, sus transparencias de distribución, sus decisiones relacionadas con CAP y PACELC, sus modelos de comunicación y su tolerancia a fallos, comparándolo con MinIO.

Consultaré fuentes verificadas y realizaré un experimento reproducible. Formularé mis conclusiones a partir de la documentación consultada y de los resultados que observe.

## Estado del proyecto

El proyecto cuenta con la estructura de carpetas y una plantilla inicial del informe. Todavía tengo pendientes las fuentes académicas, los experimentos, las capturas y las conclusiones.

## Organización

```text
informe/             Plantilla LaTeX; posteriormente bibliografía y PDF compilado.
figuras/             Esquema a mano y diagrama digital original, pendientes.
evidencias/          Capturas originales de ejecución, pendientes.
evidencias/fuentes/  Mis capturas de lectura anotadas, pendientes.
experimento/         Configuración, comandos y resultados reales, pendientes.
BITACORA.md          Registro de las sesiones de trabajo.
```

Los archivos `.gitkeep` permiten conservar las carpetas inicialmente vacías en Git; no son evidencias.

## Compilación prevista

Archivo principal: `informe/informe.tex`. Se prevé utilizar una distribución LaTeX con `pdflatex`, Biber y los paquetes `babel` (español), `fontenc`, `inputenc`, `geometry`, `graphicx`, `booktabs`, `csquotes`, `hyperref`, `biblatex` y el estilo `biblatex-ieee`.

La plantilla aún no activa la bibliografía. Cuando exista `informe/referencias.bib` con fuentes verificadas, se habilitarán las líneas indicadas en el archivo y se ejecutará, desde `informe/`:

```text
pdflatex informe.tex
biber informe
pdflatex informe.tex
pdflatex informe.tex
```

La revisión detectó `pdflatex` y Biber instalados. Todavía tengo pendiente comprobar los paquetes necesarios y compilar el informe.

## Evidencias y sustentación

Pendientes: cuatro capturas originales de SeaweedFS, experimento propio, fotografía del esquema a mano con nombre y fecha, diagrama digital, tres capturas de artículos anotadas y dos ejemplos de mi entorno.

**Video de sustentación (3–5 minutos):** pendiente de grabar y publicar; añadiré aquí el enlace.

## Entrega

Repositorio: https://github.com/jcedenoi4/TA-IND-01

Fecha límite: 15 de noviembre de 2026, 23:55 (America/Guayaquil).

En el SGA entregaré únicamente un PDF de una página con mis datos identificativos y la URL completa del repositorio en una sola línea. Publicaré el informe completo y sus archivos reproducibles en el repositorio público.
