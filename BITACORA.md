# Bitácora de trabajo

En esta bitácora registro mis avances por sesión, los problemas encontrados, cómo se resolvieron y el tiempo dedicado.

## 13 de noviembre de 2026 — Preparación del proyecto

- **Actividades:** revisión de los requisitos de la actividad, organización de las carpetas y preparación del README, `.gitignore` y la plantilla LaTeX con las secciones exigidas para el informe.
- **Estado inicial:** el proyecto tenía un README y un commit inicial (`8b4ace1`), fechado el 13 de noviembre de 2026. La rama local es `main` y tiene configurado el remoto `origin`.
- **Problema y solución:** Git no registra carpetas vacías. La estructura inicial incluye archivos `.gitkeep` para conservar esas carpetas en el repositorio.
- **Decisiones:** decidí dejar el dibujo a mano para otra sesión y avanzar hoy con la organización del proyecto y la plantilla del informe.
- **Pendientes al cerrar esta etapa:** me faltaba comprobar la visibilidad pública del repositorio, el acceso para publicar y la compilación. La revisión detectó `pdflatex` y Biber instalados.
- **Tiempo dedicado aproximado:** 30 minutos.
- **Avance registrado:** estructura y documentación inicial publicadas en el commit `4256a2c`.

## 14 de noviembre de 2026 — Bibliografía y preparación de la lectura

- **Actividades:** organización de seis artículos de 2025 y 2026; contraste de sus datos bibliográficos con Crossref y páginas editoriales; incorporación de las referencias en `referencias.bib` y configuración de las citas con BibLaTeX en estilo IEEE.
- **Problema y solución:** el registro de Crossref del artículo de Baltic Journal estaba incompleto. La lista de autores y las páginas se contrastaron con el PDF y el sumario de la revista para completar la referencia.
- **Resultado:** seis referencias incorporadas, citas vinculadas al texto y Anexo B preparado para las capturas de lectura.
- **Pendientes:** me falta revisar las paráfrasis del informe.
- **Validación técnica en esta etapa:** Biber 2.22 validó las seis entradas bibliográficas sin errores de estructura. La compilación completa se realizó posteriormente, como consta en las etapas siguientes.
- **Tiempo dedicado aproximado:** 1 hora y 30 minutos.

### Capturas de lectura de artículos

- **Actividad:** incorporación de tres capturas con fragmentos subrayados de los artículos BE-DSN, Building a modern data platform based on the data lakehouse architecture and cloud-native ecosystem y DITIS.
- **Organización:** imágenes guardadas con nombres basados en los títulos de los artículos y vinculadas al Anexo B, con su referencia y página del PDF.
- **Observación:** la segunda y la tercera imagen no muestran el número de página en el recorte; sus pies de figura indican las páginas 9 y 1, respectivamente, según los PDF originales.
- **Tiempo dedicado aproximado:** 20 minutos, adicionales al tiempo dedicado a la bibliografía.

### Entorno experimental y prueba de replicación

- **Actividades:** configuración de SeaweedFS 3.85 con imagen fijada por digest; arranque de Master, dos servidores de volúmenes, Filer y S3; preparación del script reproducible y registro de las solicitudes y respuestas.
- **Problemas y soluciones:** corrección de `-master` a `-mserver` en los servidores de volúmenes de esta versión. El primer ensayo agotó el límite de ocho volúmenes por servidor; se ajustó el crecimiento por colección y se amplió el límite a 64, conservando el registro fallido. Las lecturas finales se configuraron como locales para comprobar cada copia directamente.
- **Resultados:** archivo legible durante la caída de un servidor, nueva asignación con replicación `001` rechazada con HTTP 406 y recuperación de las nuevas escrituras tras reiniciar el nodo. Los hashes de ambas copias coincidieron.
- **Evidencias:** tres registros de ejecución en `evidencias/`, procedimiento en `experimento/comandos.md` e interpretación en `experimento/resultados.md`.
- **Sustentación:** incorporé el enlace de mi explicación oral en el README y en el informe.
- **Tiempo dedicado aproximado:** 30 minutos para la preparación, las correcciones y las pruebas del entorno, sin incluir las capturas.

### Capturas de ejecución de SeaweedFS

- **Actividades:** consulta de servicios y versión desde PowerShell, lectura del mismo archivo en ambos servidores, detención de `volume1`, lectura de la copia superviviente y reinicio con recuperación de la lectura.
- **Evidencias:** cuatro imágenes incorporadas como `captura_01.png` a `captura_04.png` y vinculadas a la sección de experimentación del informe.
- **Identificación:** la primera captura muestra fecha y hora, usuario y equipo mediante `Get-Date`, `whoami` y `hostname`. Las capturas 2 a 4 incluyen fecha y hora en las respuestas HTTP y el usuario y equipo en el contenido del archivo.
- **Tiempo dedicado:** 15 minutos.

### Ejemplos de mi entorno

- **Experiencias descritas:** lentitud del SGA durante la inscripción de materias, con actualización de la página y espera; mensajes de WhatsApp que parecían enviados pero tardaban en llegar al destinatario.
- **Avance:** incorporación de ambos ejemplos al informe, relacionados con concurrencia, latencia, reintentos y comunicación asíncrona.
- **Criterio de análisis:** diferenciación entre lo observado como usuario y las causas internas que no puedo confirmar. La espera no demuestra una cola específica y el retraso de un mensaje no demuestra por sí solo inconsistencia entre réplicas.

### Desarrollo del borrador académico

