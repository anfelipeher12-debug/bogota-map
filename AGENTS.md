# AGENTS.md — Plan del proyecto Mapa Interactivo de Bogotá

## 1. Objetivo

Mapa web interactivo de Bogotá publicado en GitHub Pages, con datos abiertos
oficiales descargados y convertidos por scripts reproducibles.

- **Tema:** divulgación territorial — localidades de Bogotá D.C.
- **Nivel de detalle:** localidades (20).
- **Interacciones:** filtro por localidad, buscador, mapa de calor, popups, zoom.
- **Tecnología:** Leaflet 1.9.4 + leaflet.heat + Python.
- **Despliegue:** GitHub Actions → GitHub Pages.

## 2. Estructura del repositorio

```
.
├─ AGENTS.md
├─ BITACORA.md
├─ README.md
├─ requirements.txt
├─ data/
│   ├─ localidades_raw.json      # descarga cruda (generada, no versionada obligatoriamente)
│   └─ localidades.geojson       # GeoJSON final (versionado para publicación inmediata)
├─ scripts/
│   ├─ download_ideca.py
│   ├─ convert_to_geojson.py
│   └─ build.py
├─ site/
│   ├─ index.html
│   ├─ style.css
│   ├─ script.js
│   └─ data/localidades.geojson  # copia consumida por el sitio
└─ .github/workflows/deploy.yml
```

## 3. Convenciones

- **Python ≥ 3.9**, dependencias en `requirements.txt`.
- **GeoJSON RFC 7946**, coordenadas WGS84 (EPSG:4326).
- **Commits:** `feat:`, `fix:`, `docs:`, `chore:`, `data:`.
- **Nombres de archivo:** `snake_case`.
- **Mensajes de scripts:** ASCII para compatibilidad con consolas Windows.
- **Un solo comando de build:** `python scripts/build.py`.

## 4. Subagentes

| Agente | Tareas |
|---|---|
| **Datos** | Descarga CKAN, conversión Esri JSON → GeoJSON, validación |
| **Mapa** | Leaflet, filtros, buscador, heatmap, estilos responsivos |
| **DevOps** | Git/GitHub, workflow de Actions, Pages |
| **Documentación** | README, AGENTS.md, BITACORA.md |

## 5. Lista de tareas

- [x] 1. Esqueleto del proyecto y convenciones.
- [x] 2. Definición de subagentes.
- [x] 3. Scripts de datos (descarga + conversión) con fuente oficial.
- [x] 4. Sitio Leaflet con filtros, buscador y mapa de calor.
- [x] 5. Workflow de GitHub Actions (build + deploy Pages + cron semanal).
- [x] 6. README con reproducción.
- [x] 7. Crear repositorio público y subir archivos.
- [x] 8. Activar GitHub Pages (Source: GitHub Actions).
- [x] 9. Ejecutar el workflow end-to-end.
- [x] 10. Verificar el mapa publicado y documentar enlaces.

## 6. Criterios de aceptación

1. `python scripts/build.py` genera `data/localidades.geojson` con 20 features. ✅
2. El sitio carga sin errores y muestra las 20 localidades. ✅
3. El buscador y los filtros funcionan. ✅
4. El mapa de calor se puede activar/desactivar. ✅
5. GitHub Actions publica el sitio y la URL responde 200. ✅

## 7. Enlaces

- **Repositorio:** https://github.com/anfelipeher12-debug/bogota-map
- **Mapa publicado:** https://anfelipeher12-debug.github.io/bogota-map/
- **Workflow:** https://github.com/anfelipeher12-debug/bogota-map/actions

---

*Fuente de verdad del proyecto. Actualizar esta lista en cada hito.*