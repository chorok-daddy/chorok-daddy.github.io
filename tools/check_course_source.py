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
for lang in ('','en/'):
    doc=BeautifulSoup((ROOT/('niil/'+lang+'courses/index.html')).read_text(),'html.parser')
    assert len(doc.select('main a[href="https://github.com/chorok-daddy/courses"]'))==1
    assert not doc.select('main a[href$=".zip"]')
    assert not doc.select('main a[href*="github.com/chorok-daddy/course-"]')
catalog=json.loads((ROOT/'tools/course-catalog.json').read_text())
for course in catalog['courses']:
    if not course['published']:continue
    p=ROOT/'niil/courses'/course['slug']/'index.html'
    doc=BeautifulSoup(p.read_text(),'html.parser')
    links=doc.select('main a[href*="github.com/chorok-daddy/courses"]')
    assert len(links)==int(course.get('zip_enabled',True) and bool(course.get('chapters') or course.get('lessons')))
    if links:assert links[0].has_attr('data-course-download')
    assert doc.select_one('header a[href="/niil/courses/"]')
    assert not doc.select('a[href$="/main.zip"]')
print(f'PASS: source revision, {checked} unchanged imports, single-repository navigation')

# Original teaching documents keep the same language selector at every depth.
framed=0
for file in (ROOT/'niil/courses').rglob('*.html'):
    if file.name=='reuse.html' or file==ROOT/'niil/courses/index.html':continue
    doc=BeautifulSoup(file.read_text(),'html.parser')
    if not doc.body or doc.select_one('meta[http-equiv="refresh"]'):continue
    menu=doc.select_one('.language-switch');assert menu,file
    links=menu.select('[data-course-language]');assert [a['data-course-language'] for a in links]==['ko','en'],file
    path='/'+file.relative_to(ROOT).as_posix()
    assert all(urlsplit(a['href']).path==path for a in links),file
    assert parse_qs(urlsplit(links[1]['href']).query).get('lang')==['en'],file
    assert doc.select_one('script[src*="course-language.js"]'),file
    framed+=1
english=BeautifulSoup((ROOT/'niil/en/courses/index.html').read_text(),'html.parser')
for link in english.select('.course-card-link'):
    assert parse_qs(urlsplit(link['href']).query).get('lang')==['en'],link
print(f'PASS: persistent same-document language controls on {framed} course pages and English catalog entry links')
