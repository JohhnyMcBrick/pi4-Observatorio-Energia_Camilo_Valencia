# Bitácora

Rol en el equipo: Data Engineer. El proyecto es individual, así que también cubro los roles de Data Quality Analyst, Analytics Engineer y BI Analyst.

## Semana 2 (19 al 25 de octubre) – EA1

**Qué hice**
- Partí del código de la clase del lunes 19 y lo reorganicé: separé las utilidades en `src/common/` (HTTP, fechas, almacenamiento, cache de descarga) y dejé un módulo por fuente en `src/extract/`. Toda la configuración (fechas, URLs, métricas, datasets) quedó en `src/config.py`.
- Amplié la extracción de XM al rango del 1 de enero de 2024 al 30 de septiembre de 2026 y agregué la generación por planta (`Gene`, entidad `Recurso`), los aportes hídricos (`AporEner`) y el catálogo de plantas (`ListadoRecursos`). Este último va al endpoint `lists`, no recibe fechas y responde con la estructura `ListEntities`, así que escribí una función aparte para aplanarlo. Quedó con 2.493 plantas.
- Amplié el IDEAM: precipitación desde el 1 de enero de 2025 y el dataset nuevo de temperatura del aire (media, mínima y máxima por día y estación). El filtro, la agregación y el orden se hacen en el servidor con SoQL, pidiendo una semana por vez.
- Agregué una fuente propia, la TRM del Banco de la República, para estudiar si el dólar influye en el precio de bolsa.
- Hice que el pipeline sea reanudable (cache por ventana), que una fuente caída no detenga las demás y que genere las muestras de 200 filas en `data/sample/`.
- Escribí el generador de perfilamiento (`src/perfilar.py`) y revisé sus 19 hallazgos. Los del Excel de EnerAndes son los más claros: 120 duplicados exactos, 347 filas en MWh mezcladas con kWh en la hoja de 2024, cuatro formatos de fecha y municipios escritos de varias formas.
- Escribí 36 pruebas con pytest que no usan internet y pasan.

**Qué aprendí**
- Por qué en bronce no se limpia nada: así cada dato se puede rastrear hasta su origen y la limpieza queda como un paso versionado en plata.
- Por qué agregar en el servidor: el IDEAM tiene millones de observaciones y descargarlas crudas no es viable.
- Que un 400 no se debe reintentar (no se arregla repitiéndolo) y que un 5xx o un 429 sí.
- Que los datos reales tienen huecos: la temperatura del IDEAM no trae datos desde el 29 de julio de 2026, y eso solo se ve mirando el log o el perfilamiento.

**Bloqueos y cómo los resolví**
- El IDEAM es la fuente más lenta. Para no perder lo descargado si algo fallaba, guardé cada ventana en un cache. La ejecución completa terminó en 965 segundos con las 5 fuentes en orden.
- `Gene` por planta es la tabla más grande: 350.361 filas y unos 43 MB en Parquet. Por eso `data/bronze/` no se sube a GitHub y solo se versiona la muestra en CSV.

**Horas dedicadas:** unas 12.