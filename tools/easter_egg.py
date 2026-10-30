"""Compile the shared multilingual template into a shared stylesheet comment."""
import json,re
from pathlib import Path
TEMPLATE=json.loads((Path(__file__).resolve().parents[1]/'templates/website-easter-egg.json').read_text())
def render_text(site_name=None,author=None,author_ko=None):
    values=dict(TEMPLATE['defaults'])
    values.update({k:v for k,v in {'site_name':site_name,'author':author,'author_ko':author_ko}.items() if v is not None})
    lines=[TEMPLATE['label'].format(**values)]
    for language in TEMPLATE['language_order']:
        localized={**values,'author':values['author_ko'] if language=='ko' else values['author']}
        lines+=['',f'[{language}]',*[line.format(**localized) for line in TEMPLATE['translations'][language]]]
    return '\n'.join(lines)
def strip_note(text):return re.sub(r'/\*\s*NiiL Easter Egg[\s\S]*?\*/\s*','',text)
def render_css():return '/*\n'+render_text()+'\n*/'
def write_note(root,stylesheet):
    css=Path(root)/stylesheet
    css.write_text(strip_note(css.read_text()).rstrip()+'\n\n'+render_css()+'\n')
EASTER_EGG_TEXT=render_text()
EASTER_EGG_HTML=''
