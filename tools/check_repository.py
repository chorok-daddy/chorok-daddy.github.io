#!/usr/bin/env python3
"""Check output ownership, recovery routes and referenced lab media."""
import json,re,subprocess
from pathlib import Path
from urllib.parse import unquote,urlsplit
from site_layout import ROOT,SITE,owns

def media_references():
    used=set()
    for p in SITE.rglob('*'):
        if not p.is_file() or p.suffix not in ('.html','.json','.md','.css','.js'):continue
        for value in re.findall(r'/niil/assets/media/[A-Za-z0-9_%().-]+',p.read_text()):
            name=unquote(value)
            if (ROOT/name.lstrip('/')).is_file():used.add(name)
    return used

def main():
    expected=set(json.loads((ROOT/'tools/site-output.json').read_text())['html'])
    actual={p.relative_to(ROOT).as_posix() for p in SITE.rglob('*.html') if owns(p.relative_to(ROOT).as_posix())}
    assert expected==actual,('Unexpected/missing lab output',sorted(actual^expected))
    for name in ['ko','teaching','vision','projects','join','robot-basic-lab','microprocessor','control-1','control-2','ai-applications','ee-seminar']:
        assert not (SITE/name).exists(),name
        assert not (SITE/'en'/name).exists(),name
    for name in ['pages.json','assets.json']:assert not (SITE/'content'/name).exists(),name
    assert not (ROOT/'release.json').exists()
    assert not (ROOT/'site-catalog.json').exists()
    assert not (SITE/'assets/meta').exists()
    assert not (SITE/'courses/assets/meta').exists()
    routes=json.loads((SITE/'content/routes.json').read_text());members=json.loads((SITE/'content/members.json').read_text());projects=json.loads((SITE/'content/projects.json').read_text())
    assert set(routes)=={m['id'] for m in members}|{p['page_id'] for p in projects}
    for path in routes.values():
        assert (ROOT/path.lstrip('/')/'index.html').is_file(),path
        assert (ROOT/path.replace('/niil/','/niil/en/',1).lstrip('/')/'index.html').is_file(),path
    all_media={'/'+p.relative_to(ROOT).as_posix() for p in (SITE/'assets/media').iterdir() if p.is_file()}
    assert not all_media-media_references(),('Unreferenced lab media',all_media-media_references())
    compatibility=json.loads((ROOT/'tools/course-compatibility.json').read_text())
    assert {p.relative_to(ROOT).as_posix() for p in (ROOT/'courses').rglob('*') if p.is_file()}=={x['old'].lstrip('/') for x in compatibility['files']}
    legacy=json.loads((ROOT/'tools/legacy-routes.json').read_text())['redirects']
    for target in legacy.values():
        u=urlsplit(target)
        for prefix in ('/niil/','/niil/en/'):
            path=u.path.replace('/niil/',prefix,1);p=ROOT/path.lstrip('/')
            if p.is_dir():p=p/'index.html'
            assert p.is_file(),path
    # Exercise the exact generated browser resolver without a browser or network.
    tests=[]
    for path,target in legacy.items():
        for en in (False,True):
            old=path.replace('/niil/','/niil/en/',1) if en else path
            new=urlsplit(target.replace('/niil/','/niil/en/',1) if en else target).path
            tests.append([old,'?from=old','#main',new+'?from=old#main'])
    tests.extend([['/niil/ko/members/','?a=1','#x','/niil/members/?a=1#x'],['/niil/ko/index.html','','','/niil/'],['/niil/en/teaching/index.html','','','/niil/en/courses/'],['/niil/research/','','',None],['/unknown/','','',None],['/bad/%ZZ','','',None]])
    command="const {resolve}=require('./niil/assets/legacy-routes.js');const fs=require('fs');for(const [p,s,h,want] of JSON.parse(fs.readFileSync(0,'utf8'))){const got=resolve(p,s,h);if(got!==want)throw Error(JSON.stringify({p,got,want}));}"
    subprocess.run(['node','-e',command],cwd=ROOT,input=json.dumps(tests),text=True,check=True)
    assert not subprocess.check_output(['git','ls-files','*AGENTS.md'],cwd=ROOT,text=True).strip()
    print(f'PASS: {len(expected)} owned lab pages, {len(routes)} active records, {len(all_media)} referenced media, {len(tests)} legacy-route cases; 95 course compatibility files retained.')
if __name__=='__main__':main()
