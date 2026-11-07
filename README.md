# 🗺️ Mapa Interactivo de Bogotá

Mapa web interactivo de las **20 localidades de Bogotá D.C.**, construido con **Leaflet**,
alimentado con datos abiertos oficiales y desplegado automáticamente en **GitHub Pages**
mediante **GitHub Actions**.

- **Mapa publicado:** https://anfelipeher12-debug.github.io/bogota-map/
- **Repositorio:** https://github.com/anfelipeher12-debug/bogota-map

## ✨ Funcionalidades

- Polígonos de las 20 localidades de Bogotá (datos oficiales, EPSG:4326).
- **Filtro** por localidad con lista generada dinámicamente.
- **Buscador** de localidades en tiempo real.
- **Mapa de calor** (densidad) con la librería `leaflet.heat`, activable/desactivable.
- Popups con el nombre de cada localidad y zoom automático al seleccionarla.
- Diseño responsivo (escritorio y móvil).
- Datos y despliegue **reproducibles con un solo comando**.

## 🛠️ Tecnologías

| Componente | Tecnología |
|---|---|
| Mapa | Leaflet 1.9.4 + leaflet.heat 0.2.0 |
| Datos | Python 3 + `requests` |
| Formato | GeoJSON (RFC 7946, EPSG:4326) |
| CI/CD | GitHub Actions + GitHub Pages |

## 📁 Estructura

```
.
├─ AGENTS.md                  # Plan del proyecto y lista de tareas
├─ BITACORA.md                # Bitácora de agentes, modelos e incidencias
├─ README.md
├─ requirements.txt
├─ data/
│   ├─ localidades_raw.json   # Descarga cruda (Esri JSON) – generada
│   └─ localidades.geojson    # GeoJSON final – generado
├─ scripts/
│   ├─ download_ideca.py      # Descarga desde datosabiertos.bogota.gov.co
│   ├─ convert_to_geojson.py  # Esri JSON → GeoJSON
│   └─ build.py               # Orquestador: un solo comando
├─ site/                      # Sitio estático publicado
│   ├─ index.html
│   ├─ style.css
│   ├─ script.js
│   └─ data/localidades.geojson
└─ .github/workflows/deploy.yml
```

## 🚀 Reproducción

### Requisitos

- Python 3.9+
- Conexión a internet (para descargar los datos)

### Un solo comando

```bash
pip install -r requirements.txt
python scripts/build.py
```

Esto descarga los datos oficiales, los convierte a GeoJSON y los copia a `site/data/`.

### Ver el mapa localmente

```bash
python -m http.server 8000 --directory site
```

Abrir <http://localhost:8000>.

### Desplegar

El workflow `.github/workflows/deploy.yml` se ejecuta en cada push a `main`,
manualmente (`workflow_dispatch`) y semanalmente (lunes 06:00 UTC).

Para GitHub Pages, configurar en **Settings → Pages → Source: GitHub Actions**.

## 📊 Fuente de datos

- **Dataset:** *Localidad. Bogotá D.C* — Secretaría Distrital de Planeación / IDECA.
- **Portal:** <https://datosabiertos.bogota.gov.co/dataset/localidad-bogota-d-c>
- **Recurso:** GeoJSON/Esri JSON (`loca.json`).
- **Licencia:** CC-BY-4.0.
- **Sistema de referencia original:** EPSG:4686 (MAGNA-SIRGAS), coordenadas
  geográficas compatibles con web (se etiquetan como EPSG:4326).

El script consulta la API CKAN del portal y, si no está disponible, usa la URL
directa del recurso. Si todo falla y no hay datos previos, genera un conjunto de
ejemplo para que el sitio nunca quede vacío.

## 🤖 Orquestación por agentes

| Agente | Responsabilidad |
|---|---|
| **Datos** | Scripts Python de descarga y conversión a GeoJSON |
| **Mapa** | Sitio Leaflet con filtros, buscador y mapa de calor |
| **DevOps** | Repositorio, GitHub Actions y GitHub Pages |
| **Documentación** | README, AGENTS.md y BITACORA.md |

## 📜 Licencia

Código: MIT. Datos: CC-BY-4.0 (Secretaría Distrital de Planeación / IDECA).