* Draft: 2020-09-21 (Mon)

# 인증 엔드포인트 구현하기

* 인증 엔드포인트를 구현하기 위해서 기존에 작성한 코드를 몇 가지 수정합니다. 
* 출처: 깔끔한 파이썬 탄탄한 백엔드, '7장 인증, 송은우 지음, pp.188-193
  * 이론적인 부분은 책을 참고하세요.

## sign-up 엔드포인트

* 지금까지는 암호화하지 않았지만,
* bcrypt 알고리즘을 사용해서 암호화합니다.
* 데이터베이스에 저장하는 것은 유사합니다.

## 소스 코드

소스코드는 `source_codes/authentication.py`입니다.

```bash
# authentication.py
# * Draft: 2020-09-21 (Mon)
#
# This code is from:
#   '깔끔한 파이썬 탄탄한 백엔드', '7장 인증', 송은우 지음, pp.188-193
#   https://github.com/rampart81/python-backend-book/tree/master/chapter7

import bcrypt
import jwt

@app.route( '/sign-up', methods=['POST'] )
def sign_up():
  new_user             = request.json
  new_user['password'] = bcrypt.hashpw(
    new_user['password'].encode('UTF-8'),
    bcrypt.gensalt()
  )
  new_user_id = app.database.execute( text("""
    INSERT INTO users(
      name,
      email,
      profile,
      hashed_password
    ) VALUES (
      :name,
      :email,
      :profile,
      :password
    )
  """), new_user).lastrowid
  new_user_info = get_user( new_user_id )

  return jsonify( new_user_info )

@app.route( '/login', methods=['POST'] )
def login():
  credential = request.json
  email      = credential[ 'email' ]
  password   = credential[ 'password' ]

  row = database.execute( text("""
    SELECT id, hashed_password
    FROM users
    WHERE email = :email
  """), {'email' : email }.fetchone()

  if row and bcrypt.checkpw( password.encode('UTF-8'), row['hashed_password'].encode('UTF-8'):
    user_id = row['id']
    payload = {
      'user_id' : user_id,
      'exp'     : datetime.utcnow() + timedelta( seconds = 60*60*24 )
    }
    token = jwt.encode( payload, app.config['JWT_SECRET_KEY'], 'HS256' )

    return jsonify({
      'access_token' : token.decode('UTF-8')
    })
  else:
    return '', 401
```

## 인증 절차를 다른 엔드포인트에 적용하기

```python
@run_this_first
def and_then_run_this()
  print( "Running the second method..." )
```

#### decorator 함수

* pp.192-193

```python
from functools import wraps

def test_decorator(f):
  @wrap(f)
  def decorated_function( *args, **kwargs ):
    print( "Decorated Function" )
    return f( *args, **kwargs )

  return decorated_function

@test_decorator
def func():
  print( "Calling func function" )
```

### 인증 decorator 함수

```python
import jwt

from functools import wraps
from flask     import request, Response

def login_required(f):
  @wraps(f)
  def decorated_function( *args, **kwargs ):
    access_token = request.headers.get( 'Authorization' )
    if access_token is not None:
      try:
        payload = jwt.decode( access_token, current_app.config['JWT_SECRET_KEY', 'HS256']
      except jwt.InvalidTokenError:
        payload = None

      if payload is None:
        return Response( status=401 )

      user_id   = payload[ 'user_id' ]
      g.user_id = user_id
      g.user    = get_user_info( user_id ) if user_id else None
    else:
      return Response( status= 401 )

    return f( *args, **kwargs )
  return decorated_function
```

### 인증 decorator 적용하기

#### 소스코드

타이핑만 하고 디버깅 하기 전의 소스코드는 아래와 같다.

