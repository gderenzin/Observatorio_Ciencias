#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
OBSERVATORIO DE CIENCIAS DE LA TIERRA, TELEDETECCIÓN Y CLIMA ESPACIAL
COMPILADOR DE PORTADA PERIODÍSTICA CIENTÍFICA (PLANTILLA EURONEWS HIGH-IMPACT)
==============================================================================
Estilo: Periódico digital corporativo y científico de alto impacto visual,
con diseño idéntico a noticias.derenzin.com, tarjetas hero destacadas,
grid de artículos con imágenes satelitales, sidebar sticky con telemetría en vivo
y cumplimiento irrestricto del Protocolo Peters & Chin-Yee (2025).
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
APROBADOS_FILE = os.path.join(DATA_DIR, "articulos_aprobados.yaml")

def formatear_fecha(iso_o_str: str) -> str:
    meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    try:
        if not iso_o_str:
            return ""
        if "T" in str(iso_o_str):
            dt = datetime.fromisoformat(str(iso_o_str).replace("Z", "+00:00"))
            return f"{dt.day:02d} de {meses[dt.month - 1]} de {dt.year}"
        partes = str(iso_o_str).split("-")
        if len(partes) == 3:
            y, m, d = int(partes[0]), int(partes[1]), int(partes[2])
            return f"{d:02d} de {meses[m - 1]} de {y}"
    except Exception:
        pass
    return str(iso_o_str)[:10]

