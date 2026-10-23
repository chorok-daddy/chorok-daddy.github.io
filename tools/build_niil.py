#!/usr/bin/env python3
"""Build the isolated NiiL site from the preserved public Notion content."""
import html, json, re, subprocess
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'niil'
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
def shell(title, content, section='', desc='Nature-inspired Intelligence Lab at Kwangwoon University', path='/niil/'):
    nav=""
    for n,s in NAV:
        current='aria-current="page"' if section==s else ""
        nav+=f'<a {current} href="/niil/{s}/">{n}</a>'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} · NiiL</title><meta name="description" content="{esc(desc)}"><meta name="robots" content="noindex,nofollow"><link rel="stylesheet" href="/niil/assets/niil.css"><script src="/niil/assets/niil.js" defer></script></head><body><a class="skip" href="#main">Skip to content</a><header class="site-header"><a class="brand" href="/niil/" aria-label="NiiL home">NiiL<span class="brand-dot">●</span></a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu <span aria-hidden="true">☰</span></button><nav id="site-nav" aria-label="Main navigation">{nav}<a class="contact-nav" href="/niil/contact/">Contact ↗</a></nav></header><main id="main">{content}</main><footer><a class="brand" href="/niil/">NiiL<span class="brand-dot">●</span></a><div>Nature-inspired Intelligence Lab<br><span>Kwangwoon University · Seoul, Korea</span></div><a href="mailto:kw.artint@gmail.com">Let’s connect ↗</a><small>© NiiL · Nature inspires. Intelligence evolves.</small></footer></body></html>'''
def heading(kicker,title,desc=''):
    lead=f'<p class="lede">{desc}</p>' if desc else ""
    return f'<section class="page-heading wrap"><p class="eyebrow">{kicker}</p><h1>{title}</h1>{lead}</section>'
def write(path,text):
    p=ROOT/path.lstrip('/')/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
def cards(ps,kind='area'):
    return '<div class="cards">'+''.join(f'<article class="card {kind}"><a class="image-link" href="{href(p)}">{image(p)}</a><div class="card-copy"><p class="eyebrow">{esc(" · ".join(props(p).get("Tags",[])))}</p><h3>{link(p)}</h3></div></article>' for p in ps)+'</div>'
def cluster_cards():
    content='<div class="cluster-grid">'
    for i,(name,key,title,description) in enumerate(CLUSTERS):
        count=sum(p['cluster']==name for p in CATALOG)
        content+=f'<a class="cluster-card cluster-{key}" href="/niil/research/?topic={key}#project-catalog"><span class="cluster-number">0{i+1}</span><p class="eyebrow">{name}</p><h3>{title}</h3><p>{description}</p><span class="cluster-count">{count} projects <b aria-hidden="true">↗</b></span></a>'
    return content+'</div>'

def redirect(path,target,title):
    page=shell(title,heading('RESEARCH',title)+f'<section class="wrap section compact"><a class="button" href="{target}">Explore research projects ↗</a></section>','research')
    page=page.replace('<meta charset="utf-8">',f'<meta charset="utf-8"><meta http-equiv="refresh" content="0;url={target}"><link rel="canonical" href="{target.split("?")[0]}">')
    write(path,page)

def database(match):
    attrs=match[1];c=re.search(r'data-source-url="([^"]+)"',attrs);url=re.search(r'url="([^"]+)"',attrs)
    ps=rows(c[1]) if c else []
    if not ps:
        u=url[1].replace('https://app.notion.com/p/','https://niilab.notion.site/') if url else 'https://niilab.notion.site/'
        return '\n\n<a class="button outline" href="https://niilab.notion.site/We-are-hiring-1b0888a17b30808398d1cbc97f1fa2ba">Application form on Notion ↗</a>\n\n'
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
def rosette():
    import math
    dots=''.join(f'<circle cx="{300+math.sqrt(i)*12*math.cos(i*2.39996):.2f}" cy="{300+math.sqrt(i)*12*math.sin(i*2.39996):.2f}" r="{2+i/160:.2f}" fill="{["#adc69d","#dfebbc","#789f81"][i%3]}" opacity="{.35+i/400:.2f}"/>' for i in range(1,400))
    return f'<svg viewBox="0 0 600 600" role="img" aria-labelledby="pattern-title"><title id="pattern-title">A sunflower-inspired pattern of interconnected possibilities</title><circle cx="300" cy="300" r="265" fill="none" stroke="#a1b899" stroke-opacity=".22"/><circle cx="300" cy="300" r="200" fill="none" stroke="#a1b899" stroke-opacity=".18"/>{dots}</svg>'
home=f'''<section class="hero"><div class="hero-copy"><p class="eyebrow">KWANGWOON UNIVERSITY · NATURE-INSPIRED INTELLIGENCE LAB</p><h1>Inspired by nature.<br>Intelligence for<br><em>the real world.</em></h1><p>We explore the intersection of natural phenomena and artificial intelligence to develop innovative solutions for complex problems.</p><a class="button" href="/niil/research/">Explore our research <span>↗</span></a></div><div class="hero-art">{rosette()}<span>FROM NATURAL PATTERNS TO NEW POSSIBILITIES</span></div><div class="hero-bottom"><span>Nature-inspired Intelligence Lab</span><a href="#research">Discover NiiL ↓</a></div></section>
<section class="wrap section" id="research"><div class="section-title"><div><p class="eyebrow">01 / RESEARCH</p><h2>Intelligence, in context.</h2></div><a href="/niil/research/">Explore research projects ↗</a></div>{cluster_cards()}</section>
<section class="wrap section"><div class="section-title"><div><p class="eyebrow">02 / PROJECT SPOTLIGHT</p><h2>Ideas meet the physical world.</h2></div><a href="/niil/research/">All projects ↗</a></div><a class="spotlight" href="{href(PROJECTS[0])}"><div class="spotlight-concept"><span>SPACE × LEARNING × ACTION</span><strong>3.3 m²</strong><p>A robot-centric workspace</p><small>Research target · 2026–2031</small></div><div><span class="badge">ONGOING · 2026—2031</span><h3>Robot-Centric Physical AI</h3><p>High-density operations in extremely tight spaces.</p><p class="korean">극협소 공간 내 고밀도 작업을 위한 로봇 중심의 피지컬 인공지능 기술</p><span>Explore project ↗</span></div></a></section>
<section class="wrap section news-section"><div><p class="eyebrow">03 / NEWS & OPPORTUNITIES</p><h2>Grow with NiiL.</h2><p>Explore, learn, and build with us.</p></div><a class="news-item" href="{href(NOTICE[0])}"><span class="eyebrow">OPPORTUNITIES · 08 MAR 2025</span><h3>Undergraduate internships <span>↗</span></h3><p>Applications welcome at any time. Discover the program and how to apply.</p></a></section>'''
write('/niil/',shell('Nature-inspired Intelligence Lab',home))

write('/niil/vision/',shell('Our Vision',heading('ABOUT NiiL','Intelligence with purpose.','NiiL explores the intersection of natural phenomena and artificial intelligence to develop innovative solutions for complex problems.')+'<section class="wrap section compact">'+cards(VISIONS)+'</section>'))

groups=[('Professor',lambda p:props(p).get('Position')=='Prof.'),('Graduate researchers',lambda p:props(p).get('Status')!='Alumni' and props(p).get('Position')!='Prof.'),('Alumni',lambda p:props(p).get('Status')=='Alumni')]
content=heading('PEOPLE','The people behind the ideas.','Our researchers and alumni connect curiosity with practical discovery.')
for name,predicate in groups:
    content+=f'<section class="wrap section compact"><h2 class="group-title">{name}</h2><div class="people-grid">'
    for p in filter(predicate,MEMBERS):
        pr=props(p);portrait=image(p,'portrait') or f'<div class="initials" aria-hidden="true">{"".join(w[0] for w in p["title"].split()[:2])}</div>'
        content+=f'<article class="person"><a href="{href(p)}">{portrait}</a><div><p class="eyebrow">{esc(pr.get("Position",""))}</p><h3>{link(p)}</h3><p>{esc(pr.get("Current Affliation",""))}</p><p class="muted">{esc(pr.get("Period",""))}</p></div></article>'
    content+='</div></section>'
write('/niil/members/',shell('People',content,'members'))

content=heading('RESEARCH / PROJECTS','From ideas to<br>working systems.','로봇의 행동, 물리적 세계의 인식, 사람과의 상호작용. 세 가지 연구 흐름에서 이어지는 프로젝트와 기여를 살펴보세요.')+'<section class="wrap section compact">'+cluster_cards()+'</section>'
content+='<section class="wrap section compact" id="project-catalog"><div class="section-title"><div><p class="eyebrow">PROJECT CATALOG</p><h2>Research in action.</h2></div></div><div class="filterbar"><label for="project-search">Find a project<input type="search" id="project-search" placeholder="Title, sponsor, or topic"></label><label for="project-topic">Research theme<select id="project-topic"><option value="">All themes</option>'+''.join(f'<option value="{key}">{name}</option>' for name,key,_,_ in CLUSTERS)+'</select></label><label for="project-status">Status<select id="project-status"><option value="">All projects</option><option value="In progress">Ongoing</option><option value="Done">Completed</option></select></label></div><p id="project-count" class="muted" aria-live="polite"></p><div class="project-list">'
for project in sorted(CATALOG,key=lambda p:p['start'],reverse=True):
    p=byid[project['page_id']]
    topic=next(c[1] for c in CLUSTERS if c[0]==project['cluster'])
    state={'In progress':'Ongoing','Done':'Completed'}[project['status']]
    content+=f'<article class="project-row" data-project data-topic="{topic}" data-status="{esc(project["status"])}"><div><span class="badge">{state}</span><p class="muted">{project["start"][:4]} — {project["end"][:4]}</p></div><div><p class="eyebrow">{project["cluster"]}</p><h2>{link(p)}</h2><p class="project-summary">{esc(project["summary"])}</p><p class="korean">{esc(project["title_ko"])}</p><p class="muted">{esc(" · ".join(project["sponsors"]))}</p></div></article>'
content+='</div><p id="no-projects" hidden>No projects match your search. Try another topic or keyword.</p></section>'
write('/niil/research/',shell('Research & Projects',content,'research'))
redirect('/niil/projects/','/niil/research/','Research & Projects')
publication_data=json.loads((SITE/'content/publications.json').read_text())
publications=publication_data['publications']
years=sorted({p['year'] for p in publications},reverse=True)
content='<header class="wrap publication-heading"><h1>Publications</h1><p class="muted">'+str(len(publications))+' publications · '+str(min(years))+'–'+str(max(years))+'</p></header>'
content+='<section class="wrap publication-catalog"><div class="filterbar"><label for="publication-search">Search<input type="search" id="publication-search" placeholder="Title, author, or venue"></label><label for="publication-year">Year<select id="publication-year"><option value="">All years</option>'+''.join(f'<option value="{y}">{y}</option>' for y in years)+'</select></label><label for="publication-type">Type<select id="publication-type"><option value="">All types</option><option>Journal</option><option>Conference</option><option>Book chapter</option></select></label></div>'
content+=f'<p id="publication-count" class="muted" aria-live="polite">{len(publications)} publications</p><div class="publication-list">'
for p in sorted(publications,key=lambda p:p['year'],reverse=True):
    citation=p['venue']
    if p['volume']: citation+=' '+p['volume']
    if p['issue']: citation+=' ('+p['issue']+')'
    if p['pages']: citation+=', '+p['pages']
    content+=f'<article class="publication-row" data-publication data-year="{p["year"]}" data-type="{p["type"]}"><div class="publication-year">{p["year"]}<span>{p["type"]}</span></div><div><h2><a href="{esc(p["url"])}">{esc(p["title"])} <span aria-hidden="true">↗</span></a></h2><p class="publication-authors">{esc(p["authors"])}</p><p class="publication-venue">{esc(citation)}</p></div></article>'
content+='</div><p id="publication-empty" hidden>No publications found.</p><p class="publication-source">Source: Google Scholar · Updated '+publication_data['updated']+'</p></section>'
write('/niil/publications/',shell('Publications',content,'publications'))
content=heading('TEACHING','Learn by understanding.<br>Understand by building.','Course information, schedules, and practical learning resources.')+'<section class="wrap section compact"><div class="course-grid">'
for i,p in enumerate(PAGES[6:12]):
    content+=f'<a class="course-card" href="{href(p)}"><span class="eyebrow">COURSE 0{i+1}</span><h2>{esc(p["title"])}</h2><span>Course overview & schedule ↗</span></a>'
content+='</div><div class="resource-note"><h3>Current course materials</h3><p>인공지능응용·제어공학1의 현재 강의자료와 실습 파일은 별도 강의자료 사이트에서 확인할 수 있습니다.</p><a href="/courses/">강의자료 바로가기 ↗</a></div></section>'
write('/niil/teaching/',shell('Teaching',content,'teaching'))
write('/niil/contact/',shell('Contact',heading('CONTACT','Let’s explore what’s next.','Research collaboration, lab inquiries, and undergraduate internships.')+'<section class="wrap section compact"><a class="contact-panel" href="mailto:kw.artint@gmail.com">kw.artint@gmail.com <span>↗</span></a><p class="muted">Nature-inspired Intelligence Lab · Kwangwoon University</p><div class="resource-note"><h2>Join the lab</h2><p>Learn about undergraduate internships and the application process.</p>'+link(NOTICE[0],'Internship opportunities')+'</div></section>'))

custom=set(p['id'] for p in PAGES[:6])|{PAGES[12]['id']}
for p in PAGES:
    if p['id'] in custom:continue
    if p in AREAS:
        redirect(href(p),'/niil/research/','Research & Projects')
        continue
    section='teaching' if p in PAGES[6:12] or (p['collection'] or '').startswith('collection://1ba888') else ('members' if p in MEMBERS else ('research' if p in PROJECTS else 'research'))
    parent='/niil/'+section+'/'
    label=section.upper()
    for course in PAGES[6:12]:
        if p['collection'] and p['collection'] in course['body']:
            parent=href(course)
            label=course['title']
    content=heading(esc(label),esc(display_title(p)),esc(PROJECT_BY_ID.get(p['id'],{}).get('summary','')))+f'<section class="wrap document-layout"><aside><a href="{parent}">← Back to {esc(label.lower())}</a><nav aria-label="On this page" class="toc"></nav></aside><article class="prose">'
    if p in PAGES[6:12]:
        content+='<p class="archive-note">Notion에서 이전한 강의 안내입니다. 수업 시간·평가 기준은 원본 시점의 내용이며, 현재 학기 공지는 KLAS에서 확인해 주세요.</p>'
        if p==PAGES[8]:content+='<a class="button outline" href="/courses/control-1/">현재 제어공학1 강의자료 ↗</a>'
        if p==PAGES[10]:content+='<a class="button outline" href="/courses/ai-applications/">현재 인공지능응용 강의자료 ↗</a>'
    if p['id'] in PROJECT_BY_ID:
        project=PROJECT_BY_ID[p['id']]
        content+=f'<p class="eyebrow">{project["cluster"]}</p>'
        content+=meta(p)
        if project.get('highlights'):
            content+='<div class="result-highlights">'+''.join(f'<div><strong>{esc(value)}</strong><span>{esc(label)}</span></div>' for value,label in project['highlights'])+'</div>'
        content+=render(p)
        if project['phases']:
            content+='<details class="project-phases"><summary>연차·관련 계약 이력</summary><div class="table-scroll"><table><thead><tr><th>기간</th><th>과제·계약</th><th>지원기관</th></tr></thead><tbody>'
            for phase in project['phases']:
                content+=f'<tr><td>{phase["start"]} — {phase["end"]}</td><td>{esc(phase["title"])}</td><td>{esc(phase["sponsor"])}</td></tr>'
            content+='</tbody></table></div></details>'
        related=[x for x in CATALOG if x['cluster']==project['cluster'] and x['key']!=project['key']][:3]
        content+='<section class="related-projects"><h2>Related research</h2><ul>'+''.join(f'<li>{link(byid[x["page_id"]])}</li>' for x in related)+'</ul></section>'
    else:
        content+=meta(p)+render(p)
    if not p['body']:content+='<p class="muted">'+esc(props(p).get('Details',''))+'</p>'
    content+='</article></section>'
    write(href(p),shell(display_title(p),content,section,path=href(p)))

(SITE/'content/routes.json').write_text(json.dumps(ROUTES,ensure_ascii=False,indent=2))
print(f'Built {len(ROUTES)+1} NiiL pages. Root index and courses remain untouched.')
