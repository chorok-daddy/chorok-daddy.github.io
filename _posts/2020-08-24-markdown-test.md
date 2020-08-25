---
layout: post
title: Markdown Test
comments: true
tags:
- Markdown
---

### Markdown 태그가 github page에서 어떻게 표시되는지 테스트
------

### [title 관련]
(태그)
```markdown
# H1
## H2
### H3
#### H4
##### H5
###### H6
```
(결과)
# H1
## H2
### H3
#### H4
##### H5
###### H6


### [list 관련]
(태그)
```markdown
- list 1
    - list 2
        - list 3
1. list 1
    1. list 1-1
1. list 2
```
(결과)
- list 1
    - list 2
        - list 3

1. list 1
    1. list 1-1
2. list 2


### [code 관련]
(태그)
~~~
```python
for i in range(10):
    if i>5:
        print(i)
```
~~~
(결과)
```python
for i in range(10):
    if i>5:
        print(i)
```
