



```zsh
$ ./run_miniter 
 * Serving Flask app "miniter.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 473-245-055
127.0.0.1 - - [21/Sep/2020 12:41:44] "POST /sing-up HTTP/1.1" 404 -

```

404 Not Found Error

```bash
$ cat test_sign_up 
#!/bin/bash
# request_sign-up
# * Draft: 2020-09-21 (Mon)

http -v POST localhost:5000/sing-up name=aimldl email=aimldl@gmail.com password=test1234

```

오타가 있습니다. `localhost:5000/sing-up` 오타인 `sing-up`을 `sign-up`으로 수정 후 실행합니다.

Client

```bash
$ ./test_sign_up 
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
Date: Mon, 21 Sep 2020 03:50:26 GMT
Server: Werkzeug/1.0.1 Python/3.8.5

{
    "email": "aimldl@gmail.com",
    "id": 1,
    "name": "aimldl",
    "password": "test1234"
}
$
```

API Server 측 로그

```bash
$ ./run_miniter 
 * Serving Flask app "miniter.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 473-245-055
127.0.0.1 - - [21/Sep/2020 12:50:26] "POST /sign-up HTTP/1.1" 200 -
```

HTTP 응답으로 200 OK가 전송되었으므로 회원가입 엔드포인트가 성공적으로 작동했습니다.



### 300자 제한 트윗 글 올리기

#### API Server

```bash
$ ./run_tweet 
 * Serving Flask app "tweet.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 473-245-055
127.0.0.1 - - [21/Sep/2020 13:09:04] "POST /tweet HTTP/1.1" 400 -

```

#### Client

```bash
$ ./test_tweet
/usr/lib/python3/dist-packages/requests/__init__.py:80: RequestsDependencyWarning: urllib3 (1.25.5) or chardet (3.0.4) doesn't match a supported version!
  RequestsDependencyWarning)
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

HTTP/1.0 400 BAD REQUEST
Content-Length: 23
Content-Type: text/html; charset=utf-8
Date: Mon, 21 Sep 2020 04:09:04 GMT
Server: Werkzeug/1.0.1 Python/3.8.5

The user does not exist

$
```

새로 tweet.py를 만들었더니, `The user does not exist` 에러가 나왔다. 그러므로 먼저 사용자를 만들고 나서 tweet을 해야한다.

#### API Server

```bash
$ ./test_sign_up 
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
Date: Mon, 21 Sep 2020 04:11:46 GMT
Server: Werkzeug/1.0.1 Python/3.8.5

{
    "email": "aimldl@gmail.com",
    "id": 1,
    "name": "aimldl",
    "password": "test1234"
}

$
```

```bash
127.0.0.1 - - [21/Sep/2020 13:11:46] "POST /sign-up HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 13:11:55] "POST /tweet HTTP/1.1" 200 -
```



```bash
$ ./test_tweet 
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
Date: Mon, 21 Sep 2020 04:11:55 GMT
Server: Werkzeug/1.0.1 Python/3.8.5

$
```

`sign-up`이 `200 OK`로 사용자가 만들어졌고, `tweet`도 `200 OK`로 트위트 메세지가 잘 처리되었다.

## 팔로우와 언팔로우 엔드포인트

#### Client

```bash
$ ./test_follow
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
Date: Mon, 21 Sep 2020 04:37:14 GMT
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
Date: Mon, 21 Sep 2020 04:37:14 GMT
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
Date: Mon, 21 Sep 2020 04:37:14 GMT
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

$
```

#### API Server

```bash
127.0.0.1 - - [21/Sep/2020 13:37:14] "POST /sign-up HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 13:37:14] "POST /tweet HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 13:37:14] "POST /follow HTTP/1.1" 200 -
```

Client가 요청한 모든 엔드포인트가 `200 OK`로 문제없이 실행됐습니다.