```python
# authentication.py
# * Rev.1: 2020-09-24 (Thu)
# * Draft: 2020-09-21 (Mon)
#
# This code is from:
#   '깔끔한 파이썬 탄탄한 백엔드', '7장 인증', 송은우 지음, pp.188-200
#   https://github.com/rampart81/python-backend-book/tree/master/chapter7

import bcrypt
import jwt

@app.route( '/sign-up', methods=['POST'] )
def sign_up():
  new_user             = request.json
  new_user['password'] = bcrypt.hashpw(
    new_user['password'].encode('UTF-8'),
    bcrypt.gensalt()
  )
  new_user_id = app.database.execute( text("""
    INSERT INTO users(
      name,
      email,
      profile,
      hashed_password
    ) VALUES (
      :name,
      :email,
      :profile,
      :password
    )
  """), new_user).lastrowid
  new_user_info = get_user( new_user_id )

  return jsonify( new_user_info )

@app.route( '/login', methods=['POST'] )
def login():
  credential = request.json
  email      = credential[ 'email' ]
  password   = credential[ 'password' ]

  row = database.execute( text("""
    SELECT id, hashed_password
    FROM users
    WHERE email = :email
  """), {'email' : email }.fetchone()

  if row and bcrypt.checkpw( password.encode('UTF-8'), row['hashed_password'].encode('UTF-8'):
    user_id = row['id']
    payload = {
      'user_id' : user_id,
      'exp'     : datetime.utcnow() + timedelta( seconds = 60*60*24 )
    }
    token = jwt.encode( payload, app.config['JWT_SECRET_KEY'], 'HS256' )

    return jsonify({
      'access_token' : token.decode('UTF-8')
    })
  else:
    return '', 401

@run_this_first
def and_then_run_this()
  print( "Running the second method..." )

from functools import wraps

def test_decorator(f):
  @wrap(f)
  def decorated_function( *args, **kwargs ):
    print( "Decorated Function" )
    return f( *args, **kwargs )

  return decorated_function

@test_decorator
def func():
  print( "Calling func function" )

# authentication decorator function, p.194
import jwt

from functools import wraps
from flask     import request, Response

def login_required(f):
  @wraps(f)
  def decorated_function( *args, **kwargs ):
    access_token = request.headers.get( 'Authorization' )
    if access_token is not None:
      try:
        payload = jwt.decode( access_token, current_app.config['JWT_SECRET_KEY', 'HS256']
      except jwt.InvalidTokenError:
        payload = None

      if payload is None:
        return Response( status=401 )

      user_id   = payload[ 'user_id' ]
      g.user_id = user_id
      g.user    = get_user_info( user_id ) if user_id else None
    else:
      return Response( status= 401 )

    return f( *args, **kwargs )
  return decorated_function

# applying authentication decorator, pp.196-197

def insert_tweet( user_tweet ):
  return current_app.database.execute( text("""
    INSERT INTO tweets (
      user_id,
      tweet
    ) VALUES (
      :id,
      :tweet
    )
   """), user_tweet ).rowcount

def insert_follow( user_follow ):
  return current_app.database.execute( text("""
    INSERT INTO users_follow_list (
      user_id,
      follow_user_id
    ) VALUES (
      :id,
      :follow
    )
  """), user_follow ).rowcount

def insert_unfollow( user_unfollow ):
  return current_app.database.execute( text("""
    DELETE FROM users_follow_list
    WHERE user_id = :id
    AND follow_user_id = :unfollow
  """), user_unfollow).rowcount

@app.route('/tweet', methods=['POST'])
@login_required
def tweet():
  user_tweet       = request.json
  user_tweet['id'] = g.user_id
  tweet            = user_tweet[ 'tweet' ]
  
  if len( tweet ) > 300:
    return 'Exceeded the 300 character limit', 400

  insert_tweet( user_tweet )

  return '', 200

@app.route('/follow', methods=['POST'])
@login_required
def follow():
  payload = request.json
  insert_follow( payload )
  return '', 200

@app.route('/unfollow', methods=['POST'])
@login_required
def unfollow():
  payload = request.json
  insert_unfollow( payload )
  return '', 200
```

### Server측

```bash
#!/bin/bash
#  run_authentication_with_db
# * Rev.1: 2020-09-24 (Thu)
# * Draft: 2020-09-21 (Mon)

# FLASK_ENV=development
#   turns on the debug mode.
#   When the .py file is changed, the change is applied on the fly.

run() {
  command=$1
  echo $command
  eval $command
}

run 'FLASK_ENV=development FLASK_APP=authentication.py FLASK_DEBUG=1 flask run'
```

#### API Server 실행하기

```bash
$ ./run_authentication_with_db 
FLASK_ENV=development FLASK_APP=authentication.py FLASK_DEBUG=1 flask run
 * Serving Flask app "authentication.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 203-761-023
```

#### Client측 HTTP 요청

tweet 엔드포인트에 tweet할 데이터를 전송합니다. 책에는 "hello world"라고 되어 있지만, 데이터베이스에 들어가는 값을 구별하기 힘들기 때문에 'hi there'로 변경했습니다.

```bash
$ http -v POST localhost:5000/tweet tweet='hi there'
```

### Problem1

`500 INTERNAL SERVER ERROR` 발생

