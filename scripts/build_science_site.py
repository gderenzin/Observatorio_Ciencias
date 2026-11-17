#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
OBSERVATORIO DE CIENCIAS DE LA TIERRA, TELEDETECCIÓN Y CLIMA ESPACIAL
COMPILADOR DE SITIO ESTÁTICO ACADÉMICO (build_science_site.py)
==============================================================================
Genera la suite web pública cumpliendo con la Regla 14 de rigor editorial,
estética de revista científica indexada, tablas formales y metadatos Dublin Core
aptos para indexación en Google Scholar y Zenodo.
==============================================================================
"""

import os
import sys
import json
import re
import html
from datetime import datetime
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SITE_DIR = os.path.join(BASE_DIR, "site")
DESPACHOS_FILE = os.path.join(DATA_DIR, "despachos.yaml")
PUBLICADAS_FILE = os.path.join(DATA_DIR, "publicadas_ciencias.json")

def limpiar_html_texto(texto: str) -> str:
    """Elimina etiquetas HTML y caracteres extraños de los extractos."""
    if not texto:
        return ""
    limpio = re.sub(r"<[^>]+>", "", texto)
    limpio = html.unescape(limpio)
    return " ".join(limpio.split())

def formatear_fecha(iso_o_str: str) -> str:
    """Convierte cadenas de fecha a formato formal DD de Mes de AAAA."""
    meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    try:
        if "T" in iso_o_str:
            dt = datetime.fromisoformat(iso_o_str.replace("Z", "+00:00"))
            return f"{dt.day:02d} de {meses[dt.month - 1]} de {dt.year}"
        partes = iso_o_str.split("-")
        if len(partes) == 3:
            y, m, d = int(partes[0]), int(partes[1]), int(partes[2])
            return f"{d:02d} de {meses[m - 1]} de {y}"
    except Exception:
        pass
    return iso_o_str[:10]

def cargar_datos():
    despachos = []
    if os.path.exists(DESPACHOS_FILE):
        with open(DESPACHOS_FILE, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            despachos = data.get("despachos", [])

    noticias = []
    if os.path.exists(PUBLICADAS_FILE):
        with open(PUBLICADAS_FILE, "r", encoding="utf-8") as f:
            noticias = json.load(f)

    return despachos, noticias

def render_top_bar():
    return """
    <div class="top-institutional-bar">
      <div class="container">
        <div class="affiliation">
          <span>🏛️ Instituto Tecnológico Superior EuroAmericano</span>
          <span>•</span>
          <span>🌐 Nodo UNESCO GlobalCoast (PS-006-08)</span>
        </div>
        <div class="live-links">
          <a href="https://geo.euroamericano.edu.ec" target="_blank" rel="noopener">📡 Observatorio Litoral (GOES-19)</a>
          <a href="https://espacial.euroamericano.edu.ec" target="_blank" rel="noopener">☀️ Clima Espacial Ecuatorial</a>
        </div>
      </div>
    </div>
    """

def render_header(activo="inicio"):
    nav_inicio = 'class="active"' if activo == "inicio" else ""
    nav_despachos = 'class="active"' if activo == "despachos" else ""
    nav_observatorios = 'class="active"' if activo == "observatorios" else ""
    nav_archivo = 'class="active"' if activo == "archivo" else ""

    return f"""
    <header class="main-header">
      <div class="container">
        <div class="header-brand">
          <div class="pre-title">Portal de Ciencia Abierta & Difusión Satelital</div>
          <h1>Observatorio de Ciencias de la Tierra, Teledetección y Clima Espacial</h1>
          <p class="sub-desc">
            Plataforma académica y experimental dedicada a la telemetría satelital (GOES-19 GLM/ABI, Sentinel-2, Landsat),
            geofísica del litoral ecuatoriano, monitoreo agro-hidrológico y heliofísica en el Pacífico ecuatorial.
          </p>
        </div>
        <nav class="editorial-nav">
          <a href="index.html" {nav_inicio}>Inicio</a>
          <a href="#despachos-nodo" {nav_despachos}>Despachos Técnicos (Preprints)</a>
          <a href="observatorios.html" {nav_observatorios}>Observatorios en Producción</a>
          <a href="archivo.html" {nav_archivo}>Archivo Histórico</a>
        </nav>
      </div>
    </header>
    """

def render_footer():
    year = datetime.now().year
    return f"""
    <footer class="main-footer">
      <div class="container">
        <div class="footer-grid">
          <div class="footer-col">
            <h4>Observatorio Científico</h4>
            <p>
              Iniciativa de ciencia abierta orientada a la investigación en teledetección multiespectral,
              sistemas de alerta temprana de tormentas y radiación ionosférica para la cuenca baja del Guayas y el litoral.
            </p>
            <p><strong>Investigador Responsable:</strong><br>Prof. Ing. Feddor Gabriel Derenzin Martínez</p>
          </div>
          <div class="footer-col">
            <h4>Infraestructura Operativa</h4>
            <ul>
              <li><a href="https://geo.euroamericano.edu.ec" target="_blank">geo.euroamericano.edu.ec (GOES-19 / Mareógrafos)</a></li>
              <li><a href="https://espacial.euroamericano.edu.ec" target="_blank">espacial.euroamericano.edu.ec (Clima Espacial / SWPC)</a></li>
              <li><a href="https://zenodo.org" target="_blank">Zenodo Open Science Repository</a></li>
              <li><a href="https://github.com/gderenzin" target="_blank">Repositorio en GitHub</a></li>
            </ul>
          </div>
          <div class="footer-col">
            <h4>Adscripción & Vínculo Internacional</h4>
            <p>
              • Instituto Tecnológico Superior EuroAmericano<br>
              • Carrera de Redes y Telecomunicaciones<br>
              • Nodo Analítico UNESCO GlobalCoast PS-006-08<br>
              • Colaboración Doctoral NMBU (Noruega)
            </p>
          </div>
        </div>
        <div class="footer-bottom">
          <div>© {year} Observatorio de Ciencias de la Tierra y el Espacio. Licencia Creative Commons Atribución 4.0 Internacional (CC BY 4.0).</div>
          <div>Cero publicidad • Código Abierto • rigor epistemológico garantizado</div>
        </div>
      </div>
    </footer>
    """

def compilar_index(despachos, noticias):
    ruta_index = os.path.join(SITE_DIR, "index.html")

    # Render dock observatorios
    dock_html = """
    <div class="observatories-dock">
      <div class="dock-card">
        <div class="dock-header">
          <h3>Observatorio Meteorológico del Litoral</h3>
          <span class="live-pill">● TELEMETRÍA EN VIVO</span>
        </div>
        <p>Sensor GLM de descargas eléctricas y canales infrarrojos ABI de GOES-19, red mareográfica UNESCO/IOC y boletín sinóptico bilingüe.</p>
        <a class="dock-meta" href="https://geo.euroamericano.edu.ec" target="_blank">Acceder a geo.euroamericano.edu.ec →</a>
      </div>
      <div class="dock-card">
        <div class="dock-header">
          <h3>Observatorio de Clima Espacial Académico</h3>
          <span class="live-pill">● CICLO SOLAR 25</span>
        </div>
        <p>Monitoreo en tiempo real de rayos X solares, índice geomagnético planetario Kp, alertas SWPC y perturbación RTK/GNSS para Ecuador.</p>
        <a class="dock-meta" href="https://espacial.euroamericano.edu.ec" target="_blank">Acceder a espacial.euroamericano.edu.ec →</a>
      </div>
    </div>
    """

    # Render despachos
    despachos_cards = []
    for d in despachos:
        palabras_html = "".join([f'<span class="keyword-tag">{kw}</span>' for kw in d.get("palabras_clave", [])])
        doi_val = d.get("doi", "")
        doi_link = f'https://doi.org/{doi_val}' if doi_val else d.get("zenodo_url", "#")
        url_detalle = f"despachos/{d.get('slug')}.html"

        card = f"""
        <article class="dispatch-card">
          <div class="dispatch-header">
            <span class="dispatch-id-badge">{d.get('id')}</span>
            <span class="dispatch-date">{formatear_fecha(d.get('fecha'))}</span>
          </div>
          <h2><a href="{url_detalle}">{d.get('titulo')}</a></h2>
          <div class="dispatch-author-line">
            Por <strong>{d.get('autor')}</strong> • {d.get('filiacion')}
          </div>
          <p class="dispatch-abstract">{d.get('resumen')}</p>
          <div class="dispatch-footer">
            <div class="dispatch-keywords">{palabras_html}</div>
            <a class="dispatch-doi-link" href="{doi_link}" target="_blank">DOI: {doi_val} ↗</a>
          </div>
        </article>
        """
        despachos_cards.append(card)

    despachos_html = "\n".join(despachos_cards)

    # Render agencias espaciales (últimas 9 noticias)
    agencias_cards = []
    for n in noticias[:9]:
        resumen_limpio = limpiar_html_texto(n.get("resumen", ""))[:220]
        if len(limpiar_html_texto(n.get("resumen", ""))) > 220:
            resumen_limpio += "..."
        card = f"""
        <article class="agency-card">
          <div>
            <div class="agency-header">
              <span class="agency-source-pill">{n.get('fuente')}</span>
            </div>
            <h3><a href="{n.get('enlace')}" target="_blank" rel="noopener">{n.get('titulo')}</a></h3>
            <p class="agency-summary">{resumen_limpio}</p>
          </div>
          <div class="agency-footer">
            <span>{formatear_fecha(n.get('fecha_publicacion', ''))}</span>
            <span>Dominio: {n.get('dominio')}</span>
          </div>
        </article>
        """
        agencias_cards.append(card)

    if not agencias_cards:
        agencias_html = """
        <div style="grid-column: 1 / -1; padding: 24px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 4px; text-align: center; color: #64748b;">
          El pipeline diario de GitHub Actions actualizará las fuentes de ESA, NASA, NOAA y Copernicus en su próxima ejecución programada.
        </div>
        """
    else:
        agencias_html = "\n".join(agencias_cards)

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Observatorio de Ciencias de la Tierra, Teledetección y Clima Espacial</title>
  <meta name="description" content="Portal de divulgación científica, telemetría satelital en vivo, reportes agro-hidrológicos y monitoreo de clima espacial para el Ecuador y el Pacífico Sudeste.">
  <link rel="stylesheet" href="assets/css/science_editorial.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220%22><text y=%2222%22 font-size=%2222%22>🛰️</text></svg>">
</head>
<body>
  {render_top_bar()}
  {render_header("inicio")}

  <main class="content-area">
    <div class="container">
      {dock_html}

      <section id="despachos-nodo" style="margin-top: 36px;">
        <div class="section-title-wrap">
          <h2 class="section-title">Despachos Técnicos & Preprints de Investigación</h2>
          <span class="section-meta-count">{len(despachos)} publicaciones registradas</span>
        </div>
        <div class="dispatches-grid">
          {despachos_html}
        </div>
      </section>

      <section id="agencias-internacionales" style="margin-top: 48px;">
        <div class="section-title-wrap">
          <h2 class="section-title">Novedades de Agencias Espaciales & Consorcios Científicos</h2>
          <span class="section-meta-count">Fuentes: ESA • NASA • NOAA SWPC • USGS Landsat • WMO</span>
        </div>
        <div class="agency-feed-list">
          {agencias_html}
        </div>
      </section>
    </div>
  </main>

  {render_footer()}
</body>
</html>
"""
    with open(ruta_index, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generado index: {ruta_index}")

def compilar_despachos_individuales(despachos):
    despachos_dir = os.path.join(SITE_DIR, "despachos")
    os.makedirs(despachos_dir, exist_ok=True)

    for d in despachos:
        slug = d.get("slug")
        ruta_archivo = os.path.join(despachos_dir, f"{slug}.html")
        palabras_html = "".join([f'<span class="keyword-tag">{kw}</span>' for kw in d.get("palabras_clave", [])])
        doi_val = d.get("doi", "")
        doi_url = f"https://doi.org/{doi_val}" if doi_val else "#"

        html_item = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{d.get('titulo')} | Observatorio de Ciencias</title>
  
  <!-- Metadatos Académicos Dublin Core & Google Scholar -->
  <meta name="citation_title" content="{d.get('titulo')}">
  <meta name="citation_author" content="{d.get('autor')}">
  <meta name="citation_publication_date" content="{d.get('fecha')}">
  <meta name="citation_doi" content="{doi_val}">
  <meta name="citation_technical_report_institution" content="Instituto Tecnológico Superior EuroAmericano">

  <link rel="stylesheet" href="../assets/css/science_editorial.css">
</head>
<body>
  {render_top_bar()}
  <header class="main-header">
    <div class="container">
      <div class="header-brand">
        <div class="pre-title"><a href="../index.html" style="color: inherit; text-decoration: none;">← Volver al Observatorio</a></div>
        <h1>{d.get('titulo')}</h1>
        <p class="sub-desc" style="font-style: italic;">{d.get('titulo_en', '')}</p>
      </div>
    </div>
  </header>

  <main class="content-area">
    <div class="container" style="max-width: 860px;">
      <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 4px; padding: 32px; margin-bottom: 40px;">
        <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #e2e8f0; padding-bottom: 14px; margin-bottom: 20px; font-family: var(--font-mono); font-size: 12px; color: #64748b;">
          <span>Identificador: <strong>{d.get('id')}</strong></span>
          <span>Fecha de radicación: {formatear_fecha(d.get('fecha'))}</span>
        </div>

        <div style="margin-bottom: 24px; font-size: 13px; line-height: 1.6;">
          <p><strong>Investigador Principal:</strong> {d.get('autor')}</p>
          <p><strong>Filiación Institucional:</strong> {d.get('filiacion')}</p>
          <p><strong>Contacto Correspondiente:</strong> <a href="mailto:{d.get('contacto')}" style="color: #0369a1;">{d.get('contacto')}</a></p>
          <p><strong>DOI Permanente:</strong> <a href="{doi_url}" target="_blank" style="color: #0369a1; font-family: var(--font-mono);">{doi_val}</a></p>
        </div>

        <h3 style="font-family: var(--font-serif); font-size: 16px; margin: 24px 0 10px 0; border-bottom: 2px solid #0f172a; padding-bottom: 4px;">Resumen Estructurado (Abstract)</h3>
        <p style="text-align: justify; line-height: 1.7; color: #334155; margin-bottom: 20px;">
          {d.get('resumen')}
        </p>

        <h3 style="font-family: var(--font-serif); font-size: 16px; margin: 24px 0 10px 0; border-bottom: 2px solid #0f172a; padding-bottom: 4px;">Palabras Clave (Keywords)</h3>
        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 28px;">
          {palabras_html}
        </div>

        <h3 style="font-family: var(--font-serif); font-size: 16px; margin: 24px 0 10px 0; border-bottom: 2px solid #0f172a; padding-bottom: 4px;">Plataforma Operativa Vinculada</h3>
        <p style="text-align: justify; line-height: 1.7; color: #334155;">
          Este despacho técnico se apoya en los datos recolectados y procesados en vivo por la infraestructura del 
          <strong>{d.get('activo_relacionado')}</strong>. Puede consultar las capas espectrales o la telemetría satelital directamente en el portal oficial:
        </p>
        <p style="margin-top: 10px;">
          <a href="{d.get('activo_url')}" target="_blank" style="display: inline-block; background: #0369a1; color: #ffffff; text-decoration: none; padding: 8px 16px; border-radius: 2px; font-family: var(--font-mono); font-size: 12px;">Acceder al Portal del Observatorio ↗</a>
        </p>

        <h3 style="font-family: var(--font-serif); font-size: 16px; margin: 32px 0 10px 0; border-bottom: 2px solid #0f172a; padding-bottom: 4px;">Cómo Citar este Despacho (APA 7ma Edición)</h3>
        <div style="background: #f8fafc; border: 1px solid #cbd5e1; padding: 14px; font-size: 12px; line-height: 1.6; font-family: var(--font-mono); color: #334155;">
          Derenzin Martínez, F. G. ({d.get('fecha')[:4]}). <em>{d.get('titulo')}</em> (Technical Dispatch Nro. {d.get('id')}). Observatorio de Ciencias de la Tierra y Clima Espacial, Instituto Tecnológico Superior EuroAmericano & Nodo UNESCO GlobalCoast. https://doi.org/{doi_val}
        </div>
      </div>
    </div>
  </main>

  {render_footer()}
</body>
</html>
"""
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write(html_item)
    print(f"Compilados {len(despachos)} despachos individuales en {despachos_dir}")

def compilar_observatorios_page():
    ruta = os.path.join(SITE_DIR, "observatorios.html")
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Infraestructura Operativa de Observatorios | Observatorio de Ciencias</title>
  <link rel="stylesheet" href="assets/css/science_editorial.css">
</head>
<body>
  {render_top_bar()}
  {render_header("observatorios")}

  <main class="content-area">
    <div class="container" style="max-width: 960px;">
      <div class="section-title-wrap">
        <h2 class="section-title">Infraestructura y Servidores en Producción</h2>
      </div>

      <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 4px; padding: 28px; margin-bottom: 30px;">
        <h3 style="font-family: var(--font-serif); font-size: 20px; color: #0f172a; margin-bottom: 8px;">1. Observatorio Meteorológico del Litoral (geo.euroamericano.edu.ec)</h3>
        <p style="text-align: justify; line-height: 1.7; color: #334155; margin-bottom: 14px;">
          Plataforma de vigilancia sinóptica marina y atmosférica alojada en servidor Debian 13 institucional (puerto 8000, Nginx con terminación SSL Let's Encrypt). 
          Integra telemetría directa de destellos convectivos del sensor GLM de GOES-19, temperatura de brillo Planck en la banda infrarroja limpia ABI Banda 13 (10.3 μm), 
          y nivel del mar en tiempo real de los mareógrafos de La Libertad y Esmeraldas bajo la red UNESCO/IOC Sea Level Station Monitoring Facility.
        </p>
        <pre class="ascii-diagram">
+--------------------+        +---------------------+        +----------------------+
| NOAA GOES-19 GLM   | -----> | Ingestor Python     | -----> | Servidor Debian 13   |
| (Destellos/Rayos)  |        | netCDF4 / GDAL      |        | Nginx :8000 (HTTPS)  |
+--------------------+        +---------------------+        +----------------------+
          |                                                             |
+--------------------+                                                  v
| UNESCO/IOC Mar     | -------------------------------------> [ geo.euroamericano ]
+--------------------+
        </pre>
        <p><a href="https://geo.euroamericano.edu.ec" target="_blank" style="color: #0369a1; font-weight: 600;">Abrir Observatorio Litoral (geo.euroamericano.edu.ec) →</a></p>
      </div>

      <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 4px; padding: 28px; margin-bottom: 30px;">
        <h3 style="font-family: var(--font-serif); font-size: 20px; color: #0f172a; margin-bottom: 8px;">2. Observatorio de Clima Espacial Académico (espacial.euroamericano.edu.ec)</h3>
        <p style="text-align: justify; line-height: 1.7; color: #334155; margin-bottom: 14px;">
          Módulo de monitoreo heliofísico e ionosférico (puerto 8001, servicio systemd `espacial.service`). 
          Monitorea los flujos de rayos X en tiempo real del sensor XRS (satélites GOES-16 y GOES-18), las alertas operativas del Space Weather Prediction Center (NOAA SWPC), 
          y el índice planetario Kp para anticipar perturbaciones en enlaces de telecomunicaciones en alta frecuencia (HF) y errores de multicamino/centelleo en receptores GNSS/RTK agrícolas y marítimos.
        </p>
        <pre class="ascii-diagram">
+--------------------+        +---------------------+        +----------------------+
| NOAA SWPC JSON/XML | -----> | Ingestor Espacial   | -----> | Servicio Systemd     |
| (Rayos X / Kp / CME)|       | Python 3 / FastAPI  |        | Nginx :8001 (HTTPS)  |
+--------------------+        +---------------------+        +----------------------+
                                                                        |
                                                                        v
                                                             [ espacial.euroamericano ]
        </pre>
        <p><a href="https://espacial.euroamericano.edu.ec" target="_blank" style="color: #0369a1; font-weight: 600;">Abrir Observatorio Clima Espacial (espacial.euroamericano.edu.ec) →</a></p>
      </div>
    </div>
  </main>

  {render_footer()}
</body>
</html>
"""
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generado observatorios.html: {ruta}")

def compilar_archivo_page(despachos, noticias):
    ruta = os.path.join(SITE_DIR, "archivo.html")

    filas_despachos = []
    for d in despachos:
        filas_despachos.append(f"""
        <tr>
          <td><code>{d.get('id')}</code></td>
          <td>{formatear_fecha(d.get('fecha'))}</td>
          <td><a href="despachos/{d.get('slug')}.html" style="color: #0369a1; font-weight: 500;">{d.get('titulo')}</a></td>
          <td>{d.get('categoria')}</td>
          <td><code>{d.get('doi')}</code></td>
        </tr>
        """)

    filas_noticias = []
    for n in noticias:
        filas_noticias.append(f"""
        <tr>
          <td>{formatear_fecha(n.get('fecha_publicacion', ''))}</td>
          <td><span class="agency-source-pill">{n.get('fuente')}</span></td>
          <td><a href="{n.get('enlace')}" target="_blank" rel="noopener" style="color: #0f172a;">{n.get('titulo')}</a></td>
          <td><code>{n.get('dominio')}</code></td>
        </tr>
        """)

    if not filas_noticias:
        filas_noticias.append("<tr><td colspan='4' style='text-align: center; color: #64748b;'>Pendiente de primera ingesta en GitHub Actions</td></tr>")

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Archivo Histórico de Publicaciones | Observatorio de Ciencias</title>
  <link rel="stylesheet" href="assets/css/science_editorial.css">
</head>
<body>
  {render_top_bar()}
  {render_header("archivo")}

  <main class="content-area">
    <div class="container">
      <div class="section-title-wrap">
        <h2 class="section-title">Catálogo Completo de Despachos Técnicos</h2>
      </div>
      <table class="formal-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Fecha</th>
            <th>Título del Despacho</th>
            <th>Área Temática</th>
            <th>DOI Oficial</th>
          </tr>
        </thead>
        <tbody>
          {"".join(filas_despachos)}
        </tbody>
      </table>

      <div class="section-title-wrap" style="margin-top: 48px;">
        <h2 class="section-title">Registro Histórico de Novedades de Agencias Espaciales</h2>
      </div>
      <table class="formal-table">
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Fuente</th>
            <th>Título del Artículo</th>
            <th>Dominio Verificado</th>
          </tr>
        </thead>
        <tbody>
          {"".join(filas_noticias)}
        </tbody>
      </table>
    </div>
  </main>

  {render_footer()}
</body>
</html>
"""
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generado archivo.html: {ruta}")

def main():
    print("Iniciando compilación del sitio estático científico...")
    despachos, noticias = cargar_datos()
    compilar_index(despachos, noticias)
    compilar_despachos_individuales(despachos)
    compilar_observatorios_page()
    compilar_archivo_page(despachos, noticias)

    # robots.txt
    with open(os.path.join(SITE_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n")

    print("Compilación completada exitosamente.")

if __name__ == "__main__":
    main()
