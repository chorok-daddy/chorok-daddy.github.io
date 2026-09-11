#!/usr/bin/env python3
"""Offline structural checks; no network or student-code execution."""
import argparse,json,subprocess
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote

class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=set();self.refs=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        for key in ('href','src'):
            if a.get(key):self.refs.append(a[key])

def check(root,public=None):
    root=Path(root).resolve();public=Path(public).resolve() if public else None
    errors=[];external=set();pages={};counts={'html':0,'notebook':0,'links':0}
    for p in root.rglob('*'):
        if any(x.startswith('.') for x in p.relative_to(root).parts):continue
        if p.suffix=='.html':
            try:pages[p.resolve()]=Page(p.read_text())
            except (UnicodeError,ValueError) as e:errors.append(f'{p}: {e}')
        elif p.suffix=='.ipynb':
            counts['notebook']+=1
            try:
                nb=json.loads(p.read_text());assert nb['nbformat']==4 and isinstance(nb['cells'],list)
                for cell in nb['cells']:
                    assert cell['cell_type'] in ('code','markdown','raw')
                    assert isinstance(cell['source'],(list,str))
            except (ValueError,KeyError,AssertionError) as e:errors.append(f'{p}: invalid notebook {e}')
    counts['html']=len(pages)
    for p,page in pages.items():
        for ref in page.refs:
            u=urlsplit(ref)
            if u.scheme in ('mailto','tel','data','javascript'):continue
            base=root
            if u.netloc:
                if u.netloc=='chorok-daddy.github.io':base=public or root
                else:external.add(ref);continue
            target=(base/unquote(u.path).lstrip('/')) if u.path.startswith('/') or u.netloc else (p.parent/unquote(u.path) if u.path else p)
            target=target.resolve()
            if target.is_dir():target=target/'index.html'
            counts['links']+=1
            if not target.exists():errors.append(f'{p.relative_to(root)}: missing {ref}');continue
            if u.fragment and target.suffix=='.html':
                if target not in pages:
                    try:pages_for_target=Page(target.read_text())
                    except (ValueError,UnicodeError):continue
                else:pages_for_target=pages[target]
                if unquote(u.fragment) not in pages_for_target.ids:errors.append(f'{p.relative_to(root)}: missing anchor {ref}')
    return {'counts':counts,'errors':sorted(set(errors)),'external_links_not_checked':len(external)}

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--public-root',type=Path);a=ap.parse_args()
    result=check(a.root.resolve(),a.public_root.resolve() if a.public_root else None)
    print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(bool(result['errors']))
