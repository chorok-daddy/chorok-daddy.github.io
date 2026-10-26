#!/usr/bin/env python3
"""Export standalone course repositories without changing canonical download bytes."""
import argparse, hashlib, html, json, posixpath
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
ORIGIN='https://chorok-daddy.github.io'
CONFIG=json.loads((ROOT/'tools/course-distribution.json').read_text())

def export_course(course, destination):
    slug=course['slug']; base=f'/niil/courses/{slug}/'
    url=ORIGIN+base; repo=f"https://github.com/{CONFIG['owner']}/{course['repository']}"
    inputs={}
    for p in (ROOT/base.lstrip('/')).rglob('*'):
        if p.is_file():inputs['/'+p.relative_to(ROOT).as_posix()]=(p.relative_to(ROOT/base.lstrip('/')).as_posix(),p.read_bytes())
    for p in (ROOT/'assets').glob('*'):
        if p.is_file():inputs['/'+p.relative_to(ROOT).as_posix()]=('assets/'+p.name,p.read_bytes())
    for p in (ROOT/'niil/assets').glob('*'):
        if p.suffix in ('.css','.js'):inputs['/'+p.relative_to(ROOT).as_posix()]=('assets/niil/'+p.name,p.read_bytes())
    common=ROOT/'niil/courses/exam-format-examples.html'
    inputs['/niil/courses/exam-format-examples.html']=('common/exam-format-examples.html',common.read_bytes())
    for p in [ROOT/'niil/courses/LICENSE.md',*(ROOT/'niil/courses/LICENSES').glob('*')]:
        inputs['/'+p.relative_to(ROOT).as_posix()]=(p.relative_to(ROOT/'niil/courses').as_posix(),p.read_bytes())
    source_hashes={key:hashlib.sha256(data).hexdigest() for key,(_,data) in sorted(inputs.items())}
    version=hashlib.sha256(json.dumps(source_hashes,sort_keys=True).encode()).hexdigest()[:12]
    credit=f"이기백 (Ki-Baek Lee), 광운대학교 NiiL, {course['title']} ({course['title_en']}). {url} · CC BY 4.0 (teaching content), MIT (original code)."
    destination.mkdir(parents=True,exist_ok=True)
    for original,(relative,data) in inputs.items():
        target=destination/relative;target.parent.mkdir(parents=True,exist_ok=True)
        if target.suffix=='.html':
            soup=BeautifulSoup(data.decode(),'html.parser')
            for tag in soup.select('[href], [src]'):
                for attr in ('href','src'):
                    if not tag.get(attr) or tag.has_attr('data-source-origin'):continue
                    ref=urlsplit(tag[attr])
                    if ref.scheme and ref.scheme not in ('http','https'):continue
                    if ref.netloc and ref.netloc!='chorok-daddy.github.io':continue
                    if not ref.path:continue
                    absolute=posixpath.normpath(ref.path if ref.path.startswith('/') else posixpath.join(posixpath.dirname(original),ref.path))
                    if ref.path.endswith('/'):absolute+='/index.html'
                    if absolute in inputs:
                        rewritten=posixpath.relpath(inputs[absolute][0],posixpath.dirname(relative) or '.')
                        tag[attr]=urlunsplit(('', '',rewritten,ref.query,ref.fragment))
                    elif not ref.netloc:
                        tag[attr]=urlunsplit(('https','chorok-daddy.github.io',absolute,ref.query,ref.fragment))
            # Canonical URLs always identify the published original, never a local copy.
            for tag in soup.select('link[rel=canonical]'):tag['href']=ORIGIN+original
            data=str(soup).encode()
        elif target.suffix=='.ipynb':
            nb=json.loads(data)
            nb['cells'].insert(0,{'cell_type':'markdown','id':'niil-source-credit','metadata':{},'source':[f'> **Original source / 원본 출처**\n> {credit}\n> Source snapshot: `{version}`. Retain attribution and note any modifications.\n']})
            nb.setdefault('metadata',{})['niil_source']={'author':CONFIG['author'],'url':url,'snapshot':version,'content_license':'CC-BY-4.0','code_license':'MIT'}
            data=(json.dumps(nb,ensure_ascii=False,indent=1)+'\n').encode()
        target.write_bytes(data)
        if target.suffix in ('.mlx','.slx','.csv'):
            target.with_name(target.name+'.SOURCE.txt').write_text(credit+'\nSource file: '+ORIGIN+original+'\nSource snapshot: '+version+'\nSee LICENSE.md; third-party terms remain applicable.\n')
    readme=f'''# {course['title']} · {course['title_en']}

**이기백 (Ki-Baek Lee) · 광운대학교 NiiL**

[온라인 강의]({url}) · [ZIP 다운로드]({repo}/archive/refs/heads/main.zip) · [라이선스](LICENSE.md)

## 가져오기

```sh
git clone {repo}.git
```

GitHub의 **Code → Download ZIP**으로도 전체 자료를 받을 수 있습니다.
압축 해제 후 `index.html`을 열면 과목 목록과 강의 내용을 읽을 수 있습니다.
HTML 및 필요한 로컬 스타일은 포함되어 있습니다. 외부 링크, Colab, KLAS,
원격 글꼴·일부 외부 기능 및 데이터 접근은 인터넷이 필요합니다.

## 구성

- `index.html`: 과목별 강의 목록
- 주차별 폴더: 강의 HTML, 실습 안내, Notebook 또는 MATLAB 실습 파일
- `assets/`: 읽기에 필요한 스타일·스크립트
- `CITATION.cff`: GitHub **Cite this repository**용 인용 정보
- `SOURCE.json`: 원본 파일 경로·해시와 배포본 해시
- `LICENSE.md`, `LICENSES/`: 이용 조건과 전문

## 출처와 재사용

> {credit}

설명·그림은 CC BY 4.0, 직접 작성한 코드는 MIT입니다. 수정본에는 변경 사실을
기재해 주세요. 제3자 자료·라이브러리·데이터의 기존 조건은 유지됩니다.
노트북 첫 셀에는 출처가 포함되어 있고, MATLAB 파일에는 `.SOURCE.txt`가 함께
제공됩니다. 원본 MATLAB·데이터 파일의 바이트는 변경하지 않았습니다.

<!-- NiiL Easter Egg: 이 주석까지 읽었다면 당신도 동료 공돌이입니다.
이기백 교수님을 향한 respect += 1;
단, 과학적 반박과 버그 제보는 언제나 환영합니다.
자료가 유용했다면 원 저자에 대한 shout out을 매우 적극적으로 충분히 널리 해 주세요 -->

## 버전 및 기여

원본 스냅샷: `{version}`.
이 저장소는 [강의 사이트 원본 저장소](https://github.com/chorok-daddy/chorok-daddy.github.io/tree/master/niil/courses/{slug})에서 내보낸 과목별 배포본입니다.
정정·개선 제안은 원본 저장소로 보내 주세요. 원본 수정 후 공식 배포 명령으로
이 저장소를 갱신합니다. 로컬 수정본은 별도 브랜치/Fork에서 관리할 수 있습니다.
'''
    (destination/'README.md').write_text(readme)
    (destination/'CITATION.cff').write_text(f'''cff-version: 1.2.0
message: "Please cite these course materials when reusing them."
type: dataset
title: "{course['title_en']} — NiiL course materials"
authors:
  - family-names: "Lee"
    given-names: "Ki-Baek"
    affiliation: "Kwangwoon University"
url: "{url}"
repository-code: "{repo}"
version: "{version}"
license:
  - CC-BY-4.0
  - MIT
''')
    manifest={'source_repository':'https://github.com/chorok-daddy/chorok-daddy.github.io','source_path':base,'snapshot':version,'source_sha256':source_hashes,'files':{p.relative_to(destination).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(destination.rglob('*')) if p.is_file() and '.git' not in p.parts and p.name!='SOURCE.json'}}
    (destination/'SOURCE.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    return {'repository':course['repository'],'snapshot':version,'files':len(manifest['files'])}

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    for c in CONFIG['courses']:print(json.dumps(export_course(c,a.output/c['repository']),ensure_ascii=False))
