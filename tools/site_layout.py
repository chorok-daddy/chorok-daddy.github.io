"""Own the lab output set; course publications are owned by their pinned import."""
import json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'niil'
def owns(name):
    if name=='niil/index.html':return False
    if not name.startswith('niil/') or not name.endswith('.html'):return False
    for prefix in ('niil/ko/courses/','niil/en/courses/'):
        if name.startswith(prefix):return name.removeprefix(prefix) in ('index.html','reuse.html')
    return not name.startswith(('niil/assets/','niil/content/'))
def finish(generated):
    expected={name for name in generated if owns(name)}
    ledger=ROOT/'tools/site-output.json'
    previous=set(json.loads(ledger.read_text())['html']) if ledger.exists() else set()
    tracked=set(subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()) if (ROOT/'.git').exists() else set()
    for p in SITE.rglob('*.html'):
        name=p.relative_to(ROOT).as_posix()
        # Unknown untracked drafts are reported by validation, never silently deleted.
        if owns(name) and name not in expected and name in (previous|tracked):p.unlink()
    for p in sorted(SITE.rglob('*'),key=lambda p:len(p.parts),reverse=True):
        if p.is_dir() and not any(p.iterdir()):p.rmdir()
    (ROOT/'tools/site-output.json').write_text(json.dumps({'html':sorted(expected)},indent=2)+'\n')
