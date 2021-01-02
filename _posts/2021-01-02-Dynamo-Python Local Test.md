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
(from [참고자료링크](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html>) )

### Prerequisites
- DynomoDB 로컬 버전을 설치 및 실행 (도커기반) [참조1](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html) [참조2](https://medium.com/@byeonggukgong/using-amazon-dynamodb-in-local-environment-feat-docker-fafbb420e161)
```console
$ docker pull amazon/dynamodb-local
$ docker run -d -p 8000:8000 amazon/dynamodb-local
$ pip3 install boto3
```

### Test code
- 다음 소스코드를 실행해본다 (AWS제공 예제 소스코드를 기반으로, aws cli 설정 안해도 실행 가능하게끔 수정하였음)
```python
import boto3
def create_movie_table(dynamodb=None):
	if not dynamodb:
		dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id="anything",
                          aws_secret_access_key="anything",
                          region_name="us-west-2",
                          endpoint_url="http://localhost:8000")
		table = dynamodb.create_table(TableName='Movies',
			KeySchema=[
			{'AttributeName': 'year','KeyType': 'HASH' # Partition key
			},
			{'AttributeName': 'title','KeyType': 'RANGE' # Sort key
			}
			],
			AttributeDefinitions=[
			{'AttributeName': 'year','AttributeType': 'N'},
			{'AttributeName': 'title','AttributeType': 'S'},
			],
			ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10}
		)
	return table
if __name__ == '__main__':
	movie_table = create_movie_table()
	print("Table status:", movie_table.table_status)
```
- 정상이라면 'Table status: ACTIVE'을 출력
