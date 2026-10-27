#!/usr/bin/env python3
"""Build the isolated NiiL site from the preserved public Notion content."""
import html, json, re, subprocess
from pathlib import Path
from bs4 import BeautifulSoup, Comment
from easter_egg import EASTER_EGG_TEXT, EASTER_EGG_HTML

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'niil'
COURSE_DISTRIBUTION=json.loads((ROOT/'tools/course-distribution.json').read_text())['courses']
PAGES = json.loads((SITE/'content/pages.json').read_text())
CATALOG = json.loads((SITE/'content/projects.json').read_text())
PROJECT_BY_ID = {p['page_id']:p for p in CATALOG}
for project in CATALOG:
    page = next((p for p in PAGES if p['id']==project['page_id']), None)
    if page is None:
        page = {'id':project['page_id'], 'title':project['title'], 'collection':'collection://1b9888a1-7b30-80cd-820b-000b52d52aa9', 'properties':{}, 'body':''}
        PAGES.append(page)
    # Preserve legacy titles for stable original URLs; use the catalog title in the UI.
    page['body'] = (SITE/'content'/project['body_file']).read_text()
    page['properties'] = {'Title(Korean)':project['title_ko'], 'Sponsor':' · '.join(project['sponsors']), 'Period':project['start']+' — '+project['end'], 'Role':'Principal investigator · Ki-Baek Lee'}
CLUSTERS = [
    ('Robotics & Autonomy','robotics','행동하고 적응하는 시스템','로봇 학습, 군집 탐색, 이동 보조와 임베디드 제어를 실제 작업으로 연결합니다.'),
    ('Visual Intelligence & Logistics','vision','보는 것을 작업 정보로','3차원 공간과 화물을 이해하고 피킹·적재·배송의 의사결정으로 연결합니다.'),
    ('Human-Centered AI','human','사람의 표현을 이해하는 AI','감정, 수어와 언어를 학습해 상호작용과 접근성을 확장합니다.')
]

ASSETS = {x['reference']:x['path'] for x in json.loads((SITE/'content/assets.json').read_text()) if 'path' in x}
byid = {p['id']:p for p in PAGES}
TOP = ['vision','members','contact','publications','projects','research','robot-basic-lab','microprocessor','control-1','control-2','ai-applications','ee-seminar']
ROUTES = {p['id']:'/niil/'+s+'/' for p,s in zip(PAGES[:12],TOP)}
ROUTES[PAGES[12]['id']]='/niil/'
for project in CATALOG:
    if project['page_id'].startswith('niil-'):
        ROUTES[project['page_id']]='/niil/research/'+project['key']+'/'
def plain(x):
    value=str(x)
    return (BeautifulSoup(value,'html.parser').get_text(' ',strip=True) if '<' in value else value).replace('\\-','—').replace('Appied Intelligence','Applied Intelligence')
def esc(x): return html.escape(plain(x),quote=True)
def slug(x): return re.sub(r'[^a-z0-9]+','-',plain(x).lower()).strip('-') or 'item'
for p in PAGES:
    ROUTES.setdefault(p['id'], '/niil/pages/'+slug(p['title'])+'-'+p['id'][-8:]+'/')
def href(p): return ROUTES[p['id']]
def display_title(p): return PROJECT_BY_ID.get(p['id'],{}).get('title',p['title'])
def rows(collection): return [p for p in PAGES if p['collection']==collection]
def props(p): return p['properties']
MEMBERS=rows('collection://1b6888a1-7b30-80dc-8548-000b1ae76dfb')
PROJECTS=rows('collection://1b9888a1-7b30-80cd-820b-000b52d52aa9')
AREAS=rows('collection://1af888a1-7b30-8060-84d2-000b9e108baf')
VISIONS=rows('collection://1b5888a1-7b30-80fc-af94-000b76af84a0')
NOTICE=rows('collection://1b0888a1-7b30-80bd-9ade-000bd380602a')
NAV=[('Research','research'),('Publications','publications'),('People','members'),('Teaching','teaching')]
def image(p, cls='', first=True):
    refs=re.findall(r'<image source="([^"]+)"',p['body'])
    return ''.join(f'<img class="{cls}" src="{ASSETS[r]}" alt="{esc(p["title"])}" loading="lazy" decoding="async">' for r in (refs[:1] if first else refs) if r in ASSETS)
def link(p,label=None): return f'<a href="{href(p)}">{esc(label or display_title(p))} <span aria-hidden="true">↗</span></a>'
def write(path,text):
    p=ROOT/path.lstrip('/')/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
def database(match):
    attrs=match[1];c=re.search(r'data-source-url="([^"]+)"',attrs);url=re.search(r'url="([^"]+)"',attrs)
    ps=rows(c[1]) if c else []
    if not ps:
        u=url[1].replace('https://app.notion.com/p/','https://niilab.notion.site/') if url else 'https://niilab.notion.site/'
        return '\n\n<a class="button outline" href="/niil/contact/#join">Application information</a>\n\n'
    if '81' in (c[1] if c else '') and any('Details' in props(p) for p in ps):
        return '\n\n<div class="table-scroll"><table class="schedule"><thead><tr><th>Session</th><th>Format</th><th>Topic</th></tr></thead><tbody>'+''.join(f'<tr><th scope="row">{link(p)}</th><td>{esc(props(p).get("Type",""))}</td><td>{esc(props(p).get("Details",""))}</td></tr>' for p in ps)+'</tbody></table></div>\n\n'
    return '\n\n'+cards(ps)+'\n\n'
