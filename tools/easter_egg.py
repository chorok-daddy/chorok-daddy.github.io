"""Render the owner's playful, source-only multilingual website signature."""
import json
from pathlib import Path

TEMPLATE=json.loads((Path(__file__).resolve().parents[1]/'templates/website-easter-egg.json').read_text())

def render_text(site_name=None, author=None, author_ko=None):
    values=dict(TEMPLATE['defaults'])
    values.update({k:v for k,v in {'site_name':site_name,'author':author,'author_ko':author_ko}.items() if v is not None})
    lines=[TEMPLATE['label'].format(**values)]
    for language in TEMPLATE['language_order']:
        localized={**values,'author':values['author_ko'] if language=='ko' else values['author']}
        lines+=['',f'[{language}]',*[line.format(**localized) for line in TEMPLATE['translations'][language]]]
    text='\n'.join(lines)
    if '--' in text:raise ValueError('Easter egg text must be safe for an HTML comment')
    return text

EASTER_EGG_TEXT=render_text()
EASTER_EGG_HTML='<!--\n'+EASTER_EGG_TEXT+'\n-->'
