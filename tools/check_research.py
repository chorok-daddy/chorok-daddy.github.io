#!/usr/bin/env python3
"""Check bilingual catalog/detail parity and research-output records."""
import json,re
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
def data(name):return json.loads((ROOT/'niil/content'/name).read_text())
def page(path):return BeautifulSoup((ROOT/path.lstrip('/')/'index.html').read_text(),'html.parser')
projects=data('projects.json');routes=data('routes.json');locales=data('project-locales.json')
for lang,prefix in [('ko','/niil/'),('en','/niil/en/')]:
 catalog=page(prefix+'research/')
 assert catalog.html['lang']==lang
 rows=catalog.select('[data-project]');assert len(rows)==len(projects)
 for p in projects:
  path=routes[p['page_id']].replace('/niil/',prefix,1)
  detail=page(path); row=next(x for x in rows if x.select_one('h2 a')['href']==path)
  expected=(locales[p['key']]['title_ko_short'] if lang=='ko' else p['title']) if p.get('title_kind')=='collection' else (p['title_ko'] if lang=='ko' else p.get('official_title_en') or p['translated_title_en']+' ('+p['title_ko']+')')
  assert detail.h1.get_text()==row.h2.get_text()==expected,(lang,p['key'])
  summary=p['summary'] if lang=='ko' else locales[p['key']]['summary_en']
  assert detail.select_one('.lede').get_text()==summary
  assert summary in row.get_text()
  target=routes[p['page_id']].replace('/niil/','/niil/en/',1) if lang=='ko' else routes[p['page_id']]
  assert detail.select_one('[data-language="'+('en' if lang=='ko' else 'ko')+'"]')['href']==target
  for a in detail.select('.title-source a'):
   if 'ntis.go.kr' in a['href']:assert a.get('target')=='_blank' and a.get_text()==('NTIS 링크' if lang=='ko' else 'NTIS link')
  if lang=='en':
   prose=BeautifulSoup(str(detail.select_one('.prose')),'html.parser')
   for table in prose.select('.project-phases table, .official-titles'):table.decompose()
   for related in prose.select('section'):related.decompose()
   assert not re.search('[가-힣]',prose.get_text()),(p['key'],'untranslated prose outside original-title annotations')
 for panel in catalog.select('.output-panel'):assert not panel.has_attr('open')
 ip=catalog.select('#intellectual-property tbody tr');transfers=catalog.select('#technology-transfer tbody tr')
 outputs=data('research-outputs.json')
 assert len(ip)==len(outputs['intellectual_property']) and len(transfers)==len(outputs['technology_transfers'])
 for record,row in zip(outputs['intellectual_property'],ip):
  assert record['title_'+lang] in row.get_text()
  for f in record['filings']:assert f['number'] in row.get_text() and f['date'] in row.get_text()
  assert record['category']=='patent' # Software excluded at user's request.
 pubs=page(prefix+'publications/').select('[data-publication]')
 for record,row in zip(data('publications.json')['publications'],pubs):
  assert record['title'] in row.h2.get_text()
  assert row.select_one('.translation-label') is None
print(f'PASS: {len(projects)} project pairs, 37 publication pairs, 7 patent families / 2 PCT filings, 3 transfers; panels initially collapsed.')
