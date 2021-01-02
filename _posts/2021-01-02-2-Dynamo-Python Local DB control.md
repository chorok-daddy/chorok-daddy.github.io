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

### Table 만들기
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
        "image_url" : "http://ia.media-imdb.com/images/N/O9ERWAU7FS797AJ7LU8HN09AMUP908RLlo5JF90EWR7LJKQ7@@._V1_SX400_.jpg",
        "plot" : "A rock band plays their music at high volumes, annoying the neighbors.",
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


