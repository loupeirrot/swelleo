// Service worker SurfAlert — cache hors-ligne (app shell) + data.json frais en ligne.
const CACHE = 'swelleo-v11';
const SHELL = [
  './', './index.html', './manifest.json',
  './assets/icon-192.png', './assets/icon-512.png',
  './assets/wave-flat.webp', './assets/wave-clean.webp', './assets/wave-epic.webp',
  './assets/wave-golden.webp', './assets/wave-messy.webp', './assets/wave-night.webp'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => Promise.all(SHELL.map(u => c.add(u).catch(() => null))))  // un 404 ne bloque pas
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // data.json : réseau d'abord (données fraîches), cache en secours hors-ligne
  if (url.pathname.endsWith('/data.json')) {
    e.respondWith(
      fetch(req).then(r => { const cp = r.clone(); caches.open(CACHE).then(c => c.put(req, cp)); return r; })
        .catch(() => caches.match(req))
    );
    return;
  }

  // navigation : page fraîche en ligne, index.html en secours hors-ligne
  if (req.mode === 'navigate') {
    e.respondWith(fetch(req).catch(() => caches.match('./index.html')));
    return;
  }

  // reste (images, polices…) : cache d'abord
  e.respondWith(caches.match(req).then(c => c || fetch(req)));
});
