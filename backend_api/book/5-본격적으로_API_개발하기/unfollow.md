# Unfollow



## Client

```bash
#!/bin/bash
# test_unfollow
# * Draft: 2020-09-21 (Mon)

# Create the first user.
http -v POST localhost:5000/sign-up name=aimldl email=aimldl@gmail.com password=test1234
http -v POST localhost:5000/tweet id:=1 tweet="My first tweet"

# Create the second user
#http -v POST localhost:5000/sign-up name=second_user email=user2@gmail.com password=test2345

# Follow 
http -v POST localhost:5000/follow id:=1 follow:=2

# Unfollow
http -v POST localhost:5000/unfollow id:=1 unfollow:=2
```



```bash
$ ./test_unfollow 
POST /sign-up HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 71
Content-Type: application/json
Host: localhost:5000
User-Agent: HTTPie/0.9.8

{
    "email": "aimldl@gmail.com",
    "name": "aimldl",
    "password": "test1234"
}

HTTP/1.0 200 OK
Content-Length: 94
Content-Type: application/json
Date: Mon, 21 Sep 2020 05:02:33 GMT
Server: Werkzeug/1.0.1 Python/3.7.6

{
    "email": "aimldl@gmail.com",
    "id": 3,
    "name": "aimldl",
    "password": "test1234"
}

POST /tweet HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 36
Content-Type: application/json
Host: localhost:5000
User-Agent: HTTPie/0.9.8

{
    "id": 1,
    "tweet": "My first tweet"
}

HTTP/1.0 200 OK
Content-Length: 0
Content-Type: text/html; charset=utf-8
Date: Mon, 21 Sep 2020 05:02:33 GMT
Server: Werkzeug/1.0.1 Python/3.7.6



POST /follow HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 22
Content-Type: application/json
Host: localhost:5000
User-Agent: HTTPie/0.9.8

{
    "follow": 2,
    "id": 1
}

HTTP/1.0 200 OK
Content-Length: 120
Content-Type: application/json
Date: Mon, 21 Sep 2020 05:02:34 GMT
Server: Werkzeug/1.0.1 Python/3.7.6

{
    "email": "aimldl@gmail.com",
    "follow": [
        2
    ],
    "id": 1,
    "name": "aimldl",
    "password": "test1234"
}

POST /unfollow HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 24
Content-Type: application/json
Host: localhost:5000
User-Agent: HTTPie/0.9.8

{
    "id": 1,
    "unfollow": 2
}

HTTP/1.0 200 OK
Content-Length: 111
Content-Type: application/json
Date: Mon, 21 Sep 2020 05:02:34 GMT
Server: Werkzeug/1.0.1 Python/3.7.6

{
    "email": "aimldl@gmail.com",
    "follow": [],
    "id": 1,
    "name": "aimldl",
    "password": "test1234"
}

$
```



## API Server

```bash
127.0.0.1 - - [21/Sep/2020 14:02:33] "POST /sign-up HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 14:02:33] "POST /tweet HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 14:02:34] "POST /follow HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 14:02:34] "POST /unfollow HTTP/1.1" 200 -
```

4개의 모든 엔드포인트가 `200 OK` 이므로 정상 실행되었습니다.

참고로 아래의 경우는 `400 Bad Request`에러로 위의 실행결과는 버그를 수정하고 해서 정상 동작하도록 한 이후의 결과입니다.

```bash
127.0.0.1 - - [21/Sep/2020 14:00:28] "POST /sign-up HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 14:00:29] "POST /tweet HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 14:00:29] "POST /follow HTTP/1.1" 400 -
127.0.0.1 - - [21/Sep/2020 14:00:29] "POST /unfollow HTTP/1.1" 400 -
```

