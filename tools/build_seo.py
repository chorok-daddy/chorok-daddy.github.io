#!/usr/bin/env python3
"""Maintain search metadata and canonical sitemap without editing visible content."""
import json,re
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
from publication_layout import localized,neutral

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'niil';BASE='https://chorok-daddy.github.io'
ROUTES=json.loads((SITE/'content/routes.json').read_text())
MEMBERS=json.loads((SITE/'content/members.json').read_text())
COURSES=[c for c in json.loads((ROOT/'tools/course-catalog.json').read_text())['courses'] if c['published']]

def canonical(path):
    return path[:-len('index.html')] if path.endswith('/index.html') else path

def clean(text):return re.sub(r'\s+',' ',text).strip()
def excerpt(text,length=170):
    text=clean(text)
    return text if len(text)<=length else text[:length].rsplit(' ',1)[0]+'…'

faculty=next(m for m in MEMBERS if m['role']['en']=='Professor')
PROFILE=canonical(localized(ROUTES[faculty['id']],'ko'))
PERSON_ID=BASE+PROFILE+'#person';ORG_ID=BASE+'/niil/#organization'
member_paths={canonical(ROUTES[m['id']]):m for m in MEMBERS}
verification_file=ROOT/'tools/search-console.json'
verification=json.loads(verification_file.read_text()).get('google_site_verification') if verification_file.exists() else None
# Keep verification on both the root redirect and its canonical landing page.
if verification:
    root_page=ROOT/'index.html'
    root_doc=BeautifulSoup(root_page.read_text(),'html.parser')
    for old in root_doc.select('meta[name="google-site-verification"]'):old.decompose()
    root_doc.head.append(root_doc.new_tag('meta',attrs={'name':'google-site-verification','content':verification}))
    root_page.write_text(str(root_doc))
