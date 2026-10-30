"""Physical publication paths shared by course export and the laboratory site."""
import json,posixpath
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit,unquote

LAYOUT=json.loads(Path(__file__).with_name('publication-layout.json').read_text())
BASE=LAYOUT['root']
def neutral(path):
    for language in LAYOUT['languages']:
        prefix=BASE+language+'/'
        if path.startswith(prefix):return BASE+path[len(prefix):]
    return path
def localized(value,language):
    assert language in LAYOUT['languages']
    u=urlsplit(value)
    if u.netloc and u.netloc!='chorok-daddy.github.io':return value
    path=neutral(u.path)
    if path.startswith(BASE) and not path.startswith((BASE+'assets/',BASE+'content/')):
        path=BASE+language+'/'+path[len(BASE):]
    return urlunsplit((u.scheme,u.netloc,path,u.query,u.fragment))
def course_url(path='',language='ko'):
    return BASE+language+'/courses/'+path
def shared_course(path):
    return LAYOUT['course_assets']+path.removeprefix('assets/')
def shared_file(path):
    return Path(path).suffix.lower() not in ('.html','.ipynb','.mlx','.md','.cff','.zip')
def course_file(path,language='ko'):
    return shared_course(path) if shared_file(path) else course_url(path,language)
def source_path(path):
    if path.startswith(LAYOUT['course_assets']):
        tail=path.removeprefix(LAYOUT['course_assets'])
        return 'assets/'+tail if (Path(__file__).resolve().parents[1]/'assets'/tail).is_file() else tail
    for language in LAYOUT['languages']:
        if path.startswith(course_url(language=language)):return path.removeprefix(course_url(language=language)) or 'index.html'
    return None

def browser_script():
    return '''/* Generated from tools/publication-layout.json. */
(() => {
  const layout = '''+json.dumps(LAYOUT,separators=(',',':'))+''';
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
'''