def render(p):
    text=p['body']
    text=re.sub(r'<database\b([^>]*)>[\s\S]*?</database>',database,text)
    text=re.sub(r'<image source="([^"]+)"\s*/>',lambda m:f'\n\n<img src="{ASSETS[m[1]]}" alt="{esc(p["title"])}" loading="lazy">\n\n' if m[1] in ASSETS else '',text)
    text=re.sub(r'<file source="([^"]+)"\s*/>',lambda m:f'\n\n<a class="button outline" href="{ASSETS[m[1]]}" download>Download PDF ↧</a>\n\n',text)
    text=re.sub(r'<bookmark source="([^"]+)"\s*/>',lambda m:f'\n\n<a href="{html.escape(m[1],quote=True)}">Open course repository ↗</a>\n\n',text)
    text=re.sub(r'<page url="[^"]*/([a-f0-9]+)">([\s\S]*?)</page>',lambda m:f'\n\n<a href="{ROUTES.get(m[1],"https://niilab.notion.site/"+m[1])}">{esc(m[2])} ↗</a>\n\n',text)
    text=text.replace('<columns>', '\n\n<div class="source-columns">\n\n').replace('</columns>', '\n\n</div>\n\n')
    text=re.sub(r'<column[^>]*>', '\n\n<div class="source-column">\n\n',text).replace('</column>', '\n\n</div>\n\n')
    text=re.sub(r'<p\s*/>','',text)
    text=re.sub(r'<span[^>]*>|</span>','',text)
    if p['id'] not in PROJECT_BY_ID: text=re.sub(r'#{1,6} ',lambda m:'#'*(min(6,len(m[0])))+' ',text)
    result=subprocess.run(['pandoc','-f','markdown+raw_html+markdown_in_html_blocks','-t','html','--wrap=none'],input=text,text=True,capture_output=True,check=True).stdout
    soup=BeautifulSoup(result,'html.parser')
    for a in soup.find_all('a',href=True):
        if a['href'].startswith('https://www.ntis.go.kr/'):
            a['target']='_blank'
            a['rel']=['noopener','noreferrer']
        m=re.search(r'(?:notion\.so|notion\.site|app\.notion\.com/p)/[^?]*?([a-f0-9]{32})(?:[?#]|$)',a['href'])
        if m: a['href']=ROUTES.get(m[1],'https://niilab.notion.site/'+m[1])
    for bad in soup(['script','iframe','style']):bad.decompose()
    for column in soup.select('.source-column'):
        if not column.get_text(strip=True) and not column.find('img'):column.decompose()
    for el in soup.find_all(True):
        for k in list(el.attrs):
            if k.startswith('on'):del el[k]
    return str(soup)
def meta(p):
    fields=[]
    for k,v in props(p).items():
        if k in ['Name','Title','title','Created','Created by'] or k.endswith(':is_datetime') or k.endswith(':end') or not v:continue
        label=k.replace('date:','').replace(':start','').replace('Current Affliation','Current affiliation')
        if k=='Email':v=str(v).replace('(at)','@')
        if isinstance(v,list):v=' · '.join(v)
        fields.append(f'<div><dt>{esc(label)}</dt><dd>{esc(v)}</dd></div>')
    return '<dl class="metadata">'+''.join(fields)+'</dl>' if fields else ''
# Maintained bilingual presentation. Original archive content is retained in its source language.
MEMBER_DATA=json.loads((SITE/'content/members.json').read_text())
PROJECT_LOCALES=json.loads((SITE/'content/project-locales.json').read_text())
CONTACT_FORM='https://docs.google.com/forms/d/e/1FAIpQLSf95YWgQxAjvJ1PvqTTlt6o53_EAymCu9aatNsyt4rzwm3A7Q/viewform'
PUBLICATION_DATA=json.loads((SITE/'content/publications.json').read_text())
SPONSORS={'한국연구재단':'National Research Foundation of Korea (NRF)','한국철도기술연구원':'Korea Railroad Research Institute (KRRI)','정보통신기획평가원':'Institute of Information & Communications Technology Planning & Evaluation (IITP)','한국전자통신연구원':'Electronics and Telecommunications Research Institute (ETRI)','중소기업청':'Small and Medium Business Administration','(주)대한스프레이시스템':'Daehan Spray System','한국항공우주연구원 연계 · 한국연구재단 전문기관':'KARI-linked project · NRF specialized agency'}
CLUSTER_KO={'Robotics & Autonomy':'로봇·자율 시스템','Visual Intelligence & Logistics':'시각 인식·물류','Human-Centered AI':'인간 중심 AI'}
CLUSTER_EN=['Robot learning, swarm search, assisted motion and embedded control.','3D perception and cargo understanding for picking, loading and delivery.','Emotion, sign language and language models for interaction and access.']
COURSE_KO=['로봇기초실험','마이크로프로세서응용','제어공학1','제어공학2','인공지능응용','전기공학세미나']
LANG='en'
def tr(en,ko):return ko if LANG=='ko' else en
def local(path):
    if path=='/niil/courses/':return '/niil/en/courses/' if LANG=='en' else path
    if path.startswith('/niil/') and not path.startswith(('/niil/assets/','/niil/courses/','/niil/en/')):
        return path.replace('/niil/','/niil/en/',1) if LANG=='en' else path
    return path
def cluster(name):return CLUSTER_KO[name] if LANG=='ko' else name
def project_title(p):
    if p.get('title_kind') == 'collection':
        return PROJECT_LOCALES[p['key']]['title_ko_short'] if LANG=='ko' else p['title']
    return p['title_ko'] if LANG=='ko' else (p.get('official_title_en') or p['translated_title_en']+' ('+p['title_ko']+')')
