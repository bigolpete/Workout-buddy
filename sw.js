/* LiftLog service worker: lets the app open with no signal (e.g. a basement gym).
 * The page itself is fetched network-first, so updates you push show up the next
 * time you open the app online; it falls back to the saved copy when offline.
 * Your workout data is NOT stored here. It lives in the browser's localStorage.
 * Bump VERSION when you add or rename files below. */
const VERSION = 'liftlog-v1';
const FILES = ['./', './index.html', './manifest.webmanifest', './icons/icon-192.png', './icons/icon-512.png', './icons/apple-touch-icon.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(VERSION).then((c) => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim()),
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;

  if (req.mode === 'navigate') {
    // network first: get the latest version, keep a copy for offline use
    e.respondWith(
      fetch(req)
        .then((res) => { const copy = res.clone(); caches.open(VERSION).then((c) => c.put('./index.html', copy)); return res; })
        .catch(() => caches.match('./index.html')),
    );
    return;
  }
  // icons and manifest: saved copy first
  e.respondWith(caches.match(req).then((hit) => hit || fetch(req)));
});
