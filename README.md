# Observatorio de Ciencias de la Tierra, Teledetección y Clima Espacial
### Earth Observation, Remote Sensing and Space Weather Dispatch Center

Plataforma académica y de ciencia abierta (*Open Science*) para el monitoreo satelital continuo, la teledetección multiespectral agrícola e hidrológica, y la vigilancia heliofísica en el litoral ecuatoriano y el Pacífico Sudeste.

---

## 1. Misión Epistemológica & Afiliación Académica

El observatorio opera como una plataforma privada de análisis técnico y divulgación científica independiente de DERENZIN S.A.S., enfocada en el procesamiento de datos satelitales abiertos (Open Data) de agencias internacionales (NOAA, NASA y Programa Copernicus).

**Investigador Responsable:**  
**Prof. Ing. Feddor Gabriel Derenzin Martínez**  
*Investigador Principal, DERENZIN S.A.S. / Director de Carrera, Instituto Tecnológico Superior EuroAmericano*  
Correo: `fderenzin@euroamericano.edu.ec`

---

## 2. Protocolo de Integridad Epistémica (Peters & Chin-Yee, 2025)

Este repositorio implementa de forma pionera las recomendaciones del estudio publicado por **Peters & Chin-Yee (2025)** en *Royal Society Open Science* (DOI: [10.1098/rsos.241776](https://doi.org/10.1098/rsos.241776)), el cual demostró que los modelos de lenguaje (LLMs) tienen **casi cinco veces más probabilidad de ampliar indebidamente el alcance de las conclusiones** que los divulgadores humanos, omitiendo los detalles que limitan la validez de los resultados.

El error típico no es inventar datos, sino **exagerar el alcance**: presentar un hallazgo de una sola microcuenca como "las lluvias en Sudamérica", o transformar una correlación observacional en una relación de causa-efecto sin prueba mecanicista.

### Reglas Inquebrantables del Pipeline:
1. **Cero Publicación Automática (*Human-in-the-Loop*):** El robot de ingesta (`fetch_science.py`) **NUNCA** publica directamente. Solo deposita candidatos en `data/borradores_pendientes.yaml`. Únicamente tras la revisión y aprobación manual del **Prof. Ing. Feddor Derenzin** pasan al catálogo público.
2. **Extracción Obligatoria de Condiciones de Borde:** Todo resumen debe aislar e imprimir un bloque visible con:
   - **Zona geográfica exacta** (área, cuenca o coordenadas; prohibido extrapolar a continentes).
   - **Período temporal evaluado** (meses/años; prohibido extrapolar a épocas no medidas).
   - **Sensores, calibración y tamaño de muestra** (satélites, bandas y sensores in-situ).
   - **Nivel epistémico** (declaración explícita de correlación vs. causalidad).
3. **Fuentes con DOI y Clasificación de Preprints:** Solo se aceptan estudios con DOI verificable. Los preprints (arXiv, EarthArXiv) se marcan con la etiqueta obligatoria:  
   `[PREPRINT - NO REVISADO POR PARES]`.
4. **Declaración Explícita de Transparencia:** Cada nota enlaza al paper original e indica textualmente:  
   *«Resumen técnico asistido por IA, revisado y validado por F. Derenzin»*.
5. **Cadencia Sobria (3 a 5 notas por semana):** Se limita el volumen para garantizar que la revisión humana sea realista, minuciosa y rigurosa.
6. **El Boletín Propio (Datos del Observatorio):** Exento de este sesgo al tratarse de mediciones directas in-situ y telemetría propia (GOES-19, Sentinel-2), auditando minuciosamente las cifras antes de su emisión.

---

## 3. Uso del Aprobador Editorial Humano (CLI)

Para gestionar la cola de literatura externa pendiente:

```bash
# 1. Listar los borradores pendientes de revisión
python scripts/aprobar_borrador.py --listar

# 2. Aprobar un borrador tras validar su resumen y limitaciones
python scripts/aprobar_borrador.py --aprobar LIT-2026-001
```

Al aprobar un borrador, el script lo transfiere a `data/articulos_aprobados.yaml` y recompila inmediatamente la suite web pública.

---

## 4. Infraestructura Operativa de Observatorios

Este repositorio centraliza y documenta los datos de dos plataformas en producción en servidor Linux Debian 13:

1. **Observatorio Meteorológico del Litoral (`https://geo.euroamericano.edu.ec`):**
   - Telemetría de destellos y energía convectiva con el sensor **GOES-19 GLM** (Geostationary Lightning Mapper).
   - Temperatura de brillo con **GOES-19 ABI** Banda 13 (10.3 μm).
   - Estaciones mareográficas públicas costeras (La Libertad y Esmeraldas).
   - Suite bilingüe completa (`ES / EN`).

2. **Observatorio de Clima Espacial Académico (`https://espacial.euroamericano.edu.ec`):**
   - Monitoreo de rayos X solares (satélites GOES Primary) y seguimiento del Ciclo Solar 25.
   - Índice geomagnético $Kp$ y alertas del Space Weather Prediction Center (NOAA SWPC).
   - Evaluación del riesgo de centelleo y degradación en enlaces HF y receptores centimétricos **GNSS/RTK**.

---

## 5. Despachos Técnicos (En Proceso de Auditoría y Revisión del Autor)

Los borradores y preprints técnicos se encuentran en la cola interna `data/borradores_pendientes.yaml`. Ningún estudio se publica de forma automática o no verificada; cada análisis requiere la previa validación empírica, calibración y aprobación manual del **Prof. Ing. Feddor Derenzin**.

| Código | Título del Despacho | Metodología | Estado DOI |
|---|---|---|---|
| `DISP-2026-001` | Diagnóstico Biofísico y Monitoreo de Estrés Hídrico en Maíz Duro (*Zea mays L.*) en Montalvo | Sentinel-2 L2A, NDVI vs NDMI en floración R1 | `10.5281/zenodo.14208001` |
| `DISP-2026-002` | Fenomenología de la Saturación del Dosel: Evaluación NDVI vs NDRE en Arrozales de Babahoyo | Sentinel-2C L2A (805 px), banda B05 RedEdge | `10.5281/zenodo.14208002` |
| `DISP-2026-003` | Arquitectura Computacional de Ingesta Continua y Telemetría de Tormentas (GOES-19 GLM) | Pipeline netCDF4, ABI B13, Golfo de Guayaquil | `10.5281/zenodo.14208003` |
| `DISP-2026-004` | Clima Espacial Ecuatorial y Riesgo de Degradación GNSS/RTK durante el Máximo Solar 25 | Rayos X GOES, Kp, centelleo ionosférico | `10.5281/zenodo.14208004` |
