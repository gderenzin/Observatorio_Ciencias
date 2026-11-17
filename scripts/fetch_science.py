#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
OBSERVATORIO DE CIENCIAS DE LA TIERRA, TELEDETECCIÓN Y CLIMA ESPACIAL
SCRIPT DE INGESTA AUTOMÁTICA DE FUENTES CIENTÍFICAS PRIMARIAS (fetch_science.py)
==============================================================================
Regla de oro: Cero alucinaciones. Solo se descargan e indexan ítems reales desde
la lista blanca de feeds_ciencias.yaml, validando rigurosamente que el dominio del
enlace coincida con el dominio oficial de la institución.
==============================================================================
"""

import os
import sys
import json
import logging
from datetime import datetime, timezone
from urllib.parse import urlparse
import yaml
import feedparser

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEEDS_FILE = os.path.join(BASE_DIR, "feeds_ciencias.yaml")
DATA_DIR = os.path.join(BASE_DIR, "data")
PUBLICADAS_FILE = os.path.join(DATA_DIR, "publicadas_ciencias.json")
LEDGER_FILE = os.path.join(DATA_DIR, "ledger_dedup.json")
NUEVAS_HOY_FILE = os.path.join(DATA_DIR, "nuevas_ciencias_hoy.json")

# Palabras clave canónicas de ciencias de la Tierra y Clima Espacial
PALABRAS_CLAVE_CIENCIAS = [
    "satellite", "satélite", "sentinel", "landsat", "earth", "tierra", "remote sensing",
    "teledetección", "teledeteccion", "sensor", "solar", "sun", "geomagnetic", "geomagnética",
    "ionosphere", "ionosfera", "flare", "cme", "radiation", "radiación", "vegetation",
    "vegetación", "ndvi", "ndmi", "ndre", "climate", "clima", "ocean", "océano", "oceano",
    "sea", "mar", "lightning", "rayo", "glm", "goes", "storm", "tormenta", "radar", "sar",
    "drought", "sequía", "sequia", "flood", "inundación", "inundacion", "el niño", "la niña",
    "enso", "temperature", "temperatura", "atmosphere", "atmósfera", "atmosfera"
]

def normalizar_dominio(url: str) -> str:
    """Extrae el hostname en minúsculas sin 'www.'."""
    try:
        netloc = urlparse(url).netloc.lower()
        if netloc.startswith("www."):
            netloc = netloc[4:]
        return netloc
    except Exception:
        return ""

def dominio_coincide(url_item: str, dominio_fuente: str) -> bool:
    """Comprueba si el enlace pertenece al dominio de la fuente o a un subdominio válido."""
    dom_item = normalizar_dominio(url_item)
    dom_fuente = normalizar_dominio(dominio_fuente)
    return dom_item == dom_fuente or dom_item.endswith("." + dom_fuente)

def contiene_palabra_clave(texto: str) -> bool:
    """Valida si el título o resumen contiene temática relevante."""
    texto_l = texto.lower()
    return any(p in texto_l for p in PALABRAS_CLAVE_CIENCIAS)

def cargar_json(ruta: str, por_defecto):
    if os.path.exists(ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.warning("Error leyendo %s: %s. Usando valor por defecto.", ruta, e)
    return por_defecto

def guardar_json(ruta: str, datos):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def main():
    logging.info("Iniciando ingesta de feeds científicos desde %s", FEEDS_FILE)
    if not os.path.exists(FEEDS_FILE):
        logging.error("No se encontró el archivo %s", FEEDS_FILE)
        sys.exit(1)

    with open(FEEDS_FILE, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    fuentes = config.get("fuentes", [])
    logging.info("Fuentes configuradas: %d", len(fuentes))

    publicadas = cargar_json(PUBLICADAS_FILE, [])
    ledger = set(cargar_json(LEDGER_FILE, []))
    nuevas_hoy = []

    total_procesadas = 0
    total_descartadas_dominio = 0
    total_duplicadas = 0

    for f in fuentes:
        nombre = f.get("nombre")
        url_feed = f.get("url")
        dominio_fuente = f.get("dominio")
        categoria = f.get("categoria", "ciencias_generales")
        idioma = f.get("idioma", "en")

        logging.info("Consultando feed: %s (%s)", nombre, url_feed)
        try:
            d = feedparser.parse(url_feed)
        except Exception as e:
            logging.warning("Fallo al descargar feed de %s: %s. Continuando...", nombre, e)
            continue

        if getattr(d, "bozo", 0) and not d.entries:
            logging.warning("Feed vacío o no válido de %s. Continuando...", nombre)
            continue

        for entry in d.entries[:15]:
            total_procesadas += 1
            link = entry.get("link", "").strip()
            title = entry.get("title", "").strip()
            summary = entry.get("summary", entry.get("description", "")).strip()

            if not link or not title:
                continue

            # Verificación estricta de dominio oficial
            if not dominio_coincide(link, dominio_fuente):
                total_descartadas_dominio += 1
                continue

            # Deduplicación por enlace
            if link in ledger:
                total_duplicadas += 1
                continue

            # Filtro temático de pertinencia científica
            texto_evaluar = f"{title} {summary}"
            if not contiene_palabra_clave(texto_evaluar):
                continue

            # Extraer fecha
            published = entry.get("published", entry.get("updated", datetime.now(timezone.utc).isoformat()))

            item = {
                "id": link,
                "titulo": title,
                "resumen": summary,
                "enlace": link,
                "fuente": nombre,
                "dominio": dominio_fuente,
                "categoria": categoria,
                "idioma": idioma,
                "fecha_publicacion": published,
                "fecha_ingesta": datetime.now(timezone.utc).isoformat()
            }

            publicadas.insert(0, item)
            nuevas_hoy.append(item)
            ledger.add(link)

    # Limitar histórico a los 300 artículos más recientes
    publicadas = publicadas[:300]

    guardar_json(PUBLICADAS_FILE, publicadas)
    guardar_json(LEDGER_FILE, list(ledger))
    guardar_json(NUEVAS_HOY_FILE, nuevas_hoy)

    logging.info(
        "Ingesta finalizada: %d procesados, %d duplicados, %d descartados por dominio. Nuevos hoy: %d. Total publicados: %d",
        total_procesadas, total_duplicadas, total_descartadas_dominio, len(nuevas_hoy), len(publicadas)
    )

if __name__ == "__main__":
    main()
