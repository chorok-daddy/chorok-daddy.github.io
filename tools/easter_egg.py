"""Keep the playful multilingual source note in a separate static file."""
import json
from pathlib import Path
TEMPLATE=json.loads((Path(__file__).resolve().parents[1]/'templates/website-easter-egg.json').read_text())
NOTE_PATH='assets/meta/cache/render.logtmp'
def render_text(site_name=None,author=None,author_ko=None):
    values=dict(TEMPLATE['defaults'])
    values.update({k:v for k,v in {'site_name':site_name,'author':author,'author_ko':author_ko}.items() if v is not None})
    lines=[TEMPLATE['label'].format(**values)]
    for language in TEMPLATE['language_order']:
        localized={**values,'author':values['author_ko'] if language=='ko' else values['author']}
        lines+=['',f'[{language}]',*[line.format(**localized) for line in TEMPLATE['translations'][language]]]
    return '\n'.join(lines)
def render_reference(path):return '<!-- ref: '+path+' -->'
def write_note(root):
    path=Path(root)/NOTE_PATH
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(render_text()+'\n')
EASTER_EGG_TEXT=render_text()
EASTER_EGG_HTML=render_reference('/niil/'+NOTE_PATH)