def phase_title(phase):
    return esc(phase['title']) if LANG=='ko' else esc(phase['title_en'])+(' ('+esc(phase['title'])+')' if phase['title_en_kind']=='translation' else '')
def project_titles(p, detail=False):
    collection = p.get('title_kind') == 'collection'
    out='<div class="official-titles">'
    if collection:
        out+='<p class="title-label">'+tr('Related contracts','관련 계약')+'</p><ul>'
        for phase in p['phases']:
            out+='<li>'+phase_title(phase)+'</li>'
        out+='</ul>'
    if detail:
        if not collection and not p.get('official_title_en'):
            if LANG=='en':out+='<p class="muted">English title is a translation; no official English title was verified.</p>'
        if p.get('official_title_en') and not p.get('title_sources'):
            out+='<p class="title-source">'+tr('English title: research proposal title page','영문 과제명: 연구계획서 표지')+'</p>'
        if p.get('title_sources'):
            out+='<p class="title-source">'+ ' · '.join('<a href="'+esc(x['url'])+'" target="_blank" rel="noopener noreferrer">'+(tr('NTIS link','NTIS 링크') if x['label']=='NTIS' else esc(x['label']))+'</a>' for x in p['title_sources'])+'</p>'
        elif not collection and p.get('official_title_en'):
            out+='<p class="title-source">'+tr('Title source: research proposal','과제명 출처: 연구계획서')+'</p>'
    return out+'</div>'

def project_summary(p):return p['summary'] if LANG=='ko' else PROJECT_LOCALES[p['key']]['summary_en']
def sponsor(s):return s if LANG=='ko' else SPONSORS.get(s,s)
def heading(kicker,title,desc=''):
    return f'<header class="wrap publication-heading"><h1>{title}</h1>'+ (f'<p class="lede">{desc}</p>' if desc else '')+'</header>'
def shell(title,content,section='',desc='',path='/niil/'):
    soup=BeautifulSoup(content,'html.parser')
    for a in soup.find_all('a',href=True):
        if a['href'].startswith('/niil/') and not a['href'].startswith('/niil/assets/'):
            a['href']=local(a['href'])
        if a['href'].startswith('/') or a['href'].startswith('#'):
            for text in a.find_all(string=True):text.replace_with(str(text).replace('↗','').strip() if str(text).strip()=='↗' else str(text).replace(' ↗',''))
    current_page='aria-current="page"'
    current_language='aria-current="true"'
    nav=''.join(f'''<a {current_page if section==s else ''} href="{(local("/niil/courses/") if s=="teaching" else local("/niil/"+s+"/"))}">{tr(n,k)}</a>''' for n,k,s in [('Research','연구','research'),('Publications','논문','publications'),('People','구성원','members'),('Course','강의자료','teaching'),('Contact','문의·지원','contact')])
    english=path.replace('/niil/','/niil/en/',1);korean=path
    toggle=f'''<nav class="language-switch" aria-label="{tr("Language","언어")}"><a data-language="ko" lang="ko" href="{korean}" {current_language if LANG=='ko' else ''}>한국어</a><span aria-hidden="true">/</span><a data-language="en" lang="en" href="{english}" {current_language if LANG=='en' else ''}>EN</a></nav>'''
    base='https://chorok-daddy.github.io'
    return f'''<!doctype html><html lang="{LANG}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} · NiiL</title><meta name="description" content="{esc(desc or tr('Nature-inspired Intelligence Lab at Kwangwoon University','광운대학교 자연모사 인공지능 연구실'))}"><meta name="robots" content="index,follow"><link rel="canonical" href="{base+local(path)}"><link rel="alternate" hreflang="en" href="{base+english}"><link rel="alternate" hreflang="ko" href="{base+korean}"><link rel="alternate" hreflang="x-default" href="{base+korean}"><link rel="stylesheet" href="/niil/assets/niil.css?v=20261026-outputs1"><script src="/niil/assets/niil.js?v=20261026-outputs1" defer></script></head><body>{EASTER_EGG_HTML}<a class="skip" href="#main">{tr('Skip to content','본문 바로가기')}</a><header class="site-header"><a class="brand" href="{local('/niil/')}" aria-label="NiiL {tr('home','홈')}">NiiL<span class="brand-dot">●</span></a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">{tr('Menu','메뉴')} ☰</button><nav id="site-nav" aria-label="{tr('Main navigation','주 메뉴')}">{nav}</nav>{toggle}</header><main id="main">{soup}</main><footer><a class="brand" href="{local('/niil/')}">NiiL<span class="brand-dot">●</span></a><div>{tr('Nature-inspired Intelligence Lab','자연모사 인공지능 연구실')}<br><span>{tr('Kwangwoon University · Seoul, Korea','광운대학교 · 서울')}</span></div><a href="{local('/niil/contact/')}">{tr('Contact','문의·지원')}</a><small>© NiiL</small></footer></body></html>'''
def emit(path,title,content,section=''):
    page=shell(title,content,section,path=path)
    if path=='/niil/members/' or 'portrait-crop' in content:
        page=page.replace('niil.css?v=20261026-outputs1','niil.css?v=20261026-portraits3')
    if path=='/niil/courses/':
        page=page.replace('</head>','<link rel="stylesheet" href="/niil/assets/courses.css?v=20261026-sharing1"></head>')
    if path=='/niil/photos/':
        page=page.replace('</head>','<link rel="stylesheet" href="/niil/assets/photos.css?v=20261026-2"></head>')
    write(local(path),page)
