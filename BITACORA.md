# BITACORA.md — Mapa Interactivo de Bogotá

## 1. Agentes y modelos

| Hito | Agente | Modelo | Notas |
|---|---|---|---|
| 1 | Orquestador | OpenCode / DeepSeek V4.1 Flash Free | Plan, estructura y coordinación |
| 2 | Agente Datos | OpenCode / DeepSeek V4.1 Flash Free | Descarga CKAN y conversión Esri JSON → GeoJSON |
| 3 | Agente Mapa | OpenCode / DeepSeek V4.1 Flash Free | Leaflet, filtros, buscador y heatmap |
| 4 | Agente DevOps | OpenCode / DeepSeek V4.1 Flash Free | Workflow de Actions y despliegue Pages |
| 5 | Agente Documentación | OpenCode / DeepSeek V4.1 Flash Free | README, AGENTS.md y esta bitácora |

> No hubo cambios de modelo durante el desarrollo.

## 2. Configuración del entorno

- **OpenCode**, sesión `ses_e4c606be2ffev47blSYwoRFsHF`.
- **SO:** Windows (win32), consola PowerShell.
- **Python:** 3.10 local; 3.11 en GitHub Actions.
- **Herramientas no disponibles localmente:** `git`, `gh`, `pwsh`.
- **Sustitutos usados:** `curl.exe` del sistema y la API REST de GitHub.

## 3. Fuentes consultadas

| Fuente | Uso | Resultado |
|---|---|---|
| `datosabiertos.bogota.gov.co` (CKAN) | Catálogo y dataset de localidades | ✅ 20 features reales |
| API CKAN `package_show? id=localidad-bogota-d-c` | Descubrimiento del recurso | ✅ |
| Recurso `loca.json` (Esri JSON) | Datos crudos | ✅ 2.36 MB |
| `api.ideca.gov.co/v1/localidades` | Intento inicial | ❌ DNS no resuelve / no existe |
| IDECA / mapas.bogota.gov.co | Referencia de datos | ℹ️ Documentación |
| OpenStreetMap | Capa base del mapa | ✅ |

## 4. Datos analizados

- Dataset: *Localidad. Bogotá D.C* — Secretaría Distrital de Planeación / IDECA.
- Formato original: **Esri JSON** (`features[].attributes` + `geometry.rings`).
- Campos usados: `LocNombre`, `LocCodigo`, `LocArea`, `LocAAdmini`, `OBJECTID`.
- Sistema de referencia: **EPSG:4686** (MAGNA-SIRGAS), geográfico.
- Resultado: 20 polígonos; bbox ≈ `(-74.450, 3.731) — (-73.987, 4.837)`.
- Salida: `data/localidades.geojson` (~1.26 MB), EPSG:4326 etiquetado.

## 5. Problemas y soluciones

| Problema | Solución |
|---|---|
| `api.ideca.gov.co` no resolvía DNS | Se cambió al portal CKAN de datos abiertos de Bogotá |
| El recurso descargado no era GeoJSON sino Esri JSON | Se implementó conversión de anillos Esri (orientación + huecos) a GeoJSON |
| Nombres en mayúsculas sostenidas | Normalización a formato título en la conversión |
| Emojis/Unicode rompían `print()` en consola Windows (cp1252) | Mensajes ASCII (`[INFO]`, `[OK]`, `[WARN]`) |
| El script de conversión sobrescribía el GeoJSON con un ejemplo cuando no había archivo crudo | Ahora valida/retiene el GeoJSON existente; el ejemplo es último recurso |
| `fetch('data/localidades.geojson')` no encontraba el archivo | `scripts/build.py` copia el GeoJSON a `site/data/` |
| Faltaba la librería `leaflet.heat` | Se agregó el CDN en `site/index.html` |
| `git`, `gh` y `pwsh` no están instalados en el entorno local | Se usa `curl.exe` + API REST de GitHub para crear repo/subir archivos |
| El PAT fine-grained no tiene permiso de creación de repositorios | Requiere `Administration: write` / `Repository creation: write`; pendiente de actualizar por el usuario |

## 6. Estimación de tokens

| Fase | Tokens estimados |
|---|---|
| Planificación y esqueleto | ~2 000 |
| Datos (scripts + depuración) | ~9 000 |
| Mapa (HTML/CSS/JS) | ~6 000 |
| DevOps (workflow + API) | ~5 000 |
| Documentación | ~4 000 |
| **Total aproximado** | **~26 000** |

## 7. Enlaces

- **Repositorio:** https://github.com/anfelipeher12-debug/bogota-map
- **Mapa:** https://anfelipeher12-debug.github.io/bogota-map/
- **Dataset:** https://datosabiertos.bogota.gov.co/dataset/localidad-bogota-d-c

---

*Bitácora viva: actualizar al cerrar cada hito.*