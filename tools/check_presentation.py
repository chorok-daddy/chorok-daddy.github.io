#!/usr/bin/env python3
"""Check language-specific footers and the lightweight source-note references."""
import json,re
from pathlib import Path
from bs4 import BeautifulSoup,Comment
from easter_egg import EASTER_EGG_TEXT
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
 notes=[str(c).strip() for c in doc.find_all(string=lambda c:isinstance(c,Comment)) if 'NiiL Easter Egg' in c]
 assert not notes,p
 assert 'NiiL Easter Egg' not in doc.get_text(),p
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
 download=index.select_one('[data-course-download]')
 assert download and download['href'].endswith('/downloads/'+course['slug']+'.zip')
 assert (ROOT/'niil/courses/downloads'/(course['slug']+'.zip')).is_file()
 for chapter in course['chapters']:
  assignment=directory/chapter['slug']/'assignment.html'
  entry=chapter['slug']+('/assignment.html' if assignment.is_file() else '/index.html')
  assert len(index.select('h2 a[href="'+entry+'"]'))==1
  if assignment.is_file():
   doc=BeautifulSoup(assignment.read_text(),'html.parser')
   assert doc.select_one('a[data-course-overlay][href="index.html"]'),assignment
   study=BeautifulSoup((directory/chapter['slug']/'index.html').read_text(),'html.parser')
   assert not study.select('a[href^="assignment.html"]'),assignment
   for a in doc.select('a[href^="index.html"]'):assert a.has_attr('data-course-overlay'),assignment
   preview=doc.select_one('[data-notebook-preview]')
   if preview:
    assert preview.get_text()=='Colab 노트북 미리보기' and preview.has_attr('data-course-overlay'),assignment
    download=preview.find_next_sibling('a')
    assert download.get_text()=='Colab 노트북 다운로드' and download.has_attr('download'),assignment
for page in (ROOT/'niil/courses').rglob('*.html'):
 doc=BeautifulSoup(page.read_text(),'html.parser')
 assert not doc.select('.course-author'),page
 if page.name.endswith('.preview.html') or page.name=='assignment.html' or len(page.relative_to(ROOT/'niil/courses').parts)>2:
  for a in doc.select('main a[href^="https://"]'):assert a.get('target')=='_blank',page
 assert '이기백' not in doc.title.get_text() and 'Ki-Baek' not in doc.title.get_text(),page
print(f'PASS: {count} content footers, dialogs, exercise entry points, concise course titles and alumni cleanup')

assert '전체 페이지' not in (ROOT/'niil/courses/assets/course-ui.js').read_text()
for lang in ('','en/'):
 text=(ROOT/('niil/'+lang+'research/index.html')).read_text()
 assert '이기백 교수가 발명에 참여한' not in text and 'Patents co-invented by' not in text

css=(ROOT/'niil/assets/niil.css').read_text()
assert css.count('NiiL Easter Egg')==1 and EASTER_EGG_TEXT in css
assert 'NiiL Easter Egg' not in (ROOT/'niil/courses/assets/course-ui.css').read_text()