def route_redirect(path,target):
    section='teaching' if target=='/niil/courses/' else ('contact' if target.startswith('/niil/contact/') else 'research')
    title=tr('Course','강의자료') if section=='teaching' else (tr('Contact & apply','문의·지원') if section=='contact' else tr('Research','연구'))
    page=shell(title,heading('',title)+f'<section class="wrap section"><a href="{local(target)}">{tr("Continue","이동")}</a></section>',section,path=path)
    page=page.replace('<meta charset="utf-8">',f'<meta charset="utf-8"><meta http-equiv="refresh" content="0;url={local(target)}">')
    write(local(path),page)
def cluster_cards():
    return '<div class="cluster-grid">'+''.join(f'<a class="cluster-card cluster-{key}" href="/niil/research/?topic={key}#project-catalog"><span class="cluster-number">0{i+1}</span><h2>{cluster(name)}</h2><p>{description if LANG=="ko" else CLUSTER_EN[i]}</p><span class="cluster-count">{sum(p["cluster"]==name for p in CATALOG)} {tr("projects","개 과제")}</span></a>' for i,(name,key,_,description) in enumerate(CLUSTERS))+'</div>'
def project_rows(items):
    out='<div class="project-list">'
    for p in items:
        key=next(c[1] for c in CLUSTERS if c[0]==p['cluster'])
        status=tr('Ongoing','수행 중') if p['status']=='In progress' else tr('Completed','종료')
        search=esc(' '.join([p['title'],p['title_ko'],p.get('official_title_en') or '',p.get('translated_title_en') or '', ' '.join(q['title'] for q in p['phases']),p['summary'],PROJECT_LOCALES[p['key']]['summary_en']]+p['sponsors']+[sponsor(s) for s in p['sponsors']]))
        out+=f'<article class="project-row" data-project data-search="{search}" data-topic="{key}" data-status="{p["status"]}"><div><span class="badge">{status}</span><p class="muted">{p["start"][:4]}–{p["end"][:4]}</p></div><div><p class="eyebrow">{cluster(p["cluster"])}</p><h2><a href="{ROUTES[p["page_id"]]}">{esc(project_title(p))}</a></h2>{project_titles(p)}<p>{esc(project_summary(p))}</p><p class="muted">{esc(" · ".join(sponsor(s) for s in p["sponsors"]))}</p></div></article>'
    return out+'</div>'
def member_affiliation(m):
    text=esc(m['affiliation'][LANG])
    if m.get('affiliation_url'):
        return f'<a href="{esc(m["affiliation_url"])}" target="_blank" rel="noopener noreferrer">{text} ↗</a>'
    return text
def member_profile_link(m):
    link=m['profile_link']
    return f'<a href="{esc(link["url"])}" target="_blank" rel="noopener noreferrer">{esc(link["label"][LANG])} ↗</a>'
def frame_portrait(portrait,crop):
    style=f"--crop-width:{100*crop['image_width']/crop['width']:.3f}%;--crop-left:{-100*crop['x']/crop['width']:.3f}%;--crop-top:{-100*crop['y']/crop['height']:.3f}%;aspect-ratio:{crop['width']}/{crop['height']}"
    return f'<span class="portrait-crop" style="{style}">{portrait}</span>'
def history(m):
    out='<ul class="member-history">'
    for h in m['history']:
        period=h['start'] or ''
        if h['end']:period+=' – '+h['end']
        elif h['ongoing']:period+=' – '+tr('Present','현재')
        elif period:period=tr('Started ','시작 ')+period
        out+=f'<li><span>{esc(h["role"][LANG])}</span><time>{esc(period)}</time></li>'
    return out+'</ul>'
def project_body(p):
    q=dict(byid[p['page_id']]);q['body']=(SITE/'content'/(p['body_file'] if LANG=='ko' else f'projects/en/{p["key"]}.md')).read_text()
    soup=BeautifulSoup(render(q),'html.parser')
    # Keep evaluation conditions beside results; only provenance/administrative notes collapse.
    notes=[]
    for para in list(soup.find_all('p')):
        if para.get_text().startswith(('근거:','Source:','Sources:')):notes.append(str(para));para.decompose()
    for h in list(soup.find_all('h2')):
        if h.get_text() in ['레거시 과제 확인','Project record']:
            following=[]
            for sib in list(h.next_siblings):
                if getattr(sib,'name',None)=='h2':break
                following.append(sib)
            notes.append(str(h));h.decompose()
            for sib in following:notes.append(str(sib));sib.extract()
    return str(soup),''.join(notes)

