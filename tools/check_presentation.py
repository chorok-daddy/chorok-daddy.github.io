#!/usr/bin/env python3
"""Check language-specific footers and the lightweight source-note references."""
import json,re
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
count=0
for p in (ROOT/'niil').rglob('*.html'):
 if any(part in ('content','assets') for part in p.relative_to(ROOT/'niil').parts):continue
 text=p.read_text();doc=BeautifulSoup(text,'html.parser')
 if not doc.select_one('.site-header') or doc.select_one('meta[http-equiv="refresh"]'):continue
 assert len(doc.select('footer.site-footer'))==1,p
 footer=doc.select_one('footer.site-footer');identity=footer.select_one('.footer-identity').get_text(' ',strip=True)
 expected='Nature-inspired Intelligence Lab Kwangwoon University · Seoul, Korea' if doc.html.get('lang')=='en' else '자연모사 인공지능 연구실 광운대학교'
 assert identity==expected,(p,identity)
 assert not footer.select('a[href="/niil/contact/"]'),p
 assert not doc.select('.course-credit'),p
 assert 'NiiL Easter Egg' not in text,p
 refs=re.findall(r'<!--\s*ref:\s*([^>]+render\.logtmp)\s*-->',text)
 assert len(refs)==1,(p,refs)
 assert (ROOT/refs[0].strip().lstrip('/')).is_file(),p
 count+=1
for lang in ('','en/'):
 catalog=BeautifulSoup((ROOT/('niil/'+lang+'courses/index.html')).read_text(),'html.parser')
 additional=catalog.select_one('details.additional-courses')
 assert additional and not additional.has_attr('open')
 assert len(catalog.select('.course-catalog > .course-cards a'))==2
 assert len(catalog.select('.repository-link'))==1
 member=ROOT/('niil/'+lang+'pages/sunmok-kim-41337dc6/index.html')
 assert 'ktr.or.kr/ktr-intro/employee' not in member.read_text()
 guide=ROOT/('niil/'+lang+'courses/reuse.html')
 assert guide.is_file()
 assert not BeautifulSoup(guide.read_text(),'html.parser').select_one('footer a')
courses=json.loads((ROOT/'tools/course-catalog.json').read_text())['courses']
for course in courses:
 if not course['published']:continue
 directory=ROOT/'niil/courses'/course['slug']
 index=BeautifulSoup((directory/'index.html').read_text(),'html.parser')
 assert not index.select('.chapter-exercise')
 for chapter in course['chapters']:
  assignment=directory/chapter['slug']/'assignment.html'
  entry=chapter['slug']+('/assignment.html' if assignment.is_file() else '/index.html')
  assert len(index.select('h2 a[href="'+entry+'"]'))==1
  if assignment.is_file():
   doc=BeautifulSoup(assignment.read_text(),'html.parser')
   assert doc.select_one('a[data-course-overlay][href="index.html"]'),assignment
for page in (ROOT/'niil/courses').rglob('*.html'):
 doc=BeautifulSoup(page.read_text(),'html.parser')
 assert not doc.select('.course-author'),page
 assert '이기백' not in doc.title.get_text() and 'Ki-Baek' not in doc.title.get_text(),page
print(f'PASS: {count} content footers, dialogs, exercise entry points, concise course titles and alumni cleanup')
