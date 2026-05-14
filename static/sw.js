const CACHE_NAME = 'vibe-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/static/bootstrap-5.3.8/css/bootstrap.min.css',
  '/static/bootstrap-5.3.8/js/bootstrap.bundle.min.js',
  '/static/css/mapa.css',
  '/static/js/mapa.js',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
  'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css'
];

// Instalação e cache inicial
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('Arquivos em cache!');
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
});

// Estratégia de Cache-First com atualização dinâmica
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      // Se encontrar no cache, retorna imediatamente (TTL Ativo)
      if (cachedResponse) {
        return cachedResponse;
      }

      // Se não estiver no cache, busca na rede e guarda para a próxima vez
      return fetch(event.request).then((networkResponse) => {
        // Verifica se a resposta é válida antes de cachear
        if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
          return networkResponse;
        }

        const responseToCache = networkResponse.clone();
        caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, responseToCache);
        });

        return networkResponse;
      });
    })
  );
});
