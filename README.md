# 강의자료 사이트

학생 배포 주소: https://chorok-daddy.github.io/

## 현재 원본

`niil/courses/`의 HTML과 실습 파일이 현재 편집 원본이다. 이전 임시 폴더의 생성 원고를 다시 실행해 덮어쓰지 않는다. `site-catalog.json`은 실제 원본 파일과 주차를 가리키는 목록이다. `assets/`는 공통 스타일·동작을 관리한다.

HTML을 직접 수정한 뒤 `python3 tools/check_site.py`로 로컬 파일·anchor·Notebook 구조를 확인한다. 화면·수식·실습 실행과 외부 서비스 로그인/복사는 변경 영향에 맞춰 별도로 확인한다. 도구가 외부 주소를 검사한 것으로 해석하지 않는다.

`/`는 `/niil/`로 이동하며, 강의자료는 `/niil/courses/` → 과목 → 각 주차 자료로 연결된다. 기존 `/courses/` 주소는 2026년 12월 31일 제거 전까지 호환용으로 유지한다. 과제 안내와 실습 파일도 해당 주차 폴더에서 관리한다.

## 설계와 배포

계획·평가·개선 전략은 별도 private 운영 저장소에서 관리한다. 이 저장소는 학생용 원본과 실제 구현·배포 이력을 축적한다. 공개 전 문제·정답·조교 기록을 추가하지 않는다.

검증 후 기존 GitHub Pages 배포 경로를 사용한다. 배포 후 실제 공개 URL을 확인한다. `release.json`은 학기 배포 표식이며 개별 수정의 식별자는 Git commit이다.

## 실습 도입

각 실습의 assignment.html 상단에 `opening-digest`를 둔다. 주차의 개념이 왜 필요한지 묻는 질문 2~3개를 선택하고, 각 질문 바로 아래에 독립된 `<details>`로 핵심 항목 2~3개의 정리를 넣는다. 기본은 접힘이며 학생 의견을 들은 뒤 해당 질문만 펼친다. 절차·함수 사용법 퀴즈로 도입을 대신하지 않는다. 공통 스타일은 assets/site.css에서 관리하고 질문·정리는 각 HTML에서 편집한다. 시험 안내에는 실습 도입을 붙이지 않는다.

도입 제목은 짧은 개념명으로 쓰고 본문에서 구체적인 질문을 제시한다. 참여를 유도하는 상투적 문구와 답이 자명한 수사적 질문은 줄인다. 설명은 친절하게 유지하되 학생의 행동을 불필요하게 지시하지 않는다.

질문의 우선 기준은 학생이 실습의 필요성을 이해하는가이다. 용어·조건을 알고 있다는 전제에서 곧바로 세부 지식을 묻지 않는다. 익숙한 대상이나 목적에서 출발하고 전문 개념은 펼친 설명에서 연결한다. 간결함을 위해 필요한 맥락까지 생략하지 않는다.

학습자료는 개념과 상세 설명의 중심이며, 실습 안내는 수행 조건·작업·제출 방법을 관리한다. `opening-digest`는 질문별 짧은 복습과 실습 목적 설정을 유지하고 자세한 설명은 학습자료로 연결한다. 긴 시나리오와 상세 실습 지시를 양쪽에 중복 저장하지 않는다.

## 과목별 Clone / ZIP 배포

- 인공지능응용: https://github.com/chorok-daddy/course-ai-applications
- 제어공학1: https://github.com/chorok-daddy/course-control-engineering-1

각 과목 저장소는 현재 사이트 원본에서 내보낸 배포본이며, Git clone / Fork /
GitHub의 Code → Download ZIP을 지원한다. 원본 편집 위치는 계속 `niil/courses/`다.
저장소를 이동하거나 기존 강의 링크를 변경하지 않는다.

강의 설명·그림은 CC BY 4.0, 직접 작성한 실습 코드는 MIT로 배포한다.
범위·제3자 자료 예외는 [강의 라이선스](niil/courses/LICENSE.md)에 명시한다.
이 라이선스는 연구실 인물 사진이나 연구 페이지 전체에 적용하는 허가가 아니다.

갱신 순서:

```sh
python3 tools/build_niil.py
python3 tools/check_site.py
python3 tools/check_migration.py
python3 tools/export_course_repos.py --output /tmp/niil-course-export
# 검토 후 과목 저장소에 일반 commit/push (force-push 없음)
python3 tools/publish_course_repos.py --publish
# 이후 이 사이트 변경을 commit/push
```

배포 명령은 기존 과목 저장소에만 게시하고 자동으로 새 저장소를 만들지 않는다.
`SOURCE.json`에 기록된 이전 생성 파일만 교체하며, 과목 저장소의 독립 편집은
다음 배포에 덮어써질 수 있으므로 원본 저장소에 반영한다. 해시 스냅샷으로 출처와
버전을 추적한다. ZIP은 GitHub가 생성하므로 별도 바이너리 ZIP을 Git에 넣지 않는다.
기존 학생용 다운로드는 그대로 두고, 배포본 Notebook에는 출처 셀을 추가한다.
MATLAB·데이터 파일은 바이트를 유지하고 `.SOURCE.txt`를 함께 제공한다.
