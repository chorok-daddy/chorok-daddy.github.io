#!/usr/bin/env python3
"""Validate imported course assets and the single-repository navigation contract."""
import hashlib,json
from pathlib import Path
from urllib.parse import urlsplit,parse_qs
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
lock=json.loads((ROOT/'tools/course-source.json').read_text())
assert lock['repository']=='https://github.com/chorok-daddy/courses'
assert len(lock['revision'])==40
checked=0
for name,digest in lock['files'].items():
    p=ROOT/name;assert p.is_file(),name
    # HTML receives the website frame and metadata after importing.
    if p.suffix!='.html':
        assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,name
        checked+=1
for lang in ('ko/','en/'):
    doc=BeautifulSoup((ROOT/('niil/'+lang+'courses/index.html')).read_text(),'html.parser')
    repository='https://github.com/chorok-daddy/'+('courses_en' if lang=='en/' else 'courses')
    assert len(doc.select(f'main a[href="{repository}"]'))==1
    assert not doc.select('main a[href$=".zip"]')
    assert not doc.select('main a[href*="github.com/chorok-daddy/course-"]')
catalog=json.loads((ROOT/'tools/course-catalog.json').read_text())
for course in catalog['courses']:
    if not course['published']:continue
    p=ROOT/'niil/ko/courses'/course['slug']/'index.html'
    doc=BeautifulSoup(p.read_text(),'html.parser')
    links=doc.select('main a[href*="github.com/chorok-daddy/courses"]')
    assert len(links)==int(course.get('zip_enabled',True) and bool(course.get('chapters') or course.get('lessons')))
    if links:assert links[0].has_attr('data-course-download')
    assert doc.select_one('header a[href="/niil/ko/courses/"]')
    assert not doc.select('a[href$="/main.zip"]')
print(f'PASS: source revision, {checked} unchanged imports, single-repository navigation')

# Every depth has real corresponding Korean and English documents.
framed=0
for prefix in ['niil/ko/courses','niil/en/courses']:
    for file in (ROOT/prefix).rglob('*.html'):
        if file.name=='reuse.html' or file==ROOT/prefix/'index.html':continue
        doc=BeautifulSoup(file.read_text(),'html.parser')
        if not doc.body or doc.select_one('meta[http-equiv="refresh"]'):continue
        menu=doc.select_one('.language-switch');assert menu,file
        links=menu.select('[data-course-language]');assert [a['data-course-language'] for a in links]==['ko','en'],file
        path='/'+file.relative_to(ROOT).as_posix();korean=path.replace('/niil/en/courses/','/niil/ko/courses/',1);english=korean.replace('/niil/ko/courses/','/niil/en/courses/',1)
        assert [urlsplit(a['href']).path for a in links]==[korean,english],file
        assert all((ROOT/urlsplit(a['href']).path.lstrip('/')).is_file() for a in links),file
        assert doc.html['lang']==('en' if prefix.startswith('niil/en/') else 'ko'),file
        assert doc.select_one('script[src*="routes.js"]'),file
        if prefix.startswith('niil/en/'):
            for a in doc.select('a[download][href]'):
                if urlsplit(a['href']).path.endswith(('.ipynb','.mlx')):assert urlsplit(a['href']).path.startswith('/niil/en/courses/'),(file,a)
            for a in doc.select('[data-colab-url]'):
                assert '/github/chorok-daddy/courses_en/blob/main/' in a['data-colab-url'],(file,a)
            for a in doc.select('[data-matlab-url]'):
                assert parse_qs(urlsplit(a['data-matlab-url']).query).get('repo')==['chorok-daddy/courses_en'] and not parse_qs(urlsplit(a['data-matlab-url']).query).get('file',[''])[0].startswith('en/'),(file,a)
        framed+=1
english=BeautifulSoup((ROOT/'niil/en/courses/index.html').read_text(),'html.parser')
for link in english.select('.course-card-link'):assert urlsplit(link['href']).path.startswith('/niil/en/courses/'),link
import subprocess
assert not any(Path(n).name.lower()=='agents.md' for n in subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()),'AGENTS.md must stay local'
print(f'PASS: real-language bodies and same-locale preview/download/run routes on {framed} framed course pages')

# Native documents also carry public links (including dataset fallbacks in code).
# Moving shared assets must not leave valid HTML with broken notebook/MLX URLs.
import re,html,zipfile
from urllib.parse import unquote
native_links=0
for language in ('ko','en'):
    for file in (ROOT/'niil'/language/'courses').rglob('*'):
        if file.suffix=='.ipynb':
            raw='\n'.join(''.join(c['source']) for c in json.loads(file.read_text())['cells'])
        elif file.suffix=='.mlx':
            with zipfile.ZipFile(file) as archive:raw=archive.read('matlab/document.xml').decode()
        else:continue
        for value in re.findall(r'https?://chorok-daddy.github.io[^\s<>"\x27\)]+',raw):
            u=urlsplit(html.unescape(value));path=unquote(u.path)
            target=ROOT/path.lstrip('/')
            if path.endswith('/'):target=target/'index.html'
            assert target.is_file(),(file,value)
            assert path.startswith(('/niil/assets/','/niil/'+language+'/')),(file,value)
            native_links+=1
print(f'PASS: {native_links} native document/data URLs exist and retain their language')