- **Actividades:** desarrollo del resumen, introducción, arquitectura, siete transparencias, CAP y PACELC, comunicación, tolerancia a fallos, comparación con MinIO, postura crítica y conclusiones. Incorporación de mis datos en la carátula.
- **Fuentes de apoyo:** documentación oficial de SeaweedFS y MinIO y un reporte público de fallo de SeaweedFS 3.85. El reporte se distingue de un diagnóstico confirmado y de los resultados del laboratorio.
- **Resultado:** resumen de 179 palabras, tabla comparativa de nueve criterios y bibliografía IEEE con los seis artículos y las fuentes técnicas adicionales. Las interpretaciones se presentan como borrador para mi revisión.
- **Problemas y soluciones:** MiKTeX no tenía algunos paquetes requeridos. Se instalaron las dependencias; el error de expansión tipográfica se resolvió con fuentes escalables Latin Modern. Se ajustó la tabla para evitar una fila aislada y se colocó cada imagen de lectura junto a su fuente.
- **Validación:** compilación mediante pdfLaTeX, Biber y dos pasadas finales de pdfLaTeX; PDF de 20 páginas totales, con revisión visual de tablas, capturas y referencias. No quedaron citas indefinidas ni desbordamientos de texto detectados.
- **Actualización del informe:** identifiqué el modelo como GPT-6.1 Sol, según la versión indicada para la actividad, e incorporé el enlace de mi explicación oral.

### Esquema a mano y diagrama digital

- **Material incorporado:** fotografía del bosquejo con mi nombre y fecha 14 de noviembre de 2026; diagrama digital en PNG y archivo editable de draw.io.
- **Organización:** archivos guardados como `figuras/esquema_mano.jpg`, `figuras/arquitectura.png` y `figuras/arquitectura.drawio`, conservando el contenido de los originales.
- **Desarrollo:** el bosquejo muestra las conexiones principales; el digital precisa roles, funciones, clases de comunicación y replicación `001`. Ambas representaciones utilizan como referencia la guía de arquitectura de la preparación.
- **Integración:** diagrama digital en la sección de arquitectura, fotografía en el Anexo A y explicación de los cambios visibles entre ambas representaciones.
- **Validación:** PDF recompilado con 21 páginas totales; comprobación visual del diagrama y de la fotografía junto al encabezado del Anexo A, sin citas indefinidas ni desbordamientos detectados.

### Ajuste de la bibliografía

- **Decisión:** mantener nueve entradas bibliográficas para evitar una lista innecesariamente extensa.
- **Cambios:** conservación de los seis artículos y sus DOI; consolidación de la documentación de cada proyecto en una referencia que identifica las secciones consultadas; uso de una referencia universitaria para CAP/PACELC.
- **Revisión:** actualización de las citas en el texto. El reporte de fallo permanece localizado como issue 6700 del proyecto SeaweedFS. No se eliminaron los artículos ni las evidencias de lectura.
- **Validación:** nueve referencias citadas, seis artículos sin cambios en sus metadatos y PDF recompilado de 19 páginas totales. Bibliografía y nota final revisadas visualmente, sin citas indefinidas ni texto fuera de los márgenes detectado.

### Video de sustentación

- **Actividad:** incorporé el enlace de mi video de sustentación en el README y en el informe.
- **Enlace:** https://youtu.be/Bx9uwho5vcA
- **Comprobación del enlace:** incorporé la URL; no he registrado una comprobación técnica de su acceso o duración.

### Distribución estimada del tiempo

El tiempo total estimado es de **8 horas**. El siguiente desglose es aproximado y resume las actividades anteriores; no constituye un cronometraje ni añade horas a las sesiones ya registradas.

| Fecha | Actividad | Tiempo aproximado |
| --- | --- | ---: |
| 13/11/2026 | Organización del proyecto, estructura y documentación inicial | 30 min |
| 14/11/2026 | Consulta de artículos y contraste bibliográfico | 1 h 30 min |
| 14/11/2026 | Capturas de lectura y organización de las imágenes | 20 min |
| 14/11/2026 | Configuración del laboratorio, correcciones y pruebas | 30 min |
| 14/11/2026 | Capturas de ejecución de SeaweedFS | 15 min |
| 14/11/2026 | Desarrollo de los dos ejemplos del entorno | 20 min |
| 14/11/2026 | Esquema a mano y fotografía | 35 min |
| 14/11/2026 | Diagrama digital y archivo editable | 45 min |
| 14/11/2026 | Desarrollo del informe y análisis comparativo | 1 h 50 min |
| 14/11/2026 | Compilación, revisión visual y ajuste de referencias | 30 min |
| 14/11/2026 | Preparación y realización del video de sustentación | 55 min |
| **Total estimado** | | **8 h** |

### Estado al cierre

- **Ajuste de extensión del 14/11/2026:** condensé las repeticiones y redistribuí las figuras para presentar una versión de nueve páginas, conservando cinco de contenido, las cuatro capturas de ejecución, las referencias y los anexos A y B. Conservé las imágenes originales y los registros del experimento. Este ajuste no añade una duración medida al total estimado anterior.

Incorporé el informe, el experimento documentado, las capturas, los diagramas y el enlace de mi video. Me queda comprobar el acceso y la duración del video y la visibilidad pública del repositorio, completar el historial auténtico exigido y preparar el PDF de una página para el SGA. Mantengo estas comprobaciones y entregas sin marcar como completadas. En esta actualización no hice commits ni push.
