"""Build only the two deliberate default entry points; retired routes are absent."""
import json
from pathlib import Path
from publication_layout import LAYOUT,browser_script
ROOT=Path(__file__).resolve().parents[1]
def redirect(name,target):
    path=ROOT/name;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="robots" content="noindex,follow"><meta http-equiv="refresh" content="0;url='+target+'"><title>NiiL</title><link rel="canonical" href="https://chorok-daddy.github.io'+target+'"><script>location.replace('+json.dumps(target)+'+location.search+location.hash)</script></head><body><a href="'+target+'">NiiL</a></body></html>')
redirect('index.html','/niil/')
redirect('niil/index.html','/niil/'+LAYOUT['default_language']+'/')
(ROOT/'niil/assets/routes.js').write_text(browser_script())
