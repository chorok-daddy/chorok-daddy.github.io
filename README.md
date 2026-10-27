# 강의자료 사이트

학생 배포 주소: https://chorok-daddy.github.io/

## 현재 원본

`chorok-daddy/courses`의 `courses/<slug>/lessons/`와 `materials/`가 편집 원본이다. 이 저장소의 `niil/courses/`는 커밋을 고정해 가져온 게시본이며 직접 편집하지 않는다. `site-catalog.json`은 실제 원본 파일과 주차를 가리키는 목록이다. `assets/`는 공통 스타일·동작을 관리한다.

원본을 수정하고 가져온 뒤 `python3 tools/check_site.py`로 로컬 파일·anchor·Notebook 구조를 확인한다. 화면·수식·실습 실행과 외부 서비스 로그인/복사는 변경 영향에 맞춰 별도로 확인한다. 도구가 외부 주소를 검사한 것으로 해석하지 않는다.

`/`는 `/niil/`로 이동하며, 강의자료는 `/niil/courses/` → 과목 → 각 주차 자료로 연결된다. 기존 `/courses/` 주소는 2026년 12월 31일 제거 전까지 호환용으로 유지한다. 과제 안내와 실습 파일도 해당 주차 폴더에서 관리한다.

## 설계와 배포

계획·평가·개선 전략은 별도 private 운영 저장소에서 관리한다. 이 저장소는 학생용 원본과 실제 구현·배포 이력을 축적한다. 공개 전 문제·정답·조교 기록을 추가하지 않는다.

검증 후 기존 GitHub Pages 배포 경로를 사용한다. 배포 후 실제 공개 URL을 확인한다. `release.json`은 학기 배포 표식이며 개별 수정의 식별자는 Git commit이다.

## 실습 도입

각 실습의 assignment.html 상단에 `opening-digest`를 둔다. 주차의 개념이 왜 필요한지 묻는 질문 2~3개를 선택하고, 각 질문 바로 아래에 독립된 `<details>`로 핵심 항목 2~3개의 정리를 넣는다. 기본은 접힘이며 학생 의견을 들은 뒤 해당 질문만 펼친다. 절차·함수 사용법 퀴즈로 도입을 대신하지 않는다. 공통 스타일은 assets/site.css에서 관리하고 질문·정리는 각 HTML에서 편집한다. 시험 안내에는 실습 도입을 붙이지 않는다.

도입 제목은 짧은 개념명으로 쓰고 본문에서 구체적인 질문을 제시한다. 참여를 유도하는 상투적 문구와 답이 자명한 수사적 질문은 줄인다. 설명은 친절하게 유지하되 학생의 행동을 불필요하게 지시하지 않는다.

질문의 우선 기준은 학생이 실습의 필요성을 이해하는가이다. 용어·조건을 알고 있다는 전제에서 곧바로 세부 지식을 묻지 않는다. 익숙한 대상이나 목적에서 출발하고 전문 개념은 펼친 설명에서 연결한다. 간결함을 위해 필요한 맥락까지 생략하지 않는다.

학습자료는 개념과 상세 설명의 중심이며, 실습 안내는 수행 조건·작업·제출 방법을 관리한다. `opening-digest`는 질문별 짧은 복습과 실습 목적 설정을 유지하고 자세한 설명은 학습자료로 연결한다. 긴 시나리오와 상세 실습 지시를 양쪽에 중복 저장하지 않는다.

## 강의자료 원본과 게시

[통합 강의 저장소](https://github.com/chorok-daddy/courses)에서 모든 과목의 강의,
Notebook, MATLAB·Simulink, 데이터와 원자료를 관리합니다. 학기·개설 여부는
해당 저장소의 `catalog.json`에 기록하며 과목 경로는 바꾸지 않습니다.

이 사이트는 `tools/course-source.json`에 고정된 커밋과 해시를 기준으로 원본을
가져와 연구실 공통 프레임·검색 메타데이터·기존 URL 호환을 적용합니다.
`tools/course-catalog.json`, `niil/courses/`, `assets/site.css`는 생성 결과입니다.
별도 과목 배포 저장소와 ZIP 산출물은 사용하지 않습니다.

원본 저장소에서 검증·commit·push한 뒤:

```sh
python3 tools/sync_courses.py --source ../courses
python3 tools/build_niil.py
python3 tools/check_site.py
python3 tools/check_migration.py
python3 tools/check_course_source.py
python3 tools/check_seo.py
# 이 사이트 변경을 commit/push → GitHub Pages
```

일반 사이트 빌드는 마지막에 고정한 원본 커밋을 재현합니다. 인접 `courses`
체크아웃이 없으면 GitHub에서 해당 커밋을 가져옵니다. 신규 강의 내용을 게시할 때만
명시적으로 원본 커밋을 갱신하므로 사이트 작업 중 강의가 임의로 바뀌지 않습니다.
학생용 HTML·다운로드 URL은 유지하며, Colab·MATLAB 실행 링크는 통합 원본을 가리킵니다.
Notebook의 이전 웹 주소도 현재 주소로 갱신했습니다. 계산 코드·문제·데이터는 변경하지 않았습니다.

[강의 라이선스](niil/courses/LICENSE.md): 저자 소유 설명·그림 CC BY 4.0,
직접 작성한 코드 MIT. 제3자 자료는 기존 조건을 따릅니다. 연구실 사진 등 다른
사이트 자료에 적용하는 허가는 아닙니다.

## 검색 메타데이터

`build_niil.py` 마지막 단계에서 `tools/build_seo.py`가 검색 제목·설명,
canonical/hreflang, Open Graph, JSON-LD, `sitemap.xml`과 `robots.txt`를 갱신한다.
화면 본문은 수정하지 않는다. 사이트맵에는 실제 콘텐츠의 대표 주소만 넣고
이동용 페이지는 제외한다. 갱신 시 `python3 tools/check_seo.py`를 실행한다.
Search Console 소유권 확인·사이트맵 제출은 Google 계정에서 별도로 완료해야 하며,
파일 생성만으로 Google 색인이나 검색 순위가 보장되지는 않는다.