def research_outputs():
    data=json.loads((SITE/'content/research-outputs.json').read_text())
    statuses={'registered':tr('Registered','등록'),'expired':tr('Registered · expired','등록 · 권리소멸'),'rejected':tr('Filed · refused','출원 · 거절'),'published':tr('Filed · published','출원 · 공개')}
    labels={'registration':tr('Registration','등록'),'application':tr('Application','출원'),'pct':tr('PCT application','PCT 국제출원')}
    def table(headers, rows):
        return '<table class="output-table"><thead><tr>'+''.join('<th scope="col">'+h+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td data-label="'+esc(h)+'">'+v+'</td>' for h,v in zip(headers,row))+'</tr>' for row in rows)+'</tbody></table>'
    rows=[]
    for p in data['intellectual_property']:
        title='<span lang="'+LANG+'">'+esc(p['title_ko'] if LANG=='ko' else p['title_en'])+'</span> <span class="muted">('+statuses[p['status']]+')</span>'
        if p.get('url'):title+='<a class="output-source" href="'+esc(p['url'])+'" target="_blank" rel="noopener noreferrer">'+tr('Patent record','특허 정보')+' ↗</a>'
        numbers=[];dates=[]
        for f in p['filings']:
            numbers.append('<div class="filing"><small>'+labels[f['kind']]+'</small>'+esc(f['number'])+('</div>' if not f.get('publication') else '<small>'+tr('Publication','공개번호')+' '+esc(f['publication'])+'</small></div>'))
            dates.append('<div class="filing"><small>'+labels[f['kind']]+'</small><time datetime="'+f['date']+'">'+f['date']+'</time></div>')
        rows.append([tr('Patent','특허') if p['category']=='patent' else tr('Software','소프트웨어'),title,''.join(numbers),''.join(dates)])
    count=len(rows)
    out='<section class="wrap research-outputs" aria-label="'+tr('Research outputs','연구 성과')+'"><details id="intellectual-property" class="output-panel"><summary>'+tr('Intellectual property','지식재산권')+' <span class="output-count">'+str(count)+'</span></summary><div class="output-body">'
    out+='<p class="muted">'+tr('Patents co-invented by Ki-Baek Lee. PCT applications are grouped with the corresponding Korean patent. Titles follow KIPRIS records.','이기백 교수가 발명에 참여한 특허입니다. PCT 국제출원은 해당 국내 특허와 함께 표시합니다.')+'</p>'
    out+=table([tr('Type','구분'),tr('Title (status)','명칭 (상태)'),tr('Registration / application number','등록 / 출원번호'),tr('Registration / application date','등록 / 출원일')],rows)+'</div></details>'
    rows=[]
    for t in data['technology_transfers']:
        title=esc(t['title_ko'] if LANG=='ko' else t['title_en'])
        recipient=esc(t['recipient'][LANG])
        if LANG=='en' and t.get('recipient_en_translated'):recipient+=' ('+esc(t['recipient']['ko'])+')'
        date=t.get('date_display',{}).get(LANG,t['date'])
        rows.append([title,recipient,esc(date)])
    out+='<details id="technology-transfer" class="output-panel"><summary>'+tr('Technology transfer','기술이전')+' <span class="output-count">'+str(len(rows))+'</span></summary><div class="output-body"><p class="muted">'+tr('Dates refer to signed contracts or the indicated transfer period. Agreements covering the same technology and recipient are grouped. English titles use the corresponding patent’s official English title.','계약 체결일 또는 해당 기술이전 기간을 표시합니다. 같은 기술·대상 기업의 국가별 계약은 한 건으로 묶었습니다.')+'</p>'
    out+=table([tr('Technology','명칭'),tr('Recipient','기술이전 대상'),tr('Transfer date','기술이전일')],rows)+'</div></details></section>'
    return out

for LANG in ('en','ko'):
    home=heading('',tr('Nature-inspired Intelligence Lab','자연모사 인공지능 연구실'),tr('We study robot learning, visual perception and human-centered AI at Kwangwoon University.','광운대학교에서 로봇 학습, 시각 인식, 인간 중심 인공지능을 연구합니다.'))
    home+='<section class="wrap section compact">'+cluster_cards()+'</section><section class="wrap section compact"><div class="section-title"><h2>'+tr('Ongoing projects','수행 중 과제')+'</h2><a href="/niil/research/">'+tr('All research','전체 연구')+'</a></div>'+project_rows([p for p in CATALOG if p['status']=='In progress'])+'</section>'
    home+='<section class="wrap section compact"><div class="resource-note"><h2>'+tr('Join the lab','연구실 참여')+'</h2><p>'+tr('Undergraduate internship applications are accepted throughout the year.','학부 인턴 지원은 상시 접수합니다.')+'</p><a href="/niil/contact/#join">'+tr('Lab application guide','연구실 지원 안내')+'</a></div></section>'
    emit('/niil/',tr('Home','홈'),home)
    content=heading('',tr('Research','연구'))+research_outputs()+'<section class="wrap section compact" id="project-catalog"><div class="filterbar">'
    content+=f'<label for="project-search">{tr("Search","검색")}<input type="search" id="project-search" placeholder="{tr("Title, sponsor, or topic","제목, 지원기관, 주제")}"></label><label for="project-topic">{tr("Theme","연구 분야")}<select id="project-topic"><option value="">{tr("All themes","전체 분야")}</option>'+''.join(f'<option value="{key}">{cluster(name)}</option>' for name,key,_,_ in CLUSTERS)+'</select></label>'
    content+=f'<label for="project-status">{tr("Status","상태")}<select id="project-status"><option value="">{tr("All projects","전체 과제")}</option><option value="In progress">{tr("Ongoing","수행 중")}</option><option value="Done">{tr("Completed","종료")}</option></select></label></div><p id="project-count" aria-live="polite"></p>'+project_rows(sorted(CATALOG,key=lambda p:p['start'],reverse=True))+f'<p id="no-projects" hidden>{tr("No projects found.","검색 결과가 없습니다.")}</p></section>'
    emit('/niil/research/',tr('Research','연구'),content,'research')
    for path in ['/niil/projects/','/niil/vision/']+[href(p) for p in AREAS+VISIONS]:route_redirect(path,'/niil/research/')
    for p in CATALOG:
        body,notes=project_body(p)
        content=heading('',esc(project_title(p)),esc(project_summary(p)))+f'<section class="wrap document-layout"><aside><a href="/niil/research/">← {tr("Research","연구")}</a><nav class="toc" aria-label="{tr("On this page","페이지 목차")}"></nav></aside><article class="prose">'
        content+=f'<p class="eyebrow">{cluster(p["cluster"])}</p><p>{p["start"]} – {p["end"]} · '+(tr('Ongoing','수행 중') if p['status']=='In progress' else tr('Completed','종료'))+'</p><p>'+esc(' · '.join(sponsor(s) for s in p['sponsors']))+'</p>'+project_titles(p,detail=True)+body
        content+=f'<details class="project-phases"><summary>{tr("Project record and sources","과제 이력 및 출처")}</summary><p>{tr("Kwangwoon University principal investigator: Ki-Baek Lee","광운대학교 연구책임자: 이기백")}</p>'
        if p['phases']:
            content+=f'<p class="muted">{tr("Contract titles are listed below.","계약별 공식 과제명입니다.")}</p><div class="table-scroll"><table><thead><tr><th>{tr("Period","기간")}</th><th>{tr("Contract","계약")}</th><th>{tr("Sponsor","지원기관")}</th></tr></thead><tbody>'
            for phase in p['phases']:content+=f'<tr><td>{phase["start"]} – {phase["end"]}</td><td>{phase_title(phase)}</td><td>{esc(sponsor(phase["sponsor"]))}</td></tr>'
            content+='</tbody></table></div>'
        content+=notes+'</details>'
        related=[x for x in CATALOG if x['cluster']==p['cluster'] and x['key']!=p['key']][:3]
        content+='<section><h2>'+tr('Related research','관련 연구')+'</h2><ul>'+''.join(f'<li><a href="{ROUTES[x["page_id"]]}">{esc(project_title(x))}</a></li>' for x in related)+'</ul></section></article></section>'
        emit(ROUTES[p['page_id']],project_title(p),content,'research')
    content=heading('',tr('People','구성원'))+'<div class="wrap"><a class="button outline" href="/niil/photos/">'+tr('Lab photos','연구실 사진')+'</a></div>'
    for en,ko,predicate in [('Faculty','교수',lambda m:m['role']['en']=='Professor'),('Graduate researchers','대학원생',lambda m:not m['alumni'] and m['role']['en']!='Professor'),('Alumni','졸업생·이전 구성원',lambda m:m['alumni'])]:
        content+='<section class="wrap section compact"><h2 class="group-title">'+tr(en,ko)+'</h2><div class="people-grid">'
        for m in filter(predicate,MEMBER_DATA):
            p=byid[m['id']];portrait=image(p,'portrait') or '<div class="initials" aria-hidden="true">'+esc(''.join(w[0] for w in m['name']['en'].split()[:2]))+'</div>'
            if m.get('thumbnail_image'):
                portrait=f'<img class="portrait" src="{esc(m["thumbnail_image"])}" alt="{esc(m["name"][LANG])}" loading="lazy" decoding="async">'
            elif m.get('portrait_crop') or m.get('thumbnail_crop'):
                portrait=frame_portrait(portrait,m.get('portrait_crop') or m['thumbnail_crop'])
            content+=f'<article class="person"><a href="{href(p)}">{portrait}</a><div><p class="eyebrow">{m["role"][LANG]}</p><h3><a href="{href(p)}">{esc(m["name"][LANG])}</a></h3>'+history(m)
            if m.get('profile_link'):content+='<p class="member-affiliation">'+member_profile_link(m)+'</p>'
            elif m['affiliation'][LANG]:content+='<p class="member-affiliation">'+member_affiliation(m)+'</p>'
            content+='</div></article>'
        content+='</div></section>'
    emit('/niil/members/',tr('People','구성원'),content,'members')
    photos=json.loads((SITE/'content/photos.json').read_text())
    content=heading('',tr('Lab photos','연구실 사진'))+'<section class="wrap photo-gallery"><a class="photo-back" href="/niil/members/">← '+tr('People','구성원')+'</a>'
    for photo in photos:
        content+=f'<figure class="lab-photo {esc(photo.get("frame", ""))}" id="{esc(photo["id"])}"><a href="{esc(photo["image"])}" target="_blank" rel="noopener" aria-label="{esc(photo["title"][LANG]+tr(" — open full size"," — 크게 보기"))}"><img src="{esc(photo["image"])}" alt="{esc(photo["title"][LANG])}" loading="lazy" decoding="async"></a><figcaption><h2>{esc(photo["title"][LANG])}</h2><p>{esc(photo["caption"][LANG])}</p></figcaption></figure>'
    content+='</section>'
    emit('/niil/photos/',tr('Lab photos','연구실 사진'),content,'members')
    for m in MEMBER_DATA:
        p=byid[m['id']];portrait=image(p,'portrait')
        if m.get('portrait_crop'):portrait=frame_portrait(portrait,m['portrait_crop'])
        content=heading('',esc(m['name'][LANG]))+'<section class="wrap document-layout"><aside><a href="/niil/members/">← '+tr('People','구성원')+'</a>'+portrait+'</aside><article class="prose"><h2>'+tr('At NiiL','NiiL 이력')+'</h2>'+history(m)
        if m.get('profile_link'):content+='<h2>'+tr('Profile','프로필')+'</h2><p>'+member_profile_link(m)+'</p>'
        elif m['affiliation'][LANG]:content+='<h2>'+tr('Affiliation','소속')+'</h2><p>'+member_affiliation(m)+'</p>'
        if m.get('updates'):
            content+='<h2>'+tr('Recent updates','최근 근황')+'</h2><ul>'
            for update in m['updates']:
                content+=f'<li><a href="{esc(update["url"])}" target="_blank" rel="noopener noreferrer">{esc(update["label"][LANG])} ↗</a> <span class="muted">({esc(update["date"])})</span></li>'
            content+='</ul>'
        if m['email']:content+='<h2>'+tr('Email','이메일')+'</h2><a href="mailto:'+esc(m['email'])+'">'+esc(m['email'])+'</a>'
        if m['reference']:content+=f'<p><a href="{m["reference"]}">{tr("UNICON Lab profile","UNICON Lab 구성원 소개")} ↗</a></p>'
        content+='</article></section>';emit(href(p),m['name'][LANG],content,'members')
    pubs=PUBLICATION_DATA['publications'];years=sorted({p['year'] for p in pubs},reverse=True)
    kind={'Journal':tr('Journal','학술지'),'Conference':tr('Conference','학술대회'),'Book chapter':tr('Book chapter','단행본 수록')}
    content=heading('',tr('Publications','논문'),f'{min(years)}–{max(years)}')+'<section class="wrap publication-catalog"><div class="filterbar">'
    content+=f'<label for="publication-search">{tr("Search","검색")}<input type="search" id="publication-search" placeholder="{tr("Title, author, or venue","제목, 저자, 게재처")}"></label><label for="publication-year">{tr("Year","연도")}<select id="publication-year"><option value="">{tr("All years","전체 연도")}</option>'+''.join(f'<option value="{y}">{y}</option>' for y in years)+f'</select></label><label for="publication-type">{tr("Type","유형")}<select id="publication-type"><option value="">{tr("All types","전체 유형")}</option>'+''.join(f'<option value="{k}">{v}</option>' for k,v in kind.items())+'</select></label></div>'
    content+=f'<p id="publication-count" aria-live="polite">{len(pubs)} {tr("publications","편")}</p><div class="publication-list">'
    for p in pubs:
        citation=p['venue']+(' '+p['volume'] if p['volume'] else '')+(' ('+p['issue']+')' if p['issue'] else '')+(', '+p['pages'] if p['pages'] else '')
        content+=f'''<article class="publication-row" data-publication data-search="{esc(p["title"]+" "+p["title_ko"]+" "+p["authors"]+" "+p["venue"])}" data-year="{p["year"]}" data-type="{p["type"]}"><div class="publication-year">{p["year"]}<span>{kind[p["type"]]}</span></div><div><h2><a href="{esc(p["url"])}">{esc(p['title'])} ↗</a></h2><p class="publication-authors">{esc(p["authors"])}</p><p class="publication-venue">{esc(citation)}</p></div></article>'''
    content+=f'</div><p id="publication-empty" hidden>{tr("No publications found.","검색 결과가 없습니다.")}</p><p class="publication-source">{tr("Source","출처")}: Google Scholar · {PUBLICATION_DATA["updated"]}</p></section>'
    emit('/niil/publications/',tr('Publications','논문'),content,'publications')
    course_content=heading('',tr('Course','강의자료'))+'<section class="wrap section compact"><p>'+tr('Read the course online, clone its repository, or download the complete ZIP.','온라인으로 읽거나, 과목별 저장소를 Clone하고 ZIP으로 한 번에 내려받을 수 있습니다.')+'</p><ul class="course-list">'
    for course in COURSE_DISTRIBUTION:
        repo='https://github.com/chorok-daddy/'+course['repository']
        course_content+='<li><a href="/niil/courses/'+course['slug']+'/index.html">'+esc(course['title'] if LANG=='ko' else course['title_en'])+'</a><div class="course-distribution"><a href="'+repo+'">'+tr('Source repository','원본 저장소')+' ↗</a><a href="'+repo+'/archive/refs/heads/main.zip">'+tr('Download ZIP','과목 묶음 ZIP')+'</a></div></li>'
    course_content+='</ul><p class="course-license">'+tr('Ki-Baek Lee · Kwangwoon University NiiL. Teaching content: CC BY 4.0; original code: MIT. Retain attribution and indicate modifications. Third-party terms remain applicable.','이기백 · 광운대학교 NiiL. 강의 설명·그림: CC BY 4.0 · 직접 작성한 코드: MIT. 출처를 유지하고 수정 사항을 밝혀 주세요. 제3자 자료는 별도 조건을 따릅니다.')+' <a href="/niil/courses/LICENSE.md">'+tr('License details','라이선스 안내')+'</a></p></section>'
    emit('/niil/courses/',tr('Course','강의자료'),course_content,'teaching')
    route_redirect('/niil/teaching/','/niil/courses/')
    application=(SITE/'content/join'/f'application-{LANG}.md').read_text().replace('{{CONTACT_FORM}}',CONTACT_FORM)
    application_html=subprocess.run(['pandoc','-f','markdown','-t','html','--wrap=none'],input=application,text=True,capture_output=True,check=True).stdout
    content=heading('',tr('Contact & apply','문의·지원'),tr('Research collaboration, lab applications and general inquiries.','연구 협업, 연구실 지원 및 일반 문의를 받습니다.'))
    content+='<section class="wrap section compact"><div class="inquiry-entry" id="inquiry"><h2>'+tr('Send an inquiry','문의·지원 접수')+'</h2><p>'+tr('Choose your inquiry type in the form and leave your message.','양식에서 문의 유형을 선택하고 내용을 남겨 주세요.')+'</p><a class="button" href="'+CONTACT_FORM+'">'+tr('Inquiry & application form','문의·지원 양식')+' ↗</a><p class="inquiry-note">'+tr('English / Korean · No Google account required','영어·한국어 지원 · Google 계정 불필요')+'</p></div><section class="join-guidance prose" id="join"><h2>'+tr('Joining the lab','연구실 참여 안내')+'</h2>'+application_html.replace('<h2','<h3').replace('</h2>','</h3>')+'</section><div class="contact-fallback"><p>'+tr('For course questions, use the course channel on KLAS.','수업 문의는 KLAS의 해당 과목 채널을 이용해 주세요.')+'</p><p>'+tr('If you cannot use the form: ','양식 이용이 어려운 경우: ')+'<a href="mailto:kw.artint@gmail.com">kw.artint@gmail.com</a></p></div></section>'
    emit('/niil/contact/',tr('Contact & apply','문의·지원'),content,'contact')
    for old_path in ['/niil/join/','/niil/join/apply/']+[href(p) for p in NOTICE]:route_redirect(old_path,'/niil/contact/#join')
    handled={p['id'] for p in PAGES[:6]}|{PAGES[12]['id']}|{p['id'] for p in AREAS+VISIONS+PROJECTS+MEMBERS+NOTICE}
    for p in PAGES:
        if p['id'] in handled:continue
        content=heading('',tr('Original course material','강의자료 원문'))+'<section class="wrap document-layout"><aside><a href="/niil/courses/">← '+tr('Course','강의자료')+'</a><nav class="toc" aria-label="'+tr('On this page','페이지 목차')+'"></nav></aside><article class="prose"><p class="archive-note">'+tr('Archived source material (Korean / English). Course content is retained in its original language; use KLAS for current semester announcements.','이전 강의 자료입니다. 원문 언어를 유지하며, 현재 학기 공지는 KLAS에서 확인해 주세요.')+'</p><div class="archive-source" lang="ko">'+meta(p)+render(p)+'</div></article></section>'
        emit(href(p),tr('Original course material','강의자료 원문'),content,'teaching')
(SITE/'content/routes.json').write_text(json.dumps(ROUTES,ensure_ascii=False,indent=2)+'\n')
# Keep canonical course documents intact, adding the same site frame on every build.
# Quarto scripts, styles, anchor IDs and relative download paths remain in place.
LANG='ko'
for course_file in sorted((SITE/'courses').rglob('*.html')):
    if course_file == SITE/'courses/index.html':continue
    doc=BeautifulSoup(course_file.read_text(),'html.parser')
    if not doc.body or doc.select_one('meta[http-equiv="refresh"]'):continue
    for old in doc.select('[data-niil-frame], .skip-site'):old.decompose()
    for home in doc.select('a[href="/niil/courses/"]'):
        sibling=home.find_next_sibling()
        if sibling and sibling.get_text(strip=True)=='/':sibling.decompose()
        home.decompose()
    for breadcrumb in doc.select('nav.breadcrumb'):
        if not breadcrumb.get_text(strip=True):breadcrumb.decompose()
    main=doc.select_one('main')
    if main is not None and not main.get('id'):main['id']='main'
    course=next((c for c in COURSE_DISTRIBUTION if course_file.is_relative_to(SITE/'courses'/c['slug'])),None)
    source_url='https://chorok-daddy.github.io/'+course_file.relative_to(ROOT).as_posix()
    credit=BeautifulSoup('<p class="course-credit" data-niil-frame>이기백 (Ki-Baek Lee) · 광운대학교 NiiL<br><a data-source-origin href="'+source_url+'">원본 강의자료</a> · 설명·그림 <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> · 코드 <a href="/niil/courses/LICENSES/MIT.txt">MIT</a></p>','html.parser')
    credit.p.append(Comment(EASTER_EGG_TEXT))
    main.append(credit)
    author_meta=doc.new_tag('meta',attrs={'name':'author','content':'Ki-Baek Lee (이기백)','data-niil-frame':''})
    doc.head.append(author_meta)
    structured=doc.new_tag('script',type='application/ld+json');structured['data-niil-frame']=''
    structured.string=json.dumps({'@context':'https://schema.org','@type':'LearningResource','name':doc.h1.get_text() if doc.h1 else doc.title.get_text(),'url':source_url,'author':{'@type':'Person','name':'Ki-Baek Lee','alternateName':'이기백','affiliation':{'@type':'Organization','name':'Kwangwoon University · NiiL'}},'license':'https://creativecommons.org/licenses/by/4.0/','creditText':'Teaching content: Ki-Baek Lee, CC BY 4.0. Original exercise code: MIT; see course LICENSE.md. Third-party terms retained.'},ensure_ascii=False)
    doc.head.append(structured)
    if course and course_file == SITE/'courses'/course['slug']/'index.html':
        repo='https://github.com/chorok-daddy/'+course['repository']
        downloads=BeautifulSoup('<nav class="course-distribution" data-niil-frame aria-label="자료 가져오기"><a href="'+repo+'">GitHub 저장소 ↗</a><a href="'+repo+'/archive/refs/heads/main.zip">과목 묶음 ZIP ↓</a></nav>','html.parser')
        main.h1.insert_after(downloads)
    frame=BeautifulSoup(shell(doc.h1.get_text() if doc.h1 else doc.title.get_text(),'','teaching'),'html.parser')
    # Course documents retain their original language; the bilingual catalog has the switch.
    frame.select_one('.language-switch').decompose()
    for selector in ['.skip','.site-header','footer']:
        element=frame.select_one(selector);element['data-niil-frame']=''
        if selector=='.skip':element['href']='#'+doc.select_one('main')['id']
        if selector=='footer':doc.body.append(element)
        else:doc.body.insert(0 if selector=='.skip' else 1,element)
    for element in frame.head.select('link[rel="stylesheet"],script[src]'):
        element['data-niil-frame']='';doc.head.append(element)
    bridge=doc.new_tag('link',rel='stylesheet',href='/niil/assets/courses.css?v=20261026-sharing1')
    bridge['data-niil-frame']='';doc.head.append(bridge)
    doc.body['class']=list(dict.fromkeys(doc.body.get('class',[])+['niil-course']))
    course_file.write_text(str(doc))
subprocess.run(['python3',str(ROOT/'tools/build_compat_routes.py')],check=True)
subprocess.run(['python3',str(ROOT/'tools/build_seo.py')],check=True)
print('Built Korean /niil/, English /niil/en/, and compatibility routes.')