```bash
127.0.0.1 - - [24/Sep/2020 16:48:43] "POST /tweet HTTP/1.1" 500 -
Traceback (most recent call last):
  ...
File "/home/aimldl/projects/api/authentication.py", line 44
    if row and bcrypt.checkpw( password.encode('UTF-8'), row['hashed_password'].encode('UTF-8'):
                                                                                               ^
SyntaxError: invalid syntax
```

#### Solution

오타 수정: 마지막에 `)`가 빠짐. 2개의 `)`를 추가로 넣습니다.

```python
# Before
  """), {'email' : email }.fetchone()
  
  if row and bcrypt.checkpw( password.encode('UTF-8'), row['hashed_password'].encode('UTF-8') :
# After
  """), {'email' : email }).fetchone()

  if row and bcrypt.checkpw( password.encode('UTF-8'), row['hashed_password'].encode('UTF-8') ):
```

#### Problem2

```bash
File "/home/aimldl/projects/api/authentication.py", line 90
    except jwt.InvalidTokenError:
         ^
SyntaxError: invalid syntax
```

#### Solution2

`jwt.decode(`의 `)`가 없어서 생긴 syntax error이므로 오타를 수정. 

```python
# Before
      try:
        payload = jwt.decode( access_token, current_app.config['JWT_SECRET_KEY', 'HS256']
      except jwt.InvalidTokenError:
        payload = None
# After
      try:
        payload = jwt.decode( access_token, current_app.config['JWT_SECRET_KEY', 'HS256'] )
      except jwt.InvalidTokenError:
        payload = None
                             
```

#### Problem3

```bash
  File "/home/aimldl/projects/api/authentication.py", line 11, in <module>
    import jwt
ModuleNotFoundError: No module named 'jwt'
```

#### Hint3

```bash
(api) $ pip install PyJWT
Requirement already satisfied: PyJWT in /home/aimldl/anaconda3/envs/api/lib/python3.8/site-packages (1.7.1)
$
```

이미 설치가 되어있는데 `jwt`모듈을 발견하지 못 함. API서버의 실행을 Ctrl+C로 취소했더니

```bash
ModuleNotFoundError: No module named 'jwt'
^C%                                                                                     (base) $
```

`api` 가상환경이 아니였음.

#### Solution3

`api` 가상환경으로 들어가서

```
(base) $ conda activate api
(api) $
```

API서버를 다시 시작해서

```bash
(api) $ ./run_authentication_with_db    
FLASK_ENV=development FLASK_APP=authentication.py FLASK_DEBUG=1 flask run
 * Serving Flask app "authentication.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 473-245-055
```

Client에서 ping 요청을 합니다. 원래 목적으로 하는 엔드포인트 호출은 `/tweet`이지만 가장 간단한 `/ping` 을 이용해서 문제를 좀 간단히 하려는 의도입니다.

```bash
(api) $ http -v POST localhost:5000/ping
```

Server측 로그에 아래와 같은 에러가 발생. 일단 이전의 `ModuleNotFoundError` 문제는 해결되었습니다.

#### Problem 4

다음 문제는 `app`이 정의되지 않아서 생기는 문제입니다.

```bash
127.0.0.1 - - [24/Sep/2020 17:21:43] "POST /ping HTTP/1.1" 500 -
Traceback (most recent call last):
  File "/home/aimldl/anaconda3/envs/api/lib/python3.8/site-packages/flask/_compat.py", line 39, in reraise
    raise value
  File "/home/aimldl/projects/api/authentication.py", line 13, in <module>
    @app.route( '/sign-up', methods=['POST'] )
NameError: name 'app' is not defined
```

#### Solution 4

```python
from flask    import Flask, request, jsonify, current_app

app = Flask(__name__)
```

#### Problem 5

Client에서 ping request를 했을 때,

```bash
$ http -v POST localhost:5000/ping
```

Server 로그에 `NameError` 에러가 발생합니다.

```
127.0.0.1 - - [24/Sep/2020 17:29:45] "POST /ping HTTP/1.1" 500 -
Traceback (most recent call last):
  File "/home/aimldl/anaconda3/envs/api/lib/python3.8/site-packages/flask/_compat.py", line 39, in reraise
    raise value
  File "/home/aimldl/projects/api/authentication.py", line 77, in <module>
    def func():
  File "/home/aimldl/projects/api/authentication.py", line 69, in test_decorator
    @wrap(f)
NameError: name 'wrap' is not defined

```

#### Solution 5

오타를 `@wrap(f)`에서 `@wraps(f)`로 수정 후, 

