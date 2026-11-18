#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
OBSERVATORIO DE CIENCIAS DE LA TIERRA, TELEDETECCIÓN Y CLIMA ESPACIAL
APROBADOR EDITORIAL HUMANO (Human-in-the-Loop CLI) - PROTOCOLO PETERS & CHIN-YEE
==============================================================================
Uso:
  python scripts/aprobar_borrador.py --listar
  python scripts/aprobar_borrador.py --aprobar LIT-2026-XXX
==============================================================================
"""

import os
import sys
import argparse
from datetime import datetime
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
BORRADORES_FILE = os.path.join(DATA_DIR, "borradores_pendientes.yaml")
APROBADOS_FILE = os.path.join(DATA_DIR, "articulos_aprobados.yaml")

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

def listar_borradores():
    borradores = cargar_yaml(BORRADORES_FILE, "borradores")
    print(f"\n=== COLA DE BORRADORES PENDIENTES ({len(borradores)}) ===")
    if not borradores:
        print("No hay borradores pendientes de revisión. El pipeline está al día.")
        return

    for b in borradores:
        preprint_tag = "[PREPRINT - NO REVISADO POR PARES]" if b.get("es_preprint") else "[PEER-REVIEWED]"
        print(f"\nID: {b.get('id')} | {preprint_tag}")
        print(f"Título: {b.get('titulo')}")
        print(f"Fuente / DOI: {b.get('revista_fuente')} | {b.get('doi')}")
        print(f"Fecha detectada: {b.get('fecha_publicacion')}")
        alcance = b.get("alcance_y_limitaciones", {})
        print(f"  • Zona de estudio: {alcance.get('zona_estudio', 'No delimitada')}")
        print(f"  • Período: {alcance.get('periodo_temporal', 'No especificado')}")
        print(f"  • Muestra/Sensores: {alcance.get('sensores_y_muestra', 'No especificado')}")

def aprobar_borrador(borrador_id):
    borradores = cargar_yaml(BORRADORES_FILE, "borradores")
    aprobados = cargar_yaml(APROBADOS_FILE, "articulos")

    encontrado = None
    nuevos_borradores = []
    for b in borradores:
        if b.get("id") == borrador_id:
            encontrado = b
        else:
            nuevos_borradores.append(b)

    if not encontrado:
        print(f"Error: No se encontró ningún borrador con ID '{borrador_id}'.")
        sys.exit(1)

    # Validar campos de limitaciones según Peters & Chin-Yee (2025)
    alcance = encontrado.get("alcance_y_limitaciones", {})
    if not alcance.get("zona_estudio") or not alcance.get("periodo_temporal"):
        print("ADVERTENCIA (Protocolo Peters & Chin-Yee 2025):")
        print("El borrador debe tener explicitados 'zona_estudio' y 'periodo_temporal' para evitar sobregeneralización.")

    encontrado["revisor"] = "Prof. Ing. Feddor Gabriel Derenzin Martínez"
    encontrado["fecha_aprobacion"] = datetime.now().strftime("%Y-%m-%d")
    encontrado["declaracion_transparencia"] = "Resumen técnico asistido por IA, revisado y validado por Prof. Feddor Derenzin M."

    aprobados.insert(0, encontrado)

    guardar_yaml(BORRADORES_FILE, "borradores", nuevos_borradores)
    guardar_yaml(APROBADOS_FILE, "articulos", aprobados)

    print(f"\n[OK] Borrador {borrador_id} APROBADO formalmente por Prof. Feddor Derenzin M.")
    print(f"Transferido a {APROBADOS_FILE}. Quedan {len(nuevos_borradores)} pendientes.")

    # Recompilar sitio
    os.system(f'python "{os.path.join(BASE_DIR, "scripts", "build_science_site.py")}"')

def main():
    parser = argparse.ArgumentParser(description="Aprobador Editorial de Ciencia - Human in the Loop")
    parser.add_argument("--listar", action="store_true", help="Lista los borradores pendientes")
    parser.add_argument("--aprobar", type=str, help="Aprueba un borrador por su ID y recompila el sitio")

    args = parser.parse_args()
    if args.listar:
        listar_borradores()
    elif args.aprobar:
        aprobar_borrador(args.aprobar)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
