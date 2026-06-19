// Service Worker —— PWA 离线缓存核心
// 策略：核心资源预缓存（cache-first），其它请求回退到网络

var CACHE = 'panorama-v1';

// 应用外壳：这些资源会被预缓存，断网时也能完整加载
var PRECACHE_URLS = [
  './',
  './index.html',
  './manifest.json',
  './lib/pannellum.js',
  './lib/pannellum.css',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-maskable-512.png',
  './icons/favicon-32.png'
];

// 安装：预缓存应用外壳
self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(CACHE).then(function (cache) {
      // 用 addAll，任一失败会让安装失败 —— 但我们忽略个别图标失败
      return cache.addAll(PRECACHE_URLS).catch(function (e) {
        console.warn('[SW] 部分资源预缓存失败（可能尚未部署），忽略:', e);
      });
    }).then(function () {
      // 立即接管，不必等旧 SW 释放
      return self.skipWaiting();
    })
  );
});

// 激活：清理旧缓存
self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys.filter(function (k) { return k !== CACHE; })
            .map(function (k) { return caches.delete(k); })
      );
    }).then(function () { return self.clients.claim(); })
  );
});

// 请求拦截
self.addEventListener('fetch', function (event) {
  var req = event.request;

  // 只处理同源的 GET 请求；跨域资源（如示例图 CDN）直接放行
  if (req.method !== 'GET') return;
  var url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  // blob:/data:（用户选的本地全景图）浏览器自己处理，SW 不碰
  if (url.protocol === 'blob:' || url.protocol === 'data:') return;

  // 缓存优先：有就用缓存，没有再去网络并缓存结果
  event.respondWith(
    caches.match(req).then(function (cached) {
      if (cached) return cached;
      return fetch(req).then(function (resp) {
        // 只缓存成功的、同源的基本响应
        if (resp && resp.status === 200 && resp.type === 'basic') {
          var copy = resp.clone();
          caches.open(CACHE).then(function (c) { c.put(req, copy); });
        }
        return resp;
      }).catch(function () {
        // 离线且没缓存：对于导航请求返回主页
        if (req.mode === 'navigate') {
          return caches.match('./index.html');
        }
      });
    })
  );
});

// 让新版本立即生效
self.addEventListener('message', function (event) {
  if (event.data === 'SKIP_WAITING') self.skipWaiting();
});