entries={}
for file in sorted(SITE.rglob('*.html')):
    if any(part in ('assets','content') for part in file.relative_to(SITE).parts):continue
    doc=BeautifulSoup(file.read_text(),'html.parser')
    if not doc.head:continue
    path=canonical('/'+file.relative_to(ROOT).as_posix())
    lang='en' if path.startswith('/niil/en/') else 'ko'
    ko_path=neutral(path)
    def meta(name,value,prop=False):
        key='property' if prop else 'name'
        for old in doc.head.find_all('meta',attrs={key:name}):old.decompose()
        doc.head.append(doc.new_tag('meta',attrs={key:name,'content':value}))
    if verification and path in ('/niil/','/niil/ko/'):meta('google-site-verification',verification)
    redirect=doc.select_one('meta[http-equiv="refresh"]')
    if redirect:
        meta('robots','noindex,follow')
        target=redirect.get('content','').split('url=',1)[-1]
        link=doc.select_one('link[rel=canonical]')
        if link and target.startswith('/'):link['href']=BASE+canonical(target)
        file.write_text(str(doc));continue
    for old in doc.head.select('[data-niil-seo]'):old.decompose()
    h1=doc.find('h1');name=clean(h1.get_text(' ',strip=True)) if h1 else clean(doc.title.get_text())
    member=member_paths.get(ko_path)
    course=next((c for c in COURSES if ko_path.startswith('/niil/courses/'+c['slug']+'/')),None)
    if ko_path=='/niil/':
        title='NiiL | AI & Robotics' if lang=='en' else 'NiiL | 자연모사 인공지능 연구실'
        description='Nature-inspired Intelligence Lab at Kwangwoon University, led by Ki-Baek Lee. Explore robotics, visual perception, human-centered AI, publications and open course materials.' if lang=='en' else '이기백 교수의 광운대학교 자연모사 인공지능 연구실 NiiL. 로봇·자율 시스템, 시각 인식·물류, 인간 중심 AI 연구와 논문, 공개 강의자료를 소개합니다.'
    elif member:
        role=member['role'][lang];affiliation=member['affiliation'][lang]
        title=(f'{name} | Kwangwoon University NiiL' if lang=='en' else f'{name}{" 교수" if member==faculty else ""} | 광운대학교 NiiL')
        description=(f'{name}: {role}. NiiL membership history'+(f' and affiliation: {affiliation}.' if affiliation else '.')) if lang=='en' else f'{name}의 NiiL 이력과 소속 안내.'+(f' {affiliation}.' if affiliation else '')
    elif ko_path=='/niil/courses/':
        title='Course | NiiL' if lang=='en' else '강의자료 | NiiL'
        description='Course notes, notebooks, exercises and datasets by Ki-Baek Lee, Kwangwoon University.' if lang=='en' else '광운대학교 이기백 교수의 공개 강의자료. 과목별 학습자료, 실습 안내, Notebook·MATLAB 파일과 데이터를 제공합니다.'
    elif course:
        root=ko_path==f'/niil/courses/{course["slug"]}/'
        course_name=course['title_en'] if lang=='en' else course['title']
        title=f'{course_name} | NiiL' if root else f'{name} | {course_name}'
        if not root and course_name in name:title=f'{name} | NiiL'
        description=(f'{course_name}: learning materials, practice notebooks and MATLAB files.' if lang=='en' else f'{course_name}: 학습자료와 실습 파일.') if root else f'{course_name}: {name}. '
        if not root:
            paragraphs=doc.select('main p:not(.course-credit):not(.source-note):not(.translation-note)')
            if paragraphs:description+=paragraphs[0].get_text(' ',strip=True)

    else:
        title=f'{name} | Kwangwoon University NiiL' if lang=='en' else f'{name} | 광운대학교 NiiL'
        descriptions={
            '/niil/research/':('Robotics and autonomy, visual intelligence and logistics, and human-centered AI: research projects, contributions, patents and technology transfer at NiiL.','광운대학교 NiiL의 로봇·자율 시스템, 시각 인식·물류, 인간 중심 AI 연구. 연구과제별 핵심 성과와 기여, 특허·기술이전 실적을 소개합니다.'),
            '/niil/publications/':('Research publications by Ki-Baek Lee and NiiL. Browse papers by year and publication type.','이기백 교수와 NiiL 연구진의 논문 목록. 연도·유형별 논문과 학술지·학회 정보를 확인할 수 있습니다.'),
            '/niil/members/':('Faculty, graduate researchers and alumni of NiiL at Kwangwoon University.','광운대학교 NiiL의 교수, 대학원생, 졸업생·이전 구성원과 연구실 이력을 소개합니다.'),
            '/niil/contact/':('Contact NiiL at Kwangwoon University for research collaboration, lab applications and general inquiries.','광운대학교 NiiL 연구 협업, 연구실 참여 지원 및 일반 문의 안내와 접수 양식입니다.'),
            '/niil/photos/':('NiiL lab photos and homecoming gatherings at Kwangwoon University.','광운대학교 NiiL 연구실 단체사진과 홈커밍 모임 사진입니다.')}
        if ko_path in descriptions:description=descriptions[ko_path][0 if lang=='en' else 1]
        else:
            lead=doc.select_one('.lede') or doc.select_one('article.prose p')
            description=lead.get_text(' ',strip=True) if lead else (f'{name}: materials from NiiL at Kwangwoon University.' if lang=='en' else f'{name} — 광운대학교 NiiL의 자료입니다.')
    description=excerpt(description)
    if not doc.title:doc.head.append(doc.new_tag('title'))
    doc.title.string=title
    meta('description',description);meta('robots','index,follow')
    url=BASE+path
    links=doc.head.select('link[rel=canonical]')
    for link in links:link.decompose()
    doc.head.append(doc.new_tag('link',rel='canonical',href=url))
    for tag in doc.select('link[rel=alternate][hreflang]'):
        parts=urlsplit(tag['href']);tag['href']=parts._replace(path=canonical(parts.path)).geturl()
    for prop,value in [('og:title',title),('og:description',description),('og:url',url),('og:type','website'),('og:site_name','NiiL · Kwangwoon University'),('og:locale','en_US' if lang=='en' else 'ko_KR')]:meta(prop,value,True)
    meta('twitter:card','summary');meta('twitter:title',title);meta('twitter:description',description)
    org={'@type':'Organization','@id':ORG_ID,'name':'Nature-inspired Intelligence Lab (NiiL)','alternateName':'자연모사 인공지능 연구실','url':BASE+'/niil/','parentOrganization':{'@type':'CollegeOrUniversity','name':'Kwangwoon University','alternateName':'광운대학교'}}
    graph=[org,{'@type':'WebPage','@id':url+'#webpage','url':url,'name':title,'description':description,'inLanguage':lang,'isPartOf':{'@id':BASE+'/niil/#website'}}]
    if ko_path=='/niil/':graph.append({'@type':'WebSite','@id':BASE+'/niil/#website','url':BASE+'/niil/','name':'NiiL · Kwangwoon University','publisher':{'@id':ORG_ID},'inLanguage':['ko','en']})
    if member==faculty:
        person={'@type':'Person','@id':PERSON_ID,'name':'Ki-Baek Lee','alternateName':'이기백','jobTitle':'Professor','url':BASE+PROFILE,'affiliation':org['parentOrganization'],'sameAs':['https://scholar.google.co.kr/citations?user=yZ9xxNcAAAAJ']}
        photo=doc.select_one('aside img.portrait')
        if photo:person['image']=BASE+photo['src']
        graph[1]['@type']='ProfilePage';graph[1]['mainEntity']={'@id':PERSON_ID};graph.append(person)
    # Existing course JSON-LD retains its licensing scope and references the same author.
    for block in doc.head.select('script[type="application/ld+json"]:not([data-niil-seo])'):
        data=json.loads(block.string)
        if data.get('@type')=='LearningResource':
            data['name']=name;data['url']=url;data['author']['@id']=PERSON_ID
            block.string=json.dumps(data,ensure_ascii=False)
    structured=doc.new_tag('script',type='application/ld+json');structured['data-niil-seo']=''
    structured.string=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c')
    doc.head.append(structured)
    file.write_text(str(doc))
    entries[url]=[(tag.get('hreflang'),tag.get('href')) for tag in doc.select('link[rel=alternate][hreflang]')]

ns='http://www.sitemaps.org/schemas/sitemap/0.9';xhtml='http://www.w3.org/1999/xhtml'
ET.register_namespace('',ns);ET.register_namespace('xhtml',xhtml)
root=ET.Element('{'+ns+'}urlset')
for url,alternates in sorted(entries.items()):
    item=ET.SubElement(root,'{'+ns+'}url');ET.SubElement(item,'{'+ns+'}loc').text=url
    for lang,target in alternates:
        if target in entries:ET.SubElement(item,'{'+xhtml+'}link',rel='alternate',hreflang=lang,href=target)
ET.indent(root)
ET.ElementTree(root).write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+BASE+'/sitemap.xml\n')
print(f'Updated search metadata and sitemap: {len(entries)} canonical content URLs.')
