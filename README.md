# Observatorio de Ciencias de la Tierra, Teledetección y Clima Espacial
### Earth Observation, Remote Sensing and Space Weather Dispatch Center

Plataforma académica y de ciencia abierta (*Open Science*) para el monitoreo satelital continuo, la teledetección multiespectral agrícola e hidrológica, y la vigilancia heliofísica en el litoral ecuatoriano y el Pacífico Sudeste.

---

## 1. Misión Epistemológica & Afiliación Académica

El observatorio opera como un nodo de investigación y divulgación tecnológica de acceso abierto, vinculado formalmente a:
- **Instituto Tecnológico Superior EuroAmericano** (Carrera de Redes y Telecomunicaciones).
- **Nodo Analítico UNESCO GlobalCoast (`PS-006-08`)** (Monitoreo costero y oceánico del Golfo de Guayaquil).
- **Colaboración Académica Doctoral con la Norwegian University of Life Sciences (NMBU)**, Departamento de Geomática (Líneas de super-resolución espectral, deep learning en series temporales de Sentinel-2 y procesamiento Big Data en software de código abierto).

**Investigador Principal:**  
**Prof. Ing. Feddor Gabriel Derenzin Martínez**  
*Director de Carrera / Investigador Principal*  
Correo: `fderenzin@euroamericano.edu.ec`

---

## 2. Infraestructura Operativa de Observatorios

Este repositorio centraliza y documenta los datos recolectados por dos infraestructuras en producción permanente en servidor Linux Debian 13:

1. **Observatorio Meteorológico del Litoral (`https://geo.euroamericano.edu.ec`):**
   - Telemetría en tiempo real de destellos de rayos y energía convectiva con el sensor **GOES-19 GLM** (Geostationary Lightning Mapper).
   - Infrarrojo térmico y temperatura de brillo con el sensor **GOES-19 ABI** Banda 13 (10.3 μm).
   - Red mareográfica en vivo bajo el protocolo UNESCO/IOC Sea Level Station Monitoring Facility (estaciones La Libertad y Esmeraldas).
   - Suite bilingüe completa (`ES / EN`).

2. **Observatorio de Clima Espacial Académico (`https://espacial.euroamericano.edu.ec`):**
   - Monitoreo en vivo de flujos de rayos X solares (satélites GOES Primary) y seguimiento del Ciclo Solar 25.
   - Índice geomagnético planetario $Kp$ y alertas del Space Weather Prediction Center (NOAA SWPC).
   - Evaluación continua del riesgo de degradación ionosférica en enlaces de telecomunicaciones en alta frecuencia (HF) y receptores de precisión centimétrica **GNSS/RTK**.

---

## 3. Despachos Técnicos & Preprints Radicados

Los despachos de investigación corresponden a reportes técnicos con metodología IMRyD y reproducibilidad computacional:

| Código | Título del Despacho | Enfoque Metodológico | Estado DOI |
|---|---|---|---|
| `DISP-2026-001` | Diagnóstico Biofísico y Monitoreo de Estrés Hídrico en Maíz Duro (*Zea mays L.*) en Montalvo | Sentinel-2 L2A, NDVI vs NDMI en floración R1 | `10.5281/zenodo.14208001` |
| `DISP-2026-002` | Fenomenología de la Saturación del Dosel: Evaluación NDVI vs NDRE en Arrozales de Babahoyo | Sentinel-2C L2A (805 px), banda B05 RedEdge | `10.5281/zenodo.14208002` |
| `DISP-2026-003` | Arquitectura Computacional de Ingesta Continua y Telemetría de Tormentas (GOES-19 GLM) | Pipeline netCDF4, ABI B13, Golfo de Guayaquil | `10.5281/zenodo.14208003` |
| `DISP-2026-004` | Clima Espacial Ecuatorial y Riesgo de Degradación GNSS/RTK durante el Máximo Solar 25 | Rayos X GOES, Kp, centelleo ionosférico | `10.5281/zenodo.14208004` |

---

## 4. Fuentes de Ingesta Automatizada (Lista Blanca Oficial)

Siguiendo el principio de **cero alucinaciones**, el pipeline automatizado consulta exclusivamente canales RSS institucionales verificados en `feeds_ciencias.yaml`:
- **ESA Earth Observation:** Misiones Sentinel y Earth Explorers de la Agencia Espacial Europea.
- **NASA Earth Observatory:** Cobertura de balance hídrico, sequías e incendios.
- **NOAA SWPC:** Alertas geomagnéticas y heliofísica operativa.
- **USGS Landsat Program:** Reflectancia de superficie y calibración radiométrica de Landsat 8/9.
- **WMO (OMM):** Vigilancia climática mundial y dinámica oceánica ENSO.
- **Copernicus EU:** Servicios terrestres, marinos y atmosféricos.

---

## 5. Automatización & Despliegue CI/CD

El portal es 100% estático y se compila de manera autónoma en la nube de GitHub:
- **Flujo:** `.github/workflows/ciencia_diario.yml`
- **Cadencia:** Todos los días a las `11:00 UTC` (`06:00 AM` hora continental de Ecuador).
- **Proceso:** `fetch_science.py` descarga y deduplica las novedades $\rightarrow$ `build_science_site.py` compila el catálogo estático en `site/` $\rightarrow$ Commits automáticos a la rama principal.

---

## 6. Configuración de Dominio Personalizado

Para publicar este observatorio bajo un subdominio institucional:
1. Cree un registro `CNAME` en su DNS:  
   `ciencias.euroamericano.edu.ec` $\rightarrow$ `<usuario>.github.io`
2. En GitHub: `Settings` $\rightarrow$ `Pages` $\rightarrow$ Seleccionar carpeta `/site` en la rama `main`, e ingresar el Custom domain.
