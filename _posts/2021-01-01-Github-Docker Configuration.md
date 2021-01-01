---
layout: post
title: Github-Docker Configuration
comments: true
tags:
- Docker
- VScode
---

### Docker 연동의 필요성을 느껴 정리
------
### VScode 설치
[이전글](Github-VScode-Configuation) 참조

### Extension 추가
(from <https://89douner.tistory.com/123>)
- Remote Development 검색 후 install
- Docker, Docker Explorer 검색 후 install

### VS 와 Docker 연동
- cmd(ctrl)+shift+p 후 remote-Containers: Attach to Running Container 입력
- 구동중인 container가 없는데 테스트해보고 싶다면, docker extension icon을 클릭한 후 보유중인 image를 run interactive 하여 bash를 실행시켜둔 후 테스트하면 좋다