def cargar_datos():
    despachos = []
    if os.path.exists(DESPACHOS_FILE):
        with open(DESPACHOS_FILE, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            despachos = data.get("despachos", [])

    articulos = []
    if os.path.exists(APROBADOS_FILE):
        with open(APROBADOS_FILE, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            articulos = data.get("articulos", [])

    return despachos, articulos

def render_cabecera(activo="inicio"):
    nav_inicio = 'class="activo"' if activo == "inicio" else ""
    nav_archivo = 'class="activo"' if activo == "archivo" else ""

    return f"""
  <header class="cabecera">
    <div class="cabecera-contenido">
      <a href="/index.html" class="marca-enlace">
        <img src="/assets/logo-derenzin.png" alt="DERENZIN" class="marca-logo">
        <div class="marca-texto">
          <span class="marca-titulo">Observatorio de Ciencias</span>
          <span class="marca-byline">Teledetección, Geociencias & Clima Espacial • <strong>DERENZIN S.A.S.</strong></span>
        </div>
      </a>
      <nav class="nav">
        <a href="/index.html" {nav_inicio}>Portada</a>
        <a href="/archivo.html" {nav_archivo}>Archivo</a>
        <a href="https://geo.euroamericano.edu.ec" target="_blank" rel="noopener noreferrer">Observatorio Litoral ↗</a>
        <a href="https://espacial.euroamericano.edu.ec" target="_blank" rel="noopener noreferrer">Clima Espacial ↗</a>
        <a href="https://noticias.derenzin.com" target="_blank" rel="noopener noreferrer">Ciberseguridad ↗</a>
      </nav>
    </div>
  </header>
  <script src="/assets/cabecera-sticky.js" defer></script>
    """

def render_pie():
    year = datetime.now().year
    return f"""
  <footer class="pie">
    <div class="pie-contenido">
      <div class="pie-marca">
        <a href="https://derenzin.com" target="_blank" rel="noopener noreferrer" class="pie-marca-enlace">
          <img src="/assets/logo-derenzin.png" alt="DERENZIN" class="pie-logo">
          <span class="pie-marca-nombre">DERENZIN S.A.S.</span>
        </a>
        <p class="pie-tagline">Centro de Teledetección y Heliofísica de DERENZIN S.A.S. — <a href="https://derenzin.com" target="_blank" rel="noopener noreferrer">derenzin.com ↗</a></p>
      </div>
      <div class="pie-legal">
        <p><strong>Estándar Epistémico Peters & Chin-Yee (2025):</strong> Este portal no publica resúmenes automáticos. Toda literatura externa delimita estrictamente su zona geográfica, período temporal y tamaño muestral con revisión humana del Prof. Ing. Feddor Derenzin.</p>
        <p class="pie-fuentes">Red Operativa: NOAA GOES-19 GLM / ABI, Constelación Copernicus Sentinel-1/2/3, NOAA SWPC, UNESCO/IOC Sea Level Network.</p>
        <p class="pie-recurso">Nodo Regional: <a href="https://ciencias.derenzin.com">UNESCO GlobalCoast (PS-006-08)</a> • Articulación con Instituto EuroAmericano & NMBU Noruega.</p>
        <p class="pie-copyright">© {year} DERENZIN S.A.S. — Prof. Ing. Feddor Gabriel Derenzin Martínez. Todos los derechos reservados.</p>
      </div>
    </div>
  </footer>
    """

def render_sidebar():
    return """
      <aside class="sidebar-noticia">
        <div class="sidebar-noticia-sticky">
          <!-- Widget 1: Telemetría en Vivo -->
          <section class="sidebar-bloque">
            <h2 class="sidebar-titulo">Observatorios en Vivo</h2>
            <div style="display: flex; flex-direction: column; gap: 12px; margin-top: 10px;">
              <div style="background: #ffffff; border: 1px solid var(--borde); border-radius: var(--radio); padding: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                  <strong style="font-size: 13px; color: var(--texto);">Observatorio Litoral</strong>
                  <span style="font-size: 10px; font-weight: 700; color: #15803d; background: #dcfce7; padding: 2px 6px; border-radius: 3px;">● EN VIVO</span>
                </div>
                <p style="font-size: 12px; color: var(--texto-tenue); margin: 0 0 8px 0; line-height: 1.45;">
                  Sensor GOES-19 GLM de rayos cada 20s, canales ABI infrarrojos y mareógrafos UNESCO/IOC.
                </p>
                <a href="https://geo.euroamericano.edu.ec" target="_blank" style="font-size: 12px; font-weight: 600; color: var(--marca-acento-oscuro); text-decoration: none;">Acceder a geo.euroamericano.edu.ec →</a>
              </div>

              <div style="background: #ffffff; border: 1px solid var(--borde); border-radius: var(--radio); padding: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                  <strong style="font-size: 13px; color: var(--texto);">Clima Espacial</strong>
                  <span style="font-size: 10px; font-weight: 700; color: #d97706; background: #fef3c7; padding: 2px 6px; border-radius: 3px;">● CICLO 25</span>
                </div>
                <p style="font-size: 12px; color: var(--texto-tenue); margin: 0 0 8px 0; line-height: 1.45;">
                  Flujos de rayos X solares GOES, índice Kp, perturbación RTK y centelleo en Ecuador.
                </p>
                <a href="https://espacial.euroamericano.edu.ec" target="_blank" style="font-size: 12px; font-weight: 600; color: var(--marca-acento-oscuro); text-decoration: none;">Acceder a espacial.euroamericano.edu.ec →</a>
              </div>
            </div>
          </section>

          <!-- Widget 2: Integridad Epistémica -->
          <section class="sidebar-bloque">
            <h2 class="sidebar-titulo">Protocolo Peters & Chin-Yee (2025)</h2>
            <p style="font-size: 12px; color: var(--texto-tenue); line-height: 1.5; margin: 8px 0;">
              <em>Royal Society Open Science</em> (DOI: 10.1098/rsos.241776).
              Los modelos de lenguaje tienden a multiplicar por 5 la probabilidad de exagerar conclusiones científicas.
            </p>
            <div style="background: #f8f9fa; border: 1px solid var(--borde); border-radius: var(--radio-chico); padding: 10px; font-size: 11px; line-height: 1.45; color: var(--texto);">
              ✓ Cero publicación automática.<br>
              ✓ Delimitación espacial y temporal.<br>
              ✓ Preprints rotulados sin par.<br>
              ✓ Revisión por F. Derenzin.
            </div>
          </section>

          <!-- Widget 3: Afiliación Científica -->
          <section class="sidebar-bloque">
            <h2 class="sidebar-titulo">Adscripción y Doctorado</h2>
            <p style="font-size: 12px; color: var(--texto-tenue); line-height: 1.5; margin: 8px 0;">
              • <strong>Nodo UNESCO GlobalCoast:</strong> Código internacional PS-006-08.<br>
              • <strong>Proyecto Doctoral NMBU:</strong> Dept. of Geomatics, Norwegian University of Life Sciences.<br>
              • <strong>EuroAmericano:</strong> Dirección de Investigación y Redes.
            </p>
          </section>
        </div>
      </aside>
    """

def compilar_portada(despachos, articulos):
    ruta_index = os.path.join(SITE_DIR, "index.html")
    fecha_hoy = datetime.now().strftime("%d de %B de %Y").replace("November", "noviembre").replace("December", "diciembre")

    # 1. Articulo Destacado (Hero)
    destacado = despachos[0] if despachos else None
    destacada_html = ""
    if destacado:
        destacada_html = f"""
    <article class="destacada {destacado.get('categoria_slug', 'cat-teledeteccion')}">
      <a class="destacada-imagen-enlace" href="/despachos/{destacado.get('slug')}.html">
        <figure class="noticia-imagen noticia-imagen--destacada">
          <span class="categoria-badge">{destacado.get('categoria')}</span>
          <img src="{destacado.get('imagen')}" alt="{destacado.get('titulo')}" loading="eager" fetchpriority="high">
          <figcaption>{destacado.get('imagen_pie', 'Telemetría Satelital')}</figcaption>
        </figure>
      </a>
      <div class="destacada-cuerpo">
        <span class="destacada-eyebrow">Despacho Principal del Observatorio</span>
        <span class="eyebrow-categoria">Código: {destacado.get('id')}</span>
        <h2 class="destacada-titulo"><a href="/despachos/{destacado.get('slug')}.html">{destacado.get('titulo')}</a></h2>
        <p class="destacada-resumen">{destacado.get('resumen')}</p>
        <div class="noticia-meta">
          <span class="fuente">Investigador: {destacado.get('autor')}</span>
          <span class="fecha">Radicado: {formatear_fecha(destacado.get('fecha'))}</span>
          <span class="fecha">DOI: {destacado.get('doi')}</span>
        </div>
        <a class="destacada-cta" href="/despachos/{destacado.get('slug')}.html">Leer el despacho técnico completo →</a>
      </div>
    </article>
        """

    # 2. Grid de Despachos del Observatorio (Resto de despachos)
    despachos_cards = []
    for d in despachos[1:]:
        card = f"""
      <article class="tarjeta {d.get('categoria_slug', 'cat-teledeteccion')}">
        <a class="tarjeta-imagen-enlace" href="/despachos/{d.get('slug')}.html">
          <figure class="noticia-imagen">
            <span class="categoria-badge">{d.get('categoria')}</span>
            <img src="{d.get('imagen')}" alt="{d.get('titulo')}" loading="lazy">
            <figcaption>{d.get('imagen_pie', 'Telemetría')}</figcaption>
          </figure>
        </a>
        <div class="tarjeta-cuerpo">
          <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
            <span class="eyebrow-categoria">{d.get('id')}</span>
            <span class="badge-despacho-propio">BOLETÍN PROPIO</span>
          </div>
          <h3 class="tarjeta-titulo"><a href="/despachos/{d.get('slug')}.html">{d.get('titulo')}</a></h3>
          <p class="tarjeta-resumen">{d.get('resumen')}</p>
          <div class="noticia-meta">
            <span class="fuente">Autor: {d.get('autor')}</span>
            <span class="fecha">DOI: {d.get('doi')}</span>
          </div>
        </div>
      </article>
        """
        despachos_cards.append(card)

    despachos_grid_html = "\n".join(despachos_cards)

    # 3. Grid de Literatura Externa Validada
    articulos_cards = []
    for art in articulos:
        slug = art.get("slug", art.get("id"))
        es_preprint = art.get("es_preprint", False)
        badge_peer = '<span class="badge-preprint-alerta">PREPRINT - NO REVISADO</span>' if es_preprint else '<span class="badge-peer-reviewed">REVISADO POR PARES</span>'
        alcance = art.get("alcance_y_limitaciones", {})

        card = f"""
      <article class="tarjeta {art.get('categoria_slug', 'cat-hidrologia')}">
        <a class="tarjeta-imagen-enlace" href="/articulos/{slug}.html">
          <figure class="noticia-imagen">
            <span class="categoria-badge">{art.get('categoria')}</span>
            <img src="{art.get('imagen')}" alt="{art.get('titulo')}" loading="lazy">
            <figcaption>{art.get('imagen_pie', 'Literatura')}</figcaption>
          </figure>
        </a>
        <div class="tarjeta-cuerpo">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span class="eyebrow-categoria">{art.get('id')}</span>
            {badge_peer}
          </div>
          <h3 class="tarjeta-titulo"><a href="/articulos/{slug}.html">{art.get('titulo')}</a></h3>
          <p class="tarjeta-resumen">{art.get('resumen_fiel', '')}</p>
          
          <div class="bloque-limitaciones">
            <h4>Condiciones de Borde & Limitaciones:</h4>
            <ul>
              <li><strong>Cobertura:</strong> {alcance.get('zona_estudio', '')}</li>
              <li><strong>Período:</strong> {alcance.get('periodo_temporal', '')}</li>
              <li><strong>Muestra:</strong> {alcance.get('sensores_y_muestra', '')}</li>
            </ul>
          </div>

          <div class="noticia-meta">
            <span class="fuente">{art.get('revista_fuente')}</span>
            <span class="fecha">DOI: {art.get('doi')}</span>
          </div>
        </div>
      </article>
        """
        articulos_cards.append(card)

    articulos_grid_html = "\n".join(articulos_cards)

    html_completo = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Observatorio de Ciencias — DERENZIN S.A.S.</title>
  <meta name="description" content="Plataforma de inteligencia satelital, teledetección multiespectral, dinámica oceanográfica y clima espacial. Un proyecto de DERENZIN S.A.S.">
  <link rel="canonical" href="https://ciencias.derenzin.com/">
  <link rel="icon" href="/assets/favicon.png">
  <meta name="theme-color" content="#0052cc">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Fira+Code:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/style.css">
</head>
<body>
  {render_cabecera("inicio")}

  <main class="contenido portada con-sidebar-grid">
    <h1 class="sr-only">Observatorio de Ciencias de la Tierra, Teledetección y Clima Espacial — DERENZIN S.A.S.</h1>
    <p class="subtitulo-pagina">Edición del {fecha_hoy} • Nodo Analítico UNESCO GlobalCoast PS-006-08 • Protocolo Peters & Chin-Yee (2025)</p>
    
    <div class="layout-grid-sidebar">
      <div class="contenido-principal">
        <!-- SECCIÓN HERO DESTACADA -->
        {destacada_html}

        <!-- SECCIÓN 1: BOLETÍN PROPIO -->
        <h2 class="seccion-titulo">Boletín Propio: Despachos Técnicos del Observatorio</h2>
        <div class="grid-noticias">
          {despachos_grid_html}
        </div>

        <!-- SECCIÓN 2: LITERATURA CIENTÍFICA VALIDADA -->
        <h2 class="seccion-titulo" style="margin-top: 48px;">Literatura Científica Validada (Contención de Conclusiones)</h2>
        <div class="grid-noticias">
          {articulos_grid_html}
        </div>
      </div>

      <!-- SIDEBAR COMPLETO -->
      {render_sidebar()}
    </div>
  </main>

  {render_pie()}
</body>
</html>
"""
    with open(ruta_index, "w", encoding="utf-8") as f:
        f.write(html_completo)
    print(f"Portada de alto impacto generada: {ruta_index}")

def compilar_despachos_detalle(despachos):
    despachos_dir = os.path.join(SITE_DIR, "despachos")
    os.makedirs(despachos_dir, exist_ok=True)

    for d in despachos:
        slug = d.get("slug")
        ruta_archivo = os.path.join(despachos_dir, f"{slug}.html")
        palabras_html = " • ".join([f'<span>#{kw}</span>' for kw in d.get("palabras_clave", [])])

        html_item = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{d.get('titulo')} — Observatorio de Ciencias</title>
  
  <meta name="citation_title" content="{d.get('titulo')}">
  <meta name="citation_author" content="{d.get('autor')}">
  <meta name="citation_publication_date" content="{d.get('fecha')}">
  <meta name="citation_doi" content="{d.get('doi')}">

  <link rel="icon" href="/assets/favicon.png">
  <link rel="stylesheet" href="/style.css">
</head>
<body>
  {render_cabecera("despachos")}

  <main class="contenido pagina-noticia con-sidebar-grid">
    <div class="layout-grid-sidebar">
      <article class="noticia-detalle {d.get('categoria_slug', 'cat-teledeteccion')}">
        <header class="noticia-detalle-cabecera">
          <div style="display: flex; gap: 8px; margin-bottom: 12px;">
            <span class="categoria-badge">{d.get('categoria')}</span>
            <span class="badge-despacho-propio">DESPACHO INSTITUCIONAL</span>
          </div>
          <h1 class="noticia-detalle-titulo">{d.get('titulo')}</h1>
          <p style="font-size: 15px; color: var(--texto-suave); font-style: italic; margin-bottom: 16px;">{d.get('titulo_en', '')}</p>
          <div class="noticia-meta">
            <span class="fuente">Investigador Responsable: <strong>{d.get('autor')}</strong></span>
            <span class="fecha">Radicado: {formatear_fecha(d.get('fecha'))}</span>
            <span class="fecha">DOI Permanente: <a href="https://doi.org/{d.get('doi')}" target="_blank">{d.get('doi')}</a></span>
          </div>
        </header>

        <figure class="noticia-imagen" style="margin: 24px 0;">
          <img src="{d.get('imagen')}" alt="{d.get('titulo')}">
          <figcaption>{d.get('imagen_pie', 'Telemetría Satelital')}</figcaption>
        </figure>

        <div class="noticia-cuerpo-texto" style="font-size: 17px; line-height: 1.7; color: var(--texto);">
          <h3 style="font-size: 18px; margin-top: 24px; color: var(--texto);">Resumen Ejecutivo & Fundamento Biofísico</h3>
          <p style="text-align: justify;">{d.get('resumen')}</p>

          <h3 style="font-size: 18px; margin-top: 28px; color: var(--texto);">Plataforma y Sensores Vinculados</h3>
          <p style="text-align: justify;">
            Este despacho forma parte de la serie de investigaciones operativas del <strong>{d.get('activo_relacionado')}</strong>. 
            Los datos multiespectrales crudos fueron procesados bajo la metodología de reflectancia de superficie (BOA) calibrada para las condiciones atmosféricas del Ecuador.
          </p>

          <div style="background: var(--fondo); border: 1px solid var(--borde); border-radius: var(--radio); padding: 18px; margin: 24px 0;">
            <strong style="display: block; font-size: 13px; color: var(--texto); margin-bottom: 6px;">CÓMO CITAR ESTE DESPACHO (APA 7ma Edición):</strong>
            <code style="display: block; font-family: var(--fuente); font-size: 12px; color: var(--texto-tenue); line-height: 1.5;">
              Derenzin Martínez, F. G. ({d.get('fecha')[:4]}). <em>{d.get('titulo')}</em> (Technical Dispatch Nro. {d.get('id')}). Observatorio de Ciencias de la Tierra y Clima Espacial, DERENZIN S.A.S. & Nodo UNESCO GlobalCoast. https://doi.org/{d.get('doi')}
            </code>
          </div>

          <div style="margin-top: 20px; font-size: 13px; color: var(--texto-suave);">
            <strong>Palabras Clave:</strong> {palabras_html}
          </div>
        </div>
      </article>

      {render_sidebar()}
    </div>
  </main>

  {render_pie()}
</body>
</html>
"""
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write(html_item)
    print(f"Compilados {len(despachos)} páginas de detalle de despachos.")

def compilar_articulos_detalle(articulos):
    art_dir = os.path.join(SITE_DIR, "articulos")
    os.makedirs(art_dir, exist_ok=True)

    for art in articulos:
        slug = art.get("slug", art.get("id"))
        ruta_archivo = os.path.join(art_dir, f"{slug}.html")
        es_preprint = art.get("es_preprint", False)
        badge_peer = '<span class="badge-preprint-alerta">PREPRINT - NO REVISADO</span>' if es_preprint else '<span class="badge-peer-reviewed">REVISADO POR PARES</span>'
        alcance = art.get("alcance_y_limitaciones", {})

        html_item = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{art.get('titulo')} — Observatorio de Ciencias</title>
  
  <meta name="citation_title" content="{art.get('titulo')}">
  <meta name="citation_author" content="{art.get('autores')}">
  <meta name="citation_publication_date" content="{art.get('fecha_publicacion')}">
  <meta name="citation_doi" content="{art.get('doi')}">

  <link rel="icon" href="/assets/favicon.png">
  <link rel="stylesheet" href="/style.css">
</head>
<body>
  {render_cabecera("literatura")}

  <main class="contenido pagina-noticia con-sidebar-grid">
    <div class="layout-grid-sidebar">
      <article class="noticia-detalle {art.get('categoria_slug', 'cat-hidrologia')}">
        <header class="noticia-detalle-cabecera">
          <div style="display: flex; gap: 8px; margin-bottom: 12px; align-items: center;">
            <span class="categoria-badge">{art.get('categoria')}</span>
            {badge_peer}
          </div>
          <h1 class="noticia-detalle-titulo">{art.get('titulo')}</h1>
          <p style="font-size: 15px; color: var(--texto-suave); font-style: italic; margin-bottom: 16px;">{art.get('titulo_en', '')}</p>
          <div class="noticia-meta">
            <span class="fuente">Autores: <strong>{art.get('autores')}</strong></span>
            <span class="fecha">Revista: {art.get('revista_fuente')}</span>
            <span class="fecha">DOI: <a href="{art.get('doi_url')}" target="_blank" rel="noopener">{art.get('doi')} ↗</a></span>
          </div>
        </header>

        <figure class="noticia-imagen" style="margin: 24px 0;">
          <img src="{art.get('imagen')}" alt="{art.get('titulo')}">
          <figcaption>{art.get('imagen_pie', 'Literatura')}</figcaption>
        </figure>

        <!-- RECUADRO OBLIGATORIO PETERS & CHIN-YEE (2025) -->
        <div style="background: #f8f9fa; border-left: 4px solid var(--marca-primario); border-radius: var(--radio); padding: 20px; margin: 24px 0;">
          <h3 style="font-size: 14px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--texto); margin: 0 0 10px 0;">
            🛡️ Delimitación del Alcance & Condiciones de Borde (Roy. Soc. Open Sci. 2025)
          </h3>
          <ul style="margin: 0; padding-left: 20px; font-size: 14px; line-height: 1.6; color: var(--texto-tenue);">
            <li><strong>Cobertura Espacial:</strong> {alcance.get('zona_estudio', '')}</li>
            <li><strong>Ventana Temporal:</strong> {alcance.get('periodo_temporal', '')}</li>
            <li><strong>Sensores y Muestra:</strong> {alcance.get('sensores_y_muestra', '')}</li>
            <li><strong>Nivel Epistémico:</strong> {alcance.get('tipo_conclusion', '')}</li>
          </ul>
        </div>

        <div class="noticia-cuerpo-texto" style="font-size: 17px; line-height: 1.7; color: var(--texto);">
          <h3 style="font-size: 18px; margin-top: 24px; color: var(--texto);">Resumen Fiel del Estudio</h3>
          <p style="text-align: justify;">{art.get('resumen_fiel', '')}</p>

          <div style="margin-top: 32px; padding: 16px; background: var(--fondo); border: 1px solid var(--borde); border-radius: var(--radio); font-size: 13px; color: var(--texto-suave);">
            <strong>Declaración de Transparencia:</strong> {art.get('declaracion_transparencia', 'Resumen técnico asistido por IA, revisado y validado por F. Derenzin.')}
            <div style="margin-top: 10px;">
              <a href="{art.get('doi_url')}" target="_blank" rel="noopener" style="font-weight: 600; color: var(--enlace);">Leer artículo original completo en la revista (DOI) →</a>
            </div>
          </div>
        </div>
      </article>

      {render_sidebar()}
    </div>
  </main>

  {render_pie()}
</body>
</html>
"""
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write(html_item)
    print(f"Compilados {len(articulos)} páginas de detalle de literatura.")

def compilar_archivo(despachos, articulos):
    ruta_archivo = os.path.join(SITE_DIR, "archivo.html")

    filas_despachos = []
    for d in despachos:
        filas_despachos.append(f"""
        <li>
          <a href="/despachos/{d.get('slug')}.html">{d.get('titulo')}</a>
          <span class="sidebar-recientes-fecha">{formatear_fecha(d.get('fecha'))} • DOI: {d.get('doi')}</span>
        </li>
        """)

    filas_articulos = []
    for art in articulos:
        slug = art.get("slug", art.get("id"))
        filas_articulos.append(f"""
        <li>
          <a href="/articulos/{slug}.html">{art.get('titulo')}</a>
          <span class="sidebar-recientes-fecha">{formatear_fecha(art.get('fecha_publicacion'))} • {art.get('revista_fuente')}</span>
        </li>
        """)

    html_completo = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Archivo Histórico — Observatorio de Ciencias</title>
  <link rel="icon" href="/assets/favicon.png">
  <link rel="stylesheet" href="/style.css">
</head>
<body>
  {render_cabecera("archivo")}

  <main class="contenido pagina-noticia con-sidebar-grid">
    <div class="layout-grid-sidebar">
      <div class="noticia-detalle" style="padding: 32px;">
        <h1 class="noticia-detalle-titulo" style="font-size: 28px; margin-bottom: 24px;">Archivo Histórico de Publicaciones</h1>

        <h2 class="seccion-titulo" style="font-size: 20px;">Boletín Propio: Despachos del Observatorio</h2>
        <ul class="sidebar-recientes" style="margin-bottom: 36px;">
          {"".join(filas_despachos)}
        </ul>

        <h2 class="seccion-titulo" style="font-size: 20px;">Literatura Externa Validada</h2>
        <ul class="sidebar-recientes">
          {"".join(filas_articulos)}
        </ul>
      </div>

      {render_sidebar()}
    </div>
  </main>

  {render_pie()}
</body>
</html>
"""
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(html_completo)
    print(f"Generado archivo histórico: {ruta_archivo}")

def main():
    print("Iniciando compilación del portal de ciencias con plantilla Euronews...")
    despachos, articulos = cargar_datos()
    compilar_portada(despachos, articulos)
    compilar_despachos_detalle(despachos)
    compilar_articulos_detalle(articulos)
    compilar_archivo(despachos, articulos)

    # robots.txt y CNAME
    with open(os.path.join(SITE_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n")

    with open(os.path.join(SITE_DIR, "CNAME"), "w", encoding="utf-8") as f:
        f.write("ciencias.derenzin.com\n")

    # Sincronización a la raíz del repositorio para compatibilidad tanto con /(root) como con /site en GitHub Pages
    import shutil
    for item in os.listdir(SITE_DIR):
        src = os.path.join(SITE_DIR, item)
        dst = os.path.join(BASE_DIR, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)

    print(f"Compilación completada: {len(despachos)} despachos y {len(articulos)} artículos generados con diseño de alto impacto.")

if __name__ == "__main__":
    main()
