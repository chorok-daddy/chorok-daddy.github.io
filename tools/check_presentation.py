#!/usr/bin/env python3
"""Check language-specific footers and the lightweight source-note references."""
import json,re,hashlib
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
 assert not index.select('a[href="files.html"]')
 if (directory/'files.html').is_file():
  old=BeautifulSoup((directory/'files.html').read_text(),'html.parser')
  assert old.select_one('meta[http-equiv="refresh"]')['content']=='0;url=index.html'
 download=index.select_one('[data-course-download]')
 enabled=course.get('zip_enabled',True) and bool(course.get('chapters') or course.get('lessons'))
 if enabled:
  assert download and download['href']=='https://github.com/chorok-daddy/courses/blob/main/'+course['slug']+'/README.md'
  assert not download.has_attr('download') and download.get_text()=='자료 받기 ↗'
  assert (ROOT/'niil/courses/downloads'/(course['slug']+'.zip')).is_file()
 else:
  assert download is None
  assert not (ROOT/'niil/courses/downloads'/(course['slug']+'.zip')).exists()
 for chapter in course['chapters']:
  assignment=directory/chapter['slug']/'assignment.html'
  entry=chapter['slug']+('/assignment.html' if assignment.is_file() else '/index.html')
  assert index.select('main a[href="'+entry+'"], main a[href^="'+entry+'#"]'), (course['slug'], entry)
  if assignment.is_file():
   doc=BeautifulSoup(assignment.read_text(),'html.parser')
   lesson=next((l for l in course['lessons'] if l['slug']==chapter['slug']),{})
   split=bool(lesson.get('learning_notebook'))
   if split:
    for role,word in [('learning','학습용'),('practice','실습용')]:
     links=doc.select('[data-course-overlay][data-notebook-role="'+role+'"]');assert len(links)==1,(assignment,role)
     link=links[0];assert link.has_attr('data-course-overlay') and word in link.get_text(),assignment
     target=assignment.parent/link['href'];assert target.is_file(),target
     download=link.find_next_sibling('a');assert word in download.get_text() and download.has_attr('download'),assignment
   else:assert doc.select_one('a[data-course-overlay][href="index.html"]'),assignment
   study=BeautifulSoup((directory/chapter['slug']/'index.html').read_text(),'html.parser')
   if not study.select_one('meta[http-equiv="refresh"]'):assert not study.select('a[href^="assignment.html"]'),assignment
   for a in doc.select('a[href^="index.html"]'):assert a.has_attr('data-course-overlay'),assignment
   preview=doc.select_one('[data-notebook-preview]')
   if preview and not split:
    assert preview.get_text()=='Colab 노트북 미리보기' and preview.has_attr('data-course-overlay'),assignment
    download=preview.find_next_sibling('a')
    assert download.get_text()=='Colab 노트북 다운로드' and download.has_attr('download'),assignment
   mlx=doc.select_one('[data-mlx-preview]')
   if mlx and not split:
    assert mlx.get_text()=='mlx 스크립트 미리보기' and mlx.has_attr('data-matlab-url'),assignment
    download=mlx.find_next_sibling('a')
    assert download.get_text()=='mlx 스크립트 다운로드' and download.has_attr('download'),assignment
  for source in (directory/chapter['slug']).glob('*.mlx'):
   preview=source.with_suffix('.mlx.preview.html')
   page=BeautifulSoup(preview.read_text(),'html.parser')
   assert page.select_one('.mlx-document') and page.select_one('meta[name="mlx-export-run"]')['content']=='false'
   assert page.select_one('meta[name="mlx-source-sha256"]')['content']==hashlib.sha256(source.read_bytes()).hexdigest()
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
