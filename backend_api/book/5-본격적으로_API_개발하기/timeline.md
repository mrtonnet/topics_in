* Draft: 2020-09-21 (Mon)

# Timeline 엔드포인트

## 소스코드

### API Server측

#### `timeline.py` 

```bash
# timeline.py
  ...
@app.route('/timeline/<int:user_id>', methods=['POST'])
def timeline( user_id ):
  if user_id not in app.user:
    return 'The user does not exist', 400

  follow_list = app.users[ user_id ].get( 'follow',set() )
  follow_list.add( user_id )
  timeline = [ tweet for tweet in app.tweets if tweet['user_id'] in follow_list ]

  return jsonify( {
    'user_id'  : user_id,
    'timeline' : timeline
  } )
```

#### `run_timeline`

```bash
#!/bin/bash
#  run_timeline
#  * Draft: 2020-09-21 (Mon)

# FLASK_ENV=development
#   turns on the debug mode.
#   When miniter.py is changed, the change is applied on the fly.

FLASK_ENV=development FLASK_APP=timeline.py FLASK_DEBUG=1 flask run
```

### Client측

#### `test_timeline`

```bash
#!/bin/bash
# test_timeline
# * Draft: 2020-09-21 (Mon)

# Create the first user.
http -v POST localhost:5000/sign-up name=first_user email=user1@gmail.com password=pw2user1
http -v POST localhost:5000/tweet id:=1 tweet="My first tweet"
http -v POST localhost:5000/tweet id:=1 tweet="My 2nd tweet"
http -v POST localhost:5000/tweet id:=1 tweet="Third!"

# Create the second user
http -v POST localhost:5000/sign-up name=second_user email=user2@gmail.com password=pw4user2
http -v POST localhost:5000/tweet id:=2 tweet="Second user's first tweet"
http -v POST localhost:5000/tweet id:=2 tweet="Second user has this as the second message."

# follow 
http -v POST localhost:5000/follow id:=1 follow:=2

# Create the 3rd user
http -v POST localhost:5000/sign-up name=third_user email=user3@gmail.com password=pw4user3
http -v POST localhost:5000/tweet id:=3 tweet="Third user's first tweet"

# Unfollow
http -v POST localhost:5000/unfollow id:=1 unfollow:=2

# timeline
http -v GET localhost:5000/timeline/1
```



## Problem

다음처럼 `timeline` 엔드포인트에 `405 METHOD NOT ALLOWED` 에러가 발생했습니다.

### Client 측 에러

```bash
$ ./run_timeline
  ...
GET /timeline/1 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:5000
User-Agent: HTTPie/0.9.8



HTTP/1.0 405 METHOD NOT ALLOWED
Allow: POST, OPTIONS
Content-Length: 178
Content-Type: text/html; charset=utf-8
Date: Mon, 21 Sep 2020 06:35:16 GMT
Server: Werkzeug/1.0.1 Python/3.7.6

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>405 Method Not Allowed</title>
<h1>Method Not Allowed</h1>
<p>The method is not allowed for the requested URL.</p>

$
```

### API Server 측 에러

```bash
$ ./run_timeline
  ...
127.0.0.1 - - [21/Sep/2020 14:27:11] "POST /sign-up HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 14:27:11] "POST /tweet HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 14:27:11] "POST /unfollow HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 14:27:11] "GET /timeline/1 HTTP/1.1" 405 -
```

## Hint

`timeline.py` 소스코드의 `route decorator`의 `methods`를 확인해보니 `POST`방식으로 정의되어 있습니다.

```python
@app.route('/timeline/<int:user_id>', methods=['POST'])
```

그런데 client의 요청은 `GET`방식이므로 client와 server의 처리방식, 즉 methods가 일치하지 않습니다. 이것이  `405 METHOD NOT ALLOWED` 에러의 원인인 것 같네요.

## Solution

`timeline.py` 소스코드의 처리방식을 `GET`으로 변경했습니다.

```python
@app.route('/timeline/<int:user_id>', methods=['GET'])
```

소스코드를 실행할 때, 디버그 모드로 실행했기 때문에 API server가 소스코드를 자동으로 reload합니다.

```bash
 * Detected change in '/home/aimldl/projects/api/timeline.py', reloading
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 260-263-585
```

## Problem2

### API Server측 에러

`500 Internal Server Error`가 발생했습니다. 일단  `405 METHOD NOT ALLOWED` 에러는 사라진 듯 하므로 다음 에러를 

