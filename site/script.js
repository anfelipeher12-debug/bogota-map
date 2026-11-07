/* script.js – Mapa interactivo de Bogotá (Leaflet) */
'use strict';

const DATA_URL = 'data/localidades.geojson';
const FALLBACK = {
  type: 'FeatureCollection',
  features: [
    { type: 'Feature', properties: { nombre: 'Usme' },
      geometry: { type: 'Polygon', coordinates: [[[-74.18, 4.55], [-74.08, 4.55], [-74.08, 4.65], [-74.18, 4.65], [-74.18, 4.55]]] } },
    { type: 'Feature', properties: { nombre: 'Kennedy' },
      geometry: { type: 'Polygon', coordinates: [[[-74.25, 4.55], [-74.15, 4.55], [-74.15, 4.65], [-74.25, 4.65], [-74.25, 4.55]]] } },
    { type: 'Feature', properties: { nombre: 'Suba' },
      geometry: { type: 'Polygon', coordinates: [[[-74.12, 4.68], [-74.02, 4.68], [-74.02, 4.78], [-74.12, 4.78], [-74.12, 4.68]]] } },
    { type: 'Feature', properties: { nombre: 'Engativá' },
      geometry: { type: 'Polygon', coordinates: [[[-74.22, 4.75], [-74.12, 4.75], [-74.12, 4.85], [-74.22, 4.85], [-74.22, 4.75]]] } },
    { type: 'Feature', properties: { nombre: 'San Cristóbal' },
      geometry: { type: 'Polygon', coordinates: [[[-74.28, 4.62], [-74.18, 4.62], [-74.18, 4.72], [-74.28, 4.72], [-74.28, 4.62]]] } }
  ]
};

let map;
let geoLayer = null;
let heatLayer = null;
let features = [];
const layersByName = new Map();

document.addEventListener('DOMContentLoaded', init);

async function init() {
  map = L.map('mapa', { center: [4.65, -74.1], zoom: 11, preferCanvas: true });

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(map);

  let geojson = FALLBACK;
  try {
    const resp = await fetch(DATA_URL, { cache: 'no-cache' });
    if (resp.ok) {
      const parsed = await resp.json();
      if (parsed && Array.isArray(parsed.features) && parsed.features.length) {
        geojson = parsed;
      }
    }
  } catch (err) {
    console.warn('No se pudo cargar', DATA_URL, '- usando datos de ejemplo.', err);
  }

  features = geojson.features;
  drawFeatures(features);
  buildFilterButtons();
  wireSearch();
  wireHeatToggle();
}

function nombreOf(feature) {
  const p = feature.properties || {};
  return p.nombre || p.NOMBRE || p.name || p.LOCALIDAD || 'Localidad';
}

function drawFeatures(feats) {
  if (geoLayer) map.removeLayer(geoLayer);
  layersByName.clear();

  geoLayer = L.geoJSON({ type: 'FeatureCollection', features: feats }, {
    style: () => ({ color: '#006d77', weight: 2, fillColor: '#83c5be', fillOpacity: 0.45 }),
    onEachFeature: (feature, layer) => {
      const nombre = nombreOf(feature);
      layersByName.set(nombre, layer);
      layer.bindPopup(`<b>${nombre}</b>`);
      layer.on('mouseover', () => layer.setStyle({ fillOpacity: 0.7 }));
      layer.on('mouseout', () => layer.setStyle({ fillOpacity: 0.45 }));
    }
  }).addTo(map);

  const bounds = geoLayer.getBounds();
  if (bounds.isValid()) map.fitBounds(bounds, { padding: [20, 20] });

  buildHeatLayer(feats);
}

function centroid(feature) {
  const geom = feature.geometry;
  if (!geom || !geom.coordinates) return null;
  if (geom.type === 'Point') return [geom.coordinates[1], geom.coordinates[0]];
  const ring = geom.type === 'Polygon' ? geom.coordinates[0]
    : geom.type === 'MultiPolygon' ? geom.coordinates[0][0] : null;
  if (!ring || !ring.length) return null;
  let x = 0, y = 0;
  for (const c of ring) { x += c[0]; y += c[1]; }
  return [y / ring.length, x / ring.length];
}

function buildHeatLayer(feats) {
  if (heatLayer) { map.removeLayer(heatLayer); heatLayer = null; }
  if (typeof L.heatLayer !== 'function') {
    console.warn('leaflet.heat no disponible; se omite el mapa de calor.');
    return;
  }
  const points = feats.map(centroid).filter(Boolean).map(([lat, lng]) => [lat, lng, 0.8]);
  if (!points.length) return;
  heatLayer = L.heatLayer(points, { radius: 45, blur: 30, maxZoom: 13, minOpacity: 0.25 });
  if (document.getElementById('toggle-calor').checked) heatLayer.addTo(map);
}

function buildFilterButtons() {
  const container = document.getElementById('lista-filtros');
  container.innerHTML = '';

  const todas = document.createElement('button');
  todas.className = 'filter-btn active';
  todas.textContent = 'Todas las localidades';
  todas.onclick = () => resetView(todas);
  container.appendChild(todas);

  const names = [...new Set(features.map(nombreOf))].sort((a, b) => a.localeCompare(b, 'es'));
  names.forEach((name) => {
    const btn = document.createElement('button');
    btn.className = 'filter-btn';
    btn.textContent = name;
    btn.dataset.nombre = name;
    btn.onclick = () => focusLocalidad(name, btn);
    container.appendChild(btn);
  });
}

function resetView(btn) {
  setActive(btn);
  geoLayer.eachLayer((l) => l.setStyle({ fillOpacity: 0.45 }));
  map.closePopup();
  const bounds = geoLayer.getBounds();
  if (bounds.isValid()) map.fitBounds(bounds, { padding: [20, 20] });
}

function focusLocalidad(name, btn) {
  setActive(btn);
  geoLayer.eachLayer((l) => l.setStyle({ fillOpacity: 0.12 }));
  const layer = layersByName.get(name);
  if (!layer) return;
  layer.setStyle({ fillOpacity: 0.75 });
  layer.bringToFront();
  map.fitBounds(layer.getBounds(), { padding: [40, 40], maxZoom: 14 });
  layer.openPopup();
}

function setActive(btn) {
  document.querySelectorAll('.filter-btn').forEach((b) => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
}

function wireSearch() {
  const input = document.getElementById('buscador');
  input.addEventListener('input', () => {
    const q = input.value.trim().toLowerCase();
    document.querySelectorAll('#lista-filtros .filter-btn[data-nombre]').forEach((btn) => {
      btn.style.display = btn.dataset.nombre.toLowerCase().includes(q) ? 'block' : 'none';
    });
  });
}

function wireHeatToggle() {
  const toggle = document.getElementById('toggle-calor');
  toggle.addEventListener('change', () => {
    if (!heatLayer) return;
    if (toggle.checked) heatLayer.addTo(map);
    else map.removeLayer(heatLayer);
  });
}