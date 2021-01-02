---
layout: post
title: DynamoDB-Python Local DB control
comments: true
tags:
- DynamoDB
- Python
---

### AWS lambda 활용의 준비단계로 DynamoDB를 local에서 control 하는 방법을 정리
------
([공식문서링크](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html))

### Create table
- Sample code
<script src="https://gist.github.com/chorok-daddy/760343100b1a5f8174df7ee47e02dd6b.js"></script>
- 몇 가지 상식
    * Primary key: 보통 첫 번째 column에 들어가는 index이며, primary key로 지정된 column에는 중복된 item이 들어갈 수 없어야 하므로 대개 ID나 고유명 등등이 좋은 예이다 
    * Key type: hash(일치하는 값만 query 가능), range (범위지정 query 가능)
    * Data type: Scalar (number, string, binary, bool, null), Document (list, map(json)), Set (string set, number set, binary set)
    * Attribute type: S(String), N(Number), B(Binary), BOOL(bool), BS(Binary Set), ...

### Write data
- Sample code
<script src="https://gist.github.com/chorok-daddy/d85dd269a8340c2351fbbd1b48087ab8.js"></script>
- 핵심은 아래처럼 json format으로(table의 스키마에 맞게) 데이타를 만들고 put_time() 함수를 활용하는 것
```json
{
    "year" : 2013,
    "title" : "Turn It Down, Or Else!",
    "info" : {
        "directors" : [
            "Alice Smith",
            "Bob Jones"
        ],
        "release_date" : "2013-01-18T00:00:00Z",
        "rating" : 6.2,
        "genres" : [
            "Comedy",
            "Drama"
        ],
        "image_url" : "somewhere",
        "plot" : "something",
        "rank" : 11,
        "running_time_secs" : 5215,
        "actors" : [
            "David Matthewman",
            "Ann Thomas",
            "Jonathan G. Neff"
       ]
    }
}
```
- 물론 아래와 같이 직접 입력도 가능
```python
response = table.put_item(
    Item={
        'year': year,
        'title': title,
        'info': {
            'plot': plot,
            'rating': rating
        }
    }
)
```

### Read data
- key를 이용해서 query하는데, 아래와 같이 get_item() 함수를 활용
```python
try:
    response = table.get_item(Key={'year': year, 'title': title})
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    return response['Item']
```

### Update data
- update_item() 함수로 처리되는 점은 간단하나, 다음과 같이 조금 복잡한 절차를 거친다
    * key를 이용해 query
    * update expression에 어떤 attribute가 바뀌는지 표시
    * 실제 attribute 값이 어떻게 대입되는지 표시
    * 결과 return 형식 (예, UPDATED_NEW >> update된 attribute만 return)
    * 이외에 좀 더 복잡한 기작들은 최상단 공식문서 링크를 참조하면 된다
```python
response = table.update_item(
    Key={
        'year': year,
        'title': title
    },
    UpdateExpression="set info.rating=:r, info.plot=:p, info.actors=:a",
    ExpressionAttributeValues={
        ':r': Decimal(rating),
        ':p': plot,
        ':a': actors
    },
    ReturnValues="UPDATED_NEW"
)
return response
```

### Remove data
- delete_item() 함수를 이용, 아래와 같이 조건을 추가할 수 있다
```python
try:
    response = table.delete_item(
        Key={
            'year': year,
            'title': title
        },
        ConditionExpression="info.rating <= :val",
        ExpressionAttributeValues={
            ":val": Decimal(rating)
        }
    )
except ClientError as e:
    if e.response['Error']['Code'] == "ConditionalCheckFailedException":
        print(e.response['Error']['Message'])
    else:
        raise
else:
    return response
```
- 만약 조건이 필요 없다면, 그냥 간단하게
```python
response = table.delete_item(
    Key={
        'year': year,
        'title': title
    }
) 
```

### Query data
- Hash key 기반 '일치' 조건으로 query할 때는 다음과 같이 간단하다
```python
response = table.query(
        KeyConditionExpression=Key('year').eq(year)
)
return response['Items']
```
- Range key를 추가해 query하고 싶은 경우
```python
response = table.query(
    ProjectionExpression="#yr, title, info.genres, info.actors[0]",
    ExpressionAttributeNames={"#yr": "year"},
    KeyConditionExpression=
        Key('year').eq(year) & Key('title').between(title_range[0], title_range[1])
)
return response['Items']
```
- key가 아닌 attribute 값으로 검색도 가능한데(scan), 자세한 사항은 공식문서 링크 참조

### Delete table
- table.delete() 한줄로 끝