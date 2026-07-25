// sw.js

// Bump this version number every time you update your app files.
// Changing it forces browsers to install a fresh service worker and re-cache everything.
const CACHE_NAME = 'mumtal-care-v1';

// List every file your app needs to run with zero internet.
const FILES_TO_CACHE = [
  './',
  './index.html',
  './app.js',
  './manifest.json',
  './ppd_model.onnx',
  './ort.min.js',
  './ort-wasm-simd-threaded.wasm',
  './ort-wasm-simd-threaded.jsep.mjs',
  './logo.png',
  './favicon.ico'
];

// 'install' fires once, the first time the browser loads this service worker.
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[SW] Caching app files for offline use');
      return cache.addAll(FILES_TO_CACHE);
    })
  );
  self.skipWaiting(); // activate this new service worker immediately, don't wait for old tabs to close
});

// 'activate' fires after install — good place to delete old caches from previous versions.
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name))
      );
    })
  );
  self.clients.claim();
});

// 'fetch' fires every time the app requests a file (a script, the model, an image, etc).
// This is what actually makes the app work offline.
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      // If we have it cached, serve the cached version instantly.
      if (cachedResponse) {
        return cachedResponse;
      }
      // Otherwise try the network (e.g. first load), and fall back gracefully if offline.
      return fetch(event.request).catch(() => {
        // Optional: you could return a fallback page here if a file is missing offline.
      });
    })
  );
});