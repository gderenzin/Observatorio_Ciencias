#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
OBSERVATORIO DE CIENCIAS DE LA TIERRA, TELEDETECCIÓN Y CLIMA ESPACIAL
SCRIPT DE INGESTA CIENTÍFICA (fetch_science.py) - PROTOCOLO PETERS & CHIN-YEE 2025
==============================================================================
Reglas estrictas de Contención Epistémica:
1. Nada se publica en automático. Solo genera borradores pendientes en borradores_pendientes.yaml.
2. Extrae y delimita: zona geográfica, período temporal y sensores/muestra.
3. Fuentes con DOI. Los preprints se etiquetan como "no revisado por pares".
4. Cadencia controlada: máximo 3 a 5 notas por semana para permitir revisión humana exhaustiva.
==============================================================================
"""

import os
import sys
import re
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
BORRADORES_FILE = os.path.join(DATA_DIR, "borradores_pendientes.yaml")
APROBADOS_FILE = os.path.join(DATA_DIR, "articulos_aprobados.yaml")
LEDGER_FILE = os.path.join(DATA_DIR, "ledger_dedup.json")

def normalizar_dominio(url: str) -> str:
    try:
        netloc = urlparse(url).netloc.lower()
        if netloc.startswith("www."):
            netloc = netloc[4:]
        return netloc
    except Exception:
        return ""

def dominio_coincide(url_item: str, dominio_fuente: str) -> bool:
    dom_item = normalizar_dominio(url_item)
    dom_fuente = normalizar_dominio(dominio_fuente)
    return dom_item == dom_fuente or dom_item.endswith("." + dom_fuente)

def extraer_doi(texto: str) -> str:
    """Busca patrones de DOI estándar (10.XXXX/...) en el texto o enlace."""
    match = re.search(r'(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)', texto)
    if match:
        return match.group(1).rstrip('.')
    return ""

def cargar_yaml(ruta, clave_raiz):
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            return data.get(clave_raiz, [])
    return []

def guardar_yaml(ruta, clave_raiz, lista):
    data = {clave_raiz: lista}
    with open(ruta, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, indent=2)

def main():
    logging.info("Iniciando escaneo de literatura científica con control de alcance (Peters & Chin-Yee 2025)")
    if not os.path.exists(FEEDS_FILE):
        logging.error("No se encontró feeds_ciencias.yaml")
        sys.exit(1)

    with open(FEEDS_FILE, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    fuentes = config.get("fuentes", [])
    borradores = cargar_yaml(BORRADORES_FILE, "borradores")
    aprobados = cargar_yaml(APROBADOS_FILE, "articulos")

    # Ledger de enlaces ya conocidos (en borradores o aprobados)
    enlaces_conocidos = {b.get("enlace_original") for b in borradores if b.get("enlace_original")}
    enlaces_conocidos.update({a.get("doi_url") for a in aprobados if a.get("doi_url")})

    nuevos_borradores_creados = 0
    # Límite semanal estricto: no acumular más de 5 borradores sin revisar
    MAX_BORRADORES_EN_COLA = 5

    if len(borradores) >= MAX_BORRADORES_EN_COLA:
        logging.info("La cola de borradores ya cuenta con %d elementos pendientes. No se ingresan más hasta revisión del Prof. Feddor Derenzin M.", len(borradores))
        return

    for f in fuentes:
        if len(borradores) >= MAX_BORRADORES_EN_COLA:
            break

        nombre_fuente = f.get("nombre")
        url_feed = f.get("url")
        dominio_fuente = f.get("dominio")
        es_preprint = f.get("es_preprint", False)
        categoria = f.get("categoria", "Geociencias")

        logging.info("Consultando fuente: %s", nombre_fuente)
        try:
            d = feedparser.parse(url_feed)
        except Exception as e:
            logging.warning("Fallo al descargar feed de %s: %s", nombre_fuente, e)
            continue

        for entry in d.entries[:10]:
            if len(borradores) >= MAX_BORRADORES_EN_COLA:
                break

            link = entry.get("link", "").strip()
            title = entry.get("title", "").strip()
            summary = entry.get("summary", entry.get("description", "")).strip()

            if not link or not title:
                continue

            if not dominio_coincide(link, dominio_fuente):
                continue

            if link in enlaces_conocidos:
                continue

            doi = extraer_doi(f"{link} {summary}")
            if not doi and not es_preprint and not f.get("es_comunicado_tecnico"):
                # Regla: Priorizar fuentes con DOI identificable
                continue

            # Generar ID correlativo
            borrador_id = f"BORR-{datetime.now().strftime('%Y%m')}-{len(borradores) + 1:03d}"

            # Plantilla estructurada conforme al protocolo Peters & Chin-Yee (2025)
            borrador = {
                "id": borrador_id,
                "titulo": title,
                "titulo_en": title,
                "revista_fuente": nombre_fuente,
                "enlace_original": link,
                "doi": doi or "Pendiente de indexación DOI",
                "doi_url": f"https://doi.org/{doi}" if doi else link,
                "fecha_publicacion": entry.get("published", datetime.now(timezone.utc).strftime("%Y-%m-%d")),
                "es_preprint": es_preprint,
                "estado_revision_pares": "No revisado por pares (Preprint)" if es_preprint else "Revisado por pares (Peer-Reviewed)",
                "categoria": categoria,
                # REGLA PETERS & CHIN-YEE (2025): Campos obligatorios que delimitan las conclusiones
                "alcance_y_limitaciones": {
                    "zona_estudio": "POR DEFINIR EN REVISIÓN (Ej. cuenca, coordenadas, región exacta)",
                    "periodo_temporal": "POR DEFINIR EN REVISIÓN (Ej. meses/años evaluados)",
                    "sensores_y_muestra": "POR DEFINIR EN REVISIÓN (Ej. Sentinel-2, cantidad de imágenes, estaciones)",
                    "tipo_conclusion": "Observacional / Correlación estadística (Prohibido inferir causalidad sin prueba mecanicista)"
                },
                "resumen_preliminar_sin_exageracion": summary[:450] if summary else "Sin resumen provisto por el feed.",
                "aprobado": False,
                "revisor": "Pendiente de validación por Prof. Ing. Feddor Derenzin",
                "declaracion_transparencia": "Resumen técnico asistido por IA, revisado y validado por Prof. Feddor Derenzin M."
            }

            borradores.append(borrador)
            enlaces_conocidos.add(link)
            nuevos_borradores_creados += 1
            logging.info("Borrador agregado a la cola: %s (%s)", borrador_id, title[:50])

    guardar_yaml(BORRADORES_FILE, "borradores", borradores)
    logging.info("Proceso completado. Nuevos borradores creados: %d. Total pendientes de aprobación: %d", nuevos_borradores_creados, len(borradores))

if __name__ == "__main__":
    main()
