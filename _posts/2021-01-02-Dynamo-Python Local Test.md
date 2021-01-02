---
layout: post
title: DynamoDB-Python Local Test
comments: true
tags:
- DynamoDB
- Python
---

### AWS lambda 활용의 준비단계로 DynamoDB를 local에서 테스트하는 방법을 정리
------
(좀더 자세히 알고싶다면, [참고자료링크](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html>))

### Prerequisites
- DynomoDB 로컬 버전을 설치 및 실행 (도커기반) [참조1](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html) [참조2](https://medium.com/@byeonggukgong/using-amazon-dynamodb-in-local-environment-feat-docker-fafbb420e161)
```console
$ docker pull amazon/dynamodb-local
$ docker run -d -p 8000:8000 amazon/dynamodb-local
$ pip3 install boto3
```

### Test code
- 다음 소스코드를 실행해본다 (AWS제공 예제 소스코드를 기반으로, aws cli 설정 안해도 실행 가능하게끔 수정하였음)
<script src="https://gist.github.com/chorok-daddy/760343100b1a5f8174df7ee47e02dd6b.js"></script>
- 정상이라면 'Table status: ACTIVE'을 출력
