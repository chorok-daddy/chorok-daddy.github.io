#!/usr/bin/env python3
"""Verify publication ownership, shared assets and the locale path contract."""
import json,re,subprocess
from pathlib import Path
from urllib.parse import unquote
from site_layout import ROOT,SITE,owns
from publication_layout import localized,browser_script

def main():
 expected=set(json.loads((ROOT/'tools/site-output.json').read_text())['html'])
 actual={p.relative_to(ROOT).as_posix() for p in SITE.rglob('*.html') if owns(p.relative_to(ROOT).as_posix())}
 assert expected==actual,('Unexpected/missing lab output',sorted(actual^expected))
 assert {p.name for p in SITE.iterdir() if p.is_dir()}=={'assets','content','ko','en'}
 for name in ['courses','assets','release.json','site-catalog.json','tools/course-compatibility.json','tools/legacy-routes.json']:assert not (ROOT/name).exists(),name
 routes=json.loads((SITE/'content/routes.json').read_text());members=json.loads((SITE/'content/members.json').read_text());projects=json.loads((SITE/'content/projects.json').read_text())
 assert set(routes)=={m['id'] for m in members}|{p['page_id'] for p in projects}
 for path in routes.values():
  for lang in ('ko','en'):assert (ROOT/localized(path,lang).lstrip('/')/'index.html').is_file(),path
 all_media={'/'+p.relative_to(ROOT).as_posix() for p in (SITE/'assets/media').iterdir() if p.is_file()};used=set()
 for p in SITE.rglob('*'):
  if p.is_file() and p.suffix in ('.html','.json','.md','.css','.js'):
   used.update(unquote(v) for v in re.findall(r'/niil/assets/media/[A-Za-z0-9_%().-]+',p.read_text()))
 assert not all_media-used,('Unreferenced media',all_media-used)
 assert (SITE/'assets/routes.js').read_text()==browser_script()
 tests=[]
 for name in expected:
  if name=='niil/index.html':continue
  for lang in ('ko','en'):tests.append(['/'+name+'?runtime=matlab#main',lang,localized('/'+name+'?runtime=matlab#main',lang)])
 tests.append(['/niil/assets/courses/site.css','en','/niil/assets/courses/site.css'])
 command="global.location={href:'https://example.test/niil/ko/',origin:'https://example.test'};const {localized}=require('./niil/assets/routes.js');for(const [p,l,want] of JSON.parse(require('fs').readFileSync(0,'utf8'))){if(localized(p,l)!==want)throw Error(p);}"
 subprocess.run(['node','-e',command],cwd=ROOT,input=json.dumps(tests),text=True,check=True)
 assert not subprocess.check_output(['git','ls-files','*AGENTS.md'],cwd=ROOT,text=True).strip()
 print(f'PASS: {len(expected)} owned pages, {len(routes)} records, {len(all_media)} media; {len(tests)} shared Python/browser route cases')
if __name__=='__main__':main()
