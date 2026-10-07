const APP = 'app-v6', TILES = 'tiles-v6', MAX_TILES = 2500;
const SHELL = ['./', 'index.html', 'data.json', 'manifest.webmanifest', 'apple-touch-icon.png', 'icon-192.png',
  'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css',
  'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js'];
self.addEventListener('install', e => { e.waitUntil(caches.open(APP).then(c => c.addAll(SHELL))); self.skipWaiting(); });
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== APP && k !== TILES).map(k => caches.delete(k)))));
  self.clients.claim();
});
async function trim(){ const c = await caches.open(TILES), ks = await c.keys(); for (let i = 0; i < ks.length - MAX_TILES; i++) await c.delete(ks[i]); }
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET') return;
  if (url.hostname.endsWith('tiles.stadiamaps.com')) {
    e.respondWith(caches.open(TILES).then(async c => {
      const hit = await c.match(e.request); if (hit) return hit;
      const res = await fetch(e.request); if (res.ok) { c.put(e.request, res.clone()); trim(); } return res;
    }));
    return;
  }
  // network first for app files and data, cache fallback when offline
  e.respondWith(fetch(e.request).then(res => {
    if (res.ok && (url.origin === location.origin || url.hostname.includes('cdnjs') || url.hostname.includes('fonts.g')))
      caches.open(APP).then(c => c.put(e.request, res.clone()));
    return res;
  }).catch(() => caches.match(e.request, {ignoreSearch: true})));
});
