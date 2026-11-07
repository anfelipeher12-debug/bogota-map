#!/usr/bin/env python3
"""
Convierte el archivo crudo de Localidades de Bogotá a GeoJSON RFC 7946.

Soporta:
- Esri JSON (features con "attributes" y "geometry.rings"), formato del portal
  datosabiertos.bogota.gov.co.
- GeoJSON estándar (FeatureCollection).

Salida: data/localidades.geojson con CRS EPSG:4326 (etiquetado para web).
"""

import json
import os
import sys

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
RAW_FILE = os.path.join(DATA_DIR, "localidades_raw.json")
OUTPUT_FILE = os.path.join(DATA_DIR, "localidades.geojson")


def log(msg):
    print(msg, flush=True)


def close_ring(ring):
    if not ring:
        return ring
    if ring[0] != ring[-1]:
        ring = ring + [ring[0]]
    return ring


def signed_area(ring):
    """Área con signo (fórmula del cordón). Negativa = sentido horario."""
    total = 0.0
    for i in range(len(ring) - 1):
        x1, y1 = ring[i]
        x2, y2 = ring[i + 1]
        total += x1 * y2 - x2 * y1
    return total / 2.0


def point_in_ring(point, ring):
    """Ray casting: indica si un punto está dentro de un anillo."""
    x, y = point
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi
        ):
            inside = not inside
        j = i
    return inside


def rings_to_geometry(rings):
    """Convierte anillos Esri (exteriores horarios, huecos antihorarios) en geometría GeoJSON."""
    cleaned = []
    for ring in rings:
        ring = [[round(float(c[0]), 6), round(float(c[1]), 6)] for c in ring]
        cleaned.append(close_ring(ring))

    outers = [r for r in cleaned if signed_area(r) < 0]
    holes = [r for r in cleaned if signed_area(r) >= 0]

    # Si la orientación no sigue la convención Esri, tratar todo como exterior.
    if not outers:
        outers, holes = cleaned, []

    polygons = []
    for outer in outers:
        contained = [h for h in holes if point_in_ring(h[0], outer)]
        polygons.append([outer] + contained)

    if len(polygons) == 1:
        return {"type": "Polygon", "coordinates": polygons[0]}
    return {"type": "MultiPolygon", "coordinates": polygons}


def pretty_name(value):
    """Normaliza nombres en mayúsculas sostenidas a formato título."""
    if not value:
        return value
    return " ".join(word.capitalize() for word in str(value).split())


def esri_to_geojson(esri):
    features = []
    for item in esri.get("features", []):
        attrs = item.get("attributes", {})
        rings = (item.get("geometry") or {}).get("rings")
        if not rings:
            continue
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "nombre": pretty_name(attrs.get("LocNombre")),
                    "codigo": attrs.get("LocCodigo"),
                    "area_m2": attrs.get("LocArea"),
                    "acuerdo": attrs.get("LocAAdmini"),
                    "objectid": attrs.get("OBJECTID"),
                },
                "geometry": rings_to_geometry(rings),
            }
        )
    return {"type": "FeatureCollection", "features": features}


def normalize_geojson(data):
    features = []
    for feat in data.get("features", []):
        geom = feat.get("geometry")
        if not geom:
            log("[WARN] Feature sin geometría omitida.")
            continue
        props = feat.get("properties") or {}
        if "nombre" not in props:
            for key in ("LocNombre", "NOMBRE", "Nombre", "name", "LOCALIDAD"):
                if key in props:
                    props["nombre"] = props[key]
                    break
        features.append(
            {
                "type": "Feature",
                "properties": props,
                "geometry": {
                    "type": geom.get("type"),
                    "coordinates": geom.get("coordinates"),
                },
            }
        )
    return {"type": "FeatureCollection", "features": features}


def is_esri(data):
    return (
        isinstance(data, dict)
        and isinstance(data.get("features"), list)
        and data["features"]
        and "attributes" in data["features"][0]
    )


def save_geojson(features, path):
    payload = {
        "type": "FeatureCollection",
        "crs": {"type": "name", "properties": {"name": "EPSG:4326"}},
        "features": features,
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, separators=(",", ":"))
    log(f"[OK] GeoJSON guardado en {path} ({len(features)} features)")


def main():
    if not os.path.exists(RAW_FILE):
        if os.path.exists(OUTPUT_FILE):
            log("[INFO] No hay archivo crudo; se conserva el GeoJSON existente.")
            with open(OUTPUT_FILE, encoding="utf-8") as fh:
                data = json.load(fh)
            save_geojson(data.get("features", []), OUTPUT_FILE)
            return
        log("[ERROR] No hay datos crudos ni GeoJSON previo. Ejecuta download_ideca.py.")
        sys.exit(1)

    with open(RAW_FILE, encoding="utf-8") as fh:
        raw = json.load(fh)

    if is_esri(raw):
        log("[INFO] Formato detectado: Esri JSON. Convirtiendo a GeoJSON...")
        collection = esri_to_geojson(raw)
    else:
        log("[INFO] Formato detectado: GeoJSON. Normalizando...")
        collection = normalize_geojson(raw)

    save_geojson(collection["features"], OUTPUT_FILE)


if __name__ == "__main__":
    main()