```python
# Before
from functools import wraps

def test_decorator(f):
  @wrap(f)
# After
  @wraps(f)
```

Server를 재실행하고, Client에서 ping request를 실행하면 `NameError`는 일단 해결되었습니다.

#### Problem 6

대신  `404 NOT FOUND`가 발생했습니다.

##### Server 로그

```bash
127.0.0.1 - - [24/Sep/2020 17:34:08] "POST /ping HTTP/1.1" 404 -
```

##### Client의 HTTP 응답

```bash
$ http -v POST localhost:5000/ping
  ...
HTTP/1.0 404 NOT FOUND
Content-Length: 232
Content-Type: text/html; charset=utf-8
Date: Thu, 24 Sep 2020 08:39:35 GMT
Server: Werkzeug/1.0.1 Python/3.8.5

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
$
```

#### Hint 6

디버깅의 힌트는 에러 메세지에 있습니다. 

```bash
The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again
```

일단 URL이 없다고 했는데... URL에 오타는 없어보입니다.

```bash
$ http -v POST localhost:5000/ping
```

생각해보니 ping은 POST 방식이 아니라 GET 방식으로 호출해야 하네요. HTTP 요청을 하는 명령어를 GET 방식으로 바꿔봅니다.

```bash
$ http -v GET localhost:5000/ping
```

하지만 여전히 똑같은 에러가 발생합니다.

```bash
The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again
```

혹시나해서 서버의 소스코드를 훑어봤는데 `/ping` 엔드포인트가 누락되었다는 것을 발견했습니다.

#### Solution 6

아래처럼 ping 엔드포인트를 정의해주고

```python
# authentication.py
  ...
@app.route('/ping', methods=['GET'])
def ping():
  return 'pong'
```

다시 한번 Client에서 ping을 날립니다.

```
$ http -v GET localhost:5000/ping
```

Server 로그에 `200 OK`가 보입니다.

```bash
127.0.0.1 - - [24/Sep/2020 17:51:05] "GET /ping HTTP/1.1" 200 -
```

이렇게 ping을 이용해서 소스코드에 있는 간단한 버그들을 찾아내서 수정했습니다.

`/ping` 엔드포인트가 정상 동작하므로, 원래 목적으로 하는 `/tweet`엔드포인트를 호출해봅니다.

#### Problem 7

##### Client의 HTTP 요청

아래처럼 요청을 하면

```bash
$ http -v POST localhost:5000/tweet tweet='hi there'
```

HTTP 응답이 `401 UNAUTHORIZED`로 나옵니다.

```bash
HTTP/1.0 401 UNAUTHORIZED
Content-Length: 0
Content-Type: text/html; charset=utf-8
Date: Thu, 24 Sep 2020 08:55:49 GMT
Server: Werkzeug/1.0.1 Python/3.8.5
```

이것은 책의 pp.197-198에 나오는 것처럼 예상된 반응으로 버그가 아닙니다.

##### Server 로그

이 때 Server의 로그는 아래와 같습니다.

```bash
127.0.0.1 - - [24/Sep/2020 17:55:49] "POST /tweet HTTP/1.1" 401 -
```

##### Client의 `/login`엔드포인트 호출

user1으로 로그인 시도를 했을 때,

```bash
$ http -v POST localhost:5000/login email='user1@email.com' password='pw4user1'
```

##### Server 로그

`NameError`가 발생합니다.

```bash
127.0.0.1 - - [24/Sep/2020 18:07:19] "POST /login HTTP/1.1" 500 -
Traceback (most recent call last):
  ...
File "/home/aimldl/projects/api/authentication.py", line 50, in login
    row = database.execute( text("""
NameError: name 'database' is not defined
```

#### Hint7

소스코드를 확인해보면 `database`가 정의되어 있지 않음을 알 수 있습니다.

```python
from flask    import Flask, request, jsonify, current_app
  ...
app = Flask(__name__)
  ...
@app.route( '/login', methods=['POST'] )
def login():
  credential = request.json
  email      = credential[ 'email' ]
  password   = credential[ 'password' ]

  row = database.execute( text("""
  ...
```

#### Solution 7

`database`를 정의하는 코드를 추가해줍니다.

