/* Generated from tools/publication-layout.json. */
(() => {
  const layout = {"root":"/niil/","languages":["ko","en"],"default_language":"ko","course_assets":"/niil/assets/courses/"};
  function localized(value, language) {
    const url = new URL(value, location.href);
    if (url.origin !== location.origin) return url.href;
    let path = url.pathname;
    for (const code of layout.languages) {
      const prefix = layout.root + code + '/';
      if (path.startsWith(prefix)) { path = layout.root + path.slice(prefix.length); break; }
    }
    if (path.startsWith(layout.root) && !path.startsWith(layout.root+'assets/') && !path.startsWith(layout.root+'content/'))
      path = layout.root + language + '/' + path.slice(layout.root.length);
    return path + url.search + url.hash;
  }
  const api = {localized};
  if (typeof module !== 'undefined') module.exports = api;
  else window.NiiLRoutes = api;
})();
