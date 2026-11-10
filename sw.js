/* Daily Observer — makes the site installable as an app. Caches nothing: every load is fresh from GitHub.
   Also receives the alerts for the Setups app (Web Push from the tv-signal function) and shows them as notifications. */
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', e => { e.respondWith(fetch(e.request)); });

self.addEventListener('push', e => {
  let d = {};
  try { d = e.data ? e.data.json() : {}; } catch (_) { d = { title: 'Daily Observer', body: e.data ? e.data.text() : '' }; }
  const base = new URL('./index.html?app=setups', self.registration.scope).href;
  const opts = {
    body: d.body || '',
    icon: 'icon-setups-192.png',
    badge: 'badge-setups.png',
    tag: d.tag || undefined,
    renotify: !!d.tag,
    vibrate: [180, 80, 180],
    timestamp: d.ts || Date.now(),
    data: { url: d.url || base, chart: d.chart || '' },
    actions: d.chart ? [{ action: 'chart', title: '📈 Chart' }, { action: 'open', title: 'Setups' }] : []
  };
  e.waitUntil(self.registration.showNotification(d.title || 'Daily Observer', opts));
});

self.addEventListener('notificationclick', e => {
  e.notification.close();
  const { url, chart } = e.notification.data || {};
  const target = e.action === 'chart' && chart ? chart : (url || new URL('./index.html?app=setups', self.registration.scope).href);
  e.waitUntil((async () => {
    if (target !== chart) {
      const all = await self.clients.matchAll({ type: 'window', includeUncontrolled: true });
      const app = all.find(c => c.url.includes('app=setups'));
      if (app) { await app.focus(); try { await app.navigate(target); } catch (_) {} return; }
    }
    await self.clients.openWindow(target);
  })());
});

/* the phone rotated the subscription → the app saves the new one next time it opens */
self.addEventListener('pushsubscriptionchange', () => {});
