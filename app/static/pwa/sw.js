const CACHE_NAME = 'ntl-pwa-cache-0.0.8';
const FILES_TO_CACHE = [
    '/static/pwa/pages/index.html',
    '/static/pwa/pages/home.html',
    '/static/pwa/pages/schedule.html',
    '/static/pwa/pages/podcasts.html',
    '/static/pwa/pages/broadcastSchedule.html',
    '/static/pwa/pages/programGuide.html',
    '/static/pwa/js/app.js',
    '/static/pwa/img/NTL_new-192.png',
    '/static/pwa/img/NTL_new-512.png',
];

// Install — cache all static assets
self.addEventListener('install', (event) => {
  console.log('[ServiceWorker] Install');
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[ServiceWorker] Caching app shell');
      return cache.addAll(FILES_TO_CACHE);
    })
  );
  self.skipWaiting();
});

// Activate — clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[ServiceWorker] Activate');
  event.waitUntil(
    caches.keys().then((keyList) =>
      Promise.all(
        keyList.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[ServiceWorker] Removing old cache:', key);
            return caches.delete(key);
          }
        })
      )
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request, { ignoreSearch: true })
      .then(cached => cached || fetch(event.request))
      .catch(() => {
        // Fallback: Show home page if nothing is found and request is HTML
        if (event.request.headers.get('accept').includes('text/html')) {
          return caches.match('/static/pwa/pages/home.html');
        }
      })
  );
});

