#!/usr/bin/env python3
"""Regression checks for public URL and download compatibility."""
import hashlib
import json
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'tools/course-compatibility.json').read_text())
pages = downloads = 0
for item in manifest['files']:
    old = ROOT / item['old'].lstrip('/')
    new = ROOT / item['new'].lstrip('/')
    assert old.is_file() and new.is_file(), item['old']
    if item['kind'] == 'download':
        assert hashlib.sha256(old.read_bytes()).hexdigest() == item['sha256'], old
        assert old.read_bytes() == new.read_bytes(), new
        downloads += 1
        continue
    alias = BeautifulSoup(old.read_text(), 'html.parser')
    target=item['new']
    if new.name=='files.html':target='/'+new.parent.relative_to(ROOT).as_posix()+'/index.html'
    assert alias.select_one('meta[http-equiv="refresh"]')['content'] == '0;url=' + target, old
    assert 'location.search+location.hash' in old.read_text(), old
    new_page = BeautifulSoup(new.read_text(), 'html.parser')
    if new.name=='files.html':
        assert new_page.select_one('meta[http-equiv="refresh"]')['content']=='0;url=index.html'
        new_page=BeautifulSoup((new.parent/'index.html').read_text(),'html.parser')
    assert set(item['anchors']) <= {x['id'] for x in new_page.select('[id]')}, new
    homes = new_page.select('a[href="/niil/courses/"]:not([data-language])')
    assert len(homes) == 1 and homes[0].get_text() == '강의자료', new
    assert new_page.select_one('.site-header #site-nav') and new_page.select_one('footer'), new
    assert not new_page.select('a[href="/"]'), new
    assert not new_page.select('[href^="/courses/"], [src^="/courses/"]'), new
    assert not new_page.select('a[href*="blob/master/courses/"]'), new
    pages += 1

root = BeautifulSoup((ROOT / 'index.html').read_text(), 'html.parser')
assert root.select_one('meta[http-equiv="refresh"]')['content'] == '0;url=/niil/'
for lang, prefix in [('ko', 'niil'), ('en', 'niil/en')]:
    page = BeautifulSoup((ROOT / prefix / 'index.html').read_text(), 'html.parser')
    assert page.html['lang'] == lang
    assert [a['data-language'] for a in page.select('.language-switch a')] == ['ko', 'en']
    assert page.select_one('#site-nav a[href="'+('/niil/courses/' if lang=='ko' else '/niil/en/courses/')+'"]')
    assert page.select_one('[data-language="ko"]')['href'] == '/niil/'
    assert page.select_one('[data-language="en"]')['href'] == '/niil/en/'
print(json.dumps({'legacy_pages': pages, 'byte_identical_downloads': downloads,
                  'languages': ['ko', 'en'], 'errors': []}, ensure_ascii=False, indent=2))
