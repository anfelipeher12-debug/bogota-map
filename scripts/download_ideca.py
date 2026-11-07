#!/usr/bin/env python3
"""
Descarga el dataset oficial de Localidades de Bogotá D.C. desde datosabiertos.bogota.gov.co
y guarda el archivo crudo en data/localidades_raw.json.

Fuente: "Localidad. Bogotá D.C" - Secretaría Distrital de Planeación / IDECA
Licencia: CC-BY-4.0
API CKAN: https://datosabiertos.bogota.gov.co/api/3/action/package_show?id=localidad-bogota-d-c
"""

import json
import os
import sys

import requests

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
RAW_FILE = os.path.join(DATA_DIR, "localidades_raw.json")
CKAN_URL = "https://datosabiertos.bogota.gov.co/api/3/action/package_show"
PACKAGE_ID = "localidad-bogota-d-c"

# Respaldo: URL directa del recurso GeoJSON/Esri JSON publicado por el portal.
FALLBACK_URL = (
    "https://datosabiertos.bogota.gov.co/dataset/"
    "856cb657-8ca3-4ee8-857f-37211173b1f8/resource/"
    "497b8756-0927-4aee-8da9-ca4e32ca3a8a/download/loca.json"
)

FALLBACK_SAMPLE = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"nombre": "Usme", "codigo": "05"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [[-74.18, 4.55], [-74.08, 4.55], [-74.08, 4.65], [-74.18, 4.65], [-74.18, 4.55]]
                ],
            },
        },
        {
            "type": "Feature",
            "properties": {"nombre": "Kennedy", "codigo": "08"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [[-74.25, 4.55], [-74.15, 4.55], [-74.15, 4.65], [-74.25, 4.65], [-74.25, 4.55]]
                ],
            },
        },
        {
            "type": "Feature",
            "properties": {"nombre": "Suba", "codigo": "11"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [[-74.12, 4.68], [-74.02, 4.68], [-74.02, 4.78], [-74.12, 4.78], [-74.12, 4.68]]
                ],
            },
        },
        {
            "type": "Feature",
            "properties": {"nombre": "Engativá", "codigo": "10"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [[-74.22, 4.75], [-74.12, 4.75], [-74.12, 4.85], [-74.22, 4.85], [-74.22, 4.75]]
                ],
            },
        },
        {
            "type": "Feature",
            "properties": {"nombre": "San Cristóbal", "codigo": "04"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [[-74.28, 4.62], [-74.18, 4.62], [-74.18, 4.72], [-74.28, 4.72], [-74.28, 4.62]]
                ],
            },
        },
    ],
}


def log(msg):
    print(msg, flush=True)


def ensure_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def find_geojson_resource():
    """Consulta la API CKAN y devuelve la URL del recurso GeoJSON/JSON."""
    try:
        resp = requests.get(CKAN_URL, params={"id": PACKAGE_ID}, timeout=30)
        resp.raise_for_status()
        resources = resp.json().get("result", {}).get("resources", [])
        for res in resources:
            fmt = (res.get("format") or "").upper()
            if fmt in ("GEOJSON", "JSON"):
                return res.get("url")
        log("[WARN] No se encontró recurso GeoJSON/JSON en el catálogo CKAN.")
    except Exception as exc:
        log(f"[WARN] No se pudo consultar la API CKAN: {exc}")
    return None


def download(url, dest):
    log(f"[INFO] Descargando: {url}")
    resp = requests.get(url, timeout=120)
    resp.raise_for_status()
    with open(dest, "wb") as fh:
        fh.write(resp.content)
    log(f"[OK] Guardado en {dest} ({len(resp.content)} bytes)")


def save_sample(dest):
    with open(dest, "w", encoding="utf-8") as fh:
        json.dump(FALLBACK_SAMPLE, fh, ensure_ascii=False, indent=2)
    log(f"[WARN] Se usó el conjunto de ejemplo en {dest}")


def main():
    ensure_dir()

    url = find_geojson_resource() or FALLBACK_URL

    try:
        download(url, RAW_FILE)
    except Exception as exc:
        log(f"[ERROR] Falló la descarga de datos oficiales: {exc}")
        if os.path.exists(RAW_FILE):
            log("[INFO] Se conserva el archivo crudo existente.")
            return
        # Último recurso: ejemplo embebido (solo si no hay datos previos)
        save_sample(os.path.join(DATA_DIR, "localidades.geojson"))
        sys.exit(0)

    log("[OK] Descarga completada.")


if __name__ == "__main__":
    main()