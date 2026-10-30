#!/usr/bin/env python3
"""Validate the new entry points and symmetric locale navigation."""
from pathlib import Path
from bs4 import BeautifulSoup
from publication_layout import localized
ROOT=Path(__file__).resolve().parents[1]
for file,target in [('index.html','/niil/'),('niil/index.html','/niil/ko/')]:
 doc=BeautifulSoup((ROOT/file).read_text(),'html.parser')
 assert doc.select_one('meta[http-equiv="refresh"]')['content']=='0;url='+target
 assert 'location.search+location.hash' in (ROOT/file).read_text()
for language in ('ko','en'):
 for name in ('index.html','courses/index.html','members/index.html','research/index.html'):
  path=f'niil/{language}/{name}'
  doc=BeautifulSoup((ROOT/path).read_text(),'html.parser')
  assert doc.html['lang']==language,path
  links=doc.select('.language-switch a')
  assert [a['data-language'] for a in links]==['ko','en'],path
  logical='/'+path
  if name.endswith('index.html'):logical=logical.removesuffix('index.html')
  assert [a['href'] for a in links]==[localized(logical,l) for l in ('ko','en')],path
  assert doc.select_one(f'#site-nav a[href="/niil/{language}/courses/"]'),path
assert not (ROOT/'courses').exists() and not (ROOT/'assets').exists()
assert not (ROOT/'niil/courses').exists()
print('PASS: root/default entries, symmetric KO/EN navigation; retired top-level routes removed')
