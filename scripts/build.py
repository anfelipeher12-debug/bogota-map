#!/usr/bin/env python3
"""
Orquestador de construcción: un solo comando para reproducir todo.

Uso:
    python scripts/build.py

Pasos:
  1. Descarga los datos oficiales de Localidades de Bogotá.
  2. Convierte el archivo crudo a GeoJSON (EPSG:4326).
  3. Copia el GeoJSON a site/data/ para que el sitio estático lo consuma.
"""

import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
SITE_DATA = os.path.join(ROOT, "site", "data")


def run(script):
    path = os.path.join(HERE, script)
    print(f"\n=== Ejecutando {script} ===", flush=True)
    subprocess.check_call([sys.executable, path])


def main():
    run("download_ideca.py")
    run("convert_to_geojson.py")

    os.makedirs(SITE_DATA, exist_ok=True)
    src = os.path.join(DATA, "localidades.geojson")
    dst = os.path.join(SITE_DATA, "localidades.geojson")
    shutil.copyfile(src, dst)
    print(f"\n[OK] Datos copiados a {dst}")


if __name__ == "__main__":
    main()