```bash
  ...
127.0.0.1 - - [21/Sep/2020 15:43:07] "GET /timeline/1 HTTP/1.1" 500 -
Traceback (most recent call last):
  File "/home/aimldl/anaconda3/lib/python3.7/site-packages/flask/app.py", line 2464, in __call__
    return self.wsgi_app(environ, start_response)
  File "/home/aimldl/anaconda3/lib/python3.7/site-packages/flask/app.py", line 2450, in wsgi_app
    response = self.handle_exception(e)
  File "/home/aimldl/anaconda3/lib/python3.7/site-packages/flask/app.py", line 1867, in handle_exception
    reraise(exc_type, exc_value, tb)
  File "/home/aimldl/anaconda3/lib/python3.7/site-packages/flask/_compat.py", line 39, in reraise
    raise value
  File "/home/aimldl/anaconda3/lib/python3.7/site-packages/flask/app.py", line 2447, in wsgi_app
    response = self.full_dispatch_request()
  File "/home/aimldl/anaconda3/lib/python3.7/site-packages/flask/app.py", line 1952, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/home/aimldl/anaconda3/lib/python3.7/site-packages/flask/app.py", line 1821, in handle_user_exception
    reraise(exc_type, exc_value, tb)
  File "/home/aimldl/anaconda3/lib/python3.7/site-packages/flask/_compat.py", line 39, in reraise
    raise value
  File "/home/aimldl/anaconda3/lib/python3.7/site-packages/flask/app.py", line 1950, in full_dispatch_request
    rv = self.dispatch_request()
  File "/home/aimldl/anaconda3/lib/python3.7/site-packages/flask/app.py", line 1936, in dispatch_request
    return self.view_functions[rule.endpoint](**req.view_args)
  File "/home/aimldl/projects/api/timeline.py", line 112, in timeline
    if user_id not in app.user:
AttributeError: 'Flask' object has no attribute 'user'
```

## Hint2

위의 에러메세지 마지막 3줄을 보면 `if user_id not in app.user:`에서 `user`가 없다고 합니다.

```bash
  ...
  File "/home/aimldl/projects/api/timeline.py", line 112, in timeline
    if user_id not in app.user:
AttributeError: 'Flask' object has no attribute 'user'
```

`timeline.py` 소스코드를 훑어보면 `app.user`가 아니라 `app.users`라는 것을 알 수 있습니다. 잘못된 변수명을 `app.users`로 수정하고 파일을 저장합니다.

Flask가 디버그 모드이므로 `timeline.py`에 변화를 감지하고 파일을 `reload`합니다.

```bash
   ...
 * Detected change in '/home/aimldl/projects/api/timeline.py', reloading
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 733-396-676
```

## Solution2

### Client측

`test_timeline`으로 서버에 HTTP요청을 전송합니다.

```bash
$ ./test_timeline
  ...
GET /timeline/1 HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:5000
User-Agent: HTTPie/0.9.8



HTTP/1.0 200 OK
Content-Length: 230
Content-Type: application/json
Date: Mon, 21 Sep 2020 06:56:09 GMT
Server: Werkzeug/1.0.1 Python/3.7.6

{
    "timeline": [
        {
            "tweet": "My first tweet",
            "user_id": 1
        },
        {
            "tweet": "My 2nd tweet",
            "user_id": 1
        },
        {
            "tweet": "Third!",
            "user_id": 1
        }
    ],
    "user_id": 1
}
$
```

서버 측에서 `200 OK`응답을 보내왔습니다. 

### Server측

Client의 모든 HTTP요청에 대해 `200 OK` 결과가 나왔음을 Flask의 로그에서 알 수 있습니다. 

```bash
  ...
 * Detected change in '/home/aimldl/projects/api/timeline.py', reloading
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 733-396-676
127.0.0.1 - - [21/Sep/2020 15:56:06] "POST /sign-up HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 15:56:06] "POST /tweet HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 15:56:07] "POST /tweet HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 15:56:07] "POST /tweet HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 15:56:07] "POST /sign-up HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 15:56:07] "POST /tweet HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 15:56:08] "POST /tweet HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 15:56:08] "POST /follow HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 15:56:08] "POST /sign-up HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 15:56:08] "POST /tweet HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 15:56:09] "POST /unfollow HTTP/1.1" 200 -
127.0.0.1 - - [21/Sep/2020 15:56:09] "GET /timeline/1 HTTP/1.1" 200 -
```

에러가 났던 마지막 줄도 `200 OK`로 응답했습니다.

```bash
127.0.0.1 - - [21/Sep/2020 15:56:09] "GET /timeline/1 HTTP/1.1" 200 -
```



