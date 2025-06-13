const CACHE_NAME = 'ntl-pwa-cache-0.1.22';
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

self.addEventListener('message', (event) => {
  if (event.data && event.data.action === 'skipWaiting') {
    self.skipWaiting();
  }
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
    ).then(() => {
      return self.clients.claim();  // ✅ moved inside
    })
  );
});


self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);
  if (url.pathname.startsWith('/stream/')) return; // Don't cache or intercept livestream

  event.respondWith(
    caches.match(event.request, { ignoreSearch: true }).then(cached => {
      if (cached) {
        console.log('[SW] Serving from cache:', event.request.url);
        return cached;
      }
      console.log('[SW] Fetching from network:', event.request.url);
      return fetch(event.request).then(response => {
        return caches.open(CACHE_NAME).then(cache => {
          cache.put(event.request, response.clone());
          return response;
        });
      });
    }).catch(() => {
      console.log('[SW] Fetch failed; returning fallback for:', event.request.url);
      if (event.request.headers.get('accept').includes('text/html')) {
        return caches.match('/static/pwa/pages/home.html');
      }
    })
  );
});

