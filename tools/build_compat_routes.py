#!/usr/bin/env python3
"""Maintain temporary course compatibility through 2026-2, and lab URL aliases.

Edit course content in the courses source repository; niil/courses is generated. Remove the course compatibility
manifest/files together at the approved 2026-12-31 cutoff, never the canonical files.
"""
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def redirect(path, target, anchors=()):
    escaped = html.escape(target, quote=True)
    ids = ''.join(f'<span id="{html.escape(x, quote=True)}"></span>' for x in anchors)
    # Fragment and query preservation matters for previously shared lecture links.
    text = ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<link rel="canonical" href="https://chorok-daddy.github.io{escaped}">'
            f'<meta http-equiv="refresh" content="0;url={escaped}">'
            '<meta name="robots" content="noindex,follow"><title>페이지 이동</title>'
            f'<script>location.replace({json.dumps(target)}+location.search+location.hash);</script>'
            f'</head><body>{ids}<a href="{escaped}">페이지로 이동</a></body></html>')
    p = ROOT / path.lstrip('/')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def main():
    redirect('/index.html', '/niil/')
    # Prior Korean links remain valid; English now has an explicit /en/ prefix.
    for path in (ROOT / 'niil').rglob('*.html'):
        rel = path.relative_to(ROOT / 'niil')
        if rel.parts[0] in ('en', 'ko', 'courses', 'assets'):
            continue
        redirect('/niil/ko/' + rel.as_posix(), '/niil/' + rel.as_posix())
    manifest = json.loads((ROOT / 'tools/course-compatibility.json').read_text())
    for item in manifest['files']:
        new = ROOT / item['new'].lstrip('/')
        old = ROOT / item['old'].lstrip('/')
        if item['kind'] == 'page':
            redirect(item['old'], item['new'], item['anchors'])
        else:
            # Static hosting cannot redirect arbitrary binary downloads. Keep an
            # exact mirror so existing direct downloads and Colab links work.
            old.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(new, old)


if __name__ == '__main__':
    main()