```python
from flask    import Flask, request, jsonify, current_app
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text

# Custom Class Definition
class CustomJSONEncoder( JSONEncoder ):
  def default( self, obj ):
    if isinstance( obj, set ):
      return list( obj )

    # else
    return JSONENcoder.default( self, obj )

  ...
def create_app( test_config = None ):
  app = Flask( __name__ )

  app.json_encoder = CustomJSONEncoder

  if test_config is None:
    app.config.from_pyfile( 'config.py' )
  else:
    app.config.update( test_config )

  database = create_engine( app.config['DB_URL'], encoding='utf-8', max_overflow=0 )
  app.database = database

  # indent all the endpoints
```

그리고 아래에 들어가는 모든 엔드포인트를 띄워쓰기 해줍니다.

```python
from flask    import Flask, request, jsonify, current_app
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text
import bcrypt
import jwt

# Custom Class Definition
class CustomJSONEncoder( JSONEncoder ):
  def default( self, obj ):
    if isinstance( obj, set ):
      return list( obj )

    # else
    return JSONENcoder.default( self, obj )


def create_app( test_config = None ):
  app = Flask( __name__ )

  app.json_encoder = CustomJSONEncoder

  if test_config is None:
    app.config.from_pyfile( 'config.py' )
  else:
    app.config.update( test_config )

  database = create_engine( app.config['DB_URL'], encoding='utf-8', max_overflow=0 )
  app.database = database

  @app.route('/ping', methods=['GET'])
  def ping():
    return 'pong'

  @app.route( '/sign-up', methods=['POST'] )
  def sign_up():
    new_user             = request.json
    new_user['password'] = bcrypt.hashpw(
      new_user['password'].encode('UTF-8'),
      bcrypt.gensalt()
    )
    new_user_id = app.database.execute( text("""
      INSERT INTO users(
        name,
        email,
        profile,
        hashed_password
      ) VALUES (
        :name,
        :email,
        :profile,
        :password
      )
    """), new_user).lastrowid
    new_user_info = get_user( new_user_id )

    return jsonify( new_user_info )

  @app.route( '/login', methods=['POST'] )
  def login():
    credential = request.json
    email      = credential[ 'email' ]
    password   = credential[ 'password' ]

    row = database.execute( text("""
      SELECT id, hashed_password
      FROM users
      WHERE email = :email
    """), {'email' : email }).fetchone()

    if row and bcrypt.checkpw( password.encode('UTF-8'), row['hashed_password'].encode('UTF-8') ):
      user_id = row['id']
      payload = {
        'user_id' : user_id,
        'exp'     : datetime.utcnow() + timedelta( seconds = 60*60*24 )
      }
      token = jwt.encode( payload, app.config['JWT_SECRET_KEY'], 'HS256' )

      return jsonify({
        'access_token' : token.decode('UTF-8')
      })
    else:
      return '', 401
  ...
```

#### Server 실행

```bash
$ ./run_authentication_with_db                                                 
FLASK_ENV=development FLASK_APP=authentication.py flask run
 * Serving Flask app "authentication.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 473-245-055
```

##### Server측 로그

```bash
127.0.0.1 - - [24/Sep/2020 18:21:06] "POST /login HTTP/1.1" 500 -
Traceback (most recent call last):
  File "/home/aimldl/anaconda3/envs/api/lib/python3.8/site-packages/flask/_compat.py", line 39, in reraise
    raise value
  File "/home/aimldl/anaconda3/envs/api/lib/python3.8/site-packages/flask/cli.py", line 97, in find_best_app
    raise NoAppException(
flask.cli.NoAppException: Failed to find Flask application or factory in module "authentication". Use "FLASK_APP=authentication:name to specify one.
```

##### Client측 에러

```bash
$ http -v POST localhost:5000/login email='user1@email.com' password='pw4user1'
POST /login HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 52
Content-Type: application/json
Host: localhost:5000
User-Agent: HTTPie/0.9.8

{
    "email": "user1@email.com",
    "password": "pw4user1"
}

HTTP/1.0 500 INTERNAL SERVER ERROR
Connection: close
Content-Type: text/html; charset=utf-8
Date: Fri, 25 Sep 2020 05:29:52 GMT
Server: Werkzeug/1.0.1 Python/3.8.5
X-XSS-Protection: 0
  ...
<!--

Traceback (most recent call last):
  File "/home/aimldl/anaconda3/envs/api/lib/python3.8/site-packages/flask/_compat.py", line 39, in reraise
    raise value
  File "/home/aimldl/anaconda3/envs/api/lib/python3.8/site-packages/flask/cli.py", line 97, in find_best_app
    raise NoAppException(
flask.cli.NoAppException: Failed to find Flask application or factory in module "authentication". Use "FLASK_APP=authentication:name to specify one.

-->
$
```

