/* Old lab addresses resolve here instead of duplicating published directories. */
(() => {
  const routes = __LEGACY_ROUTES__;
  function resolve(path, search = '', hash = '') {
    try { path = decodeURIComponent(path); } catch (_) { return null; }
    const oldKorean = path.startsWith('/niil/ko/');
    if (oldKorean) path = path.replace('/niil/ko/', '/niil/');
    const english = path.startsWith('/niil/en/');
    let key = english ? path.replace('/niil/en/', '/niil/') : path;
    key = key.replace(/index\.html$/, '');
    if (!key.endsWith('/') && !key.split('/').pop().includes('.')) key += '/';
    let target = routes[key];
    if (!target && !oldKorean) return null;
    if (!target) target = english ? key.replace('/niil/', '/niil/en/') : key;
    else if (english) target = target.replace('/niil/', '/niil/en/');
    const url = new URL(target, 'https://chorok-daddy.github.io');
    if (search) url.search = search;
    if (hash) url.hash = hash;
    return url.pathname + url.search + url.hash;
  }
  if (typeof module !== 'undefined') module.exports = {resolve, routes};
  if (typeof window === 'undefined') return;
  const target = resolve(location.pathname, location.search, location.hash);
  if (target) { location.replace(target); return; }
  if (location.pathname.startsWith('/niil/en/')) {
    document.documentElement.lang = 'en';
    document.title = 'Page not found · NiiL';
    document.querySelectorAll('[data-label-en]').forEach(el => { el.textContent = el.dataset.labelEn; });
    document.querySelectorAll('a[data-localized]').forEach(el => { el.href = el.getAttribute('href').replace('/niil/', '/niil/en/'); });
  }
})();
