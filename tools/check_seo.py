#!/usr/bin/env python3
"""Validate canonical search metadata, sitemap alternatives and structured data."""
import json
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1];BASE='https://chorok-daddy.github.io'
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
root=ET.parse(ROOT/'sitemap.xml').getroot();urls=[u.find('s:loc',ns).text for u in root]
assert len(urls)==len(set(urls))
for item in root:
 url=item.find('s:loc',ns).text;path=urlsplit(url).path
 file=ROOT/path.lstrip('/')
 if path.endswith('/'):file=file/'index.html'
 assert file.is_file(),url
 doc=BeautifulSoup(file.read_text(),'html.parser')
 assert not doc.select_one('meta[http-equiv=refresh]'),url
 assert 'noindex' not in doc.select_one('meta[name=robots]')['content'],url
 assert len(doc.select('link[rel=canonical]'))==1 and doc.select_one('link[rel=canonical]')['href']==url,url
 assert doc.title.get_text().strip() and doc.select_one('meta[name=description]')['content'].strip(),url
 assert doc.select_one('meta[property="og:url"]')['content']==url,url
 for link in item.findall('x:link',ns):assert link.attrib['href'] in urls,link.attrib
 for block in doc.select('script[type="application/ld+json"]'):json.loads(block.string)
faculty=BeautifulSoup((ROOT/'niil/pages/ki-baek-lee-36f11249/index.html').read_text(),'html.parser')
graph=json.loads(faculty.select_one('script[data-niil-seo]').string)['@graph']
assert any(n['@type']=='ProfilePage' for n in graph)
assert any(n['@type']=='Person' and 'yZ9xxNcAAAAJ' in n['sameAs'][0] for n in graph)
assert 'Sitemap: '+BASE+'/sitemap.xml' in (ROOT/'robots.txt').read_text()
print(f'PASS: {len(urls)} canonical URLs, sitemap, language alternatives and JSON-LD; verified faculty identity link.')
